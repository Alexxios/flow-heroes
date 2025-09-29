import typing as tp

from controls import Controls
from controls.recognizer import Recognizer
from controls.standard import KeyboardMouse

from entities.hero import HeroConfig


class Player:
    _name: str
    _controls: Controls
    _hero_config: HeroConfig

    def __init__(self, name: str = "player", hero_config: tp.Optional[HeroConfig] = None):
        self._name = name
        if hero_config:
            self._hero_config = hero_config
        else:
            self._hero_config = HeroConfig(
                HeroConfig.Path.APPRENTICE,
                HeroConfig.Skin.DUDE_MONSTER,
                skills=["Sun Strike"]
            )

        try:
            self._controls = Recognizer()
            # raise OSError()
        except OSError:
            self._controls = KeyboardMouse()

    def get_inputs(self):
        return self._controls.get_inputs()

    @property
    def name(self):
        return self._name

    @property
    def controls(self):
        return self._controls

    @property
    def hero_config(self):
        return self._hero_config