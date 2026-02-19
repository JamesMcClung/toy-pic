from lib.vec3 import Bool3, Float3, Int3


class Domain:
    def __init__(
        self,
        dims: Int3,
        deltas: Float3,
        *,
        n_ghosts: int = 1,
        corner_pos: Float3 | None = None,
        vary_dims: Bool3 | None = None,
    ):
        self.dims = dims
        self.deltas = deltas
        self.n_ghosts = n_ghosts
        self.corner_pos = corner_pos or Float3(0, 0, 0)
        self.vary_dims = vary_dims or dims != Int3(1, 1, 1)
