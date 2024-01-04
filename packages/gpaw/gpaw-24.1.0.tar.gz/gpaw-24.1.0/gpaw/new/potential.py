from __future__ import annotations

import numpy as np
from ase.units import Bohr, Ha

from gpaw.core.arrays import DistributedArrays as XArray
from gpaw.core.atom_arrays import AtomArrays, AtomDistribution
from gpaw.core.domain import Domain as XDesc
from gpaw.core.uniform_grid import UGArray, UGDesc
from gpaw.mpi import MPIComm
from gpaw.new import zips


class Potential:
    def __init__(self,
                 vt_sR: UGArray,
                 dH_asii: AtomArrays,
                 dedtaut_sR: UGArray | None,
                 energies: dict[str, float],
                 vHt_x: XArray | None = None):
        self.vt_sR = vt_sR
        self.dH_asii = dH_asii
        self.dedtaut_sR = dedtaut_sR
        self.energies = energies
        self.vHt_x = vHt_x  # initial guess for Hartree potential

    def __repr__(self):
        return (f'Potential({self.vt_sR}, {self.dH_asii}, '
                f'{self.dedtaut_sR}, {self.energies})')

    def __str__(self) -> str:
        return (f'potential:\n'
                f'  grid points: {self.vt_sR.desc.size}\n')

    def dH(self, P_ani, out_ani, spin):
        if len(P_ani.dims) == 1:  # collinear wave functions
            P_ani.block_diag_multiply(self.dH_asii, out_ani, spin)
            return

        # Non-collinear wave functions:
        P_ansi = P_ani
        out_ansi = out_ani

        for (a, P_nsi), out_nsi in zips(P_ansi.items(), out_ansi.values()):
            v_ii, x_ii, y_ii, z_ii = (dh_ii.T for dh_ii in self.dH_asii[a])
            assert v_ii.dtype == complex
            out_nsi[:, 0] = (P_nsi[:, 0] @ (v_ii + z_ii) +
                             P_nsi[:, 1] @ (x_ii - 1j * y_ii))
            out_nsi[:, 1] = (P_nsi[:, 1] @ (v_ii - z_ii) +
                             P_nsi[:, 0] @ (x_ii + 1j * y_ii))
        return out_ansi

    def move(self, atomdist: AtomDistribution) -> None:
        """Move atoms inplace."""
        self.dH_asii = self.dH_asii.moved(atomdist)

    def redist(self,
               grid: UGDesc,
               desc: XDesc,
               atomdist: AtomDistribution,
               comm1: MPIComm,
               comm2: MPIComm) -> Potential:
        return Potential(
            self.vt_sR.redist(grid, comm1, comm2),
            self.dH_asii.redist(atomdist, comm1, comm2),
            None if self.dedtaut_sR is None else self.dedtaut_sR.redist(
                grid, comm1, comm2),
            self.energies.copy(),
            None if self.vHt_x is None else self.vHt_x.redist(
                desc, comm1, comm2))

    def _write_gpw(self, writer, ibzwfs):
        from gpaw.new.calculation import combine_energies
        energies = combine_energies(self, ibzwfs)
        energies['band'] = ibzwfs.energies['band']
        if 'stress' in self.energies:
            energies['stress'] = self.energies['stress']
        dH_asp = self.dH_asii.to_cpu().to_lower_triangle().gather()
        vt_sR = self.vt_sR.to_xp(np).gather()
        assert self.vHt_x is not None
        vHt_x = self.vHt_x.to_xp(np).gather()
        if self.dedtaut_sR is not None:
            dedtaut_sR = self.dedtaut_sR.to_xp(np).gather()
        if dH_asp is None:
            return
        writer.write(
            potential=vt_sR.data * Ha,
            electrostatic_potential=vHt_x.data * Ha,
            atomic_hamiltonian_matrices=dH_asp.data * Ha,
            **{f'e_{name}': val * Ha for name, val in energies.items()})
        if self.dedtaut_sR is not None:
            writer.write(mgga_potential=dedtaut_sR.data * Bohr**3)
