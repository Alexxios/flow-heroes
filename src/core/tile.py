from core.entity import Entity
from pygame.transform import scale2x

class Tile(Entity):
    def __init__(self, pos, surf, *groups, name='tile'):
        super().__init__(*groups, name=name)
        self.image = scale2x(surf)
        self.rect = self.image.get_rect(topleft=pos)