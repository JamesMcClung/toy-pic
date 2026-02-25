from abc import ABC, abstractmethod
from typing import Callable

import numpy as np

from lib.ghost_setters.ghost_setter_base import GhostSetter
from lib.state import State

type WaveForm = Callable[[np.ndarray, np.ndarray, float], float | np.ndarray]


class WaveForm(ABC):
    @abstractmethod
    def sample(self, pos_x: np.ndarray, pos_y: np.ndarray, t: float) -> np.ndarray | float: ...


class PlaneWave(WaveForm):
    def __init__(self, amplitude: float, wavelength: float):
        self.amplitude = amplitude
        self.wavelength = wavelength

    def sample(self, pos_x: np.ndarray, pos_y: np.ndarray, t: float) -> np.ndarray | float:
        return self.amplitude * np.sin(-t / self.wavelength)


class ZeroForm(WaveForm):
    def sample(self, pos_x: np.ndarray, pos_y: np.ndarray, t: float) -> np.ndarray | float:
        return 0.0


class SetGhostsRadiative(GhostSetter):
    def __init__(
        self,
        dt: float,
        *,
        s: WaveForm | None = None,
        p: WaveForm | None = None,
    ):
        self.dt = dt

        self.s = s or ZeroForm()
        self.p = p or ZeroForm()

    def set_ghosts_e(self, state: State, d: int, upper: bool):
        pass

    def set_ghosts_b(self, state: State, d: int, upper: bool):
        assert not upper

        d1 = (d + 1) % 3
        d2 = (d + 2) % 3

        by = state.b[d2]
        by_ghost_slices = by.inner_slices()
        by_ghost_slices[d] = slice(by.n_ghosts_lower[d] - 1, by.n_ghosts_lower[d])
        by_slices = by.inner_slices()
        by_slices[d] = slice(by.n_ghosts_lower[d], by.n_ghosts_lower[d] + 1)

        ex = state.e[d1]
        ex_slices = ex.inner_slices()
        ex_slices[d] = slice(ex.n_ghosts_lower[d], ex.n_ghosts_lower[d] + 1)

        if state.domain.vary_dims[d2]:
            bz = state.b[d]
            bz_upper_slices = bz.inner_slices()
            bz_upper_slices[d] = slice(bz.n_ghosts_lower[d], bz.n_ghosts_lower[d] + 1)
            bz_lower_slices = bz.inner_slices()
            bz_lower_slices[d] = slice(bz.n_ghosts_lower[d], bz.n_ghosts_lower[d] + 1)
            bz_lower_slices[d2] = slice(bz_lower_slices[d2].start - 1, bz_lower_slices[d2].stop - 1)
            bz_grad = bz._array[*bz_upper_slices] - bz._array[*bz_lower_slices]
        else:
            bz_grad = 0.0

        jx = state.j[d1]
        jx_slices = jx.inner_slices()
        jx_slices[d] = slice(jx.n_ghosts_lower[d], jx.n_ghosts_lower[d] + 1)

        sx_posx, sx_posy = np.meshgrid(ex.get_inner_positions(d1), ex.get_inner_positions(d2))
        sx = self.s.sample(sx_posx, sx_posy, state.time)

        # By[t; x+, y, 0-] = 1/(1+dt/dz) * (
        #       4 * S[t; x+, y, 0]
        #     - 2 * Ex[t-; x+, y, 0]
        #     + dt/dy * (Bz[t; x+, y+, 0] - Bz[n; x+, y-, 0])
        #     - (1-dt/dz) * By[t; x+, y, 0+]
        #     + dt * Jx[t; x+, y, 0]
        # )

        by._array[*by_ghost_slices] = (
            1.0
            / (1.0 + self.dt / state.domain.deltas[d])
            * (
                4.0 * sx
                - 2.0 * ex._array[*ex_slices]
                + (self.dt / state.domain.deltas[d2]) * bz_grad
                - (1.0 - self.dt / state.domain.deltas[d]) * by._array[*by_slices]
                + self.dt * jx._array[*jx_slices]
                #
            )
        )

        bx = state.b[d1]
        bx_ghost_slices = bx.inner_slices()
        bx_ghost_slices[d] = slice(bx.n_ghosts_lower[d] - 1, bx.n_ghosts_lower[d])
        bx_slices = bx.inner_slices()
        bx_slices[d] = slice(bx.n_ghosts_lower[d], bx.n_ghosts_lower[d] + 1)

        ey = state.e[d2]
        ey_slices = ey.inner_slices()
        ey_slices[d] = slice(ey.n_ghosts_lower[d], ey.n_ghosts_lower[d] + 1)

        if state.domain.vary_dims[d1]:
            bz = state.b[d]
            bz_upper_slices = bz.inner_slices()
            bz_upper_slices[d] = slice(bz.n_ghosts_lower[d], bz.n_ghosts_lower[d] + 1)
            bz_lower_slices = bz.inner_slices()
            bz_lower_slices[d] = slice(bz.n_ghosts_lower[d], bz.n_ghosts_lower[d] + 1)
            bz_lower_slices[d1] = slice(bz_lower_slices[d1].start - 1, bz_lower_slices[d1].stop - 1)
            bz_grad = bz._array[*bz_upper_slices] - bz._array[*bz_lower_slices]
        else:
            bz_grad = 0.0

        jy = state.j[d1]
        jy_slices = jy.inner_slices()
        jy_slices[d] = slice(jy.n_ghosts_lower[d], jy.n_ghosts_lower[d] + 1)

        py_posx, py_posy = np.meshgrid(ey.get_inner_positions(d1), ey.get_inner_positions(d2))
        py = self.s.sample(py_posx, py_posy, state.time)

        # Bx[t; x, y+, 0-] = 1/(1+dt/dz) * (
        #      -4 * P[t; x, y+, 0]
        #     + 2 * Ey[t-; x, y+, 0]
        #     + dt/dx * (Bz[t; x+, y+, 0] - Bz[n; x-, y+, 0])
        #     - (1-dt/dz) * Bx[t; x, y+, 0+]
        #     - dt * Jy[t; x, y+, 0]
        # )

        bx._array[*bx_ghost_slices] = (
            1.0
            / (1.0 + self.dt / state.domain.deltas[d])
            * (
                -4.0 * py
                + 2.0 * ey._array[*ey_slices]
                + (self.dt / state.domain.deltas[d1]) * bz_grad
                - (1.0 - self.dt / state.domain.deltas[d]) * bx._array[*bx_slices]
                - self.dt * jy._array[*jy_slices]
                #
            )
        )

    def set_ghosts_j(self, state: State, d: int, upper: bool):
        pass
