from enum import Enum, auto

from lib.vec3 import Bool3


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


if __name__ == "__main__":
    # basic tests

    assert (VectorCentering.EC.component_centered(0) == Bool3(True, False, False)).all()
    assert (VectorCentering.FC.component_centered(0) == Bool3(False, True, True)).all()

    print("tests passed")
