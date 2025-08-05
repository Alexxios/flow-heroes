import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Initialize webcam
cap = cv2.VideoCapture(0)

# For gesture recognition timing
last_gesture_time = time.time()
gesture_interval = 0.5  # seconds between gesture prints

def recognize_gesture(hand_landmarks):
    """
    Recognize hand gesture based on the landmarks
    """
    # Get all landmark points
    points = []
    for landmark in hand_landmarks.landmark:
        points.append((landmark.x, landmark.y, landmark.z))

    # Check if fingers are extended
    # Thumb
    thumb_tip = points[4]
    thumb_ip = points[3]
    thumb_extended = thumb_tip[0] < thumb_ip[0]  # For right hand

    # Other fingers
    fingers_extended = []
    for finger_id in range(1, 5):  # Index, Middle, Ring, Pinky
        finger_tip_id = finger_id * 4 + 4
        finger_pip_id = finger_id * 4 + 2

        # Check if finger is extended
        finger_tip = points[finger_tip_id]
        finger_pip = points[finger_pip_id]
        finger_extended = finger_tip[1] < finger_pip[1]  # Y-axis is inverted in image
        fingers_extended.append(finger_extended)

    # Recognize gestures
    if all(fingers_extended) and thumb_extended:
        return "Open Hand"
    elif not any(fingers_extended) and not thumb_extended:
        return "Closed Fist"
    elif not any(fingers_extended) and thumb_extended:
        return "Thumbs Up"
    elif fingers_extended[0] and not any(fingers_extended[1:]) and not thumb_extended:
        return "Pointing"
    elif fingers_extended[0] and fingers_extended[1] and not any(fingers_extended[2:]):
        return "Victory"
    else:
        return "Unknown Gesture"

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a later selfie-view display
    image = cv2.flip(image, 1)

    # Convert the BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and find hands
    results = hands.process(image_rgb)

    # Draw hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            # Recognize and print gesture at intervals
            current_time = time.time()
            if current_time - last_gesture_time > gesture_interval:
                gesture = recognize_gesture(hand_landmarks)
                print(f"Detected Gesture: {gesture}")
                last_gesture_time = current_time

    # Display the resulting image
    cv2.imshow('MediaPipe Hands', image)

    # Exit on 'q' press
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
