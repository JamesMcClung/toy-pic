from numpy import s_

from lib.ghost_manager import GhostSetter
from lib.scalar_field import ScalarField
from lib.state import State


def set_ghosts_periodic(field: ScalarField, d: int, upper: bool):
    if not field.domain.vary_dims[d]:
        return

    ghost_slices = field.inner_slices()
    inner_edge_slices = field.inner_slices()
    if upper:
        ghost_slices[d] = s_[field._array.shape[d] - field.n_ghosts_upper[d] :]
        inner_edge_slices[d] = s_[field.n_ghosts_lower[d] : field.n_ghosts_lower[d] + field.n_ghosts_upper[d]]
    else:
        ghost_slices[d] = s_[: field.n_ghosts_lower[d]]
        inner_edge_slices[d] = s_[field._array.shape[d] - field.n_ghosts_lower[d] - field.n_ghosts_upper[d] : field._array.shape[d] - field.n_ghosts_upper[d]]

    field._array[*ghost_slices] = field._array[*inner_edge_slices]


class SetGhostsPeriodic(GhostSetter):
    def set_ghosts_e(self, state: State, d: int, upper: bool):
        set_ghosts_periodic(state.e.x, d, upper)
        set_ghosts_periodic(state.e.y, d, upper)
        set_ghosts_periodic(state.e.z, d, upper)

    def set_ghosts_b(self, state: State, d: int, upper: bool):
        set_ghosts_periodic(state.b.x, d, upper)
        set_ghosts_periodic(state.b.y, d, upper)
        set_ghosts_periodic(state.b.z, d, upper)

    def set_ghosts_j(self, state: State, d: int, upper: bool):
        set_ghosts_periodic(state.j.x, d, upper)
        set_ghosts_periodic(state.j.y, d, upper)
        set_ghosts_periodic(state.j.z, d, upper)
