import pygame
import math

from setuptools import sic

from .tleng2 import *

from .tleng2.systems.renderer import ResizeWindowEvent
from .tleng2.components.events import QuitGameEvent
from .tleng2.components.renderable import RenderableComp


class HandleEventsSystem(ecs.System):
    def parameters(self, events: ecs.Events, sm: ecs.ScenesManager):
        self.events = events
        self.sm = sm


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


class QuitGameSystem(ecs.System):
    def parameters(self, world: ecs.World, events: ecs.Events):
        self.world = world
        self.events = events

    def update(self) -> None:
        
        events = self.events.read(QuitGameEvent)
        if events:
            EngineProperties.GAME_RUNNING = False


class LogicSystem(ecs.System):
    def parameters(self, world: ecs.World, events: ecs.Events):
        self.world = world

    def update(self) -> None:
        # print(self.world.schedule.system_schedule[1]._display)
        pygame.display.set_caption(f"{EngineProperties._clock.get_fps():.2f} | {(EngineProperties._dt):.5f} ms'")
        # ...

class MoveBoxSystem(ecs.System):
    def parameters(self, world: ecs.World) -> None:
        self.world = world
    
    def update(self) -> None:
        components = self.world.single_fast_query(RenderableComp)

        for e, renderable in components:
            renderable.rect.x += 0.7
            renderable.rect.y += math.sin(renderable.rect.x/10)*10
            if renderable.rect.x > GlobalSettings._win_res[0]:
                renderable.rect.x = 0
        