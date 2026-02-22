import numpy as np

from cases.case_base import Case
from lib.domain import Domain
from lib.vec3 import Float3


class WavePacket(Case):
    def __init__(self, domain: Domain):
        self.domain = domain

        self.packet_width = domain.lengths.x / 16.0
        self.packet_pos = domain.corner_pos.x + self.packet_width / 2.0
        self.wavelength = self.packet_width / 2.0

    def ey(self, pos: Float3) -> float:
        return 1.0 * np.exp(-(((pos.x - self.packet_pos) / self.packet_width) ** 2)) * np.sin(2.0 * np.pi * (pos.x - self.packet_pos) / self.wavelength)

    def bz(self, pos: Float3) -> float:
        return 1.0 * np.exp(-(((pos.x - self.packet_pos) / self.packet_width) ** 2)) * np.sin(2.0 * np.pi * (pos.x - self.packet_pos) / self.wavelength)
