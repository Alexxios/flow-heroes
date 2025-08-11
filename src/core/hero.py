import typing as tp
from enum import auto

from core.entity import LivingEntity
from core.fsm import State, FiniteStateMachine


class Hero(LivingEntity):
    class HeroState(State):
        ATTACK1 = auto()
        ATTACK2 = auto()
        CLIMB = auto()
        DEATH = auto()
        HURT = auto()
        IDLE = auto()
        JUMP = auto()
        PUSH = auto()
        RUN = auto()
        THROW = auto()
        WALK = auto()
        WALK_ATTACK = auto()

    class HeroFSM(FiniteStateMachine):
        def __init__(self, hero: 'Hero'):
            super().__init__(
                Hero.HeroState,
                {
                }
            )

    def __init__(self, x, y, width, height):
        super().__init__('hero', x, y, width, height)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._fsm.update(*args, **kwargs)

    def process_input(self, *args, **kwargs):
        # TODO: process input
        return self.HeroState.IDLE

    def _state_init(self, *args, **kwargs):
        self._fsm.state = self.HeroState.IDLE

    def _state_idle(self, *args, **kwargs):
        pass

    def _state_dead(self, *args, **kwargs):
        self._fsm.state = self.HeroState.DEAD

class Apprentice(Hero):
    pass

class Warrior(Hero):
    pass

class Hunter(Hero):
    pass

class HeroFactory:
    @staticmethod
    def create_hero(hero_type, x, y, width, height):
        if hero_type == 'hero':
            return Hero(x, y, width, height)
