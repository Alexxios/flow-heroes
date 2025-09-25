import pygame
import pygame.camera
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyGame Camera Effects")

# Initialize the camera module
pygame.camera.init()

# Get available cameras
cam_list = pygame.camera.list_cameras()
if not cam_list:
    print("No cameras found!")
    sys.exit()

# Use the first available camera
cam = pygame.camera.Camera(cam_list[0], (640, 480))
cam.start()

# Create a surface to capture the camera image
camera_surface = pygame.Surface((640, 480))

# Font for UI
font = pygame.font.SysFont('Arial', 24)

# Effect variables
current_effect = "Normal"
effects = ["Normal", "Grayscale", "Invert", "Pixelate", "Edge Detect", "Blur", "Color Shift", "Mirror", "Thermal"]
effect_index = 0

# For pixelation effect
pixel_size = 8

# For color shift effect
color_shift = 0

# For thermal effect
thermal_palette = [
    (0, 0, 0),       # Black
    (0, 0, 128),     # Dark Blue
    (0, 0, 255),     # Blue
    (0, 128, 255),   # Light Blue
    (0, 255, 255),   # Cyan
    (0, 255, 128),   # Light Green
    (0, 255, 0),     # Green
    (128, 255, 0),   # Yellow-Green
    (255, 255, 0),   # Yellow
    (255, 128, 0),   # Orange
    (255, 0, 0),     # Red
    (255, 0, 128),   # Pink
    (255, 0, 255),   # Magenta
    (255, 255, 255)  # White
]

# Clock for controlling frame rate
clock = pygame.time.Clock()

def apply_grayscale(surface):
    """Convert the surface to grayscale"""
    gray_surface = surface.copy()
    pixels = pygame.surfarray.pixels3d(gray_surface)
    # Convert to grayscale using luminance formula
    gray_pixels = (0.299 * pixels[:,:,0] + 0.587 * pixels[:,:,1] + 0.114 * pixels[:,:,2]).astype('uint8')
    pixels[:,:,0] = gray_pixels
    pixels[:,:,1] = gray_pixels
    pixels[:,:,2] = gray_pixels
    del pixels  # Unlock the surface
    return gray_surface

def apply_invert(surface):
    """Invert the colors of the surface"""
    invert_surface = surface.copy()
    pixels = pygame.surfarray.pixels3d(invert_surface)
    pixels[:,:,:] = 255 - pixels[:,:,:]
    del pixels
    return invert_surface

