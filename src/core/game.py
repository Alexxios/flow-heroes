import pygame

from constants import FPS
from controls.recognizer import Recognizer
from scenes import SceneManager
from scenes.main_menu import MainMenuScene
from scenes.game_scene import GameScene

class Game:
    def __init__(self, title: str, width: int, height: int):
        super().__init__()

        # Setup
        self.title = title
        self.width = width
        self.height = height

    def run(self):
        """Main game loop."""
        # pygame setup
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.SCALED)
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
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    continue

            # handle events and update
            manager.handle_events(events)
            manager.update(dt)

            # draw and flip() the display to put everything on screen
            manager.draw()
            pygame.display.flip()

        pygame.quit()
