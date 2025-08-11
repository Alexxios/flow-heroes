from enum import auto

from pygame.transform import scale2x

from core.entity import Entity
from core.fsm import State, SingletonFSM

from utils.animation import Animation
from utils.resource_manager import ResourceManager

# class InstantSpellFSM(SingletonFSM):
#     class SpellState(State):
#         ACTIVE = auto()

#     def __init__(self):
#         super().__init__(
#             self.SpellState,
#             {
#                 self.SpellState.INIT: lambda: self.SpellState.ACTIVE,
#                 self.SpellState.ACTIVE: ,
#             },

#         )
#         self.

#     def update_init(self, dt):

#         return self.SpellState.ACTIVE

#     def update_active(self):
#         pass

class Spell(Entity):
    _dmg: int
    _animation: Animation

    def __init__(self, path, dmg = 10):
        manager = ResourceManager(path)
        super().__init__(manager.base_path.stem)

        self._dmg = dmg
        self._animation = Animation(manager.load_image())
        self._surf = self._animation.start()

    def update(self, dt):
        self._surf = self._animation.update(dt)

    def draw(self, parent):
        parent.blit(scale2x(self._surf), self.pos)

class SpellFactory:
    @staticmethod
    def create_spell(path, dmg = 10):
        return Spell(path, dmg)
