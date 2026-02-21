from abc import ABC, abstractmethod

from lib.state import State


class GhostSetter(ABC):
    @abstractmethod
    def set_ghosts_e(self, state: State, d: int, upper: bool): ...

    @abstractmethod
    def set_ghosts_b(self, state: State, d: int, upper: bool): ...

    @abstractmethod
    def set_ghosts_j(self, state: State, d: int, upper: bool): ...
