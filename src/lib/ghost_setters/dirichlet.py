from numpy import s_

from lib.ghost_setters.ghost_setter_base import GhostSetter
from lib.scalar_field import ScalarField
from lib.state import State
from lib.vec3 import Float3


def set_ghosts_dirichlet(field: ScalarField, d: int, upper: bool, value: float):
    if not field.domain.vary_dims[d]:
        return

    ghost_slices = field.inner_slices()
    if upper:
        ghost_slices[d] = s_[field._array.shape[d] - field.n_ghosts_upper[d] :]
    else:
        ghost_slices[d] = s_[: field.n_ghosts_lower[d]]

    field._array[*ghost_slices] = value


class SetGhostsDirichlet(GhostSetter):
    def __init__(self, e: Float3, b: Float3):
        self.e = e
        self.b = b

    def set_ghosts_e(self, state: State, d: int, upper: bool):
        set_ghosts_dirichlet(state.e.x, d, upper, self.e.x)
        set_ghosts_dirichlet(state.e.y, d, upper, self.e.y)
        set_ghosts_dirichlet(state.e.z, d, upper, self.e.z)

    def set_ghosts_b(self, state: State, d: int, upper: bool):
        set_ghosts_dirichlet(state.b.x, d, upper, self.b.x)
        set_ghosts_dirichlet(state.b.y, d, upper, self.b.y)
        set_ghosts_dirichlet(state.b.z, d, upper, self.b.z)

    def set_ghosts_j(self, state: State, d: int, upper: bool):
        pass
