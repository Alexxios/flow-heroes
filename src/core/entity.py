from abc import ABC

from pygame import Vector2, Surface

from core.fsm import FiniteStateMachine


class Entity(ABC):
    name: str
    pos: Vector2
    _surf: Surface
    _fsm: FiniteStateMachine

    def __init__(self, name: str = "", pos: Vector2 = Vector2(0, 0)) -> None:
        self.name = name
        self.pos = Vector2(pos)

    def update(self, dt: int) -> None:
        ...

    def draw(self, parent: Surface) -> None:
        ...

class LivingEntity(Entity):
    _hp: int
    _atk: int
    _def: int
