from pygame import Vector2
from pygame.sprite import Sprite

from core.fsm import FiniteStateMachine


class Entity(Sprite):

    def __init__(self, name: str = "") -> None:
        super().__init__()
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def pos(self) -> Vector2:
        return self.rect.center

    @property
    def fsm(self) -> FiniteStateMachine:
        return self._fsm



class LivingEntity(Entity):
    _hp: int
    _atk: int
    _def: int
