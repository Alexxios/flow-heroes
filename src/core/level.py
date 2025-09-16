import pathlib

import pygame
from pygame import Surface
from pygame.sprite import Group

from core.player import Player

from core.hero import Hero
from core.tile import Tile

from utils import load_tiled_map


_BASE_DIR = "assets/levels"
_levels = ["test_level.tmx"]
_load = lambda n: load_tiled_map(pathlib.Path(_BASE_DIR, _levels[n]))

class Level:
    def __init__(self, n, player: Player):
        tiled_map = _load(n)
        self.tiled_map = tiled_map

        # TODO: create groups and entities
        self.ground = Group()
        for x, y, surf in tiled_map.get_layer_by_name('ground').tiles():
            Tile((x * 64, y * 64), surf, self.ground)

    def draw(self, surface: Surface):
        self.ground.draw(surface)

    def update(self, dt: float) -> None:
        self.ground.update(dt=dt)

if __name__ == "__main__":
    import pygame
    import pytmx

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))

    # Load the TMX map and its images
    level = Level(0, None)
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                continue

        level.draw(screen)

        pygame.display.flip()
        # ... rest of your game loop
    pygame.quit()