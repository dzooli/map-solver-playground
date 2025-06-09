"""
Widget component serving as a base class for all UI components.
"""

from abc import ABC, abstractmethod
from typing import Any, Tuple


class Widget(ABC):
    """
    A base UI component for all widgets in the application.
    This serves as a parent class for TextPanel, MapView, and other UI components.
    """

    def __init__(
        self,
        renderer,
        screen_width,
        screen_height,
        position=(0, 0),
        size=(100, 100),
    ):
        """
        Initialize the widget component.

        Args:
            renderer: The renderer to use for drawing
            screen_width: The width of the screen
            screen_height: The height of the screen
            position: The position of the widget (x, y)
            size: The size of the widget (width, height)
        """
        self.renderer = renderer
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

    @abstractmethod
    def draw(self):
        """
        Draw the widget on the screen.
        This method must be implemented by subclasses.
        """
        pass
