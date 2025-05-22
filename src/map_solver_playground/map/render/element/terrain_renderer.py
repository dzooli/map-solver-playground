"""
Terrain renderer for rendering Terrain map elements.
"""

import pygame
import numpy as np

from map_solver_playground.map.types.terrain import Terrain
from map_solver_playground.map.render.color_maps import ColorGradient


class TerrainRenderer:
    """
    Renderer for Terrain map elements.
    """

    @staticmethod
    def render(
        screen: pygame.Surface,
        terrain: Terrain,
        image_x: int,
        image_y: int,
        current_view: int = 0,
    ) -> None:
        """
        Render a terrain on the screen.

        Args:
            screen: The pygame surface to render on
            terrain: The terrain to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
            current_view: The current view index (0 for original, 1 for small map)
        """
        # Skip rendering if the terrain is not visible
        if not terrain.visible:
            return

        # Use the appropriate image based on the current view
        if current_view == 0:
            # Original map view
            if terrain.map_image is None:
                return
            screen.blit(terrain.map_image, (image_x, image_y))
        else:
            # Small map view
            if terrain.small_map_image is None:
                return
            screen.blit(terrain.small_map_image, (image_x, image_y))

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
    def _create_terrain_surface(map_data):
        terrain_surface = pygame.Surface((map_data.width, map_data.height))
        height_data = map_data.data

        normalized_data = TerrainRenderer._normalize_height_data(height_data)
        if normalized_data is None:
            return terrain_surface

        color_gradient = ColorGradient.TOPO_COLORS
        max_color_index = len(color_gradient) - 1

        for y in range(map_data.height):
            for x in range(map_data.width):
                if y < normalized_data.shape[0] and x < normalized_data.shape[1]:
                    color_index = int(normalized_data[y, x] * max_color_index)
                    terrain_surface.set_at((x, y), color_gradient[color_index])

        return terrain_surface
