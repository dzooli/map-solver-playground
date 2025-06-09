"""
Factory for creating map surface renderers based on the current renderer backend.
"""

from typing import Dict, Type
import importlib.util

from map_solver_playground.map.render.renderer_backend import RendererBackend
from map_solver_playground.map.render.map_surface_renderer_interfaces import BaseMapSurfaceRenderer

# Define placeholder classes for renderers
class PygameMapSurfaceRenderer(BaseMapSurfaceRenderer):
    pass

class SDL2MapSurfaceRenderer(BaseMapSurfaceRenderer):
    pass

# Check if renderers are available without importing them
PYGAME_AVAILABLE = importlib.util.find_spec('map_solver_playground.map.render.pygame_map_surface_renderer') is not None
SDL2_AVAILABLE = importlib.util.find_spec('map_solver_playground.map.render.sdl2_map_surface_renderer') is not None


class MapSurfaceRendererFactory:
    """
    Factory for creating map surface renderers based on the current renderer backend.
    """

    # Map renderer backends to their corresponding map surface renderer classes
    _map_surface_renderers: Dict[RendererBackend, Type[BaseMapSurfaceRenderer]] = {
        RendererBackend.PYGAME: PygameMapSurfaceRenderer,
        RendererBackend.SDL2: SDL2MapSurfaceRenderer,
    }

    @classmethod
    def initialize_renderers(cls, backend: RendererBackend) -> None:
        """
        Initialize the renderers for the specified backend.
        This method imports the renderer classes for the specified backend only.

        Args:
            backend: The renderer backend to initialize
        """
        global PYGAME_AVAILABLE, SDL2_AVAILABLE, PygameMapSurfaceRenderer, SDL2MapSurfaceRenderer

        if backend == RendererBackend.PYGAME and PYGAME_AVAILABLE:
            # Only import pygame renderer if it's available and requested
            if not hasattr(PygameMapSurfaceRenderer, 'render'):
                try:
                    from map_solver_playground.map.render.pygame_map_surface_renderer import PygameMapSurfaceRenderer as PMR
                    cls._map_surface_renderers[RendererBackend.PYGAME] = PMR
                except ImportError:
                    pass

        elif backend == RendererBackend.SDL2 and SDL2_AVAILABLE:
            # Only import SDL2 renderer if it's available and requested
            if not hasattr(SDL2MapSurfaceRenderer, 'render'):
                try:
                    from map_solver_playground.map.render.sdl2_map_surface_renderer import SDL2MapSurfaceRenderer as SMR
                    cls._map_surface_renderers[RendererBackend.SDL2] = SMR
                except ImportError:
                    pass

    @classmethod
    def get_map_surface_renderer(cls, backend: RendererBackend) -> Type[BaseMapSurfaceRenderer]:
        """
        Get the map surface renderer for the specified backend.

        Args:
            backend: The renderer backend

        Returns:
            Type[BaseMapSurfaceRenderer]: The map surface renderer class for the backend
        """
        # Initialize renderers for the specified backend if not already initialized
        cls.initialize_renderers(backend)

        renderer = cls._map_surface_renderers.get(backend)
        if renderer is None:
            raise ValueError(f"No map surface renderer registered for backend: {backend.value}")
        return renderer
