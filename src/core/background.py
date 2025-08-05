from pygame import Surface
from pygame.transform import scale2x

from core.entity import Entity
from utils.resource_manager import ResourceManager


class Background(Entity):
    _surf: Surface

    def __init__(self):
        super().__init__("background")
        self._surf = ResourceManager("assets/gamekit/Background/Background.png").load_image()

    def draw(self, parent: Surface) -> None:
        parent.blit(scale2x(self._surf), dest=self.pos)
