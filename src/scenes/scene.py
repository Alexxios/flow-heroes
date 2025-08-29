from abc import ABC, abstractmethod

class Scene(ABC):
    def __init__(self):
        self.next = self

    @abstractmethod
    def process_input(self, events):
        ...

    @abstractmethod
    def update(self):
        ...

    @abstractmethod
    def render(self, screen):
        ...

    def terminate(self):
        self.next = None

    def switch_to_scene(self, next_scene):
        self.next = next_scene
