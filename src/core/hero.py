import os.path
import typing as tp
import logging
from enum import Enum, auto

from pymunk import Body
import pygame.event

from core.physics import Physics
from core.entity import LivingEntity
from core.fsm import State, FiniteStateMachine
from utils import load_image
from utils.animation import Animation
from constants import GESTURE_EVENT

logger = logging.getLogger(__name__)

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
                    Hero.HeroState.DEAD: hero._state_dead,
                    Hero.HeroState.WALK: hero._state_walk
                }
            )

    def __init__(self, image_dir: str, *groups):
        name = image_dir.split()[-1]
        super().__init__(*groups, name=name)
        self._fsm = Hero.HeroFSM(self)

        self.surfaces = {
            Hero.HeroState.INIT: load_image(os.path.join(image_dir, f"{name}.png")),
            Hero.HeroState.ATTACK1: load_image(os.path.join(image_dir, f"{name}_Attack1_4.png")),
            Hero.HeroState.ATTACK2: load_image(os.path.join(image_dir, f"{name}_Attack2_6.png")),
            Hero.HeroState.CLIMB: load_image(os.path.join(image_dir, f"{name}_Climb_4.png")),
            Hero.HeroState.DEATH: load_image(os.path.join(image_dir, f"{name}_Death_8.png")),
            Hero.HeroState.HURT: load_image(os.path.join(image_dir, f"{name}_Hurt_4.png")),
            Hero.HeroState.IDLE: load_image(os.path.join(image_dir, f"{name}_Idle_4.png")),
            Hero.HeroState.JUMP: load_image(os.path.join(image_dir, f"{name}_Jump_8.png")),
            Hero.HeroState.PUSH: load_image(os.path.join(image_dir, f"{name}_Push_6.png")),
            Hero.HeroState.RUN: load_image(os.path.join(image_dir, f"{name}_Run_6.png")),
            Hero.HeroState.THROW: load_image(os.path.join(image_dir, f"{name}_Throw_4.png")),
            Hero.HeroState.WALK_ATTACK: load_image(os.path.join(image_dir, f"{name}_Walk+Attack_6.png")),
            Hero.HeroState.WALK: load_image(os.path.join(image_dir, f"{name}_Walk_6.png")),
        }

        self.image = self.surfaces[Hero.HeroState.INIT]
        self.rect = self.image.get_rect()
        self.animation = None
        self.update_rate = 15
        self.flip = False

    def update(self, *args, **kwargs):
        # FSM update
        old_state = self._fsm.state
        super().update(*args, **kwargs) # also Physics update here

        if old_state == self._fsm.state:
            self.image = self.animation.update(kwargs['dt'])
        else:
            self.animation = Animation(self.surfaces[self._fsm.state])
            self.image = self.animation.start()
        self.image = pygame.transform.flip(self.image, self.flip, False)

    def process(self):

        # process user inputs
        events = pygame.event.get(GESTURE_EVENT)
        logger.debug(events)

        state = Hero.HeroState.IDLE
        for event in events:
            gestures = event.dict["gestures"]
            if "right" in gestures:
                self.flip = False
                state = Hero.HeroState.WALK
            if "left" in gestures:
                self.flip = True
                state = Hero.HeroState.WALK
        return state

    def _state_init(self, *args, **kwargs):
        return Hero.HeroState.IDLE

    def _state_idle(self, *args, **kwargs):
        return self.process()

    def _state_dead(self, *args, **kwargs):
        return Hero.HeroState.DEAD

    def _state_walk(self, *args, **kwargs):
        if self.animation.loop > 0:
            return self.process()
        return Hero.HeroState.WALK

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
