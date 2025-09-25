import typing as tp

from controls import Controls
from controls.recognizer import Recognizer
from controls.standard import KeyboardMouse

from core.hero import Hero

class Player:
    _name: str
    _controls: Controls
    _hero: tp.Optional[Hero]

    def __init__(self, name: str = "player"):
        self._name = name
        self._hero = None

        try:
            # self._controls = Recognizer()
            raise OSError()
        except OSError:
            self._controls = KeyboardMouse()

    def get_inputs(self):
        return self._controls.get_inputs()

    @property
    def name(self):
        return self._name

    @property
    def hero(self):
        return self._hero

    @hero.setter
    def hero(self, value: Hero):
        self._hero = value