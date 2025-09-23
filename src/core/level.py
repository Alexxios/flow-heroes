import pathlib

import pymunk.pygame_util
from pymunk import Poly
import pygame
from pygame import Surface
from pygame.sprite import Group

from core.player import Player

from core.physics import Physics
from core.hero import HeroFactory
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
        # Physical objects
        self.physical = Group()

        # Ground for map layout
        self.ground = Group()
        for x, y, surf in tiled_map.get_layer_by_name('ground').tiles():
            Tile.create_rect_tile(x * 64, y * 64, surf, self.ground)

        # entities for hero, enemies & breakable objects
        self.entities = Group()
        # if player is None or player.hero is None:
        #     self.hero = HeroFactory.create_hero(self.entities)
        #
        #     pos = (0, 0)
        #     marker = tiled_map.get_object_by_name("hero")
        #     if marker:
        #         pos = (marker.x * 2, marker.y * 2)
        #     self.hero.rect = self.hero.rect.move_to(center=pos)
        # else:
        #     # TODO: create by Player settings
        #     pass

    def draw(self, surface: Surface):
        self.ground.draw(surface)

        # space = Physics.get_space()
        # for shape in space.shapes:
        #     if isinstance(shape, Poly):
        #         pygame.draw.rect(surface, (0, 0, 255), shape.bb, 2)
        #         pygame.draw.circle(surface, (255, 0, 0), shape.body.position, 4, 2)
        #         print(shape.bb)

        self.entities.draw(surface)

    def update(self, dt: float) -> None:
        # self.ground.update(dt=dt)
        self.entities.update(dt=dt)