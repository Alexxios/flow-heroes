from pygame import Surface
import pygame.image

class Animation:
    _surf: Surface
    _size: int

    def __init__(self, surf):
        self._surf = surf
        self._size = self._surf.height

    def __getitem__(self, item):
        return self._surf.subsurface(
            item * self._size, 0, self._size, self._size
        )