# from dataclasses import dataclass

from pygame import FRect

from .tleng2 import *

from .tleng2.ecs.events import EventComp, HandleEventsSystem, pygame_quit_handler
from .tleng2.object.area import AreaComp
from .tleng2.components.camera import *
from .tleng2.components.renderable import DisplayCanvasComp, RenderableComp
from .tleng2.systems.engine_syst import ClockTickSystem
from .tleng2.systems.renderer import RendererSystem
from .tleng2.uix.ui_canvas import UICanvas
# from .tleng2.uix import UICanvas, UICanvasDrawSystem, BoxLayout
from .tleng2.utils.event_manager import set_handler
from .tleng2.utils.colors import AQUAMARINE, WHITESMOKE


from typing import Callable as _Callable
# from typing import   


world = ecs.World()

RendererProperties.fill_screen_color = AQUAMARINE

world.append_unique_components(
    {
        DisplayCanvasComp: DisplayCanvasComp(GlobalSettings._win_res),
        EventComp : EventComp(
            (pygame.QUIT, 'QUIT'),
        )
    }
)

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
        # print(self.world.schedule.system_schedule[1]._display)
        EngineMethods.set_caption(f"{EngineProperties._clock.get_fps():.2f}")
        print('newframe')
        print(*[event for event in EngineProperties._events], sep='\n')
        # print(f"{EngineProperties._clock.get_fps():.2f}")



set_handler('QUIT', pygame_quit_handler)
# set_handler('RESIZE', )

world_scheduler.add_systems(
    HandleEventsSystem(10),
    LogicSystem(1),
    # DrawUICanvasSystem(0),
    RendererSystem(-1),
    ClockTickSystem(-2)
)

world.use_schedule(world_scheduler)