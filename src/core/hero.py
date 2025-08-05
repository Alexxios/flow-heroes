from core.entity import LivingEntity

class Hero(LivingEntity):
    """Base class for all heroes."""
    pass

class Apprentice(Hero):
    pass

class Warrior(Hero):
    pass

class Hunter(Hero):
    pass

class HeroFactory:
    @staticmethod
    def create_hero(hero_type, x, y, width, height):
        if hero_type == 'hero':
            return Hero(x, y, width, height)
