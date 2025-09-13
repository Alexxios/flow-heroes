import numpy as np

def angle_between(v1, v2):
    v1_norm = np.linalg.norm(v1)
    v2_norm = np.linalg.norm(v2)
    if v1_norm == 0 or v2_norm == 0:
        return 0
    dot_product = np.dot(v1, v2) / (v1_norm * v2_norm)
    # Clamp to avoid numerical errors
    dot_product = max(-1.0, min(1.0, dot_product))
    return np.arccos(dot_product)



def is_curled(finger_landmarks, curl_threshold=0.7) -> bool:
    """
    Determines if a finger is curled based on its landmarks.

    The function analyzes the angle between finger segments and the overall
    length ratio to determine if a finger is curled.

    Args:
        finger_landmarks: List of 4 landmarks for a finger
                         [MCP, PIP, DIP, TIP] joints in order
        curl_threshold: Threshold value to classify as curled (0.0 to 1.0)

    Returns:
        bool: True if finger is curled, False otherwise
    """
    # Convert landmarks to numpy arrays for easier calculation
    mcp = np.array([finger_landmarks[0].x, finger_landmarks[0].y, finger_landmarks[0].z])
    pip = np.array([finger_landmarks[1].x, finger_landmarks[1].y, finger_landmarks[1].z])
    dip = np.array([finger_landmarks[2].x, finger_landmarks[2].y, finger_landmarks[2].z])
    tip = np.array([finger_landmarks[3].x, finger_landmarks[3].y, finger_landmarks[3].z])

    # Calculate vectors for each finger segment
    v1 = pip - mcp
    v2 = dip - pip
    v3 = tip - dip

    # Calculate straight-line distance from MCP to TIP
    direct_distance = np.linalg.norm(tip - mcp)

    # Calculate actual path length along the finger
    path_length = np.linalg.norm(v1) + np.linalg.norm(v2) + np.linalg.norm(v3)

    # Ratio of direct distance to path length (smaller when curled)
    # This is a good primary indicator of curl
    distance_ratio = direct_distance / path_length if path_length > 0 else 1.0

    # Calculate angles at PIP and DIP joints
    angle_pip = angle_between(v1, v2)
    angle_dip = angle_between(v2, v3)

    # Normalize angles to 0-1 range (0 = straight, 1 = fully bent)
    angle_pip_norm = angle_pip / np.pi
    angle_dip_norm = angle_dip / np.pi

    # Combine metrics for final curl score
    curl_score = (1.0 - distance_ratio) * 0.7 + (angle_pip_norm + angle_dip_norm) / 2 * 0.3

    return curl_score > curl_threshold


def is_extended(finger_landmarks, mcp_landmark=None, wrist_landmark=None, extension_threshold=0.6) -> bool:
    """
    Determines if a finger is extended based on its landmarks.

    The function compares finger tip distance from wrist/palm to determine
    if the finger is extended.

    Args:
        finger_landmarks: List of 4 landmarks for a finger
                         [MCP, PIP, DIP, TIP] joints in order
        mcp_landmark: Optional MCP landmark if not included in finger_landmarks
        wrist_landmark: Optional wrist landmark for additional reference
        extension_threshold: Threshold value to classify as extended (0.0 to 1.0)

    Returns:
        bool: True if finger is extended, False otherwise
    """
    # Convert landmarks to numpy arrays
    if mcp_landmark is None:
        mcp = np.array([finger_landmarks[0].x, finger_landmarks[0].y, finger_landmarks[0].z])
    else:
        mcp = np.array([mcp_landmark.x, mcp_landmark.y, mcp_landmark.z])

    pip = np.array([finger_landmarks[1].x, finger_landmarks[1].y, finger_landmarks[1].z])
    dip = np.array([finger_landmarks[2].x, finger_landmarks[2].y, finger_landmarks[2].z])
    tip = np.array([finger_landmarks[3].x, finger_landmarks[3].y, finger_landmarks[3].z])

    # Use wrist as additional reference if provided
    if wrist_landmark is not None:
        wrist = np.array([wrist_landmark.x, wrist_landmark.y, wrist_landmark.z])
    else:
        wrist = None

    # Calculate vectors for each finger segment
    v1 = pip - mcp
    v2 = dip - pip
    v3 = tip - dip

    # Calculate angles at PIP and DIP joints (should be close to 0 if extended)
    angle_pip = angle_between(v1, v2)
    angle_dip = angle_between(v2, v3)

    # Normalize angles to 0-1 range (0 = straight, 1 = fully bent)
    angle_pip_norm = angle_pip / np.pi
    angle_dip_norm = angle_dip / np.pi

    # Calculate straight-line distance ratio (should be close to 1 if extended)
    direct_distance = np.linalg.norm(tip - mcp)
    path_length = np.linalg.norm(v1) + np.linalg.norm(v2) + np.linalg.norm(v3)
    distance_ratio = direct_distance / path_length if path_length > 0 else 1.0

    # If wrist is provided, check finger direction relative to palm plane
    palm_extension_score = 0.0
    if wrist is not None:
        # Vector from wrist to MCP
        v_wrist_mcp = mcp - wrist
        # Vector from MCP to tip
        v_mcp_tip = tip - mcp

        # Check if finger direction aligns with palm normal
        if np.linalg.norm(v_wrist_mcp) > 0 and np.linalg.norm(v_mcp_tip) > 0:
            v_wrist_mcp = v_wrist_mcp / np.linalg.norm(v_wrist_mcp)
            v_mcp_tip = v_mcp_tip / np.linalg.norm(v_mcp_tip)
            alignment = np.dot(v_wrist_mcp, v_mcp_tip)
            palm_extension_score = max(0, (alignment + 1) / 2)  # Convert from [-1,1] to [0,1]

    # Calculate finger extension score based on:
    # 1. Low angle at joints (straight finger)
    # 2. High distance ratio (straight path)
    # 3. Good alignment with palm direction if wrist provided
    angle_score = 1.0 - (angle_pip_norm + angle_dip_norm) / 2

    if wrist is not None:
        extension_score = distance_ratio * 0.4 + angle_score * 0.4 + palm_extension_score * 0.2
    else:
        extension_score = distance_ratio * 0.5 + angle_score * 0.5

    return extension_score > extension_threshold
