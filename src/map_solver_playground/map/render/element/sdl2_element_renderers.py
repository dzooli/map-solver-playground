"""
SDL2 implementations of the element renderer interfaces.
"""

from typing import List, Tuple

import numpy as np
import sdl2
import sdl2.ext
from sdl2.ext.renderer import Texture

from map_solver_playground.map.render.element.element_renderer_interfaces import (
    BaseFlagRenderer,
    BaseGeoPathRenderer,
    BaseTerrainRenderer,
)
from map_solver_playground.map.types import Flag, GeoPath, Terrain
from map_solver_playground.map.render.color_maps import ColorGradient
from map_solver_playground.map.render.sdl2_texture_utils import (
    create_texture_from_array,
    create_grayscale_texture,
    create_colored_texture_from_grayscale,
)


class SDL2TerrainRenderer(BaseTerrainRenderer):
    """
    SDL2 implementation of the terrain renderer interface.
    """

    # Texture cache to store SDL2 textures for terrain objects
    # This avoids storing renderer-specific data on the Terrain objects
    _texture_cache = {}

    @classmethod
    def clear_texture_cache(cls, terrain_id=None) -> None:
        """
        Clear the texture cache for a specific terrain or all terrains.

        Args:
            terrain_id: The ID of the terrain to clear textures for, or None to clear all textures
        """
        if terrain_id is None:
            # Clear all textures
            cls._texture_cache = {}
        elif terrain_id in cls._texture_cache:
            # Clear textures for a specific terrain
            del cls._texture_cache[terrain_id]

    @classmethod
    def render(
        cls,
        renderer: sdl2.ext.Renderer,
        terrain: Terrain,
        image_x: int,
        image_y: int,
        current_view: int = 0,
    ) -> None:
        """
        Render a terrain on the screen using SDL2.

        Args:
            renderer: The SDL2 renderer to render on
            terrain: The terrain to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
            current_view: The current view index (0 for original, 1 for small map)
        """
        # Skip rendering if the terrain is not visible
        if not terrain.visible:
            return

        # Generate a unique ID for this terrain object
        terrain_id = id(terrain)

        # Initialize cache entry for this terrain if it doesn't exist
        if terrain_id not in cls._texture_cache:
            cls._texture_cache[terrain_id] = {
                'map_image': None,
                'small_map_image': None
            }

        # Use the appropriate image based on the current view
        if current_view == 0:
            # Original map view
            if terrain.map_image is None:
                return

            # Convert surface to SDL2 texture if needed
            if cls._texture_cache[terrain_id]['map_image'] is None:
                cls._texture_cache[terrain_id]['map_image'] = cls._surface_to_sdl2_texture(terrain.map_image, renderer)

            # Render the texture
            # Get the dimensions of the image (handle both objects with get_width/get_height and numpy arrays)
            if isinstance(terrain.map_image, np.ndarray):
                # For numpy arrays, use the shape attribute
                if len(terrain.map_image.shape) == 3:
                    height, width, _ = terrain.map_image.shape
                else:
                    height, width = terrain.map_image.shape
            else:
                # For objects with get_width and get_height methods
                width = terrain.map_image.get_width()
                height = terrain.map_image.get_height()

            renderer.copy(
                cls._texture_cache[terrain_id]['map_image'],
                dstrect=(image_x, image_y, width, height),
            )
        else:
            # Small map view
            if terrain.small_map_image is None:
                return

            # Convert surface to SDL2 texture if needed
            if cls._texture_cache[terrain_id]['small_map_image'] is None:
                cls._texture_cache[terrain_id]['small_map_image'] = cls._surface_to_sdl2_texture(
                    terrain.small_map_image, renderer
                )

            # Render the texture
            # Get the dimensions of the image (handle both objects with get_width/get_height and numpy arrays)
            if isinstance(terrain.small_map_image, np.ndarray):
                # For numpy arrays, use the shape attribute
                if len(terrain.small_map_image.shape) == 3:
                    height, width, _ = terrain.small_map_image.shape
                else:
                    height, width = terrain.small_map_image.shape
            else:
                # For objects with get_width and get_height methods
                width = terrain.small_map_image.get_width()
                height = terrain.small_map_image.get_height()

            renderer.copy(
                cls._texture_cache[terrain_id]['small_map_image'],
                dstrect=(image_x, image_y, width, height),
            )

    @staticmethod
    def _surface_to_sdl2_texture(surface, renderer):
        """
        Convert a surface to an SDL2 texture.

        Args:
            surface: The surface to convert (either a numpy array, PIL Image, or a pygame Surface)
            renderer: The SDL2 renderer to create the texture with

        Returns:
            An SDL2 texture
        """
        # Check if the surface is an SDL2TextureWrapper (returned by backend_independent_image_loader)
        if hasattr(surface, 'get_width') and hasattr(surface, 'get_height') and hasattr(surface, 'texture'):
            # Return the texture directly from the wrapper
            return surface.texture

        # Handle case where surface has get_width and get_height but is not an SDL2TextureWrapper
        # This is a fallback for when we have a custom object with dimensions but no texture
        elif hasattr(surface, 'get_width') and hasattr(surface, 'get_height') and not hasattr(surface, 'mode'):
            # Create a default texture with the same dimensions
            width = surface.get_width()
            height = surface.get_height()

            # Create a colored array (green for terrain visibility)
            array = np.zeros((height, width, 4), dtype=np.uint8)
            # Green color with full opacity
            array[:, :, 1] = 200  # Green
            array[:, :, 3] = 255  # Full opacity

            # Create a texture from the array
            return create_texture_from_array(array, renderer)

        # Check if the surface is a numpy array
        elif isinstance(surface, np.ndarray):
            # If it's already a numpy array, use it directly
            array = surface
        else:
            # Check if we're dealing with a PIL Image
            try:
                from PIL import Image

                if isinstance(surface, Image.Image):
                    # Convert PIL Image to numpy array
                    array = np.array(surface)
                else:
                    # Try to get pixel data from the surface
                    # This is a fallback for pygame Surface objects
                    try:
                        # Try to import pygame and convert the surface if it's a pygame Surface
                        import pygame
                        if isinstance(surface, pygame.Surface):
                            array = pygame.surfarray.array3d(surface)
                        else:
                            raise TypeError(f"Unsupported surface type: {type(surface)}")
                    except (ImportError, TypeError) as e:
                        # If pygame is not available or the surface is not a pygame Surface,
                        # raise a more informative error
                        raise TypeError(f"Unsupported surface type: {type(surface)}. Error: {str(e)}")
            except ImportError:
                # If PIL is not available, try the pygame fallback
                try:
                    # Try to import pygame and convert the surface if it's a pygame Surface
                    import pygame
                    if isinstance(surface, pygame.Surface):
                        array = pygame.surfarray.array3d(surface)
                    else:
                        raise TypeError(f"Unsupported surface type: {type(surface)}")
                except (ImportError, TypeError) as e:
                    # If pygame is not available or the surface is not a pygame Surface,
                    # raise a more informative error
                    raise TypeError(f"Unsupported surface type: {type(surface)}. Error: {str(e)}")

        # Use the utility function to create a texture from the array
        # Note: We don't swap axes here to prevent rotation issues
        return create_texture_from_array(array, renderer)

    @staticmethod
    def _normalize_height_data(height_data):
        if height_data.size == 0:
            return None

        min_height = np.min(height_data)
        max_height = np.max(height_data)
        height_range = max_height - min_height

        if height_range == 0:
            return np.zeros_like(height_data)

        return (height_data - min_height) / height_range

    @staticmethod
    def _create_terrain_surface(map_data, renderer):
        # Create an SDL2 texture
        texture = renderer.create_texture(
            sdl2.SDL_PIXELFORMAT_RGBA8888, sdl2.SDL_TEXTUREACCESS_TARGET, map_data.width, map_data.height
        )

        # Set the texture as the render target
        renderer.target = texture

        # Clear the texture
        renderer.clear()

        height_data = map_data.data
        normalized_data = SDL2TerrainRenderer._normalize_height_data(height_data)
        if normalized_data is None:
            # Reset render target
            renderer.target = None
            return texture

        color_gradient = ColorGradient.TOPO_COLORS
        max_color_index = len(color_gradient) - 1

        # Draw each pixel
        for y in range(map_data.height):
            for x in range(map_data.width):
                if y < normalized_data.shape[0] and x < normalized_data.shape[1]:
                    color_index = int(normalized_data[y, x] * max_color_index)
                    color = color_gradient[color_index]
                    renderer.color = sdl2.ext.Color(*color)
                    renderer.draw_point((x, y))

        # Reset render target
        renderer.target = None

        return texture


