"""
TextPanel component serving as a base class for text-based UI components.
"""

from typing import List

import pygame


class TextPanel:
    """
    A base UI component for displaying text on the screen.
    This serves as a parent class for InfoPanel, StatusBar, and ToolTipPanel.
    """

    def __init__(
        self,
        screen,
        width,
        height,
        font,
        position=(0, 0),
        size=(100, 100),
        color=None,
    ):
        """
        Initialize the text panel component.

        Args:
            screen: The pygame screen to draw on
            width: The width of the screen
            height: The height of the screen
            font: The font to use for text
            position: The position of the panel (x, y)
            size: The size of the panel (width, height)
        """
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        self.position = position
        self.size = size
        self.visible = True
        self.text: str | List[str] = ""
        self.color = color if color is not None else pygame.color.THECOLORS["white"]

    def set_text(self, text):
        """
        Set the text to display in the info panel.

        Args:
            text: The text to display
        """
        self.text = text

    def toggle_visibility(self):
        """
        Toggle the visibility of the panel.
        """
        self.visible = not self.visible

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
