from lib.state import State
from lib.vec3 import Float3


class InitialCondition:
    def ex(self, pos: Float3) -> float:
        return 0.0

    def ey(self, pos: Float3) -> float:
        return 0.0

    def ez(self, pos: Float3) -> float:
        return 0.0

    def bx(self, pos: Float3) -> float:
        return 0.0

    def by(self, pos: Float3) -> float:
        return 0.0

    def bz(self, pos: Float3) -> float:
        return 0.0

    def init_state(self, state: State):
        state.e.x.set_from_func(self.ex)
        state.e.y.set_from_func(self.ey)
        state.e.z.set_from_func(self.ez)

        state.b.x.set_from_func(self.bx)
        state.b.y.set_from_func(self.by)
        state.b.z.set_from_func(self.bz)
