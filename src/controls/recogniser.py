from threading import Thread

import pygame

import cv2
import mediapipe as mp
import numpy as np
import time
import pickle
import os



# Constants
GESTURE_FILE = "custom_gestures.pkl"
SAMPLES_PER_GESTURE = 30
RECOGNITION_THRESHOLD = 0.6

# Определим пользовательское событие
CUSTOM_EVENT = pygame.USEREVENT + 1
DATA_EVENT = pygame.USEREVENT + 2


class Recogniser(Thread):
    def run(self):
        # Initialize MediaPipe Hands
        mp_hands = mp.solutions.hands
        mp_drawing = mp.solutions.drawing_utils
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,  # For simplicity, track only one hand
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )

        # Initialize webcam
        cap = cv2.VideoCapture(0)

        # Load existing gestures or create empty dictionary
        if os.path.exists(GESTURE_FILE):
            with open(GESTURE_FILE, 'rb') as f:
                gesture_database = pickle.load(f)
            print(f"Loaded {len(gesture_database)} custom gestures.")
        else:
            gesture_database = {}

        # For timing
        last_recognition_time = time.time()
        recognition_interval = 0.5  # seconds between gesture recognitions

        # Mode flags
        recording_mode = False
        current_gesture_name = ""
        recording_samples = []

        def extract_hand_features(hand_landmarks):
            """Extract a normalized feature vector from hand landmarks"""
            # Get all landmark points
            points = np.array([(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark])

            # Center the points (translation invariance)
            center = np.mean(points, axis=0)
            centered_points = points - center

            # Scale to unit size (scale invariance)
            scale = np.max(np.linalg.norm(centered_points, axis=1))
            normalized_points = centered_points / scale if scale > 0 else centered_points

            # Flatten to feature vector
            return normalized_points.flatten()

        def compare_gestures(gesture1, gesture2):
            """Compute similarity between two gesture feature vectors"""
            # Use cosine similarity for comparing the gestures
            similarity = np.dot(gesture1, gesture2) / (np.linalg.norm(gesture1) * np.linalg.norm(gesture2))
            return similarity

        def recognize_gesture(features):
            """Recognize a gesture by comparing with stored templates"""
            if not gesture_database:
                return "No gestures defined"

            best_match = None
            best_score = -1

            for gesture_name, gesture_samples in gesture_database.items():
                # Compare with each sample of the gesture
                scores = [compare_gestures(features, sample) for sample in gesture_samples]
                avg_score = np.mean(scores)

                if avg_score > best_score:
                    best_score = avg_score
                    best_match = gesture_name

            if best_score >= RECOGNITION_THRESHOLD:
                # Создаем событие с данными
                event = pygame.event.Event(DATA_EVENT, {"message": best_match})
                # Отправляем событие в очередь событий pygame
                pygame.event.post(event)
                return f"{best_match} ({best_score:.2f})"
            else:
                return f"Unknown ({best_score:.2f})"

        def start_recording(name):
            """Start recording samples for a new gesture"""
            global recording_mode, current_gesture_name, recording_samples
            recording_mode = True
            current_gesture_name = name
            recording_samples = []
            print(f"Recording gesture '{name}'. Please perform the gesture {SAMPLES_PER_GESTURE} times.")

        def save_gestures():
            """Save gesture database to file"""
            with open(GESTURE_FILE, 'wb') as f:
                pickle.dump(gesture_database, f)
            print(f"Saved {len(gesture_database)} gestures to {GESTURE_FILE}")

        # Main loop
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # Flip the image horizontally
            image = cv2.flip(image, 1)

            # Convert the BGR image to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Process the image and find hands
            results = hands.process(image_rgb)

            # Interface text
            cv2.putText(image, "Controls:", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(image, "R - Record new gesture", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(image, "S - Save gestures", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(image, "Q - Quit", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if recording_mode:
                cv2.putText(image, f"RECORDING: {current_gesture_name} ({len(recording_samples)}/{SAMPLES_PER_GESTURE})",
                        (10, 440), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(image, "Perform gesture and press SPACE to capture",
                        (10, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Draw hand landmarks and process gestures
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS
                    )

                    # Extract features
                    features = extract_hand_features(hand_landmarks)

                    # Handle recording mode
                    if recording_mode and len(recording_samples) < SAMPLES_PER_GESTURE:
                        # Visual cue for recording
                        cv2.circle(image, (30, 30), 10, (0, 0, 255), -1)

                    # Recognition mode
                    elif not recording_mode:
                        current_time = time.time()
                        if current_time - last_recognition_time > recognition_interval:
                            gesture_name = recognize_gesture(features)
                            cv2.putText(image, f"Gesture: {gesture_name}",
                                    (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                            last_recognition_time = current_time

            # Display the resulting image
            # cv2.imshow('Custom Gesture Recognition', image)

            # Handle key presses
            key = cv2.waitKey(5) & 0xFF

            if key == ord('q'):  # Quit
                break
            elif key == ord('r'):  # Record new gesture
                if not recording_mode:
                    gesture_name = input("Enter a name for the new gesture: ")
                    start_recording(gesture_name)
            elif key == ord('s'):  # Save gestures
                save_gestures()
            elif key == ord(' '):  # Space to capture a sample during recording
                if recording_mode and results.multi_hand_landmarks:
                    features = extract_hand_features(results.multi_hand_landmarks[0])
                    recording_samples.append(features)
                    print(f"Recorded sample {len(recording_samples)}/{SAMPLES_PER_GESTURE}")

                    # Check if we have enough samples
                    if len(recording_samples) >= SAMPLES_PER_GESTURE:
                        gesture_database[current_gesture_name] = recording_samples
                        print(f"Gesture '{current_gesture_name}' recorded successfully with {len(recording_samples)} samples!")
                        recording_mode = False

        # Clean up
        cap.release()
        cv2.destroyAllWindows()
