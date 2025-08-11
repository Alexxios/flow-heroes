from abc import ABC, abstractmethod
import typing as tp
from typing import NamedTuple

class Gesture(ABC):
    name: str

    def __init__(self, name: str, k: float = 1.0) -> None:
        self.name = name

    @abstractmethod
    def score(self, multi_hand_landmarks: NamedTuple) -> float:
        ...

class CustomGesture(Gesture):
    features: tp.Any

    def score(self, multi_hand_landmarks: NamedTuple) -> float:
        # TODO: implement
        pass

class SingletonGesture(Gesture):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonGesture, cls).__new__(cls)
        return cls.instance
