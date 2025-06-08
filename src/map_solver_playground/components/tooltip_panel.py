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
        renderer,
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
            renderer: The renderer to use for drawing
            screen_width: The width of the screen
            screen_height: The height of the screen
            font: The font to use for text
            position: The position of the panel (x, y)
            size: The size of the panel (width, height)
            color: The color to use for text
        """
        self._text = None
        super().__init__(renderer, screen_width, screen_height, font, position, size, color)

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

        # Use the renderer's static methods for text rendering
        from map_solver_playground.map.render.element.renderer_factory import RendererFactory
        renderer_class = RendererFactory.get_current_renderer()

        # Draw the tooltips
        y_offset = 10
        for tooltip in self._text.split("\n"):
            text_surface = renderer_class.render_text(self.font, tooltip, self.color)
            text_pos = (self.position[0] + 10, self.position[1] + y_offset)
            # Use the renderer class's blit method instead of the renderer's blit method
            renderer_class.blit(text_surface, self.renderer, text_pos)
            y_offset += 20
