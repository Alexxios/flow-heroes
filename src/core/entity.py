import typing as tp

from pygame import Vector2
from pygame.sprite import Sprite

from core.fsm import FiniteStateMachine


class Entity(Sprite):
    _fsm: tp.Optional[FiniteStateMachine]

    def __init__(self, name: str = "", *groups) -> None:
        super().__init__(*groups)
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def pos(self) -> tuple[float, float]:
        return self.rect.center

    @property
    def fsm(self) -> tp.Optional[FiniteStateMachine]:
        return self._fsm



class LivingEntity(Entity):
    _hp: int
    _atk: int
    _def: int
