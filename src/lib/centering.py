from enum import Enum, auto

from lib.vec3 import Bool3, Float3


class VectorCentering(Enum):
    NC = auto()
    EC = auto()
    FC = auto()
    CC = auto()

    def component_centered(self, d: int) -> Bool3:
        match self:
            case VectorCentering.NC:
                return Bool3(False, False, False)
            case VectorCentering.EC:
                return Bool3(d == 0, d == 1, d == 2)
            case VectorCentering.FC:
                return Bool3(d != 0, d != 1, d != 2)
            case VectorCentering.CC:
                return Bool3(True, True, True)

    def component_offsets(self, d: int) -> Float3:
        return self.component_centered(d).to_mask().to_float3() * 0.5


def test():
    assert (VectorCentering.EC.component_centered(0) == Bool3(True, False, False)).all()
    assert (VectorCentering.FC.component_centered(0) == Bool3(False, True, True)).all()
