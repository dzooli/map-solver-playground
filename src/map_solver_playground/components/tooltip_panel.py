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
        width,
        height,
        font,
        position=(10, 710),
        size=(880, 155),
        color=None,
    ):
        """
        Initialize the tooltip panel component.

        Args:
            screen: The pygame screen to draw on
            width: The width of the screen
            height: The height of the screen
            font: The font to use for text
            position: The position of the panel (x, y)
            size: The size of the panel (width, height)
        """
        super().__init__(screen, width, height, font, position, size, color)

        # Default tooltips
        self._tooltips = [
            "LMB to place a flag",
            "Press 'N' to generate a new map",
            "Press 'V' to view the small map",
            "Press 'S' solve the map",
            "Press 'H' to toggle path visibility",
            'Press "T" to toggle the tooltips',
            "Press 'ESC' to exit",
        ]

    @property
    def tooltips(self):
        return self._tooltips

    @tooltips.setter
    def tooltips(self, tooltips: List[str]):
        """
        Set new tooltips for the panel.
        Args:
            tooltips: List of strings containing the new tooltips
        """
        if tooltips is None:
            raise ValueError("Tooltips cannot be None")
        if not isinstance(tooltips, list):
            raise TypeError("Tooltips must be a list of strings")
        self._tooltips = tooltips

    def set_text(self, text):
        raise ValueError("Text cannot be set. Use tooltips instead.")

    def draw(self):
        """
        Draw the tooltip panel on the screen.
        """
        if not self.visible:
            return

        self._draw_background()

        # Draw the tooltips
        y_offset = 10
        for tooltip in self._tooltips:
            text_surface = self.font.render(tooltip, True, self.color)
            text_rect = text_surface.get_rect(topleft=(self.position[0] + 10, self.position[1] + y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 20
