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
    main()
    # main_test(5)

# State machine for scenes (schedule side)
# Control Systems (turn them on/off at will)