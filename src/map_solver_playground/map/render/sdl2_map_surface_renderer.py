"""
SDL2 implementation of the BaseMapSurfaceRenderer interface.
"""

import numpy as np
import sdl2
import sdl2.ext

from map_solver_playground.map.map_data import Map
from map_solver_playground.map.render.color_maps import TerrainColorGradient
from map_solver_playground.map.render.map_surface_renderer_interfaces import BaseMapSurfaceRenderer
from map_solver_playground.map.render.sdl2_texture_utils import (
    create_texture_from_array,
    create_grayscale_texture,
    create_colored_texture_from_grayscale,
)


class SDL2MapSurfaceRenderer(BaseMapSurfaceRenderer):
    """
    SDL2 implementation of the BaseMapSurfaceRenderer interface.

    This class provides methods for converting map data to SDL2 textures
    and applying visual effects.
    """

    @staticmethod
    def to_surface(map_obj: Map) -> np.ndarray:
        """
        Convert a map to a numpy array suitable for creating an SDL2 texture.

        Args:
            map_obj: The map to convert

        Returns:
            np.ndarray: A numpy array representing the map data
        """
        # Convert height values to grayscale (0-255) using numpy operations
        # Clip values to ensure they're in the 0-1 range
        normalized_data = np.clip(map_obj.data, 0.0, 1.0)
        grayscale_data = (normalized_data * 255).astype(np.uint8)

        return grayscale_data

    @staticmethod
    def color_map(grayscale_array: np.ndarray, color_map_array: TerrainColorGradient) -> np.ndarray:
        """
        Map grayscale values in a numpy array to colors in a color map.

        Args:
            grayscale_array: The grayscale numpy array
            color_map_array: A list of RGB tuples representing the color map

        Returns:
            np.ndarray: A new numpy array with mapped colors
        """
        # Convert color_map_array to a numpy array for faster indexing
        color_map_np = np.array(color_map_array, dtype=np.uint8)

        # Normalize the grayscale values to the range [0, 1] if needed
        if grayscale_array.dtype != np.float32 and grayscale_array.dtype != np.float64:
            normalized = grayscale_array.astype(np.float32) / 255.0
        else:
            normalized = grayscale_array

        # Map the normalized values to indices in the color map
        # Scale to the range [0, len(color_map_array)-1] and clip to valid indices
        color_indices = np.clip((normalized * (len(color_map_array) - 1)).astype(np.int32), 0, len(color_map_array) - 1)

        # Create a new RGB array by mapping each index to its color
        # This is a vectorized operation that replaces the nested loops
        mapped_colors = color_map_np[color_indices]

        return mapped_colors

    @staticmethod
    def scale(array: np.ndarray, width: int, height: int) -> np.ndarray:
        """
        Scale a numpy array to the specified width and height.

        Args:
            array: The numpy array
            width: The target width
            height: The target height

        Returns:
            np.ndarray: The scaled numpy array
        """
        # Get the original dimensions
        if len(array.shape) == 2:
            # Grayscale
            orig_height, orig_width = array.shape
            channels = 1
        else:
            # RGB or RGBA
            orig_height, orig_width, channels = array.shape

        # Create a new array with the target dimensions
        if channels == 1:
            scaled = np.zeros((height, width), dtype=array.dtype)
        else:
            scaled = np.zeros((height, width, channels), dtype=array.dtype)

        # Calculate scaling factors
        x_ratio = orig_width / width
        y_ratio = orig_height / height

        # Simple nearest-neighbor scaling
        for y in range(height):
            for x in range(width):
                px = int(x * x_ratio)
                py = int(y * y_ratio)
                if channels == 1:
                    scaled[y, x] = array[py, px]
                else:
                    scaled[y, x] = array[py, px]

        return scaled

    @staticmethod
    def array_to_sdl2_texture(array: np.ndarray, renderer: sdl2.ext.Renderer) -> sdl2.ext.Texture:
        """
        Convert a numpy array to an SDL2 texture.

        Args:
            array: The numpy array to convert (grayscale or RGB)
            renderer: The SDL2 renderer to create the texture with

        Returns:
            sdl2.ext.Texture: An SDL2 texture
        """
        # Check array dimensions
        if len(array.shape) == 2:
            # Grayscale array
            return create_grayscale_texture(array, renderer)
        elif len(array.shape) == 3 and array.shape[2] in (3, 4):
            # RGB or RGBA array
            return create_texture_from_array(array, renderer)
        else:
            raise ValueError(f"Unsupported array shape: {array.shape}")
