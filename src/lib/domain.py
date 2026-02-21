from typing import Any

from lib.vec3 import Bool3, Float3, Int3


class Domain:
    def __init__(
        self,
        dims: Int3,
        deltas: Float3,
        *,
        corner_pos: Float3 | None = None,
        periodic_dims: Bool3 | None = None,
    ):
        self.dims = dims
        self.deltas = deltas
        self.corner_pos = corner_pos or Float3(0, 0, 0)
        self.periodic_dims = periodic_dims or Bool3(True, True, True)

        self.vary_dims = ~((dims == Int3(1, 1, 1)) & self.periodic_dims)
        self.lengths = self.dims.to_float3() * self.deltas

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Domain):
            return False

        return all((self.dims == other.dims) & (self.deltas == other.deltas) & (self.corner_pos == other.corner_pos) & (self.periodic_dims == other.periodic_dims))
