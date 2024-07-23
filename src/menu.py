from dataclasses import dataclass

from .tleng2 import *
from .tleng2.components.camera import *
from .tleng2.systems.engine_syst import FpsComp, ClockTickSystem
from .tleng2.systems.renderer import  RenderableComp, RendererSystem

# from .tleng2.uix import UICanvas, UICanvasDrawSystem, BoxLayout

world = ecs.World()

engine_params = world.spawn(
    FpsComp(60),
)


# ui = world.spawn(
#     UICanvas(
#         Image(),
#         Button(),
#         layout=BoxLayout('VERTICAL')
#     )
# )


world_scheduler = ecs.Schedule()


world_scheduler.add_systems(
    # DrawUICanvasSystem(-1),
    RendererSystem(-1),
    ClockTickSystem(-2)
)

world.use_schedule(world_scheduler)