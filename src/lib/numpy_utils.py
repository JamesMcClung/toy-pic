import numpy as np
from numpy import s_


def take_slice(arr: np.ndarray, axis: int, s: slice) -> np.ndarray:
    return arr[(s_[:],) * axis + (s,) + (s_[:],) * (arr.ndim - axis - 1)]
