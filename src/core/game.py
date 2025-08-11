import pygame
from pygame.sprite import Group

from constants import FPS
from core.background import Background
from core.player import Player

from controls.recognizer import Recognizer, DATA_EVENT
from entities.spells import SUN_STRIKE

class Game:
    def __init__(self, title: str, width: int, height: int):
        super().__init__()

        # Setup
        self.title = title
        self.width = width
        self.height = height
        self.scenes = []

    def run(self):
        """Main game loop."""
        # pygame setup
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.SCALED)
        clock = pygame.time.Clock()
        running = True


        recognizer = Recognizer(daemon=True)
        recognizer.start()

        static_objects = Group()
        background = Background()
        background.add(static_objects)

        spells = Group()

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == DATA_EVENT:
                    # Обрабатываем наше пользовательское событие с данными
                    last_message = event.message
                    print(f"Получено новое сообщение: {last_message}")

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                SUN_STRIKE.add(spells)

            # draw Groups
            static_objects.draw(screen)
            spells.draw(screen)

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = clock.tick(FPS)


            # update Groups
            static_objects.update(dt=dt)
            spells.update(dt=dt)


        pygame.quit()
