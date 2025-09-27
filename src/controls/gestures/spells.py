import math
import typing as tp
from typing import NamedTuple

from controls.gestures import SingletonGesture


class GesturePray(SingletonGesture):
    def __init__(self):
        super().__init__('pray')

    def score(self, multi_hand_landmarks: NamedTuple) -> tp.List[float]:
        """
        Calculate a gesture recognition score [0, 1] for the "pray" gesture.

        Criteria:
        1. All fingers are extended
        2. All fingertips are touching each other
        3. All fingers are pointing upwards

        Args:
            multi_hand_landmarks: MediaPipe hand landmarks object

        Returns:
            tp.List[float]: Score between 0 and 1 for all hands representing how well the gesture matches
        """

        if len(multi_hand_landmarks) != 2:
            return [0.0] * len(multi_hand_landmarks)

        # Get landmarks for both hands
        hand1 = multi_hand_landmarks[0].landmark
        hand2 = multi_hand_landmarks[1].landmark

        # Fingertip indices for each finger (thumb, index, middle, ring, pinky)
        finger_tips = [4, 8, 12, 16, 20]

        # Finger PIP joints (proximal interphalangeal) for checking extension
        pip_joints = [3, 6, 10, 14, 18]

        # Finger MCP joints (metacarpophalangeal) for checking extension
        mcp_joints = [2, 5, 9, 13, 17]

        total_score = 0.0
        max_possible_score = 3.0  # Three criteria

        # 1. Check if all fingers are extended
        extension_score = self._check_finger_extension(hand1, pip_joints, mcp_joints, finger_tips)
        extension_score += self._check_finger_extension(hand2, pip_joints, mcp_joints, finger_tips)
        extension_score /= 2.0  # Average for both hands

        # 2. Check if all fingertips are touching each other
        touching_score = self._check_finger_tips_touching(hand1, hand2, finger_tips)

        # 3. Check if all fingers are pointing upwards
        upward_score = self._check_fingers_upward(hand1, finger_tips, mcp_joints)
        upward_score += self._check_fingers_upward(hand2, finger_tips, mcp_joints)
        upward_score /= 2.0  # Average for both hands

        total_score = (extension_score + touching_score + upward_score) / max_possible_score

        return [max(0.0, min(1.0, total_score))] * len(multi_hand_landmarks)  # Clamp between 0 and 1

    def _check_finger_extension(self, hand_landmarks, pip_joints, mcp_joints, finger_tips):
        """
        Check if all fingers are extended.
        Extended finger: tip is further from wrist than PIP joint, which is further than MCP joint.
        """
        wrist = hand_landmarks[0]  # Wrist landmark

        extended_fingers = 0
        total_fingers = len(finger_tips)

        for i in range(total_fingers):
            tip = hand_landmarks[finger_tips[i]]
            pip = hand_landmarks[pip_joints[i]]
            mcp = hand_landmarks[mcp_joints[i]]

            # Calculate distances from wrist (using y-coordinate since y increases downward)
            dist_tip = abs(tip.y - wrist.y)
            dist_pip = abs(pip.y - wrist.y)
            dist_mcp = abs(mcp.y - wrist.y)

            # For extended finger: tip should be furthest from wrist
            if dist_tip > dist_pip and dist_pip > dist_mcp:
                extended_fingers += 1

        return extended_fingers / total_fingers

    def _check_finger_tips_touching(self, hand1, hand2, finger_tips, threshold=0.05):
        """
        Check if corresponding finger tips from both hands are touching each other.
        """
        touching_pairs = 0
        total_pairs = len(finger_tips)

        for tip_idx in finger_tips:
            tip1 = hand1[tip_idx]
            tip2 = hand2[tip_idx]

            # Calculate Euclidean distance between corresponding tips
            distance = math.sqrt((tip1.x - tip2.x) ** 2 + (tip1.y - tip2.y) ** 2 + (tip1.z - tip2.z) ** 2)

            if distance < threshold:
                touching_pairs += 1

        return touching_pairs / total_pairs

    def _check_fingers_upward(self, hand_landmarks, finger_tips, mcp_joints, angle_threshold=30):
        """
        Check if fingers are pointing upwards.
        Compare the vector from MCP joint to finger tip with vertical direction.
        """
        upward_fingers = 0
        total_fingers = len(finger_tips)

        for i in range(total_fingers):
            tip = hand_landmarks[finger_tips[i]]
            mcp = hand_landmarks[mcp_joints[i]]

            # Calculate finger direction vector
            finger_vector = (tip.x - mcp.x, tip.y - mcp.y)

            # Vertical upward vector (pointing up in image coordinates where y increases downward)
            upward_vector = (0, -1)

            # Calculate angle between finger vector and upward vector
            dot_product = finger_vector[0] * upward_vector[0] + finger_vector[1] * upward_vector[1]
            mag_finger = math.sqrt(finger_vector[0] ** 2 + finger_vector[1] ** 2)
            mag_upward = math.sqrt(upward_vector[0] ** 2 + upward_vector[1] ** 2)

            if mag_finger > 0 and mag_upward > 0:
                cosine_angle = dot_product / (mag_finger * mag_upward)
                cosine_angle = max(-1, min(1, cosine_angle))  # Clamp to valid range
                angle = math.degrees(math.acos(cosine_angle))

                if angle < angle_threshold:
                    upward_fingers += 1

        return upward_fingers / total_fingers

    # Alternative simpler version for upward check (using y-coordinates)
    def _check_fingers_upward_simple(self, hand_landmarks, finger_tips, mcp_joints):
        """
        Simplified version: check if finger tips are above MCP joints (pointing upward).
        """
        upward_fingers = 0
        total_fingers = len(finger_tips)

        for i in range(total_fingers):
            tip = hand_landmarks[finger_tips[i]]
            mcp = hand_landmarks[mcp_joints[i]]

            # In image coordinates, y increases downward, so smaller y means higher position
            if tip.y < mcp.y:  # Tip is above MCP joint
                upward_fingers += 1

        return upward_fingers / total_fingers