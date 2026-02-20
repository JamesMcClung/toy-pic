import numpy as np


def take_slice(arr: np.ndarray, axis: int, s: slice) -> np.ndarray:
    return arr[(slice(None),) * axis + (s,) + (slice(None),) * (arr.ndim - axis - 1)]
