import fastplotlib as fpl
import numpy as np

from cases.wave_packet import WavePacket
from lib.domain import Domain
from lib.integrator import IntegratorBuilder
from lib.state import State
from lib.vec3 import Float3, Int3

domain = Domain(Int3(256, 2, 1), Float3(1.0, 1.0, 1.0))

builder = IntegratorBuilder(domain, 0.15)

WavePacket(domain).init_state(builder.initial_state)

integrator = builder.build()

figure = fpl.Figure(size=(700, 560))


def get_image_data(state: State) -> np.ndarray:
    return state.e.y._inner_array.mean(axis=2).T


IMAGE_NAME = "image"
figure[0, 0].add_image(data=get_image_data(integrator.state), name=IMAGE_NAME)


def next_image(subplot: fpl.layouts.Subplot):
    integrator.step()
    subplot[IMAGE_NAME].data = get_image_data(integrator.state)


figure[0, 0].add_animations(next_image)

figure.show(maintain_aspect=False)
fpl.loop.run()
