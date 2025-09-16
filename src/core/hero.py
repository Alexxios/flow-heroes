import os.path
import typing as tp
from enum import Enum, auto

from core.entity import LivingEntity
from core.fsm import State, FiniteStateMachine
from utils import load_image
from utils.animation import Animation


_HERO_IMAGE_DIRS = [
    "assets/gamekit/1 Pink_Monster",
    "assets/gamekit/2 Owlet_Monster",
    "assets/gamekit/3 Dude_Monster"
]


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
                    Hero.HeroState.INIT: hero._state_init,
                    Hero.HeroState.IDLE: hero._state_idle,
                    Hero.HeroState.DEAD: hero._state_dead
                }
            )

    def __init__(self, image_dir: str, *groups):
        name = image_dir.split()[-1]
        super().__init__(*groups, name=name)
        self._fsm = Hero.HeroFSM(self)

        self.surfaces = {
            Hero.HeroState.INIT: load_image(os.path.join(image_dir, f"{name}.png")),
            Hero.HeroState.IDLE: load_image(os.path.join(image_dir, f"{name}_Idle_4.png")),
            Hero.HeroState.ATTACK1: load_image(os.path.join(image_dir, f"{name}_Attack1_4.png")),
            # TODO: so on
        }

        self.image = self.surfaces[Hero.HeroState.INIT]
        self.rect = self.image.get_rect(center=(100, 100)) # fixme
        self.animation = None

    def update(self, *args, **kwargs):
        old_state = self._fsm.state
        super().update(*args, **kwargs)

        if old_state == self._fsm.state:
            self.image = self.animation.update(kwargs['dt'])
        else:
            self.animation = Animation(self.surfaces[self._fsm.state])
            self.image = self.animation.start()

    def process_input(self, *args, **kwargs):
        # TODO: process input
        return self.HeroState.IDLE

    def _state_init(self, *args, **kwargs):
        return self.HeroState.IDLE

    def _state_idle(self, *args, **kwargs):
        return self.HeroState.IDLE

    def _state_dead(self, *args, **kwargs):
        return self.HeroState.DEAD

class Apprentice(Hero):
    pass

class Warrior(Hero):
    pass

class Hunter(Hero):
    pass

class HeroFactory:
    @staticmethod
    def create_hero(*groups, hero_type = "apprentice", hero_id = 0):
        if hero_type == "apprentice":
            return Apprentice(_HERO_IMAGE_DIRS[hero_id], *groups)
        return None
