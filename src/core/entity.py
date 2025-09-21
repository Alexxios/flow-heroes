import typing as tp

from pygame import Vector2
from pygame.sprite import Sprite, collide_rect, spritecollide

from core.fsm import FiniteStateMachine
from constants import G

class Entity(Sprite):
    _fsm: tp.Optional[FiniteStateMachine]

    def __init__(self, *groups, name='entity') -> None:
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

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._fsm.update(*args, **kwargs)


class LivingEntity(Entity):
    _hp: int
    _atk: int
    _def: int
    _vel: Vector2
    _acc: Vector2

    def __init__(self, *groups, name='living entity'):
        super().__init__(*groups, name=name)

        self._vel = Vector2(0, 0)
        self._acc = Vector2(0, G)

    def update(self, *args, **kwargs):
        # FSM update
        super().update(*args, **kwargs)


        # Physics update
        dt = kwargs['dt']
        dx = self._vel * dt + 0.5 * self._acc * dt * dt


        self._vel += self._acc * dt
        for group in self.groups():
             spritecollide(self, group, False)
