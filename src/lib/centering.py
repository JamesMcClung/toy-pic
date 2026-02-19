from typing import Self

from lib.vec3 import Bool3, Float3


class ScalarCentering:
    def __init__(self, is_ccs: Bool3):
        self.is_ccs = is_ccs
        self.offsets = is_ccs.to_mask().to_float3() * 0.5

    def copy(self) -> Self:
        return ScalarCentering(self.is_ccs.copy())

    @classmethod
    def nc(cls) -> Self:
        return cls(Bool3(False, False, False))

    @classmethod
    def ec(cls, d: int) -> Self:
        return cls(Bool3(d == 0, d == 1, d == 2))

    @classmethod
    def fc(cls, d: int) -> Self:
        return cls(Bool3(d != 0, d != 1, d != 2))

    @classmethod
    def cc(cls) -> Self:
        return cls(Bool3(True, True, True))


class VectorCentering:
    def __init__(self, x: ScalarCentering, y: ScalarCentering, z: ScalarCentering):
        self._comp_centerings = [x, y, z]

    def comp_is_ccs(self, d: int) -> Bool3:
        return self._comp_centerings[d].is_ccs

    def comp_offsets(self, d: int) -> Float3:
        return self._comp_centerings[d].offsets

    def copy(self) -> Self:
        return VectorCentering(*(comp_centering.copy() for comp_centering in self._comp_centerings))

    @classmethod
    def nc(cls) -> Self:
        return cls(ScalarCentering.nc(), ScalarCentering.nc(), ScalarCentering.nc())

    @classmethod
    def ec(cls) -> Self:
        return cls(ScalarCentering.ec(0), ScalarCentering.ec(1), ScalarCentering.ec(2))

    @classmethod
    def fc(cls) -> Self:
        return cls(ScalarCentering.fc(0), ScalarCentering.fc(1), ScalarCentering.fc(2))

    @classmethod
    def cc(cls) -> Self:
        return cls(ScalarCentering.cc(), ScalarCentering.cc(), ScalarCentering.cc())


def test():
    assert (VectorCentering.ec().comp_is_ccs(0) == Bool3(True, False, False)).all()
    assert (VectorCentering.fc().comp_is_ccs(0) == Bool3(False, True, True)).all()
