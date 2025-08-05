from core.entity import LivingEntity

class Enemy(LivingEntity):
    """Base class for all enemies."""
    pass

class Servant(Enemy):
    """Weakest enemy. Easily defeated."""
    pass

class Warrior(Enemy):
    """Regular enemy."""
    pass

class Commander(Enemy):
    """Dangerous being."""
    pass

class Monarch(Enemy):
    """EXTREMELY DANGEROUS!"""
    pass

class EnemyFactory:
    @staticmethod
    def create_enemy(enemy_type, x, y, width, height):
        if enemy_type == 'servant':
            return Servant(x, y, width, height)
        elif enemy_type == 'warrior':
            return Warrior(x, y, width, height)
        elif enemy_type == 'commander':
            return Commander(x, y, width, height)
        elif enemy_type == 'monarch':
            return Monarch(x, y, width, height)
