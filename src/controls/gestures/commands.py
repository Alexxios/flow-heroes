import mediapipe as mp
import numpy as np

from controls.gestures import SingletonGesture


mp_hands = mp.solutions.hands

class GesturePause(SingletonGesture):
    def __init__(self):
        super().__init__('pause')

    def score(self, multi_hand_landmarks):
        pass
