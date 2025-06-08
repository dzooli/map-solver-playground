"""
Pygame implementation of the BaseRenderer interface using the new element renderers.
"""

from typing import Any, Tuple, List

import pygame

from map_solver_playground.map.render.element.base_renderer import BaseRenderer
from map_solver_playground.map.render.element.element_renderer_factory import ElementRendererFactory
from map_solver_playground.map.render.renderer_backend import RendererBackend
from map_solver_playground.map.types import MapElement, Terrain, Flag, GeoPath


class PygameRenderer(BaseRenderer):
    """
    Pygame implementation of the BaseRenderer interface.
    """

    @staticmethod
    def render(
        screen: pygame.Surface,
        element: MapElement,
        image_x: int,
        image_y: int,
        current_view: int = 0,
    ) -> None:
        """
        Render a map element on the screen using Pygame.

        Args:
            screen: The pygame surface to render on
            element: The map element to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
            current_view: The current view index (0 for original, 1 for small map)
        """
        # Delegate to the appropriate renderer for the element type
        if isinstance(element, Terrain):
            terrain_renderer = ElementRendererFactory.get_terrain_renderer(RendererBackend.PYGAME)
            terrain_renderer.render(screen, element, image_x, image_y, current_view)
        elif isinstance(element, Flag):
            flag_renderer = ElementRendererFactory.get_flag_renderer(RendererBackend.PYGAME)
            flag_renderer.render(screen, element, image_x, image_y, current_view)
        elif isinstance(element, GeoPath):
            geo_path_renderer = ElementRendererFactory.get_geo_path_renderer(RendererBackend.PYGAME)
            geo_path_renderer.render(screen, element, image_x, image_y, current_view)
        else:
            raise ValueError(f"No renderer found for element type: {type(element).__name__}")

    @staticmethod
    def create_surface(width: int, height: int) -> pygame.Surface:
        """
        Create a new Pygame surface with the specified dimensions.

        Args:
            width: The width of the surface
            height: The height of the surface

        Returns:
            A new Pygame surface with the specified dimensions
        """
        return pygame.Surface((width, height))

    @staticmethod
    def blit(source: pygame.Surface, destination: pygame.Surface, position: Tuple[int, int]) -> None:
        """
        Blit (copy) a source surface onto a destination surface using Pygame.

        Args:
            source: The source Pygame surface
            destination: The destination Pygame surface
            position: The position (x, y) to blit the source onto the destination
        """
        destination.blit(source, position)

    @staticmethod
    def draw_lines(
        surface: pygame.Surface,
        color: Tuple[int, int, int],
        closed: bool,
        points: list[Tuple[int, int]],
        width: int = 1,
    ) -> None:
        """
        Draw a series of lines on the surface using Pygame.

        Args:
            surface: The Pygame surface to draw on
            color: The color of the lines (RGB)
            closed: Whether to connect the last point to the first
            points: List of points to connect with lines
            width: The width of the lines
        """
        pygame.draw.lines(surface, color, closed, points, width)

    @staticmethod
    def get_dimensions(surface: pygame.Surface) -> Tuple[int, int]:
        """
        Get the dimensions of a Pygame surface.

        Args:
            surface: The Pygame surface to get dimensions for

        Returns:
            A tuple of (width, height)
        """
        return surface.get_width(), surface.get_height()

    @staticmethod
    def set_pixel(surface: pygame.Surface, position: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """
        Set the color of a pixel on a Pygame surface.

        Args:
            surface: The Pygame surface to modify
            position: The (x, y) position of the pixel
            color: The color to set (RGB)
        """
        surface.set_at(position, color)

    @staticmethod
    def fill_rect(surface: pygame.Surface, rect: Tuple[int, int, int, int], color: Tuple[int, int, int]) -> None:
        """
        Fill a rectangle on the surface with a color using Pygame.

        Args:
            surface: The Pygame surface to draw on
            rect: The rectangle to fill (x, y, width, height)
            color: The color to fill with (RGB)
        """
        pygame.draw.rect(surface, color, pygame.Rect(*rect))

    @staticmethod
    def draw_rect(surface: pygame.Surface, rect: Tuple[int, int, int, int], color: Tuple[int, int, int], width: int = 1) -> None:
        """
        Draw a rectangle outline on the surface using Pygame.

        Args:
            surface: The Pygame surface to draw on
            rect: The rectangle to draw (x, y, width, height)
            color: The color to draw with (RGB)
            width: The width of the outline
        """
        pygame.draw.rect(surface, color, pygame.Rect(*rect), width)

    @staticmethod
    def render_text(font: pygame.font.Font, text: str, color: Tuple[int, int, int], antialias: bool = True) -> pygame.Surface:
        """
        Render text to a surface using Pygame.

        Args:
            font: The Pygame font to use
            text: The text to render
            color: The color of the text (RGB)
            antialias: Whether to use antialiasing

        Returns:
            A Pygame surface with the rendered text
        """
        return font.render(text, antialias, color)

    @staticmethod
    def create_color(r: int, g: int, b: int, a: int = 255) -> Tuple[int, int, int, int]:
        """
        Create a color object using Pygame.

        Args:
            r: The red component (0-255)
            g: The green component (0-255)
            b: The blue component (0-255)
            a: The alpha component (0-255)

        Returns:
            A Pygame color tuple (r, g, b, a)
        """
        return (r, g, b, a)

    @staticmethod
    def clear(surface: pygame.Surface, color: Tuple[int, int, int]) -> None:
        """
        Clear the surface with a color using Pygame.

        Args:
            surface: The Pygame surface to clear
            color: The color to clear with (RGB)
        """
        surface.fill(color)

    @staticmethod
    def present(surface: pygame.Surface) -> None:
        """
        Present the surface to the screen using Pygame.

        Args:
            surface: The Pygame surface to present
        """
        pygame.display.flip()

    @staticmethod
    def create_font(font_path: str = None, size: int = 24) -> pygame.font.Font:
        """
        Create a font object using Pygame.

        Args:
            font_path: The path to the font file, or None for default font
            size: The size of the font

        Returns:
            A Pygame font object
        """
        if font_path:
            return pygame.font.Font(font_path, size)
        else:
            return pygame.font.SysFont(None, size)

    @staticmethod
    def init() -> None:
        """
        Initialize Pygame.
        """
        pygame.init()

    @staticmethod
    def quit() -> None:
        """
        Clean up Pygame.
        """
        pygame.quit()

    @staticmethod
    def create_window(width: int, height: int, title: str) -> Tuple[None, pygame.Surface]:
        """
        Create a window and a screen/renderer using Pygame.

        Args:
            width: The width of the window
            height: The height of the window
            title: The title of the window

        Returns:
            A tuple of (None, screen)
        """
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        return None, screen

    @staticmethod
    def get_events() -> List[pygame.event.Event]:
        """
        Get all pending events using Pygame.

        Returns:
            A list of Pygame events
        """
        return pygame.event.get()

    @staticmethod
    def is_quit_event(event: pygame.event.Event) -> bool:
        """
        Check if an event is a quit event using Pygame.

        Args:
            event: The Pygame event to check

        Returns:
            True if the event is a quit event, False otherwise
        """
        return event.type == pygame.QUIT

    @staticmethod
    def is_keydown_event(event: pygame.event.Event) -> bool:
        """
        Check if an event is a key down event using Pygame.

        Args:
            event: The Pygame event to check

        Returns:
            True if the event is a key down event, False otherwise
        """
        return event.type == pygame.KEYDOWN

    @staticmethod
    def get_key_from_event(event: pygame.event.Event) -> int:
        """
        Get the key code from a key event using Pygame.

        Args:
            event: The Pygame key event

        Returns:
            The key code
        """
        return event.key

    @staticmethod
    def is_mouse_button_down_event(event: pygame.event.Event) -> bool:
        """
        Check if an event is a mouse button down event using Pygame.

        Args:
            event: The Pygame event to check

        Returns:
            True if the event is a mouse button down event, False otherwise
        """
        return event.type == pygame.MOUSEBUTTONDOWN

    @staticmethod
    def is_left_mouse_button(event: pygame.event.Event) -> bool:
        """
        Check if a mouse button event is for the left mouse button using Pygame.

        Args:
            event: The Pygame mouse button event

        Returns:
            True if the event is for the left mouse button, False otherwise
        """
        return event.button == 1

    @staticmethod
    def get_mouse_pos_from_event(event: pygame.event.Event) -> Tuple[int, int]:
        """
        Get the mouse position from a mouse event using Pygame.

        Args:
            event: The Pygame mouse event

        Returns:
            The (x, y) position of the mouse
        """
        return event.pos

    @staticmethod
    def handle_key_press(key: int) -> str:
        """
        Map a key code to a key name using Pygame.

        Args:
            key: The key code

        Returns:
            The key name
        """
        key_map = {
            pygame.K_q: "q",
            pygame.K_n: "n",
            pygame.K_s: "s",
            pygame.K_h: "h",
            pygame.K_v: "v",
            pygame.K_t: "t",
        }
        return key_map.get(key, "")

    @staticmethod
    def load_image(image_path: str, target_size: Tuple[int, int] = None) -> pygame.Surface:
        """
        Load an image from a file path using Pygame.

        Args:
            image_path: The path to the image file
            target_size: Optional tuple of (width, height) to resize the image

        Returns:
            A Pygame surface with the loaded image
        """
        # Load the image
        image = pygame.image.load(image_path)

        # Resize if needed
        if target_size:
            image = pygame.transform.scale(image, target_size)

        # Get color of top-left pixel for transparency
        transparent_color = image.get_at((0, 0))

        # Set that color as transparent
        image.set_colorkey(transparent_color)

        return image

    @staticmethod
    def get_image_width(image: pygame.Surface) -> int:
        """
        Get the width of an image.

        Args:
            image: The pygame surface to get the width for

        Returns:
            The width of the image
        """
        return image.get_width()

    @staticmethod
    def get_image_height(image: pygame.Surface) -> int:
        """
        Get the height of an image.

        Args:
            image: The pygame surface to get the height for

        Returns:
            The height of the image
        """
        return image.get_height()

    @staticmethod
    def scale_image(image: pygame.Surface, size: Tuple[int, int]) -> pygame.Surface:
        """
        Scale an image to the specified size.

        Args:
            image: The pygame surface to scale
            size: The target size (width, height)

        Returns:
            The scaled image
        """
        return pygame.transform.scale(image, size)
