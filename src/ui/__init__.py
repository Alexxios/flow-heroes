import abc
from typing import Tuple, Callable, Optional

import pygame

class UIElement(abc.ABC):
    """Base class for all UI elements"""
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.is_hovered = False

    @abc.abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass

    @abc.abstractmethod
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Returns True if the event was handled by this element"""
        pass

    def update(self, dt: float) -> None:
        """Update the element state. Default implementation does nothing."""
        pass

    def check_hover(self, mouse_pos: Tuple[int, int]) -> bool:
        """Check if mouse is hovering over the element"""
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return was_hovered != self.is_hovered  # Return True if hover state changed


class Button(UIElement):
    """Interactive button with text and icon"""
    def __init__(self, x: int, y: int, width: int, height: int,
                 text: str, callback: Callable[[], None],
                 font: pygame.font.Font, icon: Optional[pygame.Surface] = None,
                 bg_color: Tuple[int, int, int] = (50, 50, 50),
                 hover_color: Tuple[int, int, int] = (70, 70, 70),
                 text_color: Tuple[int, int, int] = (255, 255, 255)):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = font
        self.icon = icon
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.text_surface = self.font.render(text, True, text_color)

    def draw(self, surface: pygame.Surface) -> None:
        # Draw button background
        pygame.draw.rect(surface,
                         self.hover_color if self.is_hovered else self.bg_color,
                         self.rect,
                         border_radius=10)

        # Draw button border
        pygame.draw.rect(surface,
                         (100, 100, 100),
                         self.rect,
                         width=2,
                         border_radius=10)

        # Calculate positions for text and icon
        if self.icon:
            # If there's an icon, position it to the left of the text
            icon_rect = self.icon.get_rect(
                centery=self.rect.centery,
                left=self.rect.left + 20
            )
            text_rect = self.text_surface.get_rect(
                centery=self.rect.centery,
                left=icon_rect.right + 10
            )
            surface.blit(self.icon, icon_rect)
            surface.blit(self.text_surface, text_rect)
        else:
            # If no icon, just center the text
            text_rect = self.text_surface.get_rect(center=self.rect.center)
            surface.blit(self.text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()
                return True
        return False


class BalanceBar(UIElement):
    """UI element displaying player's balance"""
    def __init__(self, x: int, y: int, width: int, height: int,
                 font: pygame.font.Font,
                 coin_icon: pygame.Surface,
                 balance: int = 0,
                 bg_color: Tuple[int, int, int] = (30, 30, 30),
                 text_color: Tuple[int, int, int] = (255, 215, 0)):
        super().__init__(x, y, width, height)
        self.font = font
        self.coin_icon = coin_icon
        self.balance = balance
        self.bg_color = bg_color
        self.text_color = text_color
        self.update_text()

    def update_text(self) -> None:
        """Update the text surface with current balance"""
        self.text_surface = self.font.render(f"{self.balance}", True, self.text_color)

    def set_balance(self, balance: int) -> None:
        """Set a new balance value"""
        self.balance = balance
        self.update_text()

    def draw(self, surface: pygame.Surface) -> None:
        # Draw background
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, width=2, border_radius=8)

        # Draw coin icon
        icon_rect = self.coin_icon.get_rect(
            centery=self.rect.centery,
            left=self.rect.left + 10
        )
        surface.blit(self.coin_icon, icon_rect)

        # Draw balance text
        text_rect = self.text_surface.get_rect(
            centery=self.rect.centery,
            left=icon_rect.right + 10
        )
        surface.blit(self.text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        # Balance bar is non-interactive
        return False
