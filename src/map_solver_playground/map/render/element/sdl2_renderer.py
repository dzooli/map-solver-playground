"""
SDL2 implementation of the BaseRenderer interface.
"""

import os
from typing import Any, Tuple, List

import sdl2
import sdl2.ext

from map_solver_playground.map.render.element.base_renderer import BaseRenderer
from map_solver_playground.map.render.element.element_renderer_factory import ElementRendererFactory
from map_solver_playground.map.render.renderer_backend import RendererBackend
from map_solver_playground.map.types import MapElement, Terrain, Flag, GeoPath


class SDL2Renderer(BaseRenderer):
    """
    SDL2 implementation of the BaseRenderer interface.
    """

    # Class variable to store the SDL2 renderer instance
    _sdl2_renderer = None

    @staticmethod
    def render(
        screen: sdl2.ext.Renderer,
        element: MapElement,
        image_x: int,
        image_y: int,
        current_view: int = 0,
    ) -> None:
        """
        Render a map element on the screen using SDL2.

        Args:
            screen: The SDL2 renderer to render on
            element: The map element to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
            current_view: The current view index (0 for original, 1 for small map)
        """
        # Delegate to the appropriate renderer for the element type
        if isinstance(element, Terrain):
            terrain_renderer = ElementRendererFactory.get_terrain_renderer(RendererBackend.SDL2)
            terrain_renderer.render(screen, element, image_x, image_y, current_view)
        elif isinstance(element, Flag):
            flag_renderer = ElementRendererFactory.get_flag_renderer(RendererBackend.SDL2)
            flag_renderer.render(screen, element, image_x, image_y, current_view)
        elif isinstance(element, GeoPath):
            geo_path_renderer = ElementRendererFactory.get_geo_path_renderer(RendererBackend.SDL2)
            geo_path_renderer.render(screen, element, image_x, image_y, current_view)
        else:
            raise ValueError(f"No SDL2 renderer found for element type: {type(element).__name__}")

    @staticmethod
    def create_surface(width: int, height: int) -> sdl2.ext.SoftwareSprite:
        """
        Create a new SDL2 surface with the specified dimensions.

        Args:
            width: The width of the surface
            height: The height of the surface

        Returns:
            A new SDL2 surface with the specified dimensions
        """
        return sdl2.ext.SoftwareSprite(sdl2.ext.Surface(width, height), True)

    @staticmethod
    def blit(source, destination: sdl2.ext.Renderer, position: Tuple[int, int]) -> None:
        """
        Blit (copy) a source surface onto a destination surface using SDL2.

        Args:
            source: The source (SDL2 sprite, SDL_Surface, or Texture)
            destination: The destination SDL2 renderer
            position: The position (x, y) to blit the source onto the destination
        """
        # Convert SoftwareSprite to Texture if needed
        from sdl2.ext.renderer import Texture
        import sdl2.surface

        if isinstance(source, sdl2.ext.SoftwareSprite):
            # Create a texture from the sprite's surface
            texture = Texture(destination, source.surface)
            # Copy the texture to the renderer
            destination.copy(texture, dstrect=(position[0], position[1], source.size[0], source.size[1]))
        elif isinstance(source, sdl2.surface.SDL_Surface) or (
            hasattr(source, "__class__") and source.__class__.__name__ == "SDL_Surface"
        ):
            # It's an SDL_Surface directly
            # Create a texture from the surface
            texture = Texture(destination, source)
            # Copy the texture to the renderer
            destination.copy(texture, dstrect=(position[0], position[1], source.w, source.h))
        elif hasattr(source, "contents") and hasattr(source.contents, "w") and hasattr(source.contents, "h"):
            # It's a pointer to an SDL_Surface
            # Create a texture from the surface
            texture = Texture(destination, source)
            # Copy the texture to the renderer
            destination.copy(texture, dstrect=(position[0], position[1], source.contents.w, source.contents.h))
        else:
            # If it's already a texture or something else, try to copy it directly
            try:
                # Try to get the size from the source
                if hasattr(source, "size"):
                    width, height = source.size
                elif hasattr(source, "w") and hasattr(source, "h"):
                    width, height = source.w, source.h
                else:
                    # Default size if we can't determine it
                    width, height = 100, 100

                # Copy the texture to the renderer
                destination.copy(source, dstrect=(position[0], position[1], width, height))
            except Exception as e:
                # If all else fails, just try to copy it without specifying the size
                try:
                    destination.copy(source, dstrect=(position[0], position[1], 100, 100))
                except Exception as e:
                    print(f"Error blitting: {e}")
                    print(f"Source type: {type(source)}")
                    print(f"Source attributes: {dir(source)}")

    @staticmethod
    def draw_lines(
        renderer: sdl2.ext.Renderer,
        color: Tuple[int, int, int],
        closed: bool,
        points: list[Tuple[int, int]],
        width: int = 1,
    ) -> None:
        """
        Draw a series of lines on the surface using SDL2.

        Args:
            renderer: The SDL2 renderer to draw on
            color: The color of the lines (RGB)
            closed: Whether to connect the last point to the first
            points: List of points to connect with lines
            width: The width of the lines
        """
        # Set the draw color
        renderer.color = sdl2.ext.Color(*color)

        # Draw lines between points
        for i in range(len(points) - 1):
            renderer.draw_line(points[i], points[i + 1])

        # If closed, connect the last point to the first
        if closed and len(points) > 1:
            renderer.draw_line(points[-1], points[0])

    @staticmethod
    def get_dimensions(surface: sdl2.ext.SoftwareSprite) -> Tuple[int, int]:
        """
        Get the dimensions of an SDL2 surface.

        Args:
            surface: The SDL2 surface to get dimensions for

        Returns:
            A tuple of (width, height)
        """
        return surface.size

    @staticmethod
    def set_pixel(surface: sdl2.ext.SoftwareSprite, position: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        """
        Set the color of a pixel on an SDL2 surface.

        Args:
            surface: The SDL2 surface to modify
            position: The (x, y) position of the pixel
            color: The color to set (RGB)
        """
        # Convert RGB to SDL2 color format
        sdl_color = sdl2.ext.Color(*color)

        # Get the pixel view of the surface
        view = sdl2.ext.PixelView(surface)

        # Set the pixel color
        view[position[1]][position[0]] = sdl_color.value

    @staticmethod
    def fill_rect(renderer: sdl2.ext.Renderer, rect: Tuple[int, int, int, int], color: Tuple[int, int, int]) -> None:
        """
        Fill a rectangle on the surface with a color using SDL2.

        Args:
            renderer: The SDL2 renderer to draw on
            rect: The rectangle to fill (x, y, width, height)
            color: The color to fill with (RGB)
        """
        renderer.fill(rect, sdl2.ext.Color(*color))

    @staticmethod
    def draw_rect(
        renderer: sdl2.ext.Renderer, rect: Tuple[int, int, int, int], color: Tuple[int, int, int], width: int = 1
    ) -> None:
        """
        Draw a rectangle outline on the surface using SDL2.

        Args:
            renderer: The SDL2 renderer to draw on
            rect: The rectangle to draw (x, y, width, height)
            color: The color to draw with (RGB)
            width: The width of the outline
        """
        # Set the draw color
        renderer.color = sdl2.ext.Color(*color)

        # Draw the rectangle outline
        x, y, w, h = rect

        # Draw the four sides of the rectangle
        renderer.draw_line([(x, y), (x + w, y)])  # Top
        renderer.draw_line([(x, y), (x, y + h)])  # Left
        renderer.draw_line([(x + w, y), (x + w, y + h)])  # Right
        renderer.draw_line([(x, y + h), (x + w, y + h)])  # Bottom

    @staticmethod
    def render_text(
        font: sdl2.ext.FontManager, text: str, color: Tuple[int, int, int], antialias: bool = True
    ) -> sdl2.ext.SoftwareSprite:
        """
        Render text to a surface using SDL2.

        Args:
            font: The SDL2 font manager to use
            text: The text to render
            color: The color of the text (RGB)
            antialias: Whether to use antialiasing (ignored in SDL2)

        Returns:
            An SDL2 surface with the rendered text
        """
        return font.render(text, color=sdl2.ext.Color(*color))

    @staticmethod
    def create_color(r: int, g: int, b: int, a: int = 255) -> sdl2.ext.Color:
        """
        Create a color object using SDL2.

        Args:
            r: The red component (0-255)
            g: The green component (0-255)
            b: The blue component (0-255)
            a: The alpha component (0-255)

        Returns:
            An SDL2 color object
        """
        return sdl2.ext.Color(r, g, b, a)

    @staticmethod
    def clear(renderer: sdl2.ext.Renderer, color: Tuple[int, int, int]) -> None:
        """
        Clear the renderer with a color using SDL2.

        Args:
            renderer: The SDL2 renderer to clear
            color: The color to clear with (RGB)
        """
        renderer.clear(sdl2.ext.Color(*color))

    @staticmethod
    def present(renderer: sdl2.ext.Renderer) -> None:
        """
        Present the renderer to the screen using SDL2.

        Args:
            renderer: The SDL2 renderer to present
        """
        renderer.present()

    @staticmethod
    def create_font(font_path: str = None, size: int = 24) -> sdl2.ext.FontManager:
        """
        Create a font object using SDL2.

        Args:
            font_path: The path to the font file, or None for default font
            size: The size of the font

        Returns:
            An SDL2 font manager object
        """
        # Use default font if font_path is None
        if font_path is None:
            # SDL2 FontManager requires a valid font path, so we use a common system font
            # Try to find a common font that should be available on most Windows systems
            common_fonts = [
                "C:\\Windows\\Fonts\\arial.ttf",
                "C:\\Windows\\Fonts\\segoeui.ttf",
                "C:\\Windows\\Fonts\\tahoma.ttf",
                "C:\\Windows\\Fonts\\verdana.ttf",
            ]

            for font in common_fonts:
                if os.path.exists(font):
                    return sdl2.ext.FontManager(font_path=font, size=size)

            # If none of the common fonts are found, raise an error
            raise FileNotFoundError("Could not find a suitable default font. Please specify a font path.")

        return sdl2.ext.FontManager(font_path=font_path, size=size)

    @staticmethod
    def init() -> None:
        """
        Initialize SDL2.
        """
        sdl2.ext.init()

    @staticmethod
    def quit() -> None:
        """
        Clean up SDL2.
        """
        # Reset the renderer instance
        SDL2Renderer._sdl2_renderer = None
        sdl2.ext.quit()

    @classmethod
    def get_sdl2_renderer(cls) -> sdl2.ext.Renderer:
        """
        Get the SDL2 renderer instance.
        If the renderer is not initialized, initialize it with a temporary window.

        Returns:
            The SDL2 renderer instance
        """
        if cls._sdl2_renderer is None:
            # Initialize SDL2 if not already initialized
            sdl2.ext.init()

            # Create a temporary window and renderer
            window = sdl2.ext.Window("Temporary", size=(1, 1), flags=sdl2.SDL_WINDOW_HIDDEN)
            renderer = sdl2.ext.Renderer(window)

            # Store the renderer instance
            cls._sdl2_renderer = renderer

            # Log that we're using a temporary renderer
            print("Created temporary SDL2 renderer for image loading")

        return cls._sdl2_renderer

    @classmethod
    def create_window(cls, width: int, height: int, title: str) -> Tuple[sdl2.ext.Window, sdl2.ext.Renderer]:
        """
        Create a window and a screen/renderer using SDL2.

        Args:
            width: The width of the window
            height: The height of the window
            title: The title of the window

        Returns:
            A tuple of (window, renderer)
        """
        window = sdl2.ext.Window(title, size=(width, height))
        renderer = sdl2.ext.Renderer(window)
        window.show()

        # Store the renderer instance in the class variable
        cls._sdl2_renderer = renderer

        return window, renderer

    @staticmethod
    def get_events() -> List[sdl2.SDL_Event]:
        """
        Get all pending events using SDL2.

        Returns:
            A list of SDL2 events
        """
        return sdl2.ext.get_events()

    @staticmethod
    def is_quit_event(event: sdl2.SDL_Event) -> bool:
        """
        Check if an event is a quit event using SDL2.

        Args:
            event: The SDL2 event to check

        Returns:
            True if the event is a quit event, False otherwise
        """
        return event.type == sdl2.SDL_QUIT

    @staticmethod
    def is_keydown_event(event: sdl2.SDL_Event) -> bool:
        """
        Check if an event is a key down event using SDL2.

        Args:
            event: The SDL2 event to check

        Returns:
            True if the event is a key down event, False otherwise
        """
        return event.type == sdl2.SDL_KEYDOWN

    @staticmethod
    def get_key_from_event(event: sdl2.SDL_Event) -> int:
        """
        Get the key code from a key event using SDL2.

        Args:
            event: The SDL2 key event

        Returns:
            The key code
        """
        return event.key.keysym.sym

    @staticmethod
    def is_mouse_button_down_event(event: sdl2.SDL_Event) -> bool:
        """
        Check if an event is a mouse button down event using SDL2.

        Args:
            event: The SDL2 event to check

        Returns:
            True if the event is a mouse button down event, False otherwise
        """
        return event.type == sdl2.SDL_MOUSEBUTTONDOWN

    @staticmethod
    def is_left_mouse_button(event: sdl2.SDL_Event) -> bool:
        """
        Check if a mouse button event is for the left mouse button using SDL2.

        Args:
            event: The SDL2 mouse button event

        Returns:
            True if the event is for the left mouse button, False otherwise
        """
        return event.button.button == sdl2.SDL_BUTTON_LEFT

    @staticmethod
    def get_mouse_pos_from_event(event: sdl2.SDL_Event) -> Tuple[int, int]:
        """
        Get the mouse position from a mouse event using SDL2.

        Args:
            event: The SDL2 mouse event

        Returns:
            The (x, y) position of the mouse
        """
        return (event.button.x, event.button.y)

    @staticmethod
    def handle_key_press(key: int) -> str:
        """
        Map a key code to a key name using SDL2.

        Args:
            key: The key code

        Returns:
            The key name
        """
        key_map = {
            sdl2.SDLK_q: "q",
            sdl2.SDLK_n: "n",
            sdl2.SDLK_s: "s",
            sdl2.SDLK_h: "h",
            sdl2.SDLK_v: "v",
            sdl2.SDLK_t: "t",
        }
        return key_map.get(key, "")

    @staticmethod
    def load_image(image_path: str, target_size: Tuple[int, int] = None) -> sdl2.ext.Texture:
        """
        Load an image from a file path using SDL2.

        Args:
            image_path: The path to the image file
            target_size: Optional tuple of (width, height) to resize the image

        Returns:
            An SDL2 texture
        """
        # Import required modules
        import numpy as np
        from PIL import Image

        # Use PIL to load the image
        pil_image = Image.open(image_path)
        if target_size:
            pil_image = pil_image.resize(target_size)

        # Convert to RGBA mode to ensure alpha channel
        if pil_image.mode != "RGBA":
            pil_image = pil_image.convert("RGBA")

        # Convert to numpy array
        image_array = np.array(pil_image)

        # Get the SDL2 renderer instance
        sdl2_renderer = SDL2Renderer.get_sdl2_renderer()

        # Create a texture from the image array
        from map_solver_playground.map.render.sdl2_texture_utils import create_texture_from_array

        texture = create_texture_from_array(image_array, sdl2_renderer)

        return texture

    @staticmethod
    def get_image_width(image) -> int:
        """
        Get the width of an image.

        Args:
            image: The SDL2 texture or surface to get the width for

        Returns:
            The width of the image
        """
        # Handle different types of SDL2 image objects
        if hasattr(image, "size"):
            # It's a texture or sprite with a size attribute
            return image.size[0]
        elif hasattr(image, "w"):
            # It's an SDL_Surface with a w attribute
            return image.w
        elif hasattr(image, "contents") and hasattr(image.contents, "w"):
            # It's a pointer to an SDL_Surface
            return image.contents.w
        else:
            # Try to query the texture
            try:
                info = sdl2.SDL_QueryTexture(image)
                return info.w
            except Exception:
                # If all else fails, return a default value
                print(f"Warning: Could not determine width of image: {type(image)}")
                return 0

    @staticmethod
    def get_image_height(image) -> int:
        """
        Get the height of an image.

        Args:
            image: The SDL2 texture or surface to get the height for

        Returns:
            The height of the image
        """
        # Handle different types of SDL2 image objects
        if hasattr(image, "size"):
            # It's a texture or sprite with a size attribute
            return image.size[1]
        elif hasattr(image, "h"):
            # It's an SDL_Surface with an h attribute
            return image.h
        elif hasattr(image, "contents") and hasattr(image.contents, "h"):
            # It's a pointer to an SDL_Surface
            return image.contents.h
        else:
            # Try to query the texture
            try:
                info = sdl2.SDL_QueryTexture(image)
                return info.h
            except Exception:
                # If all else fails, return a default value
                print(f"Warning: Could not determine height of image: {type(image)}")
                return 0

    @staticmethod
    def scale_image(image, size: Tuple[int, int]):
        """
        Scale an image to the specified size.

        Args:
            image: The SDL2 texture or surface to scale
            size: The target size (width, height)

        Returns:
            The scaled image
        """
        # Import required modules
        import numpy as np
        from PIL import Image

        # Get the SDL2 renderer instance
        sdl2_renderer = SDL2Renderer.get_sdl2_renderer()

        # Convert the image to a PIL Image
        if hasattr(image, "surface"):
            # It's a SoftwareSprite
            # Convert SDL surface to PIL Image
            from map_solver_playground.map.render.sdl2_texture_utils import surface_to_pil_image

            pil_image = surface_to_pil_image(image.surface)
        elif isinstance(image, sdl2.ext.Texture):
            # It's a Texture
            # Convert texture to PIL Image
            from map_solver_playground.map.render.sdl2_texture_utils import texture_to_pil_image

            pil_image = texture_to_pil_image(image, sdl2_renderer)
        else:
            # Try to convert it to a PIL Image
            try:
                from map_solver_playground.map.render.sdl2_texture_utils import texture_to_pil_image

                pil_image = texture_to_pil_image(image, sdl2_renderer)
            except Exception:
                # If all else fails, create a blank image
                print(f"Warning: Could not convert image to PIL Image: {type(image)}")
                pil_image = Image.new("RGBA", size, (0, 0, 0, 0))

        # Resize the PIL Image
        resized_image = pil_image.resize(size)

        # Convert back to SDL2 texture
        image_array = np.array(resized_image)
        from map_solver_playground.map.render.sdl2_texture_utils import create_texture_from_array

        texture = create_texture_from_array(image_array, sdl2_renderer)

        return texture
