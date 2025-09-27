import pygame
import pygame.camera
import cv2
import numpy as np
import mediapipe as mp

# Initialize
pygame.init()
pygame.camera.init()

# Camera setup
cam_list = pygame.camera.list_cameras()
if not cam_list:
    print("No cameras found!")
    exit()

cam = pygame.camera.Camera(cam_list[0], (640, 480))
cam.start()

# Display window
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pygame + MediaPipe")

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2)


def process_frame(surface):
    # Convert surface to numpy array
    array_3d = pygame.surfarray.pixels3d(surface)
    array_3d = np.transpose(array_3d, (1, 0, 2))
    rgb_array = cv2.cvtColor(array_3d, cv2.COLOR_BGR2RGB)

    # Process with MediaPipe
    results = hands.process(rgb_array)

    # Convert back to surface for display
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                rgb_array, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Convert back to BGR for pygame
    bgr_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
    bgr_array = np.transpose(bgr_array, (1, 0, 2))

    # Create new surface
    new_surface = pygame.surfarray.make_surface(bgr_array)
    return new_surface


# Main loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get camera image
    if cam.query_image():
        image = cam.get_image()

        # Process with MediaPipe
        processed_image = process_frame(image)

        # Display
        screen.blit(processed_image, (0, 0))
        pygame.display.flip()

    clock.tick(30)

cam.stop()
pygame.quit()