class SDL2FlagRenderer(BaseFlagRenderer):
    """
    SDL2 implementation of the flag renderer interface.
    """

    @classmethod
    def clear_texture_cache(cls, flag_id=None) -> None:
        """
        Clear the texture cache for a specific flag or all flags.

        Args:
            flag_id: The ID of the flag to clear textures for, or None to clear all textures
        """
        # This renderer doesn't maintain a cache, but it does store textures on Flag objects
        # Since we don't have direct access to all Flag objects, this method is a no-op
        # The textures will be regenerated when the render method is called again
        pass

    @staticmethod
    def render(
        renderer: sdl2.ext.Renderer,
        flag: Flag,
        image_x: int,
        image_y: int,
        current_view: int = 0,
    ) -> None:
        """
        Render a flag on the screen using SDL2.

        Args:
            renderer: The SDL2 renderer to render on
            flag: The flag to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
            current_view: The current view index (0 for original, 1 for small map)
        """
        # Skip rendering if the flag is not visible or has no position or image
        if not flag.visible or flag.position is None or flag.image is None:
            return

        # Convert surface to SDL2 texture if needed
        if not hasattr(flag, "sdl2_image") or flag.sdl2_image is None:
            flag.sdl2_image = SDL2FlagRenderer._flag_surface_to_sdl2_texture(flag.image, renderer)

        # Calculate screen position for the flag
        screen_pos = SDL2FlagRenderer.screen_to_map_pos(
            flag.position, flag.image.get_width(), flag.image.get_height(), image_x, image_y
        )

        # Render the flag on the screen
        renderer.copy(
            flag.sdl2_image, dstrect=(screen_pos[0], screen_pos[1], flag.image.get_width(), flag.image.get_height())
        )

    @staticmethod
    def _flag_surface_to_sdl2_texture(surface, renderer):
        """
        Convert a surface to an SDL2 texture specifically for flag images.
        This method handles the conversion differently to prevent the 90-degree rotation issue.

        Args:
            surface: The surface to convert (either a numpy array, PIL Image, or a pygame Surface)
            renderer: The SDL2 renderer to create the texture with

        Returns:
            An SDL2 texture
        """
        # Check if the surface is an SDL2TextureWrapper (returned by backend_independent_image_loader)
        if hasattr(surface, 'get_width') and hasattr(surface, 'get_height') and hasattr(surface, 'texture'):
            # Return the texture directly from the wrapper
            return surface.texture

        # Handle case where surface has get_width and get_height but is not an SDL2TextureWrapper
        # This is a fallback for when we have a custom object with dimensions but no texture
        elif hasattr(surface, 'get_width') and hasattr(surface, 'get_height') and not hasattr(surface, 'mode'):
            # Create a default texture with the same dimensions
            width = surface.get_width()
            height = surface.get_height()

            # Create a colored array (blue for flag visibility)
            array = np.zeros((height, width, 4), dtype=np.uint8)
            # Blue color with full opacity
            array[:, :, 2] = 200  # Blue
            array[:, :, 3] = 255  # Full opacity

            # Create a texture from the array
            return create_texture_from_array(array, renderer)

        # Check if the surface is a numpy array
        elif isinstance(surface, np.ndarray):
            # If it's already a numpy array, use it directly
            array = surface
        else:
            # Check if we're dealing with a PIL Image
            try:
                from PIL import Image

                if isinstance(surface, Image.Image):
                    # Convert PIL Image to numpy array
                    array = np.array(surface)
                else:
                    # Try to get pixel data from the surface
                    # This is a fallback for pygame Surface objects
                    try:
                        # Try to import pygame and convert the surface if it's a pygame Surface
                        import pygame
                        if isinstance(surface, pygame.Surface):
                            array = pygame.surfarray.array3d(surface)
                        else:
                            raise TypeError(f"Unsupported surface type: {type(surface)}")
                    except (ImportError, TypeError) as e:
                        # If pygame is not available or the surface is not a pygame Surface,
                        # raise a more informative error
                        raise TypeError(f"Unsupported surface type: {type(surface)}. Error: {str(e)}")
            except ImportError:
                # If PIL is not available, try the pygame fallback
                try:
                    # Try to import pygame and convert the surface if it's a pygame Surface
                    import pygame
                    if isinstance(surface, pygame.Surface):
                        array = pygame.surfarray.array3d(surface)
                    else:
                        raise TypeError(f"Unsupported surface type: {type(surface)}")
                except (ImportError, TypeError) as e:
                    # If pygame is not available or the surface is not a pygame Surface,
                    # raise a more informative error
                    raise TypeError(f"Unsupported surface type: {type(surface)}. Error: {str(e)}")

        # Use the utility function to create a texture from the array
        # Note: We don't swap axes here to prevent rotation
        return create_texture_from_array(array, renderer)

    @staticmethod
    def screen_to_map_pos(
        rel_pos: Tuple[int, int],
        sprite_width: int,
        sprite_height: int,
        image_x: int,
        image_y: int,
    ) -> Tuple[int, int]:
        """
        Convert relative map position to screen position for sprite placement.

        Args:
            rel_pos: The (x, y) position relative to the map's upper left corner
            sprite_width: The width of the sprite
            sprite_height: The height of the sprite
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner

        Returns:
            tuple: The (x, y) screen position for the sprite
        """
        screen_x = image_x + rel_pos[0] - sprite_width // 2
        screen_y = image_y + rel_pos[1] - sprite_height // 2
        return screen_x, screen_y


