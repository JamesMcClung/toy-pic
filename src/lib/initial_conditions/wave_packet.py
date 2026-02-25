from typing import Literal

import numpy as np

from lib.domain import Domain
from lib.initial_conditions.initial_condition_base import InitialCondition
from lib.vec3 import Float3


class WavePacket(InitialCondition):
    def __init__(
        self,
        domain: Domain,
        *,
        pos: float | None = None,
        width: float | None = None,
        wavelength: float | None = None,
        amplitude: float = 1.0,
        dir: Literal[-1, 1] = 1,
    ):
        self.domain = domain

        self.packet_width = width if width is not None else domain.lengths.x / 16.0
        self.packet_pos = pos if pos is not None else domain.corner_pos.x + self.packet_width / 2.0
        self.wavelength = wavelength if wavelength is not None else self.packet_width
        self.amplitude = amplitude
        self.dir = float(dir)

    def ey(self, pos: Float3) -> float:
        return self.amplitude * np.exp(-(((pos.x - self.packet_pos) / self.packet_width) ** 2) / 2.0) * np.sin(2.0 * np.pi * (pos.x - self.packet_pos) / self.wavelength)

    def bz(self, pos: Float3) -> float:
        return self.dir * self.amplitude * np.exp(-(((pos.x - self.packet_pos) / self.packet_width) ** 2) / 2.0) * np.sin(2.0 * np.pi * (pos.x - self.packet_pos) / self.wavelength)
