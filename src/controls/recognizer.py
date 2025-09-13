from threading import Thread

import pygame

import cv2
import mediapipe as mp
import numpy as np
import time
import pickle
import os

from controls.gestures.movement import *
from controls.gestures.commands import *
from constants import GESTURE_EVENT


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Constants
GESTURE_FILE = "custom_gestures.pkl"
SAMPLES_PER_GESTURE = 30
RECOGNITION_THRESHOLD = 0.8

# Определим пользовательское событие
DATA_EVENT = pygame.USEREVENT + 2

gestures = [GesturePlay(), GesturePause(), GestureExit(), GestureShop()]

class Recognizer(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize MediaPipe Hands
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )

        # Initialize webcam
        self.cap = cv2.VideoCapture(0)


    def run(self):
        # Main loop
        while self.cap.isOpened():
            success, image = self.cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # Convert the BGR image to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the image and find hands
            results = self.hands.process(image_rgb)

            # Draw hand landmarks and process gestures
            if results.multi_hand_landmarks:
                recognized = self.recognize(results.multi_hand_landmarks)
                print(f"Gesture: {recognized}")
                for name in recognized:
                    self.post_gesture_event(name)


        # Clean up
        self.cap.release()
        cv2.destroyAllWindows()

    def recognize(self, multi_hand_landmarks):
        best_score = [RECOGNITION_THRESHOLD] * len(multi_hand_landmarks)
        best_match = [None] * len(multi_hand_landmarks)

        for gesture in gestures:
            scores = gesture.score(multi_hand_landmarks)
            print(scores, best_score)
            for i, score in enumerate(scores):
                if score > best_score[i]:
                    best_score[i] = score
                    best_match[i] = gesture.name

        return set(best_match) - {None}

    def post_gesture_event(self, gesture_name: str):
        event = pygame.event.Event(GESTURE_EVENT, {'gesture': gesture_name})
        pygame.event.post(event)