class SDL2GeoPathRenderer(BaseGeoPathRenderer):
    """
    SDL2 implementation of the geo path renderer interface.
    """

    @classmethod
    def clear_texture_cache(cls, path_id=None) -> None:
        """
        Clear the texture cache for a specific geo path or all geo paths.

        Args:
            path_id: The ID of the geo path to clear textures for, or None to clear all textures
        """
        # This renderer doesn't use any textures or maintain a cache
        # It directly draws lines on the screen using the renderer.draw_line method
        pass

    @staticmethod
    def render(
        renderer: sdl2.ext.Renderer,
        geo_path: GeoPath,
        image_x: int,
        image_y: int,
        current_view: int = 0,
    ) -> None:
        """
        Render a geo path on the screen using SDL2.

        Args:
            renderer: The SDL2 renderer to render on
            geo_path: The geo path to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
            current_view: The current view index (0 for original, 1 for small map)
        """
        # Skip rendering if the path is not visible or has no points
        if not geo_path.visible or geo_path.is_empty():
            return

        # Convert path coordinates to screen coordinates
        screen_points = SDL2GeoPathRenderer.path_to_screen_points(geo_path.path_points, image_x, image_y)

        # Set the draw color
        renderer.color = sdl2.ext.Color(*geo_path.color)

        # Draw the path as connected lines
        for i in range(len(screen_points) - 1):
            renderer.draw_line([screen_points[i], screen_points[i + 1]])

    @staticmethod
    def path_to_screen_points(
        path_points: list[Tuple[int, int]],
        image_x: int,
        image_y: int,
    ) -> list[Tuple[int, int]]:
        """
        Convert path points to screen coordinates.

        Args:
            path_points: List of (x, y) points relative to the map
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner

        Returns:
            List[Tuple[int, int]]: List of (x, y) points in screen coordinates
        """
        screen_points = []
        for point in path_points:
            screen_x = image_x + point[0]
            screen_y = image_y + point[1]
            screen_points.append((screen_x, screen_y))
        return screen_points
