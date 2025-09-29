from abc import abstractmethod
from enum import auto

from pygame import Vector2

from core.fsm import State, FiniteStateMachine
from core.entity import Entity

from utils.animation import Animation


class Spell(Entity):
    class SpellState(State):
        ACTIVE = auto()

    class FSM(FiniteStateMachine):
        def __init__(self, spell: 'Spell'):
            super().__init__(
                Spell.SpellState,
                {
                    Spell.SpellState.DEAD: spell._state_dead,
                    Spell.SpellState.INIT: spell._state_init,
                    Spell.SpellState.ACTIVE: spell._state_active,
                }
            )

    def __init__(self, animation: Animation, *groups, name: str = "spell", dmg: int = 10, pos: Vector2 = (0, 0)):
        super().__init__(*groups, name=name)
        self._fsm = Spell.FSM(self)
        self._animation = animation
        self._dmg = dmg
        self.image = self._animation.start()
        self.rect = self.image.get_rect(midbottom=pos)

    @property
    def dmg(self):
        return self._dmg

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.image = self._animation.update(kwargs['dt'])

    @abstractmethod
    def _state_init(self, *args, **kwargs):
        ...

    @abstractmethod
    def _state_dead(self, *args, **kwargs):
        ...

    @abstractmethod
    def _state_active(self, *args, **kwargs):
        ...

class InstantSpell(Spell):
    def _state_init(self, *args, **kwargs):
        return self.SpellState.ACTIVE

    def _state_dead(self, *args, **kwargs):
        return self.SpellState.DEAD

    def _state_active(self, *args, **kwargs):
        if self._animation.ended:
            self.kill()
            return self.SpellState.DEAD
        return self.SpellState.ACTIVE

class TrickSpell(Spell):
    def _state_init(self, *args, **kwargs):
        # TODO wait for collision
        return self.SpellState.ACTIVE

    def _state_dead(self, *args, **kwargs):
        return self.SpellState.DEAD

    def _state_active(self, *args, **kwargs):
        return self.SpellState.ACTIVE

class ProjectileSpell(Spell):
    def __init__(self,
        animation: Animation,
        *groups,
        name: str = "projectile_spell",
        dmg: int = 10,
        pos: Vector2 = (0, 0),
        direction: Vector2 = Vector2(0, 0)
    ):
        super().__init__(animation, *groups, name=name, dmg=dmg, pos=pos)
        self._direction = direction

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.rect.move_ip(self._direction[0] * kwargs['dt'], self._direction[1] * kwargs['dt'])

    def _state_init(self, *args, **kwargs):
        return self.SpellState.ACTIVE

    def _state_dead(self, *args, **kwargs):
        return self.SpellState.DEAD

    def _state_active(self, *args, **kwargs):
        # TODO wait for collision
        return self.SpellState.ACTIVE


class StatusSpell(Spell):
    pass

class ContinuousSpell(Spell):
    pass
