from dataclasses import dataclass, field, InitVar

from pygame import Surface

from entities.spells import ProjectileSpell

from utils import load_image
from utils.animation import Animation


@dataclass
class ProjectileSpellFactory:
    image_path: InitVar[str]
    surface: Surface = field(init=False)
    name: str = "projectile_spell"
    dmg: int = 10

    def __post_init__(self, image_path: str):
        self.surface = load_image(image_path)

    def create(self, *groups, pos=(0, 0), direction=(1,0)):
        return ProjectileSpell(
            Animation(self.surface.copy(), repeat=False),
            *groups,
            name=self.name,
            dmg=self.dmg,
            pos=pos,
            direction=direction
        )


FIREBALL = ProjectileSpellFactory("assets/gamekit/10 Fire ball/Fire-ball.png")