import typing as tp

import pygame
import pygame.camera
import mediapipe as mp

from controls import Controls, Input
from controls.gestures.movement import *
from controls.gestures.commands import *

from constants import RECOGNITION_THRESHOLD, GESTURE_EVENT

import logging
logger = logging.getLogger(__name__)

movement = [
    GestureLeft(),
    GestureRight(),
    GestureUp(),
    GestureDown()
]

commands = [
    GesturePlay(),
    GesturePause(),
    GestureExit(),
    GestureShop(),
]

gestures = movement + commands

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

        # Initialize MediaPipe Hands
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )

    def __del__(self):
        self.cam.stop()
        pygame.camera.quit()

    def get_inputs(self) -> tp.List[Input]:
        return []

    def update(self):
        # Load image into surface
        self.cam.get_image(self.surface)

        # Convert surface to numpy array
        image_rgb = pygame.surfarray.pixels3d(self.surface)

        # Process the image and find hands
        results = self.hands.process(image_rgb)

        # Draw hand landmarks and process gestures
        if results.multi_hand_landmarks:
            recognized = self.recognize(results.multi_hand_landmarks)
            print(f"Gesture: {recognized}")
            self.post_gesture_event(recognized)


    def recognize(self, multi_hand_landmarks):
        best_score = [RECOGNITION_THRESHOLD] * len(multi_hand_landmarks)
        best_match = [None] * len(multi_hand_landmarks)

        for gesture in gestures:
            scores = gesture.score(multi_hand_landmarks)
            for i, score in enumerate(scores):
                if score > best_score[i]:
                    best_score[i] = score
                    best_match[i] = gesture.name

        return set(best_match) - {None}

    def post_gesture_event(self, gestures):
        event = pygame.event.Event(GESTURE_EVENT, {'gestures': gestures})
        pygame.event.post(event)
