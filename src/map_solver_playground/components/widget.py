"""
Widget component serving as a base class for all UI components.
"""

import pygame


class Widget:
    """
    A base UI component for all widgets in the application.
    This serves as a parent class for TextPanel, MapView, and other UI components.
    """

    def __init__(
        self,
        screen,
        screen_width,
        screen_height,
        position=(0, 0),
        size=(100, 100),
    ):
        """
        Initialize the widget component.

        Args:
            screen: The pygame screen to draw on
            screen_width: The width of the screen
            screen_height: The height of the screen
            position: The position of the widget (x, y)
            size: The size of the widget (width, height)
        """
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.position = position
        self.size = size
        self.visible = True

    def toggle_visibility(self):
        """
        Toggle the visibility of the widget.
        """
        self.visible = not self.visible

    def draw(self):
        """
        Draw the widget on the screen.
        This method should be overridden by subclasses.
        """
        if not self.visible:
            return
