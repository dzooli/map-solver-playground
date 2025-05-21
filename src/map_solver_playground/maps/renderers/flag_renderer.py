"""
Flag renderer for rendering Flag map elements.
"""

from typing import Optional, Tuple

import pygame

from map_solver_playground.maps.elements.flag import Flag


class FlagRenderer:
    """
    Renderer for Flag map elements.
    """

    @staticmethod
    def render(
        screen: pygame.Surface,
        flag: Flag,
        image_x: int,
        image_y: int,
    ) -> None:
        """
        Render a flag on the screen.

        Args:
            screen: The pygame surface to render on
            flag: The flag to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
        """
        # Skip rendering if the flag is not visible or has no position or image
        if not flag.visible or flag.position is None or flag.image is None:
            return

        # Calculate screen position for the flag
        screen_pos = FlagRenderer.screen_to_map_pos(
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
        is_within_map = (
            image_x <= pos[0] <= image_x + map_width and image_y <= pos[1] <= image_y + map_height
        )

        # Calculate coordinates relative to map's upper left corner
        rel_x = pos[0] - image_x
        rel_y = pos[1] - image_y

        return is_within_safe_area, is_within_map, rel_x, rel_y
