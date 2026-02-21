from lib.vector_field import VectorField


def push_e(e: VectorField, b: VectorField, j: VectorField, dt: float):
    # dE/dt = curl B - j
    e += b.curl().__isub__(j).__imul__(dt)


def push_b(e: VectorField, b: VectorField, dt: float):
    # dB/dt = -curl E
    b -= e.curl().__imul__(dt)
