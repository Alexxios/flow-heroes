from core.entity import Entity

from utils import load_image

class Background(Entity):
    def __init__(self, *groups, name='background'):
        super().__init__(*groups, name=name)
        self.image = load_image("assets/gamekit/Background/Background.png")
        self.rect = self.image.get_rect()
