"""
Map element package for rendering map elements.
"""

from map_solver_playground.map.render.element.base_renderer import BaseRenderer
from map_solver_playground.map.render.element.element_renderer_interfaces import (
    BaseElementRenderer,
    BaseFlagRenderer,
    BaseGeoPathRenderer,
    BaseTerrainRenderer,
)
from map_solver_playground.map.render.element.renderer_factory import RendererFactory, RendererBackend
from map_solver_playground.map.render.element.element_renderer_factory import ElementRendererFactory

# Define base __all__ with common elements
__all__ = [
    "BaseRenderer", "BaseElementRenderer",
    "BaseFlagRenderer", "BaseGeoPathRenderer", "BaseTerrainRenderer",
    "RendererFactory", "RendererBackend", "ElementRendererFactory"
]

# Try to import Pygame renderer if available
PYGAME_AVAILABLE = False
try:
    from map_solver_playground.map.render.element.pygame_element_renderers import (
        PygameFlagRenderer,
        PygameGeoPathRenderer,
        PygameTerrainRenderer,
    )
    from map_solver_playground.map.render.element.pygame_renderer import PygameRenderer
    PYGAME_AVAILABLE = True
    # Register the Pygame renderer with the factory
    RendererFactory.register_renderer(RendererBackend.PYGAME, PygameRenderer)
    __all__.extend([
        "PygameFlagRenderer", "PygameGeoPathRenderer", "PygameTerrainRenderer",
        "PygameRenderer"
    ])
except ImportError:
    pass

# Try to import SDL2 renderer if available
SDL2_AVAILABLE = False
try:
    from map_solver_playground.map.render.element.sdl2_renderer import SDL2Renderer
    from map_solver_playground.map.render.element.sdl2_element_renderers import (
        SDL2TerrainRenderer,
        SDL2FlagRenderer,
        SDL2GeoPathRenderer,
    )
    SDL2_AVAILABLE = True
    # Register the SDL2 renderer with the factory
    RendererFactory.register_renderer(RendererBackend.SDL2, SDL2Renderer)
    __all__.extend([
        "SDL2Renderer", "SDL2TerrainRenderer", "SDL2FlagRenderer", "SDL2GeoPathRenderer"
    ])
except ImportError:
    pass
