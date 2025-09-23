import pygame
from pymunk import Body, Poly
from pygame.transform import scale2x

from core.physics import Physics
from core.entity import PhysicalEntity

class Tile(PhysicalEntity):
    def __init__(self, body: Body, pos, surf, *groups, name='tile'):
        super().__init__(body,*groups, name=name)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        # self.body.position = self.rect.center


    @classmethod
    def create_rect_tile(cls, x, y, surf, *groups, name='tile', mass = 0, moment = 0, body_type=Body.STATIC) -> 'Tile':
        surf = scale2x(surf)
        pos = (x, y)

        space = Physics.get_space()
        body = Body(mass=mass, moment=moment, body_type=body_type)
        body.position = surf.get_rect(topleft=pos).center
        shape = Poly.create_box(body, size=surf.size)
        space.add(body, shape)

        return Tile(body, pos, surf, *groups, name=name)