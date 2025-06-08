"""
Base renderer interface for map elements.
"""

from abc import ABC, abstractmethod
from typing import Any, Tuple, Union, List

from map_solver_playground.map.types.map_element import MapElement


class BaseRenderer(ABC):
    """
    Abstract base class for all renderers.
    This class defines the interface that all renderers must implement.
    """

    @staticmethod
    @abstractmethod
    def render(
        screen: Any,
        element: MapElement,
        image_x: int,
        image_y: int,
        current_view: int = 0,
    ) -> None:
        """
        Render a map element on the screen.

        Args:
            screen: The surface to render on (implementation-specific)
            element: The map element to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
            current_view: The current view index (0 for original, 1 for small map)
        """
        pass

    @staticmethod
    @abstractmethod
    def create_surface(width: int, height: int) -> Any:
        """
        Create a new surface with the specified dimensions.

        Args:
            width: The width of the surface
            height: The height of the surface

        Returns:
            A new surface with the specified dimensions
        """
        pass

    @staticmethod
    @abstractmethod
    def blit(source: Any, destination: Any, position: Tuple[int, int]) -> None:
        """
        Blit (copy) a source surface onto a destination surface.

        Args:
            source: The source surface
            destination: The destination surface
            position: The position (x, y) to blit the source onto the destination
        """
        pass

    @staticmethod
    @abstractmethod
    def draw_lines(
        surface: Any,
        color: Tuple[int, int, int],
        closed: bool,
        points: list[Tuple[int, int]],
        width: int = 1,
    ) -> None:
        """
        Draw a series of lines on the surface.

        Args:
            surface: The surface to draw on
            color: The color of the lines (RGB)
            closed: Whether to connect the last point to the first
            points: List of points to connect with lines
            width: The width of the lines
        """
        pass

    @staticmethod
    @abstractmethod
    def get_dimensions(surface: Any) -> Tuple[int, int]:
        """
        Get the dimensions of a surface.

        Args:
            surface: The surface to get dimensions for

        Returns:
            A tuple of (width, height)
        """
        pass

    @staticmethod
    @abstractmethod
    def set_pixel(surface: Any, position: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """
        Set the color of a pixel on a surface.

        Args:
            surface: The surface to modify
            position: The (x, y) position of the pixel
            color: The color to set (RGB)
        """
        pass

    @staticmethod
    @abstractmethod
    def fill_rect(surface: Any, rect: Tuple[int, int, int, int], color: Tuple[int, int, int]) -> None:
        """
        Fill a rectangle on the surface with a color.

        Args:
            surface: The surface to draw on
            rect: The rectangle to fill (x, y, width, height)
            color: The color to fill with (RGB)
        """
        pass

    @staticmethod
    @abstractmethod
    def draw_rect(surface: Any, rect: Tuple[int, int, int, int], color: Tuple[int, int, int], width: int = 1) -> None:
        """
        Draw a rectangle outline on the surface.

        Args:
            surface: The surface to draw on
            rect: The rectangle to draw (x, y, width, height)
            color: The color to draw with (RGB)
            width: The width of the outline
        """
        pass

    @staticmethod
    @abstractmethod
    def render_text(font: Any, text: str, color: Tuple[int, int, int], antialias: bool = True) -> Any:
        """
        Render text to a surface.

        Args:
            font: The font to use
            text: The text to render
            color: The color of the text (RGB)
            antialias: Whether to use antialiasing

        Returns:
            A surface with the rendered text
        """
        pass

    @staticmethod
    @abstractmethod
    def create_color(r: int, g: int, b: int, a: int = 255) -> Any:
        """
        Create a color object.

        Args:
            r: The red component (0-255)
            g: The green component (0-255)
            b: The blue component (0-255)
            a: The alpha component (0-255)

        Returns:
            A color object
        """
        pass

    @staticmethod
    @abstractmethod
    def clear(surface: Any, color: Tuple[int, int, int]) -> None:
        """
        Clear the surface with a color.

        Args:
            surface: The surface to clear
            color: The color to clear with (RGB)
        """
        pass

    @staticmethod
    @abstractmethod
    def present(surface: Any) -> None:
        """
        Present the surface to the screen.

        Args:
            surface: The surface to present
        """
        pass

    @staticmethod
    @abstractmethod
    def create_font(font_path: str = None, size: int = 24) -> Any:
        """
        Create a font object.

        Args:
            font_path: The path to the font file, or None for default font
            size: The size of the font

        Returns:
            A font object
        """
        pass

    @staticmethod
    @abstractmethod
    def init() -> None:
        """
        Initialize the renderer.
        """
        pass

    @staticmethod
    @abstractmethod
    def quit() -> None:
        """
        Clean up the renderer.
        """
        pass

    @staticmethod
    @abstractmethod
    def create_window(width: int, height: int, title: str) -> Tuple[Any, Any]:
        """
        Create a window and a screen/renderer.

        Args:
            width: The width of the window
            height: The height of the window
            title: The title of the window

        Returns:
            A tuple of (window, screen/renderer)
        """
        pass

    @staticmethod
    @abstractmethod
    def get_events() -> List[Any]:
        """
        Get all pending events.

        Returns:
            A list of events
        """
        pass

    @staticmethod
    @abstractmethod
    def is_quit_event(event: Any) -> bool:
        """
        Check if an event is a quit event.

        Args:
            event: The event to check

        Returns:
            True if the event is a quit event, False otherwise
        """
        pass

    @staticmethod
    @abstractmethod
    def is_keydown_event(event: Any) -> bool:
        """
        Check if an event is a key down event.

        Args:
            event: The event to check

        Returns:
            True if the event is a key down event, False otherwise
        """
        pass

    @staticmethod
    @abstractmethod
    def get_key_from_event(event: Any) -> int:
        """
        Get the key code from a key event.

        Args:
            event: The key event

        Returns:
            The key code
        """
        pass

    @staticmethod
    @abstractmethod
    def is_mouse_button_down_event(event: Any) -> bool:
        """
        Check if an event is a mouse button down event.

        Args:
            event: The event to check

        Returns:
            True if the event is a mouse button down event, False otherwise
        """
        pass

    @staticmethod
    @abstractmethod
    def is_left_mouse_button(event: Any) -> bool:
        """
        Check if a mouse button event is for the left mouse button.

        Args:
            event: The mouse button event

        Returns:
            True if the event is for the left mouse button, False otherwise
        """
        pass

    @staticmethod
    @abstractmethod
    def get_mouse_pos_from_event(event: Any) -> Tuple[int, int]:
        """
        Get the mouse position from a mouse event.

        Args:
            event: The mouse event

        Returns:
            The (x, y) position of the mouse
        """
        pass

    @staticmethod
    @abstractmethod
    def handle_key_press(key: int) -> str:
        """
        Map a key code to a key name.

        Args:
            key: The key code

        Returns:
            The key name
        """
        pass
