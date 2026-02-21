from cases.wave_packet import WavePacket
from lib.domain import Domain
from lib.integrator import IntegratorBuilder
from lib.vec3 import Float3, Int3

domain = Domain(Int3(64, 4, 4), Float3(1.0, 1.0, 1.0))

builder = IntegratorBuilder(domain, 0.75)

WavePacket(domain).init_state(builder.initial_state)

integrator = builder.build()

integrator.integrate(10)
