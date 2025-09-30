import pathlib

from pygame import Surface
from pygame.sprite import Group
import pymunk.pygame_util
from pymunk import Space, Poly, Body

from controls import Input
from core.player import Player

from entities.enemies import BAT
from entities.hero import Hero
from entities.tile import Tile
from entities.spells.instant import SUN_STRIKE

from utils import load_tiled_map
from constants import G

_BASE_DIR = "assets/levels"
_levels = ["test_level.tmx"]
_load = lambda n: load_tiled_map(pathlib.Path(_BASE_DIR, _levels[n]))

class Level:
    def __init__(self, n: int, player: Player):
        # Load map
        tiled_map = _load(n)
        self.tiled_map = tiled_map
        self.player = player

        # Setup physics
        self.space = Space()
        self.space.gravity = 0, G
        pymunk.pygame_util.positive_y_is_up = False

        # Static objects group
        self.static = Group()

        for x, y, surf in tiled_map.get_layer_by_name("ground").tiles():
            tile = Tile.create_tile(x * 64, y * 64, surf, self.static)
            tile.body.body_type = Body.STATIC
            tile.body.position = tile.rect.center
            shape = Poly.create_box(tile.body, tile.rect.size)
            self.space.add(tile.body, shape)

        # Dynamic object group
        self.dynamic = Group()

        hero_meta = tiled_map.get_object_by_name("hero")
        hero = Hero(player.hero_config, self.dynamic)
        hero.body.position = (hero_meta.x * 2, hero_meta.y * 2)
        shape = Poly.create_box(hero.body, hero.rect.size)
        shape.mass = 10
        self.space.add(hero.body, shape)

        self.enemies = Group()
        for enemy in tiled_map.get_layer_by_name("enemies"):
            bat = BAT.create(self.dynamic, self.enemies)
            bat.body.position = (enemy.x * 2, enemy.y * 2)
            shape = Poly.create_box(bat.body, bat.rect.size)
            shape.mass = 100000
            self.space.add(bat.body, shape)

    def draw(self, surface: Surface):
        self.static.draw(surface)
        self.dynamic.draw(surface)

    def update(self, dt: int) -> None:
        self.space.step(dt / 1000)

        player_inputs = self.player.get_inputs()

        self.dynamic.update(dt=dt, inputs=player_inputs, dynamic=self.dynamic, enemies=self.enemies.sprites())

