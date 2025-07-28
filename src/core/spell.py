from pygame.transform import scale2x

from core.entity import DrawableEntity

from utils.animation import Animation
from utils.resource_manager import ResourceManager


class Spell(DrawableEntity):
    _dmg: int
    _animation: Animation

    def __init__(self, path, dmg = 10):
        manager = ResourceManager(path)
        super().__init__(manager.base_path.stem)

        self._dmg = dmg
        self._animation = Animation(manager.load_image())
        self._surf = self._animation.start()

    def update(self, dt):
        self._surf = self._animation.update(dt)

    def draw(self, parent):
        parent.blit(scale2x(self._surf), self.pos)
