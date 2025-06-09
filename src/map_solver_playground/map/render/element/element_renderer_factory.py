"""
Factory for creating element renderers based on the current renderer backend.
"""

from typing import Dict, Type

from map_solver_playground.map.render.element.element_renderer_interfaces import (
    BaseFlagRenderer,
    BaseGeoPathRenderer,
    BaseTerrainRenderer,
)
from map_solver_playground.map.render.renderer_backend import RendererBackend

# Define placeholder classes for renderers
class PygameFlagRenderer(BaseFlagRenderer):
    pass

class PygameGeoPathRenderer(BaseGeoPathRenderer):
    pass

class PygameTerrainRenderer(BaseTerrainRenderer):
    pass

class SDL2FlagRenderer(BaseFlagRenderer):
    pass

class SDL2GeoPathRenderer(BaseGeoPathRenderer):
    pass

class SDL2TerrainRenderer(BaseTerrainRenderer):
    pass

# Flags to track which renderers are available
PYGAME_AVAILABLE = False
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
    def initialize_renderers(cls, backend: RendererBackend) -> None:
        """
        Initialize the renderers for the specified backend.
        This method imports the renderer classes for the specified backend only.

        Args:
            backend: The renderer backend to initialize
        """
        global PYGAME_AVAILABLE, SDL2_AVAILABLE

        if backend == RendererBackend.PYGAME and not PYGAME_AVAILABLE:
            try:
                from map_solver_playground.map.render.element.pygame_element_renderers import (
                    PygameFlagRenderer as PFR,
                    PygameGeoPathRenderer as PGPR,
                    PygameTerrainRenderer as PTR,
                )

                # Update the renderer classes with the imported ones
                cls._flag_renderers[RendererBackend.PYGAME] = PFR
                cls._geo_path_renderers[RendererBackend.PYGAME] = PGPR
                cls._terrain_renderers[RendererBackend.PYGAME] = PTR

                PYGAME_AVAILABLE = True
            except ImportError:
                pass

        elif backend == RendererBackend.SDL2 and not SDL2_AVAILABLE:
            try:
                from map_solver_playground.map.render.element.sdl2_element_renderers import (
                    SDL2FlagRenderer as SFR,
                    SDL2GeoPathRenderer as SGPR,
                    SDL2TerrainRenderer as STR,
                )

                # Update the renderer classes with the imported ones
                cls._flag_renderers[RendererBackend.SDL2] = SFR
                cls._geo_path_renderers[RendererBackend.SDL2] = SGPR
                cls._terrain_renderers[RendererBackend.SDL2] = STR

                SDL2_AVAILABLE = True
            except ImportError:
                pass

    @classmethod
    def get_flag_renderer(cls, backend: RendererBackend) -> Type[BaseFlagRenderer]:
        """
        Get the flag renderer for the specified backend.

        Args:
            backend: The renderer backend

        Returns:
            Type[BaseFlagRenderer]: The flag renderer class for the backend
        """
        # Initialize renderers for the specified backend if not already initialized
        cls.initialize_renderers(backend)

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
        # Initialize renderers for the specified backend if not already initialized
        cls.initialize_renderers(backend)

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
        # Initialize renderers for the specified backend if not already initialized
        cls.initialize_renderers(backend)

        renderer = cls._terrain_renderers.get(backend)
        if renderer is None:
            raise ValueError(f"No terrain renderer registered for backend: {backend.value}")
        return renderer

    @classmethod
    def clear_terrain_texture_cache(cls, backend: RendererBackend, terrain_id=None) -> None:
        """
        Clear the texture cache for terrain renderers.
        This is a renderer-agnostic way to clear the cache when a new map is generated.

        Args:
            backend: The renderer backend
            terrain_id: The ID of the terrain to clear textures for, or None to clear all textures
        """
        # Get the terrain renderer for the specified backend and call its clear_texture_cache method
        renderer = cls.get_terrain_renderer(backend)
        renderer.clear_texture_cache(terrain_id)
