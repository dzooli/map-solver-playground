"""
Factory for creating element for map elements.
"""

from typing import Dict, Type

from map_solver_playground.map.types import MapElement, Flag, GeoPath
from map_solver_playground.map.types.terrain import Terrain
from map_solver_playground.map.render.element.flag_renderer import FlagRenderer
from map_solver_playground.map.render.element.geo_path_renderer import GeoPathRenderer
from map_solver_playground.map.render.element.terrain_renderer import TerrainRenderer


class RendererFactory:
    """
    Factory for creating element for map elements.
    """

    # Map element types to their corresponding renderer classes
    _renderers: Dict[Type[MapElement], Type] = {
        Flag: FlagRenderer,
        GeoPath: GeoPathRenderer,
        Terrain: TerrainRenderer,
    }

    @classmethod
    def get_renderer(cls, element: MapElement) -> Type:
        """
        Get the renderer for a map element.

        Args:
            element: The map element to get a renderer for

        Returns:
            Type: The renderer class for the element

        Raises:
            ValueError: If no renderer is found for the element type
        """
        element_type = type(element)
        renderer = cls._renderers.get(element_type)

        if renderer is None:
            raise ValueError(f"No renderer found for element type: {element_type.__name__}")

        return renderer

    @classmethod
    def render(cls, screen, element: MapElement, image_x: int, image_y: int) -> None:
        """
        Render a map element on the screen.

        Args:
            screen: The pygame surface to render on
            element: The map element to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
        """
        renderer = cls.get_renderer(element)
        renderer.render(screen, element, image_x, image_y)
