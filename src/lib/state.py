from lib.centering import VectorCentering
from lib.domain import Domain
from lib.vector_field import VectorField


class State:
    def __init__(self, domain: Domain):
        self.domain = domain
        self.e = VectorField.zeros(domain, VectorCentering.ec())
        self.b = VectorField.zeros(domain, VectorCentering.fc())
        self.j = VectorField.zeros(domain, VectorCentering.ec())
        self.time = 0.0