def apply_pixelate(surface, size):
    """Pixelate the surface"""
    pixel_surface = pygame.Surface(surface.get_size())
    # Scale down
    small = pygame.transform.scale(surface, (surface.get_width() // size, surface.get_height() // size))
    # Scale back up with nearest neighbor to create pixelated effect
    pygame.transform.scale(small, surface.get_size(), pixel_surface)
    return pixel_surface

def apply_edge_detect(surface):
    """Apply a simple edge detection filter"""
    edge_surface = surface.copy()
    pixels = pygame.surfarray.pixels3d(edge_surface)

    # Create a new array for the result
    result = pixels.copy()

    # Simple edge detection kernel
    for y in range(1, pixels.shape[0]-1):
        for x in range(1, pixels.shape[1]-1):
            # Calculate gradient in x and y directions
            gx = (pixels[y-1, x-1] + 2*pixels[y, x-1] + pixels[y+1, x-1]) - \
                 (pixels[y-1, x+1] + 2*pixels[y, x+1] + pixels[y+1, x+1])

            gy = (pixels[y-1, x-1] + 2*pixels[y-1, x] + pixels[y-1, x+1]) - \
                 (pixels[y+1, x-1] + 2*pixels[y+1, x] + pixels[y+1, x+1])

            # Calculate magnitude
            magnitude = min(255, int(math.sqrt(gx[0]**2 + gy[0]**2) / 4))

            # Set all channels to the magnitude
            result[y, x] = [magnitude, magnitude, magnitude]

    # Copy result back to pixels
    pixels[:,:,:] = result[:,:,:]
    del pixels
    return edge_surface

def apply_blur(surface):
    """Apply a simple blur filter"""
    blur_surface = surface.copy()
    # Use scale trick to create a blur effect
    small = pygame.transform.scale(blur_surface, (blur_surface.get_width() // 4, blur_surface.get_height() // 4))
    pygame.transform.smoothscale(small, blur_surface.get_size(), blur_surface)
    return blur_surface

def apply_color_shift(surface, shift):
    """Shift the colors of the surface"""
    shift_surface = surface.copy()
    pixels = pygame.surfarray.pixels3d(shift_surface)

    # Shift color channels
    r = pixels[:,:,0]
    g = pixels[:,:,1]
    b = pixels[:,:,2]

    if shift % 3 == 0:  # Shift red to green, green to blue, blue to red
        pixels[:,:,0] = b
        pixels[:,:,1] = r
        pixels[:,:,2] = g
    elif shift % 3 == 1:  # Shift red to blue, green to red, blue to green
        pixels[:,:,0] = g
        pixels[:,:,1] = b
        pixels[:,:,2] = r

    del pixels
    return shift_surface

def apply_mirror(surface):
    """Mirror the surface horizontally"""
    return pygame.transform.flip(surface, True, False)

def apply_thermal(surface):
    """Apply a thermal camera effect"""
    thermal_surface = surface.copy()
    pixels = pygame.surfarray.pixels3d(thermal_surface)

    # Convert to grayscale first
    gray_pixels = (0.299 * pixels[:,:,0] + 0.587 * pixels[:,:,1] + 0.114 * pixels[:,:,2]).astype('uint8')

    # Map grayscale values to thermal palette
    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            # Normalize to palette index
            idx = min(len(thermal_palette)-1, gray_pixels[y, x] // 18)
            pixels[y, x] = thermal_palette[idx]

    del pixels
    return thermal_surface

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                effect_index = (effect_index + 1) % len(effects)
                current_effect = effects[effect_index]
            elif event.key == pygame.K_LEFT:
                effect_index = (effect_index - 1) % len(effects)
                current_effect = effects[effect_index]
            elif event.key == pygame.K_UP and current_effect == "Pixelate":
                pixel_size = min(32, pixel_size + 2)
            elif event.key == pygame.K_DOWN and current_effect == "Pixelate":
                pixel_size = max(2, pixel_size - 2)

    # Get image from camera
    if cam.query_image():
        camera_surface = cam.get_image(camera_surface)

    # Apply current effect
    if current_effect == "Normal":
        effect_surface = camera_surface
    elif current_effect == "Grayscale":
        effect_surface = apply_grayscale(camera_surface)
    elif current_effect == "Invert":
        effect_surface = apply_invert(camera_surface)
    elif current_effect == "Pixelate":
        effect_surface = apply_pixelate(camera_surface, pixel_size)
    elif current_effect == "Edge Detect":
        effect_surface = apply_edge_detect(camera_surface)
    elif current_effect == "Blur":
        effect_surface = apply_blur(camera_surface)
    elif current_effect == "Color Shift":
        effect_surface = apply_color_shift(camera_surface, color_shift)
        color_shift += 1
    elif current_effect == "Mirror":
        effect_surface = apply_mirror(camera_surface)
    elif current_effect == "Thermal":
        effect_surface = apply_thermal(camera_surface)

    # Scale the camera image to fit the screen
    scaled_surface = pygame.transform.scale(effect_surface, (width, height))

    # Draw the camera image
    screen.blit(scaled_surface, (0, 0))

    # Draw UI
    effect_text = font.render(f"Effect: {current_effect}", True, (255, 255, 255))
    screen.blit(effect_text, (10, 10))

    help_text = font.render("Use LEFT/RIGHT arrows to change effects", True, (255, 255, 255))
    screen.blit(help_text, (10, height - 60))

    if current_effect == "Pixelate":
        pixel_text = font.render(f"Pixel Size: {pixel_size} (UP/DOWN to adjust)", True, (255, 255, 255))
        screen.blit(pixel_text, (10, height - 30))

    # Update the display
    pygame.display.flip()

    # Control frame rate
    clock.tick(30)

# Clean up
cam.stop()
pygame.quit()
sys.exit()