# tl-editor
# A simple editor for scenes designated to be used by the tleng game engine.

# Copyright (C) 2024 Theolaos
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/

import random
import pygame
from pygame import FRect

# from dataclasses import dataclass

from .tleng2 import *

from .tleng2.object.area import AreaComp

from .tleng2.components.camera import MainCameraComp, CameraComp
from .tleng2.components.renderable import DisplayCanvasComp, RenderableComp
from .tleng2.components.engine import FpsComp

from .tleng2.uix.ui_canvas import UICanvas
# from .tleng2.uix import UICanvas, UICanvasDrawSystem, BoxLayout
from .tleng2.utils.colors import AQUAMARINE, WHITESMOKE

from .defaults import HandleEventsSystem, MoveBoxSystem, QuitGameSystem, TimeSystem

world = ecs.World()

RendererProperties.fill_screen_color = AQUAMARINE

world.append_resources(
    DisplayCanvasComp(GlobalSettings._win_res),
    FpsComp(2000)
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

num = 2

for x in range(num):
    srf = pygame.Surface((100,100))
    srf.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    world.spawn(
        RenderableComp(
            srf,
            FRect(random.randint(0,1200),random.randint(0, 600),100,100),
        )
    )


menu_scheduler = ecs.Scheduler()

menu_scheduler.add_systems(
    'Update',
    ecs.EventManagerSystem(),
    HandleEventsSystem(),
    TimeSystem(),
    QuitGameSystem(),
    MoveBoxSystem(),
    # DrawUICanvasSystem(0),
)


menu_scene = ecs.SceneComp(
    world.return_world_component(),
    menu_scheduler
)
