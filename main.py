import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE

from src.tleng2 import *


from src.menu import menu_scene
from src.settings import settings_scene

hide_pygame_support_prompt()

GlobalSettings.update_bresolution((1280,720))
RendererMethods.load_displays(HWSURFACE|DOUBLEBUF|RESIZABLE)
EngineMethods.set_caption("TL Editor")

GlobalSettings._fps = 60
# EngineMethods.import_render_params(`file`) the file is .json

GlobalSettings._debug = False


def main_test() -> None:
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

    game._run_test(6)

def profile():
    from cProfile import Profile
    from pstats import SortKey, Stats
    with Profile() as profile:
        main_test()
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
    # profile()

# Add states so there can be multiple schedules for one world.

# resources for the 'App'

# Default system bundle for the engine

# on the update sequence in the scheduler, the data from game is going to get updated.


# before we reach the renderer, 
#   spritestack, image, animation, fancy_animation systems, are going to 
#   run first to update their respective renderable 
# renderer renders only the renderables
