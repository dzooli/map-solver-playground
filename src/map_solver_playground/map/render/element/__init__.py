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
from map_solver_playground.map.render.element.pygame_element_renderers import (
    PygameFlagRenderer,
    PygameGeoPathRenderer,
    PygameTerrainRenderer,
)
from map_solver_playground.map.render.element.pygame_renderer import PygameRenderer
from map_solver_playground.map.render.element.renderer_factory import RendererFactory, RendererBackend
from map_solver_playground.map.render.element.element_renderer_factory import ElementRendererFactory

# Import the renderer initialization to register the renderers
import map_solver_playground.map.render.element.renderer_init

# Try to import SDL2 renderer if available
try:
    from map_solver_playground.map.render.element.sdl2_renderer import SDL2Renderer
    from map_solver_playground.map.render.element.sdl2_element_renderers import (
        SDL2TerrainRenderer,
        SDL2FlagRenderer,
        SDL2GeoPathRenderer,
    )
    __all__ = [
        "BaseRenderer", "BaseElementRenderer",
        "BaseFlagRenderer", "BaseGeoPathRenderer", "BaseTerrainRenderer",
        "PygameFlagRenderer", "PygameGeoPathRenderer", "PygameTerrainRenderer",
        "PygameRenderer", "SDL2Renderer", "RendererFactory", "RendererBackend",
        "ElementRendererFactory",
        "SDL2TerrainRenderer", "SDL2FlagRenderer", "SDL2GeoPathRenderer"
    ]
except ImportError:
    __all__ = [
        "BaseRenderer", "BaseElementRenderer",
        "BaseFlagRenderer", "BaseGeoPathRenderer", "BaseTerrainRenderer",
        "PygameFlagRenderer", "PygameGeoPathRenderer", "PygameTerrainRenderer",
        "PygameRenderer", "RendererFactory", "RendererBackend",
        "ElementRendererFactory"
    ]
