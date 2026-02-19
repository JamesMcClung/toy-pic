import numpy as np

from lib.vec3 import Int3


class FieldArray:
    def __init__(self, dims: Int3, n_ghosts: Int3 | tuple[Int3, Int3]):
        self.dims = dims
        if isinstance(n_ghosts, Int3):
            n_ghosts = (n_ghosts, n_ghosts)
        self.n_ghosts_lower, self.n_ghosts_upper = n_ghosts
        self._array = np.zeros(self.n_ghosts_lower + dims + self.n_ghosts_upper)

    def _shift_idx(self, i3: Int3) -> Int3:
        return i3 + self.n_ghosts_lower

    def __getitem__(self, i3: Int3) -> float:
        return self._array[*self._shift_idx(i3)]

    def __setitem__(self, i3: Int3, val: float):
        self._array[*self._shift_idx(i3)] = val


def test():
    field = FieldArray(Int3(4, 4, 4), Int3(2, 2, 2))

    i3 = Int3(1, -1, 0)
    assert field[i3] == 0.0

    field[i3] = 1.0
    assert field[i3] == 1.0
