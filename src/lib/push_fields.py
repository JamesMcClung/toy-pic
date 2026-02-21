from lib.state import State


def push_e(state: State, dt: float):
    # dE/dt = curl B - j
    state.e += state.b.curl().__isub__(state.j).__imul__(dt)


def push_b(state: State, dt: float):
    # dB/dt = -curl E
    state.b -= state.e.curl().__imul__(dt)
