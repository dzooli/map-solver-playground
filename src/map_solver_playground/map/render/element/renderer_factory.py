"""
Factory for creating renderers for map elements.
"""

from typing import Dict, Type, Any

from map_solver_playground.map.render.element.base_renderer import BaseRenderer
from map_solver_playground.map.render.renderer_backend import RendererBackend
from map_solver_playground.map.types import MapElement


class RendererFactory:
    """
    Factory for creating renderers for map elements.
    """

    # The current renderer backend
    _current_backend: RendererBackend = RendererBackend.PYGAME

    # Map renderer backends to their corresponding renderer classes
    _backend_renderers: Dict[RendererBackend, Type[BaseRenderer]] = {}

    @classmethod
    def register_renderer(cls, backend: RendererBackend, renderer: Type[BaseRenderer]) -> None:
        """
        Register a renderer for a backend.

        Args:
            backend: The renderer backend
            renderer: The renderer class for the backend
        """
        cls._backend_renderers[backend] = renderer

    @classmethod
    def set_backend(cls, backend: RendererBackend) -> None:
        """
        Set the current renderer backend.

        Args:
            backend: The renderer backend to use
        """
        if backend not in cls._backend_renderers:
            raise ValueError(f"No renderer registered for backend: {backend.value}")
        cls._current_backend = backend

    @classmethod
    def get_current_renderer(cls) -> Type[BaseRenderer]:
        """
        Get the current renderer.

        Returns:
            Type[BaseRenderer]: The current renderer class
        """
        renderer = cls._backend_renderers.get(cls._current_backend)
        if renderer is None:
            raise ValueError(f"No renderer registered for backend: {cls._current_backend.value}")
        return renderer

    @classmethod
    def render(cls, screen: Any, element: MapElement, image_x: int, image_y: int, current_view: int = 0) -> None:
        """
        Render a map element on the screen.

        Args:
            screen: The surface to render on (implementation-specific)
            element: The map element to render
            image_x: The x-coordinate of the map's upper left corner
            image_y: The y-coordinate of the map's upper left corner
            current_view: The current view index (0 for original, 1 for small map)
        """
        renderer = cls.get_current_renderer()
        renderer.render(screen, element, image_x, image_y, current_view)
