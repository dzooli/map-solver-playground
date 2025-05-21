"""
GeoPath renderer for rendering GeoPath map elements.
"""

from typing import List, Tuple

import pygame

from map_solver_playground.maps.elements.geo_path import GeoPath


class GeoPathRenderer:
    """
    Renderer for GeoPath map elements.
    """

    @staticmethod
    def render(
        screen: pygame.Surface,
        geo_path: GeoPath,
        image_x: int,
        image_y: int,
    ) -> None:
        """
        Render a geo path on the screen.
        
        Args:
            screen: The pygame surface to render on
            geo_path: The geo path to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
        """
        # Skip rendering if the path is not visible or has no points
        if not geo_path.visible or geo_path.is_empty():
            return

        # Convert path coordinates to screen coordinates
        screen_points = GeoPathRenderer.path_to_screen_points(geo_path.path_points, image_x, image_y)
        
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