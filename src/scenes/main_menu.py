import os

import pygame
from pygame import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE

from scene import Scene

class MainMenuScene(Scene):
    def __init__(self):
        super().__init__()
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (150, 150, 150)
        self.HIGHLIGHT = (100, 100, 255)

        # Screen dimensions
        self.WIDTH, self.HEIGHT = 800, 600

        # Load assets
        self.load_assets()

        # Button properties
        self.buttons = [
            {
                "text": "Play",
                "icon": self.icons["play"],
                "rect": pygame.Rect(self.WIDTH // 2 - 100, 250, 200, 50),
                "action": self.play_game
            },
            {
                "text": "Settings",
                "icon": self.icons["settings"],
                "rect": pygame.Rect(self.WIDTH // 2 - 100, 320, 200, 50),
                "action": self.open_settings
            },
            {
                "text": "Exit",
                "icon": self.icons["exit"],
                "rect": pygame.Rect(self.WIDTH // 2 - 100, 390, 200, 50),
                "action": self.exit_game
            }
        ]

        self.selected_button = None

    def load_assets(self):
        # Load custom font - replace 'your_font.ttf' with your actual font file
        try:
            font_path = os.path.join("assets", "fonts", "your_font.ttf")
            self.font = pygame.font.Font(font_path, 24)
            self.title_font = pygame.font.Font(font_path, 40)
        except:
            print("Could not load custom font. Using system font instead.")
            self.font = pygame.font.SysFont("Arial", 24)
            self.title_font = pygame.font.SysFont("Arial", 40)

        # Load logo - replace 'Logo.psd' with your actual converted logo file
        try:
            logo_path = os.path.join("assets", "images", "Logo.png")  # Note: Pygame can't load PSDs directly
            self.logo = pygame.image.load(logo_path).convert_alpha()
            # Scale logo if needed
            logo_width = 400
            logo_height = int(self.logo.get_height() * (logo_width / self.logo.get_width()))
            self.logo = pygame.transform.scale(self.logo, (logo_width, logo_height))
        except:
            print("Could not load logo. Creating placeholder instead.")
            self.logo = self.title_font.render("GAME LOGO", True, self.WHITE)

        # Load icons from tileset
        # In a real implementation, you would extract the 32x32 tiles from your PSD tileset
        self.icons = {}
        try:
            # This is a placeholder for loading actual icons from your tileset
            icons_path = os.path.join("assets", "images", "Icons")  # Convert PSD to PNG first
            for i, icon in enumerate(["play", "settings", "exit"]):
                self.icons[icon] = pygame.image.load(os.path.join(icons_path, f"Icons_{str(i+1).zfill(2)}.png")).convert_alpha()

            # Load frame tiles for UI elements
            # self.frame_tiles = [...] # You would extract frame tiles similarly
        except:
            print("Could not load tileset. Creating placeholder icons instead.")
            # Create placeholder icons
            self.icons["play"] = self.create_placeholder_icon((0, 255, 0))
            self.icons["settings"] = self.create_placeholder_icon((0, 0, 255))
            self.icons["exit"] = self.create_placeholder_icon((255, 0, 0))

    def extract_tile(self, tileset, x, y, tile_size=32):
        """Extract a tile from the tileset at the given position"""
        tile = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        tile.blit(tileset, (0, 0), (x * tile_size, y * tile_size, tile_size, tile_size))
        return tile

    def create_placeholder_icon(self, color):
        """Create a simple colored square as a placeholder icon"""
        icon = pygame.Surface((32, 32), pygame.SRCALPHA)
        icon.fill(color)
        return icon

    def draw_button(self, screen, button, hover=False):
        # Draw button background
        color = self.HIGHLIGHT if hover else self.GRAY
        pygame.draw.rect(screen, color, button["rect"], border_radius=5)
        pygame.draw.rect(screen, self.WHITE, button["rect"], 2, border_radius=5)

        # Draw icon
        icon_pos = (button["rect"].x + 10, button["rect"].y + button["rect"].height // 2 - 16)
        screen.blit(button["icon"], icon_pos)

        # Draw text
        text = self.font.render(button["text"], True, self.WHITE)
        text_pos = (button["rect"].x + 50, button["rect"].y + button["rect"].height // 2 - text.get_height() // 2)
        screen.blit(text, text_pos)

    def play_game(self):
        print("Starting the game...")
        # Switch to the game scene
        # self.switch_to_scene(GameScene())

    def open_settings(self):
        print("Opening settings...")
        # Switch to the settings scene
        # self.switch_to_scene(SettingsScene())

    def exit_game(self):
        print("Exiting game...")
        self.terminate()

    def process_input(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.selected_button = None

        # Check which button is being hovered
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                self.selected_button = button
                break

        for event in events:
            if event.type == QUIT:
                self.terminate()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                if self.selected_button:
                    self.selected_button["action"]()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.terminate()

    def update(self):
        # In a more complex scene, you might update animations or other elements here
        pass

    def render(self, screen):
        # Fill background
        screen.fill(self.BLACK)

        # Draw logo
        logo_pos = (self.WIDTH // 2 - self.logo.get_width() // 2, 50)
        screen.blit(self.logo, logo_pos)

        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            hover = button["rect"].collidepoint(mouse_pos)
            self.draw_button(screen, button, hover=hover)


class Director:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Game with Scene System")
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.running = True
        self.scene = MainMenuScene()

    def run(self):
        while self.running and self.scene is not None:
            events = pygame.event.get()

            # Process input
            self.scene.process_input(events)

            # Update scene
            self.scene.update()

            # Render scene
            self.scene.render(self.screen)

            # Update display
            pygame.display.flip()

            # Check for scene change
            if self.scene.next is not self.scene:
                self.scene = self.scene.next
                if self.scene is None:
                    self.running = False

            # Cap the frame rate
            self.clock.tick(self.fps)

        pygame.quit()


if __name__ == "__main__":
    director = Director()
    director.run()
