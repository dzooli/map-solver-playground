"""
Initialize the renderer factory with the available renderers.
"""

from map_solver_playground.map.render.element.pygame_renderer import PygameRenderer
from map_solver_playground.map.render.element.renderer_factory import RendererFactory, RendererBackend

# Register the Pygame renderer
RendererFactory.register_renderer(RendererBackend.PYGAME, PygameRenderer)

# Try to register the SDL2 renderer if available
try:
    from map_solver_playground.map.render.element.sdl2_renderer import SDL2Renderer
    RendererFactory.register_renderer(RendererBackend.SDL2, SDL2Renderer)
except ImportError:
    # SDL2 is not available, so we can't register the SDL2 renderer
    pass
