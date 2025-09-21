import logging

import pygame

from constants import FPS
from controls.recognizer import Recognizer
from scenes import SceneManager
from scenes.main_menu import MainMenuScene
from scenes.game_scene import GameScene

from utils import load_image

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s', filename="game.log", level=logging.DEBUG)

class Game:
    def __init__(self, title: str, width: int, height: int):
        super().__init__()

        # Setup
        self.title = title
        self.width = width
        self.height = height

    def run(self):
        """Main game loop."""

        logger.info("Game launched")

        # pygame setup
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.SCALED)
        pygame.display.set_caption("Flow Heroes")
        pygame.display.set_icon(load_image("assets/gamekit/2 512x512/2_2.png"))

        clock = pygame.time.Clock()
        running = True

        recognizer = Recognizer(daemon=True)
        recognizer.start()

        manager = SceneManager(screen)
        main_menu_scene = MainMenuScene(manager)
        game_scene = GameScene(manager)
        manager.add_scene("main_menu", main_menu_scene)
        manager.add_scene("game", game_scene)
        manager.set_scene("main_menu")

        while running:
            dt = clock.tick(FPS)

            # poll for events
            # pygame.QUIT event means the user clicked X to close the window
            events = pygame.event.get(pygame.QUIT)
            logger.debug(f"{events}")
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    continue

            # handle events and update
            manager.handle_events()
            manager.update(dt)

            # draw and flip() the display to put everything on screen
            manager.draw()
            pygame.display.flip()

        pygame.quit()
