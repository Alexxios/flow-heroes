import typing as tp

from pymunk import Body
from pygame.sprite import Sprite

from core.fsm import FiniteStateMachine, State

class Entity(Sprite):
    _fsm: tp.Optional[FiniteStateMachine]

    def __init__(self, *groups, name='entity') -> None:
        super().__init__(*groups)
        self._name = name
        self._flip = False
        self._state_changed = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def pos(self) -> tuple[float, float]:
        return self.rect.center

    @property
    def fsm(self) -> tp.Optional[FiniteStateMachine]:
        return self._fsm

    @property
    def flip(self):
        return self._flip

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._fsm.update(*args, **kwargs)
    
    def kill(self):
        super().kill()
        self._fsm.state = State.DEAD


class PhysicalEntity(Entity):

    def __init__(self, *groups, name='physical entity'):
        super().__init__(*groups, name=name)
        self.body = Body()

    def _physics_update(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        # Physics update
        self._physics_update(*args, **kwargs)

        # FSM update
        super().update(*args, **kwargs)

        # Visual update
        self.rect.center = self.body.position

class LivingEntity(PhysicalEntity):
    _hp: int
    _atk: int

    def __init__(self, *groups, name='living entity'):
        super().__init__(*groups, name=name)