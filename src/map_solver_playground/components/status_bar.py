"""
StatusBar component for displaying status messages in the application.
"""

from map_solver_playground.components.text_panel import TextPanel


class StatusBar(TextPanel):
    """
    A UI component that displays status messages at the bottom of the screen.
    """

    def __init__(
        self,
        screen,
        width,
        height,
        font,
        position=None,
        size=None,
        color=None,
    ):
        """
        Initialize the status bar component.

        Args:
            screen: The pygame screen to draw on
            width: The width of the screen
            height: The height of the screen
            font: The font to use for text
            position: The position of the status bar (x, y), defaults to bottom of screen
            size: The size of the status bar (width, height), defaults to screen width x 30
        """
        # Default position at the bottom of the screen
        position = position if position else (0, height - 30)
        # Default size is full width and 30 pixels high
        size = size if size else (width, 30)

        super().__init__(screen, width, height, font, position, size, color)

    def draw(self):
        """
        Draw the status bar on the screen.
        """
        if not self.visible:
            return

        self._draw_background()

        if not self._text or not isinstance(self._text, str):
            return

        # Draw the text
        text_surface = self.font.render(self._text, True, self.color)
        text_rect = text_surface.get_rect(midleft=(self.position[0] + 10, self.position[1] + self.size[1] // 2))
        self.screen.blit(text_surface, text_rect)
