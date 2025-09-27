import logging

import pygame

from constants import FPS

from core.player import Player

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
        logger.info("Game launched")

        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.SCALED)
        pygame.display.set_caption("Flow Heroes")
        pygame.display.set_icon(load_image("assets/gamekit/2 512x512/2_2.png"))

        # Initialize player
        self.player = Player()

        # UI setup
        self.manager = SceneManager(self.screen)
        main_menu_scene = MainMenuScene(self.manager)
        game_scene = GameScene(self.manager, self.player)
        self.manager.add_scene("main_menu", main_menu_scene)
        self.manager.add_scene("game", game_scene)
        self.manager.set_scene("main_menu")


        # Run main loop
        self._loop()


    def _loop(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        running = True
        while running:
            dt = clock.tick(FPS)

            # poll for events
            # pygame.QUIT event means the user clicked X to close the window
            events = pygame.event.get(pygame.QUIT)
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    continue

            # handle events and update
            self.manager.handle_events()
            self.manager.update(dt)

            # draw and flip() the display to put everything on screen
            self.manager.draw()
            pygame.display.flip()

        pygame.quit()
