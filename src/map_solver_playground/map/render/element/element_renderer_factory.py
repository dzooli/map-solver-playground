"""
Factory for creating element renderers based on the current renderer backend.
"""

from typing import Dict, Type

from map_solver_playground.map.render.element.element_renderer_interfaces import (
    BaseFlagRenderer,
    BaseGeoPathRenderer,
    BaseTerrainRenderer,
)
from map_solver_playground.map.render.element.pygame_element_renderers import (
    PygameFlagRenderer,
    PygameGeoPathRenderer,
    PygameTerrainRenderer,
)
from map_solver_playground.map.render.renderer_backend import RendererBackend

# Try to import SDL2 renderers if available
try:
    from map_solver_playground.map.render.element.sdl2_element_renderers import (
        SDL2FlagRenderer,
        SDL2GeoPathRenderer,
        SDL2TerrainRenderer,
    )
    SDL2_AVAILABLE = True
except ImportError:
    # Define placeholder classes for SDL2 renderers
    class SDL2FlagRenderer(BaseFlagRenderer):
        pass

    class SDL2GeoPathRenderer(BaseGeoPathRenderer):
        pass

    class SDL2TerrainRenderer(BaseTerrainRenderer):
        pass

    SDL2_AVAILABLE = False


class ElementRendererFactory:
    """
    Factory for creating element renderers based on the current renderer backend.
    """

    # Map renderer backends to their corresponding element renderer classes
    _flag_renderers: Dict[RendererBackend, Type[BaseFlagRenderer]] = {
        RendererBackend.PYGAME: PygameFlagRenderer,
        RendererBackend.SDL2: SDL2FlagRenderer,
    }

    _geo_path_renderers: Dict[RendererBackend, Type[BaseGeoPathRenderer]] = {
        RendererBackend.PYGAME: PygameGeoPathRenderer,
        RendererBackend.SDL2: SDL2GeoPathRenderer,
    }

    _terrain_renderers: Dict[RendererBackend, Type[BaseTerrainRenderer]] = {
        RendererBackend.PYGAME: PygameTerrainRenderer,
        RendererBackend.SDL2: SDL2TerrainRenderer,
    }

    @classmethod
    def get_flag_renderer(cls, backend: RendererBackend) -> Type[BaseFlagRenderer]:
        """
        Get the flag renderer for the specified backend.

        Args:
            backend: The renderer backend

        Returns:
            Type[BaseFlagRenderer]: The flag renderer class for the backend
        """
        renderer = cls._flag_renderers.get(backend)
        if renderer is None:
            raise ValueError(f"No flag renderer registered for backend: {backend.value}")
        return renderer

    @classmethod
    def get_geo_path_renderer(cls, backend: RendererBackend) -> Type[BaseGeoPathRenderer]:
        """
        Get the geo path renderer for the specified backend.

        Args:
            backend: The renderer backend

        Returns:
            Type[BaseGeoPathRenderer]: The geo path renderer class for the backend
        """
        renderer = cls._geo_path_renderers.get(backend)
        if renderer is None:
            raise ValueError(f"No geo path renderer registered for backend: {backend.value}")
        return renderer

    @classmethod
    def get_terrain_renderer(cls, backend: RendererBackend) -> Type[BaseTerrainRenderer]:
        """
        Get the terrain renderer for the specified backend.

        Args:
            backend: The renderer backend

        Returns:
            Type[BaseTerrainRenderer]: The terrain renderer class for the backend
        """
        renderer = cls._terrain_renderers.get(backend)
        if renderer is None:
            raise ValueError(f"No terrain renderer registered for backend: {backend.value}")
        return renderer
