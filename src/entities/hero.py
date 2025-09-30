import os.path
import typing as tp
import logging
from enum import Enum, auto
from dataclasses import dataclass, field

import pygame.event

from controls import Input
from core.entity import LivingEntity
from core.fsm import State, FiniteStateMachine
from entities.spells.instant import SUN_STRIKE
from utils import load_image
from utils.animation import Animation

logger = logging.getLogger(__name__)


@dataclass
class HeroConfig:
    class Path(Enum):
        APPRENTICE = "apprentice"
        WARRIOR = "warrior"
        HUNTER = "hunter"

    class Skin(Enum):
        PINK_MONSTER = "assets/gamekit/1 Pink_Monster"
        OWLET_MONSTER = "assets/gamekit/2 Owlet_Monster"
        DUDE_MONSTER = "assets/gamekit/3 Dude_Monster"

    hero_path: Path
    hero_skin: Skin
    level: int = 1
    skills: tp.List[str] = field(default_factory=list)
    skill_cooldown: int = 3

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
                    Hero.HeroState.WALK: hero._state_walk,
                    Hero.HeroState.JUMP: hero._state_jump,
                }
            )

    def __init__(self, hero_config: HeroConfig, *groups):
        image_dir = hero_config.hero_skin.value
        name = image_dir.split()[-1]

        super().__init__(*groups, name=name)
        self.config = hero_config
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
        self.cooldown = 0

    def _physics_update(self, *args, **kwargs):
        velocity_x, velocity_y = 0, self.body.velocity[1]
        if Input.RIGHT in kwargs.get('inputs', []):
            velocity_x = 128
        elif Input.LEFT in kwargs.get('inputs', []):
            velocity_x = -128

        # if Input.UP in kwargs['inputs'] and self._fsm.state != Hero.HeroState.JUMP:
        #     velocity_y = -256

        self.old_velocity_y = self.body.velocity[1]
        self.body.velocity = velocity_x, velocity_y


    def update(self, *args, **kwargs):
        old_state = self._fsm.state
        super().update(*args, **kwargs)

        self.cooldown = max(self.cooldown - kwargs.get('dt', 0), 0)
        if self.cooldown == 0 and Input.SUN_STRIKE in kwargs.get('inputs', []):
            self.cast_spell(*args, **kwargs)
            self.cooldown = self.config.skill_cooldown

        if old_state == self._fsm.state:
            self.image = self.animation.update(kwargs.get('dt', 0))
        else:
            self.animation = Animation(self.surfaces[self._fsm.state])
            self.image = self.animation.start()
        self.image = pygame.transform.flip(self.image, self._flip, False)

    def process(self):
        state = Hero.HeroState.IDLE
        if self.body.velocity[0] > 0:
            self._flip = False
            state = Hero.HeroState.WALK
        elif self.body.velocity[0] < 0:
            self._flip = True
            state = Hero.HeroState.WALK

        if self.body.velocity[1] < -10:
            state = Hero.HeroState.JUMP

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

    def _state_jump(self, *args, **kwargs):
        if self.animation.loop > 0:
            return self.process()
        return Hero.HeroState.JUMP

    def cast_spell(self, *args, **kwargs):
        dynamic = kwargs.get('dynamic', None)
        if not dynamic:
            return
        enemies = kwargs.get('enemies', [self])
        SUN_STRIKE.create(dynamic, pos=enemies[0].rect.midbottom)


class Apprentice(Hero):
    pass

class Warrior(Hero):
    pass

class Hunter(Hero):
    pass
