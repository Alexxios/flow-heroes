import pathlib
from dataclasses import dataclass
from enum import auto

from core.fsm import FiniteStateMachine, State
from core.entity import LivingEntity

from utils import load_image
from utils.animation import Animation


class Enemy(LivingEntity):
    """Base class for all enemies."""
    def __init__(self, image_dir: str, hp: int, atk: int, *groups):
        name = image_dir.split()[-1]
        super().__init__(*groups, name=name)
        self._hp = hp
        self._atk = atk

class Servant(Enemy):
    """Weakest enemy. Easily defeated."""
    class ServantState(State):
        ATTACK = auto()
        DEATH = auto()
        HURT = auto()
        IDLE = auto()
        WALK = auto()

    class FSM(FiniteStateMachine):
        def __init__(self, servant: 'Servant'):
            super().__init__(
                Servant.ServantState,
                {
                    Servant.ServantState.INIT: servant._state_init,
                    Servant.ServantState.IDLE: servant._state_idle,
                    Servant.ServantState.DEAD: servant._state_dead,
                    Servant.ServantState.HURT: servant._state_hurt,
                    Servant.ServantState.DEATH: servant._state_death,
                }
            )

    def __init__(self, image_dir: str, hp: int, atk: int, *groups):
        super().__init__(image_dir, hp, atk, *groups)
        self._fsm = Servant.FSM(self)

        _load = lambda x: load_image(pathlib.Path(image_dir, x))
        self.surfaces = {
            Servant.ServantState.INIT: _load(f"{self.name}.png"),
            Servant.ServantState.IDLE: _load(f"{self.name}_Idle.png"),
            Servant.ServantState.HURT: _load(f"{self.name}_Hurt.png"),
            Servant.ServantState.DEATH: _load(f"{self.name}_Death.png"),
        }
        self.image = self.surfaces[Servant.ServantState.INIT]
        self.rect = self.image.get_rect()
        self.animation = None

    def _state_init(self, *args, **kwargs):
        self.animation = Animation(self.surfaces[Servant.ServantState.IDLE])
        return Servant.ServantState.IDLE

    def _state_idle(self, *args, **kwargs):
        if self.fsm.state != self.fsm.previous_state:
            self.animation = Animation(self.surfaces[self.fsm.state])
            self.image = self.animation.start()
            return Servant.ServantState.IDLE

        self.image = self.animation.update(kwargs['dt'])
        return Servant.ServantState.IDLE

    def _state_dead(self, *args, **kwargs):
        return Servant.ServantState.DEAD

    def _state_hurt(self, *args, **kwargs):
        if self.fsm.state != self.fsm.previous_state:
            self.animation = Animation(self.surfaces[self.fsm.state], repeat=False)
            self.image = self.animation.start()
            return Servant.ServantState.HURT

        self.image = self.animation.update(kwargs['dt'])
        if not self.animation.ended:
            return Servant.ServantState.HURT

        if self._hp > 0:
            return Servant.ServantState.IDLE
        return Servant.ServantState.DEATH

    def _state_death(self, *args, **kwargs):
        if self.fsm.state != self.fsm.previous_state:
            self.animation = Animation(self.surfaces[self.fsm.state], repeat=False)
            self.image = self.animation.start()
            return Servant.ServantState.DEATH

        self.image = self.animation.update(kwargs['dt'])

        if self.animation.ended:
            self.kill()
            return Servant.ServantState.DEAD

class Warrior(Enemy):
    """Regular enemy."""
    pass

class Commander(Enemy):
    """Dangerous being."""
    pass

class Monarch(Enemy):
    """EXTREMELY DANGEROUS!"""
    pass

@dataclass
class ServantFactory:
    image_dir: str
    hp: int
    atk: int

    def create(self, *groups):
        return Servant(
            self.image_dir,
            self.hp,
            self.atk,
            *groups,
        )

BAT = ServantFactory("assets/gamekit/1 Bat", 15, 5)