import os

import pygame

SOURCES_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(SOURCES_ROOT)

FPS = 60

GESTURE_EVENT = pygame.USEREVENT + 1
