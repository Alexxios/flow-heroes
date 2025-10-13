import typing as tp

import numpy as np
import mediapipe as mp
import pygame
import pygame.camera
from pygame import Surface

from controls import Controls, Input

from constants import RECOGNITION_THRESHOLD, GESTURE_EVENT

import logging
logger = logging.getLogger(__name__)


class Recognizer(Controls):
    def __init__(self):
        pygame.camera.init()

        cam_list = pygame.camera.list_cameras()
        if not cam_list:
            logger.info("Cannot access the camera")
            raise OSError()

        # Initialize webcam
        self.cam = pygame.camera.Camera(cam_list[0])
        self.cam.start()
        self.surface = pygame.Surface(self.cam.get_size())
        self.processed_surface = None

        # Initialize MediaPipe Hands
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )

        self.gestures = []
        self._gesture_mapping = {
            'left': Input.LEFT,
            'right': Input.RIGHT,
            'up': Input.UP,
            'down': Input.DOWN,

            'play': Input.PLAY,
            'pause': Input.PAUSE,
            'shop': Input.SHOP,
            'exit': Input.EXIT,

            'pray': Input.SUN_STRIKE,
        }


    def __del__(self):
        self.cam.stop()
        pygame.camera.quit()

    def update(self, *args, **kwargs):
        self.gestures = args

    def get_inputs(self) -> tp.List[Input]:
        # Load image into surface
        if self.cam.query_image():
            self.cam.get_image(self.surface)

        # Convert surface to numpy array
        image_rgb = np.transpose(pygame.surfarray.pixels3d(self.surface), (1, 0, 2))
        y, x, c = image_rgb.shape # since we transpose the image it's now (y, x, c)

        # Process the image and find hands
        results = self.hands.process(image_rgb)

        # Draw hand landmarks and process gestures
        self.processed_surface = None
        if results.multi_hand_landmarks:
            recognized = self.recognize(results.multi_hand_landmarks)

            self.processed_surface = pygame.surfarray.make_surface(np.transpose(image_rgb, (1, 0, 2)))

            for handslms in results.multi_hand_landmarks:
                for lm in handslms.landmark:
                    # print(id, lm)
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)

                    pygame.draw.circle(self.processed_surface, (0, 255, 0), (lmx, lmy), 5)


            return list(map(lambda k: self._gesture_mapping[k], recognized))

        return []

    def get_surface(self) -> Surface:
        return self.processed_surface

    def recognize(self, multi_hand_landmarks):
        best_score = [RECOGNITION_THRESHOLD] * len(multi_hand_landmarks)
        best_match = [None] * len(multi_hand_landmarks)

        for gesture in self.gestures:
            scores = gesture.score(multi_hand_landmarks)
            for i, score in enumerate(scores):
                if score > best_score[i]:
                    best_score[i] = score
                    best_match[i] = gesture.name
        print(best_match)
        return set(best_match) - {None}
