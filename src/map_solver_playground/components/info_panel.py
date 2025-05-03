"""
InfoPanel component for displaying information in the application.
"""

from map_solver_playground.components.text_panel import TextPanel


class InfoPanel(TextPanel):
    """
    A UI component that displays information about the current map view.
    """

    def __init__(self, screen, width, height, font, position=(10, 10), size=(650, 30), color=None):
        """
        Initialize the info panel component.

        Args:
            screen: The pygame screen to draw on
            width: The width of the screen
            height: The height of the screen
            font: The font to use for text
            position: The position of the panel (x, y)
            size: The size of the panel (width, height)
        """
        super().__init__(screen, width, height, font, position, size, color)
        self.text = ""

    def draw(self):
        """
        Draw the info panel on the screen.
        """
        if not self.visible:
            return

        self._draw_background()

        # Draw the text
        if self.text and isinstance(self.text, str):
            text_surface = self.font.render(self.text, True, self.color)
            text_rect = text_surface.get_rect(topleft=(self.position[0] + 10, self.position[1] + 10))
            self.screen.blit(text_surface, text_rect)
