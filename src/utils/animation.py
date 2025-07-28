from pygame import Surface

from constants import FPS

class Animation:
    _surf: Surface
    _size: int
    _fpf: int
    _millis: int

    def __init__(self, surf: Surface, fpf: int = FPS // 4):
        self._surf = surf
        self._size = self._surf.height

        self._fpf = fpf
        self._millis = 0

    def __getitem__(self, item):
        return self._surf.subsurface(
            item * self._size, 0, self._size, self._size
        )

    def start(self) -> Surface:
        self._millis = 0
        return self[0]

    def update(self, dt) -> Surface:
        self._millis = (self._millis + dt) % 1000
        return self[(FPS * self._millis) // (self._fpf * 1000)]
