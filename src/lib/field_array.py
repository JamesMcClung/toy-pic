import numpy as np

from lib.vec3 import Int3


class FieldArray:
    def __init__(self, dims: Int3, n_ghosts: Int3):
        self.dims = dims
        self.n_ghosts = n_ghosts
        self.array = np.zeros(dims + 2 * n_ghosts)

    def __getitem__(self, i3: Int3) -> float:
        return self.array[*(self.n_ghosts + i3)]

    def __setitem__(self, i3: Int3, val: float):
        self.array[*(self.n_ghosts + i3)] = val


if __name__ == "__main__":
    # basic tests

    field = FieldArray(Int3(4, 4, 4), Int3(2, 2, 2))

    i3 = Int3(1, -1, 0)
    assert field[i3] == 0.0

    field[i3] == 1.0
    assert field[i3] == 1.0

    print("tests passed")
