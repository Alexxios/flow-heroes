from pymunk import Space, Body
import pymunk.pygame_util

from constants import G

class Physics:
    _space = None

    @classmethod
    def get_space(cls):
        if cls._space is None:
            cls._space = Space()
            cls._space.gravity = 0, G
            pymunk.pygame_util.positive_y_is_up = True
        return cls._space