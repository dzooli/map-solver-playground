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
        # Check if the requested backend is registered
        if backend in cls._backend_renderers:
            cls._current_backend = backend
            return

        # If the requested backend is not available, try to register it
        try:
            if backend == RendererBackend.SDL2:
                try:
                    from map_solver_playground.map.render.element.sdl2_renderer import SDL2Renderer

                    # Try to initialize SDL2 to check if the library is available
                    try:
                        import sdl2.ext

                        sdl2.ext.init()
                        sdl2.ext.quit()

                        cls.register_renderer(RendererBackend.SDL2, SDL2Renderer)
                        cls._current_backend = backend
                    except Exception as e:
                        print(f"Warning: SDL2 library initialization failed: {str(e)}. Using fallback.")
                        cls._use_fallback_renderer()
                except ImportError as e:
                    print(f"Warning: SDL2 renderer import failed: {str(e)}. Using fallback.")
                    cls._use_fallback_renderer()
            elif backend == RendererBackend.PYGAME:
                try:
                    from map_solver_playground.map.render.element.pygame_renderer import PygameRenderer

                    # Try to initialize pygame to check if the library is available
                    try:
                        import pygame

                        pygame.init()
                        pygame.quit()

                        cls.register_renderer(RendererBackend.PYGAME, PygameRenderer)
                        cls._current_backend = backend
                    except Exception as e:
                        print(f"Warning: Pygame library initialization failed: {str(e)}. Using fallback.")
                        cls._use_fallback_renderer()
                except ImportError as e:
                    print(f"Warning: Pygame renderer import failed: {str(e)}. Using fallback.")
                    cls._use_fallback_renderer()
            else:
                # If the backend is not supported, use a fallback
                print(f"Warning: Unsupported renderer backend: {backend.value}. Using fallback.")
                cls._use_fallback_renderer()
        except ImportError as e:
            # If the import fails, use a fallback
            print(f"Warning: Could not import renderer for backend: {backend.value}. Error: {str(e)}. Using fallback.")
            cls._use_fallback_renderer()

    @classmethod
    def _use_fallback_renderer(cls) -> None:
        """
        Use a fallback renderer if the requested renderer is not available.
        First tries to use any already registered renderer.
        If no renderers are registered, tries to register the SDL2 renderer.
        If that fails, tries to register the pygame renderer.
        If that fails, raises an error.
        """
        # If any renderer is already registered, use the first one
        if cls._backend_renderers:
            cls._current_backend = next(iter(cls._backend_renderers.keys()))
            print(f"Using fallback renderer: {cls._current_backend.value}")
            return

        # Try to register the SDL2 renderer first
        try:
            from map_solver_playground.map.render.element.sdl2_renderer import SDL2Renderer

            # Try to initialize SDL2 to check if the library is available
            try:
                import sdl2.ext

                sdl2.ext.init()
                sdl2.ext.quit()

                cls.register_renderer(RendererBackend.SDL2, SDL2Renderer)
                cls._current_backend = RendererBackend.SDL2
                print(f"Using fallback renderer: {cls._current_backend.value}")
                return
            except Exception as e:
                print(f"SDL2 library initialization failed: {str(e)}")
        except ImportError as e:
            print(f"SDL2 renderer import failed: {str(e)}")

        # Try to register the pygame renderer as a last resort
        try:
            from map_solver_playground.map.render.element.pygame_renderer import PygameRenderer

            # Try to initialize pygame to check if the library is available
            try:
                import pygame

                pygame.init()
                pygame.quit()

                cls.register_renderer(RendererBackend.PYGAME, PygameRenderer)
                cls._current_backend = RendererBackend.PYGAME
                print(f"Using fallback renderer: {cls._current_backend.value}")
                return
            except Exception as e:
                print(f"Pygame library initialization failed: {str(e)}")
        except ImportError as e:
            print(f"Pygame renderer import failed: {str(e)}")

        # If no renderers are available, raise an error with detailed information
        raise ValueError(
            "No renderers available. Please ensure either pygame or pysdl2 is properly installed.\n"
            "For pygame: pip install pygame\n"
            "For pysdl2: pip install pysdl2\n"
            "Note: pysdl2 also requires the SDL2 library to be installed on your system.\n"
            "For Windows, you can download SDL2 from https://github.com/libsdl-org/SDL/releases\n"
            "and place the SDL2.dll in your Python environment's DLLs directory or in your application directory."
        )

    @classmethod
    def get_current_backend(cls) -> RendererBackend:
        """
        Get the current renderer backend.

        Returns:
            RendererBackend: The current renderer backend
        """
        return cls._current_backend

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
