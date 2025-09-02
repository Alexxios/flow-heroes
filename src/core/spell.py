from abc import abstractmethod
from enum import auto

from pygame import Vector2

from core.entity import Entity
from core.fsm import State, FiniteStateMachine

from utils.animation import Animation


class Spell(Entity):
    class SpellState(State):
        ACTIVE = auto()

    class SpellFSM(FiniteStateMachine):
        def __init__(self, spell: 'Spell'):
            super().__init__(
                Spell.SpellState,
                {
                    Spell.SpellState.DEAD: spell._state_dead,
                    Spell.SpellState.INIT: spell._state_init,
                    Spell.SpellState.ACTIVE: spell._state_active,
                }
            )

    def __init__(self, name: str = "spell", dmg: int = 10):
        super().__init__(name)
        self._dmg = dmg

    @property
    def dmg(self):
        return self._dmg

    @property
    def animation(self):
        return self._animation

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
    def __init__(self,
        animation: Animation,
        name: str = "instant_spell",
        dmg: int = 10
    ):
        super().__init__(name, dmg)
        self._fsm = self.SpellFSM(self)
        self._animation = animation
        self.image = self.animation.start()
        self.rect = self.image.get_rect()


    def _state_init(self, *args, **kwargs):
        return self.SpellState.ACTIVE

    def _state_dead(self, *args, **kwargs):
        return self.SpellState.DEAD

    def _state_active(self, *args, **kwargs):
        self.image = self.animation.update(kwargs['dt'])
        if self.animation.ended:
            self.kill()
            return self.SpellState.DEAD
        return self.SpellState.ACTIVE

class TrickSpell(Spell):
    def __init__(self,
        animation: Animation,
        name: str = "trick_spell",
        dmg: int = 10
    ):
        super().__init__(name, dmg)
        self._fsm = self.SpellFSM(self)
        self._animation = animation

    def _state_init(self, *args, **kwargs):
        # TODO wait for collision
        return self.SpellState.ACTIVE

    def _state_dead(self, *args, **kwargs):
        return self.SpellState.DEAD

    def _state_active(self, *args, **kwargs):
        return self.SpellState.ACTIVE

class TravellingSpell(Spell):
    def __init__(self,
        animation: Animation,
        name: str = "travelling_spell",
        dmg: int = 10,
        direction: Vector2 = Vector2(0, 0)
    ):
        super().__init__(name, dmg)
        self._fsm = self.SpellFSM(self)

class StatusSpell(Spell):
    pass

class ContinuousSpell(Spell):
    pass

class SpellFactory:
    pass
