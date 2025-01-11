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

import pygame
from pygame import FRect

from .tleng2 import *

from .tleng2.object.area import AreaComp
from .tleng2.components.renderable import DisplayCanvasComp
from .tleng2.components.camera import MainCameraComp, CameraComp
from .tleng2.components.scene import SceneComp
from .tleng2.components.engine import FpsComp
from .tleng2.components.renderable import DisplayCanvasComp, RenderableComp
from .tleng2.systems.engine_systems import ClockTickSystem

from .tleng2.utils.colors import AZURE

from .defaults import HandleEventsSystem, MoveBoxSystem, QuitGameSystem, TimeSystem


world = ecs.World()


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


srf = pygame.Surface((100,100))
srf.fill(AZURE)
e1 = world.spawn(
    RenderableComp(
        srf,
        FRect(10,10,10,10),
    )
)
        

settings_scheduler = ecs.Schedule()

settings_scheduler.add_systems(
    'Update',
    ecs.EventManagerSystem(11),
    HandleEventsSystem(10),
    TimeSystem(),
    QuitGameSystem(),
    MoveBoxSystem(),
    # DrawUICanvasSystem(0),
    ClockTickSystem(-2)
)


settings_scene = SceneComp(
    world,
    settings_scheduler
)

