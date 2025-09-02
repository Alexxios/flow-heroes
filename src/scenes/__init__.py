import abc
from typing import List, Dict, Optional

import pygame

from ui import UIElement

class Scene(abc.ABC):
    """Abstract base class for all game scenes"""
    def __init__(self, manager: 'SceneManager'):
        self.manager = manager
        self.ui_elements: List[UIElement] = []

    @abc.abstractmethod
    def setup(self) -> None:
        """Initialize the scene resources"""
        pass

    @abc.abstractmethod
    def teardown(self) -> None:
        """Clean up scene resources"""
        pass

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """Process all events"""
        for event in events:
            for element in self.ui_elements:
                if element.handle_event(event):
                    break  # Event handled, stop propagation

    def update(self, dt: float) -> None:
        """Update scene state"""
        for element in self.ui_elements:
            element.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the scene"""
        for element in self.ui_elements:
            element.draw(surface)


class SceneManager:
    """Manages transitions between different game scenes"""
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.scenes: Dict[str, Scene] = {}
        self.current_scene: Optional[Scene] = None
        self.current_scene_name: Optional[str] = None
        self.player_data = {
            "balance": 1000  # Initial balance
        }

    def add_scene(self, name: str, scene: Scene) -> None:
        """Add a scene to the manager"""
        self.scenes[name] = scene

    def set_scene(self, name: str) -> None:
        """Change to a different scene"""
        if name not in self.scenes:
            raise ValueError(f"Scene '{name}' not found")

        # Teardown current scene if exists
        if self.current_scene:
            self.current_scene.teardown()

        # Setup new scene
        self.current_scene = self.scenes[name]
        self.current_scene_name = name
        self.current_scene.setup()

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """Delegate event handling to current scene"""
        if self.current_scene:
            self.current_scene.handle_events(events)

    def update(self, dt: float) -> None:
        """Update current scene"""
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self) -> None:
        """Draw current scene"""
        if self.current_scene:
            self.current_scene.draw(self.screen)
