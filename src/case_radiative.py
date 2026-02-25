import fastplotlib as fpl
import numpy as np

from lib.domain import Domain
from lib.ghost_setters.dirichlet import SetGhostsDirichlet
from lib.ghost_setters.radiative import PlaneWave, SetGhostsRadiative
from lib.integrator import IntegratorBuilder
from lib.state import State
from lib.vec3 import Bool3, Float3, Int3

domain = Domain(Int3(256, 2, 1), Float3(1.0, 1.0, 1.0), periodic_dims=Bool3(False, True, True))

builder = IntegratorBuilder(domain, 0.15)

builder.ghost_manager.x.lower = SetGhostsRadiative(builder.dt, s=PlaneWave(1.0, 4.0))
builder.ghost_manager.x.upper = SetGhostsDirichlet(Float3(0.0, 0.0, 0.0), Float3(0.0, 0.0, 0.0))

integrator = builder.build()

figure = fpl.Figure(size=(700, 560))


def get_image_data(state: State) -> np.ndarray:
    return state.e.y._inner_array.mean(axis=2).T


IMAGE_NAME = "image"
figure[0, 0].add_image(data=get_image_data(integrator.state), name=IMAGE_NAME, vmin=-2.0, vmax=2.0, cmap="RdBu")


def next_image(subplot: fpl.layouts.Subplot):
    integrator.step()
    subplot[IMAGE_NAME].data = get_image_data(integrator.state)


figure[0, 0].add_animations(next_image)

figure.show(maintain_aspect=False)
fpl.loop.run()
