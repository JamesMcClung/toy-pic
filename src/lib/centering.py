from typing import Self

from lib.vec3 import Bool3, Float3


class VectorCentering:
    def __init__(self, x_cc: Bool3, y_cc: Bool3, z_cc: Bool3):
        self._is_ccss = [x_cc, y_cc, z_cc]
        self._offsetss = [comp_is_ccs.to_mask().to_float3() * 0.5 for comp_is_ccs in self._is_ccss]

    def comp_is_ccs(self, d: int) -> Bool3:
        return self._is_ccss[d]

    def comp_offsets(self, d: int) -> Float3:
        return self._offsetss[d]

    def copy(self) -> Self:
        return VectorCentering(*(is_comp_cc.copy() for is_comp_cc in self._is_ccss))

    @classmethod
    def nc(cls) -> Self:
        return cls(
            Bool3(False, False, False),
            Bool3(False, False, False),
            Bool3(False, False, False),
        )

    @classmethod
    def ec(cls) -> Self:
        return cls(
            Bool3(True, False, False),
            Bool3(False, True, False),
            Bool3(False, False, True),
        )

    @classmethod
    def fc(cls) -> Self:
        return cls(
            Bool3(False, True, True),
            Bool3(True, False, True),
            Bool3(True, True, False),
        )

    @classmethod
    def cc(cls) -> Self:
        return cls(
            Bool3(True, True, True),
            Bool3(True, True, True),
            Bool3(True, True, True),
        )


def test():
    assert (VectorCentering.ec().comp_is_ccs(0) == Bool3(True, False, False)).all()
    assert (VectorCentering.fc().comp_is_ccs(0) == Bool3(False, True, True)).all()
