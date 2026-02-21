from __future__ import annotations

from typing import Any, Self

from lib.centering import VectorCentering
from lib.domain import Domain
from lib.scalar_field import ScalarField
from lib.vec3 import Bool3, Float3, Int3


class VectorField:
    def __init__(self, x: ScalarField, y: ScalarField, z: ScalarField):
        assert x.domain == y.domain == z.domain

        self.domain = x.domain
        self.centering = VectorCentering(x.centering, y.centering, z.centering)
        self._components = [x, y, z]

    @classmethod
    def zeros(
        cls,
        domain: Domain,
        centering: VectorCentering,
        *,
        n_ghosts: int | Int3 | tuple[Int3, Int3] = 1,
    ) -> Self:
        _components = [ScalarField(domain, c, n_ghosts=n_ghosts) for c in centering]
        return cls(*_components)

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

    def curl(self) -> VectorField:
        curl_x = self.z.gradient1d(1) - self.y.gradient1d(2)
        curl_y = self.x.gradient1d(2) - self.z.gradient1d(0)
        curl_z = self.y.gradient1d(0) - self.x.gradient1d(1)
        return VectorField(curl_x, curl_y, curl_z)

    def __iadd__(self, other: VectorField | Any) -> VectorField:
        if isinstance(other, VectorField):
            self.x.__iadd__(other.x)
            self.y.__iadd__(other.y)
            self.z.__iadd__(other.z)

        return NotImplemented

    def __isub__(self, other: VectorField | Any) -> VectorField:
        if isinstance(other, VectorField):
            self.x.__isub__(other.x)
            self.y.__isub__(other.y)
            self.z.__isub__(other.z)

        return NotImplemented

    def __imul__(self, other: float | Any) -> VectorField:
        if other == 1.0:
            return self

        if isinstance(other, float):
            self.x.__imul__(other)
            self.y.__imul__(other)
            self.z.__imul__(other)
            return self

        return NotImplemented


def test():
    dims = Int3(1, 8, 4)
    domain = Domain(dims, Float3(0.5, 0.5, 0.5), periodic_dims=Bool3(True, False, True))
    ec_field = VectorField.zeros(domain, VectorCentering.ec())

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

    # curl test

    ec_field.y.set_from_func(lambda pos: pos.z)

    ec_curl = ec_field.curl()
    assert ec_curl.centering == VectorCentering.fc()
    assert ec_curl.x[Int3(0, 1, 1)] == -1.0
    assert ec_curl.y[Int3(0, 1, 1)] == 0.0
    assert ec_curl.z[Int3(0, 1, 1)] == 0.0
