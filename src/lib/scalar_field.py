from __future__ import annotations

from typing import Any, Callable, Self

import numpy as np
from numpy import s_

from lib import numpy_utils
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
        _temp: bool = False,
    ):
        self.domain = domain
        self.centering = centering

        self.dims = domain.dims + (~domain.periodic_dims & ~self.centering.is_ccs).to_mask()

        if isinstance(n_ghosts, int):
            n_ghosts = domain.vary_dims.to_mask() * n_ghosts
        if isinstance(n_ghosts, Int3):
            n_ghosts = (n_ghosts, n_ghosts)
        self.n_ghosts_lower, self.n_ghosts_upper = n_ghosts

        if _array is None:
            self._array = np.zeros(self.n_ghosts_lower + self.dims + self.n_ghosts_upper)
        else:
            assert (Int3(*_array.shape) == self.n_ghosts_lower + self.dims + self.n_ghosts_upper).all()
            self._array = _array

        self._temp = _temp

    def temp(self, set_temp: bool = True) -> Self:
        self._temp = set_temp
        return self

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

    @property
    def _inner_array(self) -> np.ndarray:
        return self._array[*self.inner_slices()]

    def inner_slices(self) -> list[slice]:
        return [s_[lower : -upper or None] for lower, upper in zip(self.n_ghosts_lower, self.n_ghosts_upper)]

    def gradient1d(self, d: int) -> ScalarField | float:
        if not self.domain.vary_dims[d]:
            return 0.0

        grad_arr = np.diff(self._array, 1, axis=d)
        grad_arr /= self.domain.deltas[d]

        grad_centering = self.centering.switched(d)

        grad_n_ghosts_lower = self.n_ghosts_lower.copy()
        grad_n_ghosts_upper = self.n_ghosts_upper.copy()
        if self.centering.is_ccs[d]:
            # cc -> nc
            # on left side: lose a ghost
            grad_n_ghosts_lower[d] -= 1
            # on right side, if aperiodic: lose a ghost (and gain a non-ghost, which happens implicitly)
            grad_n_ghosts_upper[d] -= 1
            # on right side, if periodic: lose a ghost (and must explicitly remove it)
            if self.domain.periodic_dims[d]:
                grad_arr = numpy_utils.take_slice(grad_arr, d, s_[:-1])
        else:
            # nc -> cc
            # on left side: no change in ghosts
            # on right side, if aperiodic: no change in ghosts (so lose a non-ghost, which happens implicitly)
            # on right side, if periodic: lose a ghost (and gain a non-ghost, which happens implicitly)
            if self.domain.periodic_dims[d]:
                grad_n_ghosts_upper[d] -= 1

        if grad_n_ghosts_lower[d] < 0 or grad_n_ghosts_upper[d] < 0:
            raise NotImplementedError("shrinking domain not yet supported")

        return ScalarField(self.domain, grad_centering, n_ghosts=(grad_n_ghosts_lower, grad_n_ghosts_upper), _array=grad_arr, _temp=True)

    def is_elementwise_compatible(self, other: ScalarField) -> bool:
        return self.domain == other.domain and self.centering == other.centering

    def __add__(self, other: ScalarField | float | Any) -> ScalarField:
        if other == 0.0:
            return self

        if self._temp:
            return self.__iadd__(other)

        return NotImplementedError("nontrivial non-temp add not yet supported")

    def __radd__(self, other: ScalarField | float | Any) -> ScalarField:
        return self + other

    def __iadd__(self, other: ScalarField | float | Any) -> ScalarField:
        if other == 0.0:
            return self

        if isinstance(other, float):
            self._inner_array.__iadd__(other)
            return self

        if isinstance(other, ScalarField):
            assert self.is_elementwise_compatible(other)
            self._inner_array.__iadd__(other._inner_array)
            return self

        return NotImplemented

    def __sub__(self, other: ScalarField | float | Any) -> ScalarField:
        if other == 0.0:
            return self

        if self._temp:
            return self.__isub__(other)

        return NotImplementedError("nontrivial non-temp sub not yet supported")

    def __neg__(self) -> ScalarField:
        if self._temp:
            np.negative(self._array, out=self._array)
            return self

        return NotImplementedError("non-temp neg not yet supported")

    def __rsub__(self, other: ScalarField | float | Any) -> ScalarField:
        return -self + other

    def __isub__(self, other: ScalarField | float | Any) -> ScalarField:
        if other == 0.0:
            return self

        if isinstance(other, float):
            self._inner_array.__isub__(other)
            return self

        if isinstance(other, ScalarField):
            assert self.is_elementwise_compatible(other)
            self._inner_array.__isub__(other._inner_array)
            return self

        return NotImplemented

    def __imul__(self, other: float | Any) -> ScalarField:
        if other == 1.0:
            return self

        if isinstance(other, float):
            self._inner_array.__imul__(other)
            return self

        return NotImplemented


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

    # aperiodic gradient tests

    nc_grad_y = nc_field.gradient1d(1)
    assert nc_grad_y.centering.is_ccs[1]
    assert nc_grad_y.n_ghosts_lower[1] == 1
    assert nc_grad_y.n_ghosts_upper[1] == 1
    assert nc_grad_y.dims[1] == nc_field.dims[1] - 1
    assert nc_grad_y[Int3(0, 1, 0)] == 1.0

    nc_grad2_y = nc_grad_y.gradient1d(1)
    assert not nc_grad2_y.centering.is_ccs[1]
    assert nc_grad2_y.n_ghosts_lower[1] == 0
    assert nc_grad2_y.n_ghosts_upper[1] == 0
    assert nc_grad2_y.dims[1] == nc_field.dims[1]
    assert nc_grad2_y[Int3(0, 1, 0)] == 0.0

    # periodic gradient tests

    nc_grad_z = nc_field.gradient1d(2)
    assert nc_grad_z.centering.is_ccs[2]
    assert nc_grad_z.n_ghosts_lower[2] == 1
    assert nc_grad_z.n_ghosts_upper[2] == 0
    assert nc_grad_z.dims[2] == nc_field.dims[2]
    assert nc_grad_z[Int3(0, 1, 0)] == 0.0

    try:
        # don't have any upper ghosts, so domain has to shrink
        nc_grad2_z = nc_grad_z.gradient1d(2)
        assert False
    except NotImplementedError:
        pass
