from typing import Optional, List

import pygame
from pygame.sprite import Group
from pygame.transform import scale2x

from scenes import Scene
from utils import load_image

from core.player import Player
from core.hero import HeroFactory
from core.background import Background

class BalanceDisplay:
    """UI element to display the player's balance"""
    def __init__(self, balance: int = 0):
        self.balance = balance
        self.font = None
        self.position = (20, 20)

    def setup(self) -> None:
        """Setup font for the balance display"""
        self.font = pygame.font.SysFont('Arial', 24)

    def update(self, balance: int) -> None:
        """Update the balance value"""
        self.balance = balance

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the balance on the screen"""
        if self.font:
            text = self.font.render(f"Balance: ${self.balance}", True, (255, 255, 255))
            surface.blit(text, self.position)


class LevelDisplay:
    """UI element to display the current level"""
    def __init__(self, level: int = 1):
        self.level = level
        self.font = None
        self.position = (20, 50)

    def setup(self) -> None:
        """Setup font for the level display"""
        self.font = pygame.font.SysFont('Arial', 24)

    def update(self, level: int) -> None:
        """Update the level value"""
        self.level = level

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the level on the screen"""
        if self.font:
            text = self.font.render(f"Level: {self.level}", True, (255, 255, 255))
            surface.blit(text, self.position)


class PauseOverlay:
    """Overlay displayed when the game is paused"""
    def __init__(self):
        self.font = None

    def setup(self) -> None:
        """Setup font for the pause overlay"""
        self.font = pygame.font.SysFont('Arial', 48)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the pause overlay"""
        if self.font:
            # Semi-transparent overlay
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            surface.blit(overlay, (0, 0))

            # Pause text
            text = self.font.render("PAUSED", True, (255, 255, 255))
            text_rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
            surface.blit(text, text_rect)

            # Instructions
            font_small = pygame.font.SysFont('Arial', 24)
            instructions = font_small.render("Press P to resume", True, (255, 255, 255))
            inst_rect = instructions.get_rect(center=(surface.get_width() // 2,
                                                    (surface.get_height() // 2) + 50))
            surface.blit(instructions, inst_rect)


class GameScene(Scene):
    """Game scene that handles gameplay, player, and UI elements"""
    def __init__(self, manager, player = None, level = 1):
        super().__init__(manager)
        self.level = level

        # Init groups of objects
        self.static = Group()
        self.dynamic = Group()
        self.ui = Group()

        Background(self.static)

        if player is None or player.hero is None:
            HeroFactory.create_hero(self.dynamic)
        else:
            # TODO: create by Player settings
            pass

        # Load level

        #
        self.balance_display = BalanceDisplay()
        self.level_display = LevelDisplay(self.level)
        self.pause_overlay = PauseOverlay()
        self.is_paused = False

    def setup(self) -> None:
        """Initialize the game scene resources"""
        pygame.font.init()
        self.balance_display.setup()
        self.level_display.setup()
        self.pause_overlay.setup()
        self.balance_display.update(self.manager.player_data["balance"])

    def teardown(self) -> None:
        """Clean up scene resources"""
        # Save current balance to manager
        self.manager.player_data["balance"] = self.balance_display.balance

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """Process all events"""
        super().handle_events(events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # Toggle pause state
                    self.is_paused = not self.is_paused

                # Add to balance when + is pressed (for testing)
                elif event.key == pygame.K_EQUALS and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    self.balance_display.update(self.balance_display.balance + 100)

                # Advance level when L is pressed (for testing)
                elif event.key == pygame.K_l:
                    self.level += 1
                    self.level_display.update(self.level)

    def update(self, dt: float) -> None:
        """Update scene state"""
        # Don't update game state when paused
        if self.is_paused:
            return

        # Update UI elements
        super().update(dt)
        self.dynamic.update(dt=dt)


    def draw(self, surface: pygame.Surface) -> None:
        """Draw the scene"""

        self.static.draw(surface)
        self.dynamic.draw(surface)

        # Draw UI elements
        super().draw(surface)
        self.balance_display.draw(surface)
        self.level_display.draw(surface)

        # Draw pause overlay if paused
        if self.is_paused:
            self.pause_overlay.draw(surface)
