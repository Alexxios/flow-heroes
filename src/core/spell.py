from core.entity import DrawableEntity

from utils.animation import Animation
from utils.resource_manager import ResourceManager


class Spell(DrawableEntity):
    _animation: Animation
    dmg: int

    def __init__(self, path, dmg=10):
        super().__init__(path)
        surf = ResourceManager(path).load_image()
        self.animation = Animation(surf)
        self.dmg = dmg
