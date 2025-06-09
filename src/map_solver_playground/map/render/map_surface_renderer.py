"""
Pygame map surface renderer module.

This module provides the MapRenderer class for rendering map using pygame.
"""

import numpy as np
import pygame

from map_solver_playground.map.map_data import Map
from map_solver_playground.map.render.color_maps import TerrainColorGradient


class MapRenderer:
    """
    A class for rendering map using pygame.

    This class provides methods for converting map to pygame surfaces
    and applying visual effects.
    """

    @staticmethod
    def to_pygame_image(map_obj: Map) -> pygame.Surface:
        """
        Convert a map to a pygame image suitable for drawing.

        Args:
            map_obj (Map): The map to convert

        Returns:
            pygame.Surface: A pygame image representing the map
        """
        # Convert height values to grayscale (0-255) using numpy operations
        # Clip values to ensure they're in the 0-1 range
        normalized_data = np.clip(map_obj.data, 0.0, 1.0)
        grayscale_data = (normalized_data * 255).astype(np.uint8)

        # Create a 3D array where each pixel has the same value for R, G, and B
        rgb_array = np.stack([grayscale_data] * 3, axis=-1)

        # Create a pygame surface from the numpy array
        pygame_surface = pygame.surfarray.make_surface(rgb_array)

        return pygame_surface

    @staticmethod
    def color_map(surface: pygame.Surface, color_map_array: TerrainColorGradient) -> pygame.Surface:
        """
        Map grayscale values in a surface to colors in a color map.

        Args:
            surface (pygame.Surface): The surface
            color_map_array (list): A list of RGB tuples representing the color map

        Returns:
            pygame.Surface: A new surface with mapped colors
        """
        # Convert color_map_array to a numpy array for faster indexing
        color_map_np = np.array(color_map_array, dtype=np.uint8)

        # Get the pixel array from the surface
        pixel_array = pygame.surfarray.array3d(surface)

        # Convert to grayscale using the luminosity method: 0.21 R + 0.72 G + 0.07 B
        # This creates a 2D array of grayscale values
        grayscale = np.dot(pixel_array, [0.21, 0.72, 0.07]).astype(np.uint8)

        # Normalize the grayscale values to the range [0, 1]
        normalized = grayscale / 255.0

        # Map the normalized values to indices in the color map
        # Scale to the range [0, len(color_map_array)-1] and clip to valid indices
        color_indices = np.clip((normalized * (len(color_map_array) - 1)).astype(np.int32), 0, len(color_map_array) - 1)

        # Create a new RGB array by mapping each index to its color
        # This is a vectorized operation that replaces the nested loops
        mapped_colors = color_map_np[color_indices]

        # Create a new surface from the mapped colors
        new_surface = pygame.surfarray.make_surface(mapped_colors)

        return new_surface

    @staticmethod
    def scale(surface: pygame.Surface, width: int, height: int) -> pygame.Surface:
        """
        Scale a pygame surface to the specified width and height.

        Args:
            surface (pygame.Surface): The surface
            width (int): The target width
            height (int): The target height

        Returns:
            pygame.Surface: The scaled surface
        """
        return pygame.transform.scale(surface, (width, height))