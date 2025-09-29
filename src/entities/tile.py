from pygame import Surface
from pygame.transform import scale2x
from core.entity import PhysicalEntity

class Tile(PhysicalEntity):
    def __init__(self, pos, surf: Surface, *groups, name='tile'):
        super().__init__(*groups, name=name)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

    @classmethod
    def create_tile(cls, x, y, surf, *groups, name='tile') -> 'Tile':
        surf = scale2x(surf)
        pos = (x, y)
        return Tile(pos, surf, *groups, name=name)