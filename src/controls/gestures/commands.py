import mediapipe as mp
import numpy as np

from controls.gestures import SingletonGesture


mp_hands = mp.solutions.hands

class GesturePlay(SingletonGesture):
    def __init__(self):
        super().__init__('play')

    def score(self, multi_hand_landmarks):
        """
        Calculate score for 'play' gesture (triangle made of fingers)

        Specifically looking for:
        - Index, middle, and thumb forming a triangle shape
        - Other fingers curled in

        Returns:
            float: Score between 0 and 1
        """
        if not multi_hand_landmarks or len(multi_hand_landmarks) < 1:
            return [0.0] * len(multi_hand_landmarks)

        landmarks = multi_hand_landmarks[0].landmark

        # Check if thumb, index, and middle finger are extended
        thumb_tip = np.array([landmarks[4].x, landmarks[4].y, landmarks[4].z])
        index_tip = np.array([landmarks[8].x, landmarks[8].y, landmarks[8].z])
        middle_tip = np.array([landmarks[12].x, landmarks[12].y, landmarks[12].z])

        # Check if ring and pinky are curled
        ring_tip = np.array([landmarks[16].x, landmarks[16].y, landmarks[16].z])
        pinky_tip = np.array([landmarks[20].x, landmarks[20].y, landmarks[20].z])

        palm_center = np.array([landmarks[0].x, landmarks[0].y, landmarks[0].z])

        # Distances to check triangle formation
        dist_thumb_index = np.linalg.norm(thumb_tip - index_tip)
        dist_index_middle = np.linalg.norm(index_tip - middle_tip)
        dist_middle_thumb = np.linalg.norm(middle_tip - thumb_tip)

        # Check if ring and pinky are curled (close to palm)
        ring_curled = np.linalg.norm(ring_tip - palm_center) < 0.15
        pinky_curled = np.linalg.norm(pinky_tip - palm_center) < 0.15

        # Triangle should have roughly similar sides
        triangle_score = 1.0 - (abs(dist_thumb_index - dist_index_middle) +
                                abs(dist_index_middle - dist_middle_thumb) +
                                abs(dist_middle_thumb - dist_thumb_index)) / 3.0

        # Final score combines triangle formation and finger curling
        curl_score = 0.5 if ring_curled else 0.0
        curl_score += 0.5 if pinky_curled else 0.0

        return [min(1.0, (triangle_score * 0.7 + curl_score * 0.3))] * len(multi_hand_landmarks)


