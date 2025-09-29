from core.entity import Entity

class Bar(Entity):
    """Base class for all bars."""
    pass

class HealthBar(Bar):
    pass

class EnergyBar(Bar):
    pass

class BarFactory:
    @staticmethod
    def create_bar(bar_type, x, y, width, height):
        if bar_type == 'health':
            return HealthBar(x, y, width, height)
        elif bar_type == 'energy':
            return EnergyBar(x, y, width, height)
