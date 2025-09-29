import typing as tp
from typing import Generic, TypeVar
from abc import ABC
from enum import Enum

class _State:
    DEAD = 0
    INIT = 1

class State(_State, Enum):
    pass

T = TypeVar('T', bound=State)

class FiniteStateMachine(ABC, Generic[T]):
    states: tp.Type[T]
    transitions: tp.Dict[T, tp.Callable[..., T]]
    state: T
    previous_state: T

    def __init__(self, states: tp.Type[T], transitions: tp.Dict[T, tp.Callable[..., T]]):
        self.states = states
        self.transitions = transitions
        self.state = states.INIT
        self.previous_state = states.INIT

    def update(self, *args, **kwargs) -> None:
        self.previous_state = self.state
        self.state = self.transitions[self.state](*args, **kwargs)

class SingletonFSM(FiniteStateMachine):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance
