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
        renderer,
        screen_width,
        screen_height,
        font,
        position=None,
        size=None,
        color=None,
    ):
        """
        Initialize the status bar component.

        Args:
            renderer: The renderer to use for drawing
            screen_width: The width of the screen
            screen_height: The height of the screen
            font: The font to use for text
            position: The position of the status bar (x, y), defaults to bottom of screen
            size: The size of the status bar (width, height), defaults to screen width x 30
            color: The color to use for text
        """
        # Default position at the bottom of the screen
        position = position or (0, screen_height - 30)
        # Default size is full width and 30 pixels high
        size = size or (screen_width, 30)

        super().__init__(renderer, screen_width, screen_height, font, position, size, color)

    def draw(self):
        """
        Draw the status bar on the screen.
        """
        if not self.visible:
            return

        self._draw_background()

        if not self._text or not isinstance(self._text, str):
            return

        # Use the renderer's static methods for text rendering
        from map_solver_playground.map.render.element.renderer_factory import RendererFactory
        renderer_class = RendererFactory.get_current_renderer()

        # Draw the text
        text_surface = renderer_class.render_text(self.font, self._text, self.color)
        text_pos = (self.position[0] + 10, self.position[1] + self.size[1] // 2 - 10)  # Approximate midleft
        # Use the renderer class's blit method instead of the renderer's blit method
        renderer_class.blit(text_surface, self.renderer, text_pos)
