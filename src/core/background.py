from core.entity import Entity

from utils import load_image

class Background(Entity):
    def __init__(self, *groups):
        super().__init__("background", *groups)
        self.image = load_image("assets/gamekit/Background/Background.png")
        self.rect = self.image.get_rect()
