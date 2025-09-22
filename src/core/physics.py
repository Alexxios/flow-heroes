import pymunk
import pymunk.pygame_util

from constants import G

class Physics:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Physics, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = 0, G
        pymunk.pygame_util.positive_y_is_up = True

    def create_body(self):
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)



    def add(self, *objs):
        self.space.add(*objs)