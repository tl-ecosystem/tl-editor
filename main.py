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
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE

from src.tleng2 import *

from src.menu import menu_scene
from src.settings import settings_scene

hide_pygame_support_prompt()

GlobalSettings.update_resolutions((1280,720), (1280/5, 720/5))
RendererMethods.load_displays(HWSURFACE|DOUBLEBUF|RESIZABLE)
EngineMethods.set_caption("TL Editor")

GlobalSettings._fps = 60
# EngineMethods.import_render_params(`file`) the file is .json

GlobalSettings._debug = False


def main_test(time: int) -> None:
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()

    game = App()

    game.use_plugins(
        tleng_base_plugin
    )

    game.load_scenes(
        start_with='menu',
        menu=menu_scene,
        settings=settings_scene
    )

    from cProfile import Profile
    from pstats import SortKey, Stats
    with Profile() as profile:
        game._run_test(time)
        (
            Stats(profile)
            .strip_dirs()
            .sort_stats(SortKey.CUMULATIVE)
            .print_stats()
        )


def main() -> None:
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()

    game = App()

    game.use_plugins(
        tleng_base_plugin
    )

    game.load_scenes(
        start_with='menu',
        menu=menu_scene,
        settings=settings_scene
    )

    game.run()

if __name__ == "__main__":
    # main()
    main_test(5)

# State machine for scenes (schedule side)
#   Remove the systems schedule order, the order should be transistioned to the sequence types
# Control Systems (turn them on/off at will)