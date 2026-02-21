from abc import ABC, abstractmethod

from lib.state import State


class GhostSetter(ABC):
    @abstractmethod
    def set_ghosts_e(self, state: State, d: int, upper: bool): ...

    @abstractmethod
    def set_ghosts_b(self, state: State, d: int, upper: bool): ...

    @abstractmethod
    def set_ghosts_j(self, state: State, d: int, upper: bool): ...


class GhostManager1d:
    def __init__(self, lower: GhostSetter, upper: GhostSetter):
        self.lower = lower
        self.upper = upper

    def set_ghosts_e(self, state: State, d: int):
        self.lower.set_ghosts_e(state, d, False)
        self.upper.set_ghosts_e(state, d, True)

    def set_ghosts_b(self, state: State, d: int):
        self.lower.set_ghosts_b(state, d, False)
        self.upper.set_ghosts_b(state, d, True)

    def set_ghosts_j(self, state: State, d: int):
        self.lower.set_ghosts_j(state, d, False)
        self.upper.set_ghosts_j(state, d, True)


class GhostManager3d:
    def __init__(self, x: GhostManager1d, y: GhostManager1d, z: GhostManager1d):
        self._managers = [x, y, z]

    @property
    def x(self) -> GhostManager1d:
        return self._managers[0]

    @property
    def y(self) -> GhostManager1d:
        return self._managers[1]

    @property
    def z(self) -> GhostManager1d:
        return self._managers[2]

    def set_ghosts_e(self, state: State):
        for d in range(3):
            self._managers[d].set_ghosts_e(state, d)

    def set_ghosts_b(self, state: State):
        for d in range(3):
            self._managers[d].set_ghosts_b(state, d)

    def set_ghosts_j(self, state: State):
        for d in range(3):
            self._managers[d].set_ghosts_j(state, d)
