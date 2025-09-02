import pygame

from ui import Button, BalanceBar
from scenes import Scene, SceneManager
from utils import load_image, load_font


class MainMenuScene(Scene):
    """Main menu scene with buttons and balance display"""
    def __init__(self, manager: SceneManager):
        super().__init__(manager)
        self.bg_color = (20, 20, 30)
        self.title_font = None
        self.button_font = None
        self.balance_font = None
        self.icons = {}  # Store icons for buttons

    def setup(self) -> None:
        """Initialize main menu resources"""
        screen_width, screen_height = self.manager.screen.get_size()


        # Load fonts (you would replace these with your custom font paths)
        try:
            self.title_font = load_font("assets/gamekit/Font/Planes_ValMore.ttf", 72)  # Use custom font here
            self.button_font = load_font("assets/gamekit/Font/Planes_ValMore.ttf", 48)  # Use custom font here
            self.balance_font = load_font("assets/gamekit/Font/Planes_ValMore.ttf", 36)  # Use custom font here
        except:
            # Fallback to default font if custom fonts fail to load
            self.title_font = pygame.font.SysFont("Arial", 72)
            self.button_font = pygame.font.SysFont("Arial", 48)
            self.balance_font = pygame.font.SysFont("Arial", 36)

        # Load icons (placeholders - replace with your actual icon loading)
        icon_size = (32, 32)
        self.icons = {
            'play': self._create_placeholder_icon((0, 255, 0), icon_size),
            'store': self._create_placeholder_icon((255, 255, 0), icon_size),
            'settings': load_image("assets/gamekit/3 Icons/Icons_39.png"),
            'exit': self._create_placeholder_icon((255, 0, 0), icon_size),
            'coin': self._create_placeholder_icon((255, 215, 0), icon_size),
        }

        # Calculate button positions
        button_width = 300
        button_height = 60
        button_spacing = 20
        start_y = screen_height // 2 - (button_height * 2 + button_spacing * 1.5)

        # Create UI elements
        self.ui_elements = []

        # Add balance bar
        balance_bar = BalanceBar(
            20, 20, 200, 50,
            self.balance_font,
            self.icons['coin'],
            self.manager.player_data["balance"]
        )
        self.ui_elements.append(balance_bar)

        # Add menu buttons
        self.ui_elements.append(Button(
            screen_width // 2 - button_width // 2,
            start_y,
            button_width, button_height,
            "Play", self._on_play_click, self.button_font, self.icons['play']
        ))

        self.ui_elements.append(Button(
            screen_width // 2 - button_width // 2,
            start_y + button_height + button_spacing,
            button_width, button_height,
            "Store", self._on_store_click, self.button_font, self.icons['store']
        ))

        self.ui_elements.append(Button(
            screen_width // 2 - button_width // 2,
            start_y + (button_height + button_spacing) * 2,
            button_width, button_height,
            "Settings", self._on_settings_click, self.button_font, self.icons['settings']
        ))

        self.ui_elements.append(Button(
            screen_width // 2 - button_width // 2,
            start_y + (button_height + button_spacing) * 3,
            button_width, button_height,
            "Exit", self._on_exit_click, self.button_font, self.icons['exit']
        ))

    def _create_placeholder_icon(self, color, size):
        """Create a placeholder icon for development"""
        icon = pygame.Surface(size)
        icon.fill(color)
        # Draw a simple shape to distinguish icons
        pygame.draw.circle(icon, (255, 255, 255), (size[0]//2, size[1]//2), min(size)//3)
        return icon

    def _on_play_click(self):
        print("Play button clicked")
        # In a complete implementation, you would transition to the game scene
        # self.manager.set_scene("game")

    def _on_store_click(self):
        print("Store button clicked")
        # self.manager.set_scene("store")

    def _on_settings_click(self):
        print("Settings button clicked")
        # self.manager.set_scene("settings")

    def _on_exit_click(self):
        print("Exit button clicked")
        pygame.quit()
        exit(0)

    def teardown(self) -> None:
        """Clean up resources"""
        # Clear references to resources
        self.title_font = None
        self.button_font = None
        self.balance_font = None
        self.icons.clear()
        self.ui_elements.clear()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the main menu"""
        # Fill background
        surface.fill(self.bg_color)

        # Draw title
        title_text = self.title_font.render("Platformer Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(
            centerx=surface.get_width() // 2,
            top=50
        )
        surface.blit(title_text, title_rect)

        # Draw UI elements
        super().draw(surface)
