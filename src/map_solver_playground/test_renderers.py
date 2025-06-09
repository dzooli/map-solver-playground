"""
Test script for the new renderer interfaces.
"""

import sys
import logging

from map_solver_playground.map.render.renderer_backend import RendererBackend
from map_solver_playground.main import MapSolverApp

# Set up logging
logger = logging.getLogger("mapsolver")
logger.setLevel(logging.DEBUG)
logger.propagate = False

# Remove any existing handlers to avoid duplicate logging
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)


def test_pygame_renderer():
    """Test the Pygame renderer."""
    print("Testing Pygame renderer...")
    app = MapSolverApp(renderer_backend=RendererBackend.PYGAME)
    app.run()


def test_sdl2_renderer():
    """Test the SDL2 renderer."""
    print("Testing SDL2 renderer...")
    app = MapSolverApp(renderer_backend=RendererBackend.SDL2)
    app.run()


if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) > 1:
        renderer = sys.argv[1].lower()
        if renderer == "pygame":
            test_pygame_renderer()
        elif renderer == "sdl2":
            test_sdl2_renderer()
        else:
            print(f"Unknown renderer: {renderer}")
            print("Usage: python test_renderers.py [pygame|sdl2]")
    else:
        # Default to Pygame
        test_pygame_renderer()
