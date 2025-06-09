"""
Pygame implementations of the element renderer interfaces.
"""

from typing import List, Tuple

import pygame

from map_solver_playground.map.render.element.element_renderer_interfaces import (
    BaseFlagRenderer,
    BaseGeoPathRenderer,
    BaseTerrainRenderer,
)
from map_solver_playground.map.types import Flag, GeoPath, Terrain
from map_solver_playground.map.render.color_maps import ColorGradient


class PygameFlagRenderer(BaseFlagRenderer):
    """
    Pygame implementation of the flag renderer interface.
    """

    @classmethod
    def clear_texture_cache(cls, flag_id=None) -> None:
        """
        Clear the texture cache for a specific flag or all flags.

        Args:
            flag_id: The ID of the flag to clear textures for, or None to clear all textures
        """
        # Pygame renderer doesn't use a texture cache
        # It directly blits surfaces to the screen
        pass

    @staticmethod
    def render(
        screen: pygame.Surface,
        flag: Flag,
        image_x: int,
        image_y: int,
        current_view: int = 0,
    ) -> None:
        """
        Render a flag on the screen using Pygame.

        Args:
            screen: The pygame surface to render on
            flag: The flag to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
            current_view: The current view index (0 for original, 1 for small map)
        """
        # Skip rendering if the flag is not visible or has no position or image
        if not flag.visible or flag.position is None or flag.image is None:
            return

        # Calculate screen position for the flag
        screen_pos = PygameFlagRenderer.screen_to_map_pos(
            flag.position, flag.image.get_width(), flag.image.get_height(), image_x, image_y
        )

        # Render the flag on the screen
        screen.blit(flag.image, screen_pos)

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

    @staticmethod
    def is_within_safe_area(
        pos: Tuple[int, int],
        sprite_width: int,
        sprite_height: int,
        image_x: int,
        image_y: int,
        map_width: int,
        map_height: int,
    ) -> Tuple[bool, bool, int, int]:
        """
        Check if the given position is within the safe area of the map.
        The safe area is defined as the area where a sprite can be placed without exceeding map boundaries.

        Args:
            pos: The (x, y) position to check
            sprite_width: The width of the sprite
            sprite_height: The height of the sprite
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
            map_width: The width of the map
            map_height: The height of the map

        Returns:
            tuple: (is_within_safe_area, is_within_map, rel_x, rel_y)
                is_within_safe_area: True if the position is within the safe area
                is_within_map: True if the position is within the map boundaries
                rel_x: The x-coordinate relative to the map's upper left corner
                rel_y: The y-coordinate relative to the map's upper left corner
        """
        # Calculate the safe area where sprites can be placed without exceeding map boundaries
        # The sprite is centered on the click position, so we need to ensure it's at least half the sprite size away from edges
        safe_x_min = image_x + sprite_width // 2
        safe_x_max = image_x + map_width - sprite_width // 2
        safe_y_min = image_y + sprite_height // 2
        safe_y_max = image_y + map_height - sprite_height // 2

        # Check if position is within safe area
        is_within_safe_area = safe_x_min <= pos[0] <= safe_x_max and safe_y_min <= pos[1] <= safe_y_max

        # Check if the position is within map boundaries
        is_within_map = image_x <= pos[0] <= image_x + map_width and image_y <= pos[1] <= image_y + map_height

        # Calculate coordinates relative to map's upper left corner
        rel_x = pos[0] - image_x
        rel_y = pos[1] - image_y

        return is_within_safe_area, is_within_map, rel_x, rel_y


class PygameGeoPathRenderer(BaseGeoPathRenderer):
    """
    Pygame implementation of the geo path renderer interface.
    """

    @classmethod
    def clear_texture_cache(cls, path_id=None) -> None:
        """
        Clear the texture cache for a specific geo path or all geo paths.

        Args:
            path_id: The ID of the geo path to clear textures for, or None to clear all textures
        """
        # Pygame renderer doesn't use a texture cache
        # It directly draws lines on the screen
        pass

    @staticmethod
    def render(
        screen: pygame.Surface,
        geo_path: GeoPath,
        image_x: int,
        image_y: int,
        current_view: int = 0,
    ) -> None:
        """
        Render a geo path on the screen using Pygame.

        Args:
            screen: The pygame surface to render on
            geo_path: The geo path to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
            current_view: The current view index (0 for original, 1 for small map)
        """
        # Skip rendering if the path is not visible or has no points
        if not geo_path.visible or geo_path.is_empty():
            return

        # Convert path coordinates to screen coordinates
        screen_points = PygameGeoPathRenderer.path_to_screen_points(geo_path.path_points, image_x, image_y)

        # Draw the path as connected lines
        pygame.draw.lines(
            screen,
            geo_path.color,
            False,  # Don't connect the last point to the first
            screen_points,
            geo_path.width,
        )

    @staticmethod
    def path_to_screen_points(
        path_points: List[Tuple[int, int]],
        image_x: int,
        image_y: int,
    ) -> List[Tuple[int, int]]:
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


class PygameTerrainRenderer(BaseTerrainRenderer):
    """
    Pygame implementation of the terrain renderer interface.
    """

    @classmethod
    def clear_texture_cache(cls, terrain_id=None) -> None:
        """
        Clear the texture cache for a specific terrain or all terrains.

        Args:
            terrain_id: The ID of the terrain to clear textures for, or None to clear all textures
        """
        # Pygame renderer doesn't use a texture cache
        # It directly blits surfaces to the screen
        pass

    @staticmethod
    def render(
        screen: pygame.Surface,
        terrain: Terrain,
        image_x: int,
        image_y: int,
        current_view: int = 0,
    ) -> None:
        """
        Render a terrain on the screen using Pygame.

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
        """
        Normalize height data to the range [0, 1].

        Args:
            height_data: The height data to normalize

        Returns:
            The normalized height data
        """
        if height_data.size == 0:
            return None

        min_height = height_data.min()
        max_height = height_data.max()
        height_range = max_height - min_height

        if height_range == 0:
            return height_data.copy()

        return (height_data - min_height) / height_range

    @staticmethod
    def create_terrain_surface(map_data):
        """
        Create a terrain surface from map data.

        Args:
            map_data: The map data to create a surface from

        Returns:
            A pygame surface representing the terrain
        """
        terrain_surface = pygame.Surface((map_data.width, map_data.height))
        height_data = map_data.data

        normalized_data = PygameTerrainRenderer._normalize_height_data(height_data)
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
