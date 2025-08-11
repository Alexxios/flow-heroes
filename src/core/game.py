import pygame

from constants import FPS
from core.background import Background
from core.player import Player
from core.spell import Spell

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


        # recogniser = Recogniser(daemon=True)
        # recogniser.start()
        recognizer = Recognizer(daemon=True)
        recognizer.start()


        background = Background()

        player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
        player = Player(pos=player_pos)

        entities = set()

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
                    entities.add(SUN_STRIKE)

            # fill the screen with a color to wipe away anything from last frame
            screen.fill("purple")

            # pygame.draw.circle(screen, "red", player_pos, 40)
            # screen.blit(fireball.animation[frames % 8], dest=player_pos)

            background.draw(screen)
            player.draw(screen)

            for entity in entities:
                entity.draw(screen)


            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            dt = clock.tick(FPS)
            player.update(dt)

            for entity in entities:
                entity.update(dt)

        pygame.quit()
