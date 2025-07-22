import pygame
from threading import Thread

from constants import FPS
from core.background import Background
from core.player import Player
from core.spell import Spell


class Game(Thread):
    def __init__(self, title: str, width: int, height: int):
        super().__init__()
        self.title = title
        self.width = width
        self.height = height
        self.scenes = []
        self._running = False

    def run(self):
        """Основной цикл в отдельном потоке."""
        # pygame setup
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        clock = pygame.time.Clock()
        self._running = True

        background = Background()

        player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        player = Player(pos=player_pos)

        while self._running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("purple")

            # pygame.draw.circle(screen, "red", player_pos, 40)
            # screen.blit(fireball.animation[frames % 8], dest=player_pos)

            background.draw(screen)
            player.draw(screen)

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = clock.tick(FPS)
            player.update(dt)

        pygame.quit()