from abc import ABC

from pygame import Vector2, Surface

class Entity(ABC):
    name: str
    pos: Vector2

    def __init__(self, name: str = "", pos: Vector2 = Vector2(0, 0)) -> None:
        self.name = name
        self.pos = Vector2(pos)

class DrawableEntity(Entity):
    _surf: Surface

    def __init__(self, name: str = "", pos: Vector2 = Vector2(0, 0)):
        super().__init__(name, pos)

    def update(self, dt: int) -> None:
        ...

    def draw(self, parent: Surface) -> None:
        ...

class LivingEntity(DrawableEntity):
    _hp: int
    _atk: int
    _def: int
