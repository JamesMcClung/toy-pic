from abc import ABC, abstractmethod

from lib.state import State


class Diagnostic(ABC):
    def __init__(self, interval: int):
        self.interval = interval

    @abstractmethod
    def run_diagnostic(self, state: State): ...

    def should_run_at_timestep(self, timestep: int) -> bool:
        return self.interval > 0 and timestep % self.interval == 0
