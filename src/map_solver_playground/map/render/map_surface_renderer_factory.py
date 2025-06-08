"""
Factory for creating map surface renderers based on the current renderer backend.
"""

from typing import Dict, Type

from map_solver_playground.map.render.renderer_backend import RendererBackend
from map_solver_playground.map.render.map_surface_renderer_interfaces import BaseMapSurfaceRenderer
from map_solver_playground.map.render.pygame_map_surface_renderer import PygameMapSurfaceRenderer

# Try to import SDL2 renderer if available
try:
    from map_solver_playground.map.render.sdl2_map_surface_renderer import SDL2MapSurfaceRenderer
    SDL2_AVAILABLE = True
except ImportError:
    # Define a placeholder class for SDL2 renderer
    class SDL2MapSurfaceRenderer(BaseMapSurfaceRenderer):
        pass
    SDL2_AVAILABLE = False


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
    def get_map_surface_renderer(cls, backend: RendererBackend) -> Type[BaseMapSurfaceRenderer]:
        """
        Get the map surface renderer for the specified backend.

        Args:
            backend: The renderer backend

        Returns:
            Type[BaseMapSurfaceRenderer]: The map surface renderer class for the backend
        """
        renderer = cls._map_surface_renderers.get(backend)
        if renderer is None:
            raise ValueError(f"No map surface renderer registered for backend: {backend.value}")
        return renderer
