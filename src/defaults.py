import pygame


from .tleng2 import *

from .tleng2.systems.renderer import ResizeWindowEvent
from .tleng2.components.events import QuitGameEvent


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
        self.events = events

    def update(self) -> None:
        # print(self.world.schedule.system_schedule[1]._display)
        EngineMethods.set_caption(f"{EngineProperties._clock.get_fps():.2f}")
        if EngineProperties._clock.get_fps() < 200:
            print(True)
        
        events = self.events.read(QuitGameEvent)