from lib.centering import VectorCentering
from lib.domain import Domain
from lib.scalar_field import ScalarField
from lib.vec3 import Bool3, Float3, Int3


class VectorField:
    def __init__(
        self,
        domain: Domain,
        centering: VectorCentering,
        *,
        n_ghosts: int = 1,
    ):
        self.domain = domain
        self.centering = centering

        self._components = [ScalarField(domain, c, n_ghosts=n_ghosts) for c in centering]

    def __getitem__(self, d: int) -> ScalarField:
        return self._components[d]

    @property
    def x(self) -> ScalarField:
        return self._components[0]

    @property
    def y(self) -> ScalarField:
        return self._components[1]

    @property
    def z(self) -> ScalarField:
        return self._components[2]


def test():
    dims = Int3(1, 8, 4)
    domain = Domain(dims, Float3(0.5, 0.5, 0.5), periodic_dims=Bool3(True, False, True))
    ec_field = VectorField(domain, VectorCentering.ec())

    assert (ec_field.x.dims == Int3(1, 9, 4)).all()
    assert (ec_field.x.n_ghosts_lower == Int3(0, 1, 1)).all()
    assert (ec_field.x.n_ghosts_upper == Int3(0, 1, 1)).all()

    assert (ec_field.y.dims == Int3(1, 8, 4)).all()
    assert (ec_field.y.n_ghosts_lower == Int3(0, 1, 1)).all()
    assert (ec_field.y.n_ghosts_upper == Int3(0, 1, 1)).all()

    assert (ec_field.z.dims == Int3(1, 9, 4)).all()
    assert (ec_field.z.n_ghosts_lower == Int3(0, 1, 1)).all()
    assert (ec_field.z.n_ghosts_upper == Int3(0, 1, 1)).all()

    ec_field.x.set_from_func(lambda pos: pos.x)
    ec_field.y.set_from_func(lambda pos: pos.x)
    ec_field.z.set_from_func(lambda pos: pos.x)

    assert ec_field.x[Int3(0, 1, 0)] == 0.25
    assert ec_field.y[Int3(0, 1, 0)] == 0.0
    assert ec_field.z[Int3(0, 1, 0)] == 0.0
