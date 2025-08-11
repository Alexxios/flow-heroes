import mediapipe as mp
import numpy as np

from controls.gestures import SingletonGesture


mp_hands = mp.solutions.hands

class GestureLeft(SingletonGesture):
    def __init__(self):
        super().__init__('left')

    def score(self, multi_hand_landmarks):
        scores = []
        for hand_landmarks in multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

            vectors = [
                np.array([index_finger_tip.x, index_finger_tip.y, index_finger_tip.z]) - np.array([index_finger_mcp.x, index_finger_mcp.y, index_finger_mcp.z]),
                np.array([thumb_tip.x, thumb_tip.y, thumb_tip.z]) - np.array([pinky_mcp.x, pinky_mcp.y, pinky_mcp.z])
            ]
            scores.append(max(vector[0] / np.linalg.norm(vector) for vector in vectors))

        return scores

class GestureRight(SingletonGesture):
    def __init__(self):
        super().__init__('right')

    def score(self, multi_hand_landmarks):
        scores = []
        for hand_landmarks in multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

            vectors = [
                np.array([index_finger_tip.x, index_finger_tip.y, index_finger_tip.z]) - np.array([index_finger_mcp.x, index_finger_mcp.y, index_finger_mcp.z]),
                np.array([thumb_tip.x, thumb_tip.y, thumb_tip.z]) - np.array([pinky_mcp.x, pinky_mcp.y, pinky_mcp.z])
            ]
            scores.append(max(-vector[0] / np.linalg.norm(vector) for vector in vectors))

        return scores

class GestureUp(SingletonGesture):
    def __init__(self):
        super().__init__('up')

    def score(self, multi_hand_landmarks):
        scores = []
        for hand_landmarks in multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

            vectors = [
                np.array([index_finger_tip.x, index_finger_tip.y, index_finger_tip.z]) - np.array([index_finger_mcp.x, index_finger_mcp.y, index_finger_mcp.z]),
                np.array([thumb_tip.x, thumb_tip.y, thumb_tip.z]) - np.array([pinky_mcp.x, pinky_mcp.y, pinky_mcp.z])
            ]
            scores.append(max(-vector[1] / np.linalg.norm(vector) for vector in vectors))

        return scores

class GestureDown(SingletonGesture):
    def __init__(self):
        super().__init__('down')

    def score(self, multi_hand_landmarks):
        scores = []
        for hand_landmarks in multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

            vectors = [
                np.array([index_finger_tip.x, index_finger_tip.y, index_finger_tip.z]) - np.array([index_finger_mcp.x, index_finger_mcp.y, index_finger_mcp.z]),
                np.array([thumb_tip.x, thumb_tip.y, thumb_tip.z]) - np.array([pinky_mcp.x, pinky_mcp.y, pinky_mcp.z])
            ]
            scores.append(max(vector[1] / np.linalg.norm(vector) for vector in vectors))

        return scores
