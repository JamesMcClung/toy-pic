from typing import Callable

from lib.centering import VectorCentering
from lib.domain import Domain
from lib.field_array import FieldArray
from lib.range3 import Range3
from lib.vec3 import Bool3, Float3, Int3


class VectorField:
    def __init__(
        self,
        domain: Domain,
        centering: VectorCentering,
    ):
        self.domain = domain
        self.centering = centering

        self._components = []
        for d in range(3):
            # nc values at upper edge of aperiodic dimension are in the domain
            comp_dims = domain.dims + (~domain.periodic_dims & ~self.centering.component_centered(d)).to_mask()
            self._components.append(FieldArray(comp_dims, n_ghosts=domain.vary_dims.to_mask() * domain.n_ghosts))

    def set_component_from_func(self, d: int, func: Callable[[Float3], float]):
        for i3 in Range3(self[d].dims):
            pos = self.domain.corner_pos + self.domain.deltas * (i3.to_float3() + self.centering.component_offsets(d))
            self[d][i3] = func(pos)

    def __getitem__(self, d: int) -> FieldArray:
        return self._components[d]

    @property
    def x(self) -> FieldArray:
        return self._components[0]

    @property
    def y(self) -> FieldArray:
        return self._components[1]

    @property
    def z(self) -> FieldArray:
        return self._components[2]


def test():
    dims = Int3(1, 8, 4)
    domain = Domain(dims, Float3(0.5, 0.5, 0.5), periodic_dims=Bool3(True, False, True))
    ec_field = VectorField(domain, VectorCentering.EC)

    assert (ec_field.x.dims == Int3(1, 9, 4)).all()
    assert (ec_field.x.n_ghosts_lower == Int3(0, 1, 1)).all()
    assert (ec_field.x.n_ghosts_upper == Int3(0, 1, 1)).all()

    assert (ec_field.y.dims == Int3(1, 8, 4)).all()
    assert (ec_field.y.n_ghosts_lower == Int3(0, 1, 1)).all()
    assert (ec_field.y.n_ghosts_upper == Int3(0, 1, 1)).all()

    assert (ec_field.z.dims == Int3(1, 9, 4)).all()
    assert (ec_field.z.n_ghosts_lower == Int3(0, 1, 1)).all()
    assert (ec_field.z.n_ghosts_upper == Int3(0, 1, 1)).all()

    ec_field.set_component_from_func(0, lambda pos: pos.x)
    ec_field.set_component_from_func(1, lambda pos: pos.x)
    ec_field.set_component_from_func(2, lambda pos: pos.x)

    assert ec_field.x[Int3(0, 1, 0)] == 0.25
    assert ec_field.y[Int3(0, 1, 0)] == 0.0
    assert ec_field.z[Int3(0, 1, 0)] == 0.0
