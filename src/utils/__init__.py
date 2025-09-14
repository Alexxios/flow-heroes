import os

import pygame.image
import pygame.transform

from constants import PROJECT_ROOT

def load_image(path):
    return pygame.transform.scale2x(pygame.image.load(os.path.join(PROJECT_ROOT, path)))

def load_font(path, size):
    return pygame.font.Font(os.path.join(PROJECT_ROOT, path), size)

def load_sound(path):
    return pygame.mixer.Sound(os.path.join(PROJECT_ROOT, path))