class GesturePause(SingletonGesture):
    def __init__(self):
        super().__init__('pause')

    def score(self, multi_hand_landmarks):
        """
        Calculate score for 'pause' gesture (timeout sign)

        Specifically looking for:
        - Both hands with all fingers extended
        - Fingertips of both hands touching to form a T shape

        Returns:
            float: Score between 0 and 1
        """
        if not multi_hand_landmarks or len(multi_hand_landmarks) < 2:
            return [0.0] * len(multi_hand_landmarks)

        # We need two hands for timeout sign
        left_hand = None
        right_hand = None

        # Determine which hand is which
        for hand in multi_hand_landmarks:
            landmarks = hand.landmark
            wrist = landmarks[0]
            if wrist.x < 0.5:  # Assuming x-axis increases from left to right
                left_hand = landmarks
            else:
                right_hand = landmarks

        if not left_hand or not right_hand:
            return [0.0] * len(multi_hand_landmarks)

        # Check if fingers are extended on both hands
        left_fingers_extended = all(
            np.linalg.norm(np.array([left_hand[tip].x, left_hand[tip].y, left_hand[tip].z]) -
                        np.array([left_hand[0].x, left_hand[0].y, left_hand[0].z])) > 0.15
            for tip in [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky tips
        )

        right_fingers_extended = all(
            np.linalg.norm(np.array([right_hand[tip].x, right_hand[tip].y, right_hand[tip].z]) -
                        np.array([right_hand[0].x, right_hand[0].y, right_hand[0].z])) > 0.15
            for tip in [4, 8, 12, 16, 20]
        )

        extension_score = (left_fingers_extended + right_fingers_extended) / 2.0

        # Check if hands form a T shape (one hand horizontal, one vertical)
        left_wrist_to_pinky = np.array([left_hand[20].x - left_hand[0].x,
                                        left_hand[20].y - left_hand[0].y])
        right_wrist_to_pinky = np.array([right_hand[20].x - right_hand[0].x,
                                        right_hand[20].y - right_hand[0].y])

        # Check perpendicularity with dot product
        left_norm = np.linalg.norm(left_wrist_to_pinky)
        right_norm = np.linalg.norm(right_wrist_to_pinky)

        if left_norm > 0 and right_norm > 0:
            dot_product = np.abs(np.dot(left_wrist_to_pinky, right_wrist_to_pinky) / (left_norm * right_norm))
            perpendicular_score = 1.0 - dot_product  # Higher when more perpendicular
        else:
            perpendicular_score = 0.0

        # Final score combines finger extension and perpendicularity
        return [min(1.0, (extension_score * 0.5 + perpendicular_score * 0.5))] * len(multi_hand_landmarks)


class GestureShop(SingletonGesture):
    def __init__(self):
        super().__init__('shop')

    def score(self, multi_hand_landmarks):
        """
        Calculate score for 'shop' gesture (regular okay sign)

        Specifically looking for:
        - Thumb and index finger forming a circle
        - Other fingers extended

        Returns:
            float: Score between 0 and 1
        """
        if not multi_hand_landmarks or len(multi_hand_landmarks) < 1:
            return [0.0] * len(multi_hand_landmarks)

        landmarks = multi_hand_landmarks[0].landmark

        # Get positions of key points
        thumb_tip = np.array([landmarks[4].x, landmarks[4].y, landmarks[4].z])
        index_tip = np.array([landmarks[8].x, landmarks[8].y, landmarks[8].z])
        middle_tip = np.array([landmarks[12].x, landmarks[12].y, landmarks[12].z])
        ring_tip = np.array([landmarks[16].x, landmarks[16].y, landmarks[16].z])
        pinky_tip = np.array([landmarks[20].x, landmarks[20].y, landmarks[20].z])

        wrist = np.array([landmarks[0].x, landmarks[0].y, landmarks[0].z])

        # Check if thumb and index fingertips are close (forming the "O")
        thumb_index_distance = np.linalg.norm(thumb_tip - index_tip)
        circle_score = max(0, 1.0 - (thumb_index_distance * 10))  # Higher when closer

        # Check if other fingers are extended
        other_fingers_dist = [
            np.linalg.norm(middle_tip - wrist),
            np.linalg.norm(ring_tip - wrist),
            np.linalg.norm(pinky_tip - wrist)
        ]

        # Fingers should be extended (far from wrist)
        extension_threshold = 0.15
        extension_score = sum(1.0 for dist in other_fingers_dist if dist > extension_threshold) / 3.0

        # Final score combines circle formation and other fingers extension
        return [min(1.0, (circle_score * 0.7 + extension_score * 0.3))] * len(multi_hand_landmarks) # TODO: fixme

class GestureExit(SingletonGesture):
    def __init__(self):
        super().__init__('exit')

    def score(self, multi_hand_landmarks) -> float:
        """
        Calculate score for 'exit' gesture (frame consisting of index and thumb fingers of both hands)

        Specifically looking for:
        - Two hands forming a rectangular frame with thumbs and index fingers
        - Other fingers curled

        Returns:
            float: Score between 0 and 1
        """
        if not multi_hand_landmarks or len(multi_hand_landmarks) < 2:
            return [0.0] * len(multi_hand_landmarks)

        # We need two hands for this gesture
        left_hand = None
        right_hand = None

        # Determine which hand is which
        for hand in multi_hand_landmarks:
            landmarks = hand.landmark
            wrist = landmarks[0]
            if wrist.x < 0.5:  # Assuming x-axis increases from left to right
                left_hand = landmarks
            else:
                right_hand = landmarks

        if not left_hand or not right_hand:
            return [0.0] * len(multi_hand_landmarks)

        # Check if index and thumb are extended, others curled
        def check_hand_pose(hand):
            thumb_tip = np.array([hand[4].x, hand[4].y, hand[4].z])
            index_tip = np.array([hand[8].x, hand[8].y, hand[8].z])
            middle_tip = np.array([hand[12].x, hand[12].y, hand[12].z])
            ring_tip = np.array([hand[16].x, hand[16].y, hand[16].z])
            pinky_tip = np.array([hand[20].x, hand[20].y, hand[20].z])

            wrist = np.array([hand[0].x, hand[0].y, hand[0].z])

            # Check if thumb and index are extended
            thumb_dist = np.linalg.norm(thumb_tip - wrist)
            index_dist = np.linalg.norm(index_tip - wrist)

            # Check if other fingers are curled
            middle_curled = np.linalg.norm(middle_tip - wrist) < 0.15
            ring_curled = np.linalg.norm(ring_tip - wrist) < 0.15
            pinky_curled = np.linalg.norm(pinky_tip - wrist) < 0.15

            extension_score = (thumb_dist > 0.15) + (index_dist > 0.15)
            curl_score = middle_curled + ring_curled + pinky_curled

            return (extension_score / 2.0) * 0.5 + (curl_score / 3.0) * 0.5

        left_pose_score = check_hand_pose(left_hand)
        right_pose_score = check_hand_pose(right_hand)

        # Check if the hands form a rectangular frame
        left_thumb = np.array([left_hand[4].x, left_hand[4].y])
        left_index = np.array([left_hand[8].x, left_hand[8].y])
        right_thumb = np.array([right_hand[4].x, right_hand[4].y])
        right_index = np.array([right_hand[8].x, right_hand[8].y])

        # Calculate distances between the four points that should form corners
        distances = [
            np.linalg.norm(left_thumb - left_index),
            np.linalg.norm(left_index - right_index),
            np.linalg.norm(right_index - right_thumb),
            np.linalg.norm(right_thumb - left_thumb)
        ]

        # A good rectangle has similar opposite sides
        rect_score = 1.0 - (abs(distances[0] - distances[2]) + abs(distances[1] - distances[3])) / 2.0

        # Final score combines hand poses and rectangle formation
        pose_score = (left_pose_score + right_pose_score) / 2.0
        return [min(1.0, (pose_score * 0.6 + rect_score * 0.4))] * len(multi_hand_landmarks)
