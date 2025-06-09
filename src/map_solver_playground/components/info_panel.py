"""
InfoPanel component for displaying information in the application.
"""

from map_solver_playground.components.text_panel import TextPanel


class InfoPanel(TextPanel):
    """
    A UI component that displays information about the current map view.
    """

    def __init__(self, renderer, screen_width, screen_height, font, position=(10, 10), size=(880, 30), color=None):
        """
        Initialize the info panel component.

        Args:
            renderer: The renderer to use for drawing
            screen_width: The width of the screen
            screen_height: The height of the screen
            font: The font to use for text
            position: The position of the panel (x, y)
            size: The size of the panel (width, height)
            color: The color to use for text
        """
        super().__init__(renderer, screen_width, screen_height, font, position, size, color)

    def draw(self):
        """
        Draw the info panel on the screen.
        """
        if not self.visible or not self._text or not isinstance(self._text, str):
            return

        self._draw_background()

        # Use the renderer's static methods for text rendering
        from map_solver_playground.map.render.element.renderer_factory import RendererFactory

        renderer_class = RendererFactory.get_current_renderer()

        # Draw the text
        text_surface = renderer_class.render_text(self.font, self._text, self.color)
        text_pos = (self.position[0] + 10, self.position[1] + 10)

        # Use the renderer class's blit method instead of the renderer's blit method
        renderer_class.blit(text_surface, self.renderer, text_pos)
