"""
Base interfaces for map element renderers.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Tuple, TypeVar

from map_solver_playground.map.types import Flag, GeoPath, Terrain

# Type variable for the renderer-specific screen/surface type
ScreenType = TypeVar('ScreenType')


class BaseElementRenderer(ABC):
    """
    Base interface for all element renderers.
    """

    @staticmethod
    @abstractmethod
    def render(
        screen: Any,
        element: Any,
        image_x: int,
        image_y: int,
        current_view: int = 0,
    ) -> None:
        """
        Render an element on the screen.

        Args:
            screen: The surface to render on (implementation-specific)
            element: The element to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
            current_view: The current view index (0 for original, 1 for small map)
        """
        pass

    @classmethod
    @abstractmethod
    def clear_texture_cache(cls, element_id=None) -> None:
        """
        Clear the texture cache for a specific element or all elements.

        Args:
            element_id: The ID of the element to clear textures for, or None to clear all textures
        """
        pass


class BaseFlagRenderer(BaseElementRenderer):
    """
    Interface for flag renderers.
    """

    @staticmethod
    @abstractmethod
    def render(
        screen: Any,
        flag: Flag,
        image_x: int,
        image_y: int,
        current_view: int = 0,
    ) -> None:
        """
        Render a flag on the screen.

        Args:
            screen: The surface to render on (implementation-specific)
            flag: The flag to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
            current_view: The current view index (0 for original, 1 for small map)
        """
        pass

    @staticmethod
    @abstractmethod
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
        pass


class BaseGeoPathRenderer(BaseElementRenderer):
    """
    Interface for geo path renderers.
    """

    @staticmethod
    @abstractmethod
    def render(
        screen: Any,
        geo_path: GeoPath,
        image_x: int,
        image_y: int,
        current_view: int = 0,
    ) -> None:
        """
        Render a geo path on the screen.

        Args:
            screen: The surface to render on (implementation-specific)
            geo_path: The geo path to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
            current_view: The current view index (0 for original, 1 for small map)
        """
        pass

    @staticmethod
    @abstractmethod
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
        pass


class BaseTerrainRenderer(BaseElementRenderer):
    """
    Interface for terrain renderers.
    """

    @staticmethod
    @abstractmethod
    def render(
        screen: Any,
        terrain: Terrain,
        image_x: int,
        image_y: int,
        current_view: int = 0,
    ) -> None:
        """
        Render a terrain on the screen.

        Args:
            screen: The surface to render on (implementation-specific)
            terrain: The terrain to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
            current_view: The current view index (0 for original, 1 for small map)
        """
        pass
