import typing as tp
from enum import auto

from core.entity import LivingEntity
from core.fsm import State, FiniteStateMachine

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

"""
Finite State Machine (FSM) implementation for Hero states management.

This class extends FiniteStateMachine to handle transitions between Hero states. It initializes
with predefined transitions between different Hero states.

Args:
    transitions: A dictionary mapping HeroState to callable functions that return the next HeroState.
"""
class HeroFSM(FiniteStateMachine):

    def __init__(self, transitions: tp.Dict[HeroState, tp.Callable[..., HeroState]]):
        super().__init__(HeroState, transitions)

class Hero(LivingEntity):
    """Base class for all heroes."""
    pass

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
