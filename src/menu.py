# from dataclasses import dataclass

from pygame import FRect



from .tleng2 import *

from .tleng2.engine.event_handler import HandleEventsSystem, pygame_quit_handle
from .tleng2.object.area import AreaComp
from .tleng2.components.camera import *
from .tleng2.components.renderable import DisplayCanvasComp, RenderableComp
from .tleng2.systems.engine_syst import ClockTickSystem
from .tleng2.systems.renderer import RendererSystem
from .tleng2.uix.ui_canvas import UICanvas

from .tleng2.utils.event_manager import set_handler
from .tleng2.utils.colors import AQUAMARINE, WHITESMOKE

# from .tleng2.uix import UICanvas, UICanvasDrawSystem, BoxLayout

world = ecs.World()

RendererProperties.fill_screen_color = AQUAMARINE

display_canvas = world.spawn(
    DisplayCanvasComp(GlobalSettings._win_res)
)


# Game Enviroment Camera
camera1 = world.spawn(
    MainCameraComp(),
    CameraComp(
        display_canvas,
        AreaComp(
            0,
            0,
            GlobalSettings._win_res[0],
            GlobalSettings._win_res[0]
        ),
    ),
)

# enviroment
srf = pygame.Surface((100,100))
srf.fill(WHITESMOKE)
e1 = world.spawn(
    RenderableComp(
        srf,
        FRect(10,10,10,10),
    )
)

e2 = world.spawn(
    RenderableComp(
        srf,
        FRect(10,120,10,10),
    )
)

e3 = world.spawn(
    RenderableComp(
        srf,
        FRect(120,10,10,10),
    )
)

e4 = world.spawn(
    RenderableComp(
        srf,
        FRect(120,120,10,10),
    )
)

ui = world.spawn(
    UICanvas(
        # Image(),
        # Button(),
    ),
)

world_scheduler = ecs.Schedule()

class LogicSystem(ecs.System):
    def update(self) -> None:
        EngineMethods.set_caption(f"{EngineProperties._clock.get_fps():.2f}")
        # print(f"{EngineProperties._clock.get_fps():.2f}")


world_scheduler.add_systems(
    LogicSystem(1),
    # DrawUICanvasSystem(0),
    RendererSystem(-1),
    ClockTickSystem(-2)
)

world.use_schedule(world_scheduler)