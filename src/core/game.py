import pygame

from constants import FPS
from controls.recognizer import Recognizer
from scenes import SceneManager
from scenes.main_menu import MainMenuScene

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

        scene_manager = SceneManager()
        scene_manager.push(MainMenuScene(scene_manager))

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close the window
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    continue

            scene = scene_manager.peek()
            if scene is None:
                running = False
                continue

            scene.render(screen)
            scene.process_input(events)

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = clock.tick(FPS)
            scene.update()



        pygame.quit()
