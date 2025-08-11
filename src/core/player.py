import typing as tp

from pygame import Vector2, Surface
from pygame.transform import scale2x
import pygame.key

from core.entity import LivingEntity
from utils.animation import Animation
from utils.resource_manager import ResourceManager
from constants import GESTURE_EVENT

class Player(LivingEntity):
    _state: str
    _animap: tp.Dict[str, Animation]
    _surf: Surface

    def __init__(self, name: str = "player", pos: Vector2 = Vector2(0, 0)):
        super().__init__(name, pos)

        manager = ResourceManager("assets/gamekit/3 Dude_Monster")

        self._state = "idle"
        self._animap = {
            "idle": Animation(manager.load_image("Dude_Monster_Idle_4.png"))
        }
        self._surf = self._animap[self._state].start()

    def update(self, dt) -> None:
        self._surf = self._animap[self._state].update(dt)

        # TODO: remove
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.pos.y -= 0.3 * dt
        if keys[pygame.K_s]:
            self.pos.y += 0.3 * dt
        if keys[pygame.K_a]:
            self.pos.x -= 0.3 * dt
        if keys[pygame.K_d]:
            self.pos.x += 0.3 * dt

        for event in pygame.event.get(GESTURE_EVENT):
            # print(event)
            if event.gesture == "up":
                self.pos.y -= 0.3 * dt
            if event.gesture == "down":
                self.pos.y += 0.3 * dt
            if event.gesture == "left":
                self.pos.x -= 0.3 * dt
            if event.gesture == "right":
                self.pos.x += 0.3 * dt



    def draw(self, parent: Surface) -> None:
        parent.blit(scale2x(self._surf), dest=self.pos)
