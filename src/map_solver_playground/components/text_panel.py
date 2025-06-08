"""
TextPanel component serving as a base class for text-based UI components.
"""

from typing import List

import pygame

from map_solver_playground.components.widget import Widget


class TextPanel(Widget):
    """
    A base UI component for displaying text on the screen.
    This serves as a parent class for InfoPanel, StatusBar, and ToolTipPanel.
    """

    def __init__(
        self,
        screen,
        screen_width,
        screen_height,
        font,
        position=(0, 0),
        size=(100, 100),
        color=None,
    ):
        """
        Initialize the text panel component.

        Args:
            screen: The pygame screen to draw on
            screen_width: The width of the screen
            screen_height: The height of the screen
            font: The font to use for text
            position: The position of the panel (x, y)
            size: The size of the panel (width, height)
        """
        super().__init__(screen, screen_width, screen_height, position, size)
        self.font = font
        self._text: str | List[str] = ""
        self.color = color if color is not None else pygame.color.THECOLORS["white"]

    def set_text(self, text):
        """
        Set the text to display in the info panel.

        Args:
            text: The text to display
        """
        if text is None:
            raise ValueError("Text cannot be None")
        if not isinstance(text, str):
            raise TypeError("Text must be a string")
        self._text = text


    def _draw_background(self):
        """
        Draw the panel background.
        """
        panel_rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        pygame.draw.rect(self.screen, pygame.color.THECOLORS["darkgray"], panel_rect)
        pygame.draw.rect(self.screen, pygame.color.THECOLORS["black"], panel_rect, 1)

    def draw(self):
        """
        Draw the panel on the screen.
        This method should be overridden by subclasses.
        """
        if not self.visible:
            return

        self._draw_background()
