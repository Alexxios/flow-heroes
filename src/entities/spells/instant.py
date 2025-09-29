from dataclasses import dataclass, field, InitVar

from pygame import Surface

from entities.spells import InstantSpell

from utils import load_image
from utils.animation import Animation


@dataclass
class InstantSpellFactory:
    image_path: InitVar[str]
    surface: Surface = field(init=False)
    name: str = "instant_spell"
    dmg: int = 10

    def __post_init__(self, image_path: str):
        self.surface = load_image(image_path)

    def create(self, *groups, pos=(0, 0)):
        return InstantSpell(
            Animation(self.surface.copy(), repeat=False),
            *groups,
            name=self.name,
            dmg=self.dmg,
            pos=pos
        )


SUN_STRIKE = InstantSpellFactory("assets/gamekit/4 Sun strike/Sun-strike.png")