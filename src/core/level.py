import pathlib

import pygame

from core.player import Player
from utils import load_tiled_map


_BASE_DIR = "assets/levels"
_levels = ["test_level.tmx"]
_load = lambda n: load_tiled_map(pathlib.Path(_BASE_DIR, _levels[n]))

class Level:
    def __init__(self, n, player: Player):
        self.tiled_map = _load(n)
        print(self.tiled_map.__dict__)