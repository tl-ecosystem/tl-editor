import pygame
from pygame.locals import *

from src.tleng2 import *

from src.menu import world as Menu

GlobalSettings.update_bresolution((1280,720))
RendererMethods.load_displays(RESIZABLE)
EngineMethods.set_caption("TL Editor")

GlobalSettings._fps = 60
# EngineMethods.import_render_params(`file`) the file is .json

GlobalSettings._debug = False

def main():
    pygame.init()

    game = Game()

    game.load_worlds(
        start_with='menu',
        menu=Menu,
    )
    
    game.run()

if __name__ == "__main__":
    main()