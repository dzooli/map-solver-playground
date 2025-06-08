"""
ToolTipPanel component for displaying tooltips and instructions in the application.
"""

from typing import List

from map_solver_playground.components.text_panel import TextPanel


class ToolTipPanel(TextPanel):
    """
    A UI component that displays tooltips and instructions.
    """

    def __init__(
        self,
        screen,
        screen_width,
        screen_height,
        font,
        position=(10, 710),
        size=(880, 155),
        color=None,
    ):
        """
        Initialize the tooltip panel component.

        Args:
            screen: The pygame screen to draw on
            screen_width: The width of the screen
            screen_height: The height of the screen
            font: The font to use for text
            position: The position of the panel (x, y)
            size: The size of the panel (width, height)
        """
        self._text = None
        super().__init__(screen, screen_width, screen_height, font, position, size, color)

    def set_text(self, text: str | List[str]):
        """
        Set the text content of the tooltip panel.

        Args:
            text: Either a string that will be split by newlines,
                  or a list of strings where each item is a tooltip line

        Raises:
            ValueError: If text is None
            TypeError: If text is neither a string nor a list of strings
        """
        if text is None:
            raise ValueError("Text cannot be None")

        if isinstance(text, str):
            self._text = text
        elif isinstance(text, list):
            if not all(isinstance(item, str) for item in text):
                raise TypeError("All items in the list must be strings")
            self._text = "\n".join(text)
        else:
            raise TypeError("Text must be either a string or a list of strings")

    def draw(self):
        """
        Draw the tooltip panel on the screen.
        """
        if not self.visible or not isinstance(self._text, str):
            return

        self._draw_background()

        # Draw the tooltips
        y_offset = 10
        for tooltip in self._text.split("\n"):
            text_surface = self.font.render(tooltip, True, self.color)
            text_rect = text_surface.get_rect(topleft=(self.position[0] + 10, self.position[1] + y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 20
