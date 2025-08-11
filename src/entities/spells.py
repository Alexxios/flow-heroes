from pygame.transform import scale2x

from core.spell import InstantSpell

from utils.animation import Animation
from utils.resource_manager import ResourceManager


animation = Animation(scale2x(ResourceManager('assets/gamekit/4 Sun strike/Sun-strike.png').load_image()), repeat=False)
SUN_STRIKE = InstantSpell(animation)
