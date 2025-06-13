"""
Test script for the new renderer interfaces.
"""

import sys
from loguru import logger

from map_solver_playground.map.render.renderer_backend import RendererBackend
from map_solver_playground.main import MapSolverApp

# Set up logging
logger.remove()  # Remove default handler
# Add a handler with a specific format to match the previous logging format
logger.add(sys.stderr, format="{time:YYYY-MM-DD HH:mm:ss} - mapsolver - {level} - {message}", level="DEBUG")


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
