import typing as tp
from abc import ABC, abstractmethod
from enum import Enum, auto


class Input(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    ATTACK = auto()
    CAST = auto()
    SUN_STRIKE = auto()

class Controls(ABC):
    @abstractmethod
    def get_inputs(self) -> tp.List[Input]:
        ...

    def get_surface(self):
        return None