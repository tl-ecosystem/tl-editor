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

import time
import pygame
import math

from .tleng2 import *

from .tleng2.systems.renderer import ResizeWindowEvent
from .tleng2.components.events import QuitGameEvent
from .tleng2.components.renderable import RenderableComp


class HandleEventsSystem(ecs.System):
    def parameters(self, events: ecs.Events, sm: ecs.ScenesManager):
        self.events = events
        self.sm = sm
        # self.com = com


    def update(self) -> None:
        for event in EngineProperties._events:
            if event.type == pygame.QUIT:
                self.events.send(QuitGameEvent())
            if event.type == pygame.WINDOWRESIZED:
                self.events.send(ResizeWindowEvent())
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    self.sm.change_scene('menu')
                if event.key == pygame.K_2:
                    self.sm.change_scene('settings')

                # if event.key == pygame.K_ESCAPE:
                #     self.com.change_state('PausedState', 'Running')


class QuitGameSystem(ecs.System):
    def parameters(self, events: ecs.Events):
        self.events = events

    def update(self) -> None:
        events = self.events.read(QuitGameEvent)

        if events:
            EngineProperties.GAME_RUNNING = False


class TimeSystem(ecs.System):
    def parameters(self, world: ecs.World, events: ecs.Events):
        self.world = world

        self.t1 = time.time()
        self.t2 = time.time()
        self.getTicksLastFrame = 0
        self.frames = 0

    def update(self) -> None:
        # print(self.world.schedule.system_schedule[1]._display)
        
        
        # t = pygame.time.get_ticks()
        # # deltaTime in seconds.
        self.t2 = time.time()
        if self.t2 - self.t1 > 1:
            pygame.display.set_caption(f'{self.frames} FPS')
            self.frames = 0
            self.t1 = self.t2
        else:
            self.frames += 1
        # pygame.display.set_caption(f"{EngineProperties._clock.get_fps():.2f} | {((t - self.getTicksLastFrame) / 1000.0)} ms || {(1/(self.t2 - self.t1)):.2f} fps | {(self.t2 - self.t1):.5f} ms'")
        # self.t1 = self.t2
        # self.getTicksLastFrame = t


class MoveBoxSystem(ecs.System):
    def parameters(self, world: ecs.World) -> None:
        self.world = world
    
    def update(self) -> None:
        components = self.world.single_fast_query(RenderableComp)

        for e, renderable in components:
            renderable.rect.x += 0.7
            renderable.rect.y += math.sin(renderable.rect.x/10)
            if renderable.rect.x > GlobalSettings._win_res[0]:
                renderable.rect.x = 0
