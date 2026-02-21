from __future__ import annotations

from lib.domain import Domain
from lib.ghost_manager import GhostManager3d
from lib.ghost_setters.periodic import SetGhostsPeriodic
from lib.push_fields import push_b, push_e
from lib.state import State


class IntegratorBuilder:
    def __init__(self, domain: Domain, dt: float):
        self.dt = dt
        self.state = State(domain)
        self.ghost_manager = GhostManager3d.periodic()

    def build(self) -> Integrator:
        return Integrator(self)


class Integrator:
    def __init__(self, builder: IntegratorBuilder):
        self.state = builder.state
        self.dt = builder.dt
        self.timestep = 0
        self.ghost_manager = builder.ghost_manager
        for d in range(3):
            if self.state.domain.periodic_dims[d]:
                assert isinstance(self.ghost_manager._managers[d], SetGhostsPeriodic)

    def integrate(self, n_steps: int | None = None):
        if n_steps is None:
            while True:
                self.step()
        else:
            for _ in range(n_steps):
                self.step()

    def step(self):
        # TODO particles here

        push_b(self.state, self.dt / 2.0)
        self.ghost_manager.set_ghosts_b(self.state)

        push_e(self.state, self.dt)
        self.ghost_manager.set_ghosts_e(self.state)

        push_b(self.state, self.dt / 2.0)
        self.ghost_manager.set_ghosts_b(self.state)
