import pathlib

import pygame.image
import pygame.transform
import pytmx.util_pygame

from constants import PROJECT_ROOT

def load_image(path):
    return pygame.transform.scale2x(pygame.image.load(pathlib.Path(PROJECT_ROOT, path)))

def load_font(path, size):
    return pygame.font.Font(pathlib.Path(PROJECT_ROOT, path), size)

def load_sound(path):
    return pygame.mixer.Sound(pathlib.Path(PROJECT_ROOT, path))

def load_tiled_map(path):
    return pytmx.util_pygame.load_pygame(str(pathlib.Path(PROJECT_ROOT, path)))