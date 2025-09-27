import os

import pygame

SOURCES_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(SOURCES_ROOT)
ASSETS_ROOT = os.path.join(PROJECT_ROOT, 'assets')

FPS = 60
G = 981

RECOGNITION_THRESHOLD = 0.6
GESTURE_EVENT = pygame.USEREVENT + 1
