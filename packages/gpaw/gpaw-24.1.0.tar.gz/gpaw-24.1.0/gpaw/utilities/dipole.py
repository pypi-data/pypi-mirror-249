"""Calculate dipole matrix elements."""
from __future__ import annotations
import numpy as np
from ase.units import Bohr
from gpaw.new.ase_interface import ASECalculator, GPAW
from gpaw.typing import Array3D, Vector


def dipole_matrix_elements(*args, **kwargs):
    """Deprecated.

    Use
    ``gpaw.new.pwfd.wave_functions.PWFDWaveFunctions.dipole_matrix_elements``
    instead.
    """
    raise DeprecationWarning


def dipole_matrix_elements_from_calc(calc: ASECalculator,
                                     n1: int,
                                     n2: int,
                                     center: Vector = None
                                     ) -> list[Array3D]:
    """Calculate dipole matrix-elements (units: eÅ).

    Parameters
    ----------
    n1, n2:
        Band range.
    center:
        Center of molecule in Å.  Defaults to center of cell.
    """
    ibzwfs = calc.calculation.state.ibzwfs

    assert ibzwfs.ibz.bz.gamma_only

    if center is not None:
        center = np.asarray(center) / Bohr

    wfs_s = ibzwfs.wfs_qs[0]

    d_snnv = []
    for wfs in wfs_s:
        if calc.params.mode['name'] == 'lcao':
            basis = calc.calculation.scf_loop.hamiltonian.basis
            grid = calc.calculation.state.density.nt_sR.desc
            wfs = wfs.to_uniform_grid_wave_functions(grid, basis)
        wfs = wfs.collect(n1, n2)
        if wfs is not None:
            d_nnv = wfs.dipole_matrix_elements(center) * Bohr
        else:
            d_nnv = np.empty((n2 - n1, n2 - n1, 3))
        calc.comm.broadcast(d_nnv, 0)
        d_snnv.append(d_nnv)

    return d_snnv


def main(argv: list[str] = None) -> None:
    import argparse

    parser = argparse.ArgumentParser(
        prog='python3 -m gpaw.utilities.dipole',
        description='Calculate dipole matrix elements.  Units: eÅ.')

    add = parser.add_argument

    add('file', metavar='input-file',
        help='GPW-file with wave functions.')
    add('-n', '--band-range', nargs=2, type=int, default=[0, 0],
        metavar=('n1', 'n2'), help='Include bands: n1 <= n < n2.')
    add('-c', '--center', metavar='x,y,z',
        help='Center of charge distribution.  Default is middle of unit '
        'cell.')

    args = parser.parse_intermixed_args(argv)

    calc = GPAW(args.file)

    n1, n2 = args.band_range
    nbands = calc.get_number_of_bands()
    n2 = n2 or n2 + nbands

    if args.center:
        center = [float(x) for x in args.center.split(',')]
    else:
        center = None  # center of cell

        d_snnv = dipole_matrix_elements_from_calc(calc, n1, n2, center)

    if calc.comm.rank > 0:
        return

    print('Number of bands:', nbands)
    print('Number of valence electrons:', calc.get_number_of_electrons())
    print('Units: eÅ')
    print()

    for spin, d_nnv in enumerate(d_snnv):
        print(f'Spin={spin}')

        for direction, d_nn in zip('xyz', d_nnv.T):
            print(f' <{direction}>',
                  ''.join(f'{n:8}' for n in range(n1, n2)))
            for n in range(n1, n2):
                print(f'{n:4}', ''.join(f'{d:8.3f}' for d in d_nn[n - n1]))


if __name__ == '__main__':
    main()
