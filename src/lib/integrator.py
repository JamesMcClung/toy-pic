from lib.push_fields import push_b, push_e
from lib.state import State


class Integrator:
    def __init__(self, state: State, dt: float):
        self.timestep = 0
        self.dt = dt
        self.state = state

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
        push_e(self.state, self.dt)
        push_b(self.state, self.dt / 2.0)
