import typing as tp
from abc import ABC, abstractmethod
from collections import deque

class Scene(ABC):
    def __init__(self, scene_manager: 'SceneManager'):
        self._scene_manager = scene_manager
        self._is_transparent = False

    @abstractmethod
    def process_input(self, events):
        ...

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def render(self, screen):
        ...

class SceneManager:
    def __init__(self):
        self.scene_stack = deque()

    def push(self, scene) -> None:
        """Add a scene to the top of the stack"""
        self.scene_stack.append(scene)

    def pop(self) -> tp.Optional[Scene]:
        """Remove and return the top scene from the stack"""
        if not self.is_empty():
            return self.scene_stack.pop()
        return None

    def peek(self) -> tp.Optional[Scene]:
        """Return the current active scene (top of stack)"""
        if not self.is_empty():
            return self.scene_stack[-1]
        return None

    def replace(self, scene) -> None:
        """Replace the current scene with a new one"""
        if not self.is_empty():
            self.pop()
        self.push(scene)

    def clear(self) -> None:
        """Clear all scenes"""
        self.scene_stack.clear()

    def is_empty(self) -> bool:
        """Check if the stack is empty"""
        return len(self.scene_stack) == 0
