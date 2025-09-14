import typing as tp

from core.hero import Hero

class Player:
    _name: str
    _hero: tp.Optional[Hero]

    def __init__(self, name: str = "player"):
        self._name = name
        self._hero = None

    @property
    def name(self):
        return self._name

    @property
    def hero(self):
        return self._hero

    @hero.setter
    def hero(self, value: Hero):
        self._hero = value