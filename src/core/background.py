from pygame.transform import scale2x

from core.entity import Entity
from utils.resource_manager import ResourceManager


class Background(Entity):

    def __init__(self):
        super().__init__("background")
        self.image = scale2x(ResourceManager("assets/gamekit/Background/Background.png").load_image())
        self.rect = self.image.get_rect()
