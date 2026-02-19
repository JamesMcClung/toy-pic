from lib.centering import VectorCentering
from lib.domain import Domain
from lib.field_array import FieldArray


class VectorField:
    def __init__(
        self,
        domain: Domain,
        centering: VectorCentering,
    ):
        self.domain = domain
        self.centering = centering

        self._components = []
        for d in range(3):
            # nc values at upper edge are in domain
            comp_dims = domain.dims + centering.component_centered(d).flip().to_mask()
            self._components.append(FieldArray(comp_dims, n_ghosts=domain.vary_dims.to_mask() * domain.n_ghosts))

    def __getitem__(self, d: int) -> FieldArray:
        return self._components[d]

    @property
    def x(self) -> FieldArray:
        return self._components[0]

    @property
    def y(self) -> FieldArray:
        return self._components[1]

    @property
    def z(self) -> FieldArray:
        return self._components[2]
