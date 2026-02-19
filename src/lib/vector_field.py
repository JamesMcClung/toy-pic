from lib.centering import VectorCentering
from lib.domain import Domain
from lib.field_array import FieldArray
from lib.vec3 import Float3, Int3


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
            # nc values at upper edge are in domain
            comp_dims = domain.dims + centering.component_centered(d).flip().to_mask()
            self._components.append(FieldArray(comp_dims, n_ghosts=domain.vary_dims.to_mask() * domain.n_ghosts))

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
    domain = Domain(dims, Float3(0.5, 0.5, 0.5))
    ec_field = VectorField(domain, VectorCentering.EC)

    assert (ec_field.x.dims == Int3(1, 9, 5)).all()
    assert (ec_field.x.n_ghosts_lower == Int3(0, 1, 1)).all()
    assert (ec_field.x.n_ghosts_upper == Int3(0, 1, 1)).all()

    assert (ec_field.y.dims == Int3(1, 8, 5)).all()
    assert (ec_field.y.n_ghosts_lower == Int3(0, 1, 1)).all()
    assert (ec_field.y.n_ghosts_upper == Int3(0, 1, 1)).all()

    assert (ec_field.z.dims == Int3(1, 9, 4)).all()
    assert (ec_field.z.n_ghosts_lower == Int3(0, 1, 1)).all()
    assert (ec_field.z.n_ghosts_upper == Int3(0, 1, 1)).all()
