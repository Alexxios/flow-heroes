import typing as tp

import pygame.key
import pygame.mouse

from controls import Controls, Input

import logging
logger = logging.getLogger(__name__)

class KeyboardMouse(Controls):

    def __init__(self):
        self._key_mapping = {
            pygame.K_a: Input.LEFT,
            pygame.K_d: Input.RIGHT,
            pygame.K_w: Input.UP,
            pygame.K_s: Input.DOWN,
        }
        self._mouse_mapping = {
            0: Input.ATTACK,
            2: Input.CAST
        }

    def _cancel(self, a, b):
        return a and (a ^ b), b and (a ^ b)

    def get_inputs(self) -> tp.List[Input]:
        inputs = []

        # Handle keyboard inputs
        keyboard_pressed = pygame.key.get_pressed()
        pressed_dict = {key: False for key in self._key_mapping.keys()}

        for key in self._key_mapping.keys():
            pressed_dict[key] = keyboard_pressed[key]

        # Cancel out contradictory inputs
        pressed_dict[pygame.K_a], pressed_dict[pygame.K_d] = self._cancel(pressed_dict[pygame.K_a], pressed_dict[pygame.K_d])
        pressed_dict[pygame.K_w], pressed_dict[pygame.K_s] = self._cancel(pressed_dict[pygame.K_w], pressed_dict[pygame.K_s])

        inputs.extend([self._key_mapping[key] for key, value in pressed_dict.items() if value])


        # Handle mouse inputs
        mouse_pressed = list(pygame.mouse.get_pressed())
        mouse_just_pressed = list(pygame.mouse.get_just_pressed())

        # Cancel out contradictory inputs
        mouse_just_pressed[0], mouse_just_pressed[2] = self._cancel(mouse_just_pressed[0], mouse_just_pressed[2])

        inputs.extend([self._mouse_mapping[button] for button in self._mouse_mapping.keys() if mouse_just_pressed[button]])

        return inputs