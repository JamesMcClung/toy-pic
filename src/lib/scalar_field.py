from typing import Callable

import numpy as np

from lib.centering import ScalarCentering
from lib.domain import Domain
from lib.range3 import Range3
from lib.vec3 import Bool3, Float3, Int3


class ScalarField:
    def __init__(
        self,
        domain: Domain,
        centering: ScalarCentering,
        *,
        n_ghosts: int | Int3 | tuple[Int3, Int3] = 1,
        _array: np.ndarray | None = None,
    ):
        self.domain = domain
        self.centering = centering

        self.dims = domain.dims + (~domain.periodic_dims & ~self.centering.is_ccs).to_mask()

        if isinstance(n_ghosts, int):
            n_ghosts = domain.vary_dims.to_mask() * n_ghosts
        if isinstance(n_ghosts, Int3):
            n_ghosts = (n_ghosts, n_ghosts)
        self.n_ghosts_lower, self.n_ghosts_upper = n_ghosts

        self._array = _array if _array is not None else np.zeros(self.n_ghosts_lower + self.dims + self.n_ghosts_upper)

    def _shift_idx(self, i3: Int3) -> Int3:
        return i3 + self.n_ghosts_lower

    def __getitem__(self, i3: Int3) -> float:
        return self._array[*self._shift_idx(i3)]

    def __setitem__(self, i3: Int3, val: float):
        self._array[*self._shift_idx(i3)] = val

    def set_from_func(self, func: Callable[[Float3], float]):
        for i3 in Range3(self.dims):
            pos = self.domain.corner_pos + self.domain.deltas * (i3.to_float3() + self.centering.offsets)
            self[i3] = func(pos)


def test():
    ncells = Int3(1, 8, 4)
    deltas = Float3(1.0, 1.0, 1.0)
    domain = Domain(ncells, deltas, periodic_dims=Bool3(True, False, True))

    cc_field = ScalarField(domain, ScalarCentering.cc())

    assert (cc_field.dims == Int3(1, 8, 4)).all()
    assert (cc_field.n_ghosts_lower == Int3(0, 1, 1)).all()
    assert (cc_field.n_ghosts_upper == Int3(0, 1, 1)).all()

    cc_field.set_from_func(lambda pos: pos.y)

    assert cc_field[Int3(0, 1, 0)] == 1.5
    assert cc_field[Int3(0, 2, 0)] == 2.5

    nc_field = ScalarField(domain, ScalarCentering.nc())

    assert (nc_field.dims == Int3(1, 9, 4)).all()
    assert (nc_field.n_ghosts_lower == Int3(0, 1, 1)).all()
    assert (nc_field.n_ghosts_upper == Int3(0, 1, 1)).all()

    nc_field.set_from_func(lambda pos: pos.y)

    assert nc_field[Int3(0, 1, 0)] == 1.0
    assert nc_field[Int3(0, 2, 0)] == 2.0
