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

# We'll import renderers on-demand through the ElementRendererFactory and RendererFactory
# instead of importing them unconditionally here.
# This prevents pygame from being initialized when using SDL2.

# Flag to track which renderers are available
PYGAME_AVAILABLE = False
SDL2_AVAILABLE = False

# Try to import SDL2 renderer if available, but don't register it yet
try:
    # Just check if the module is importable without actually importing it
    import sdl2.ext
    SDL2_AVAILABLE = True
except ImportError:
    pass

# Try to check if pygame is available, but don't import or initialize it yet
try:
    # Just check if the module is importable without actually importing it
    import importlib.util
    spec = importlib.util.find_spec('pygame')
    PYGAME_AVAILABLE = spec is not None
except ImportError:
    pass
