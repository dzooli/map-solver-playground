"""
SDL2-based implementation of the MapSolverApp.
"""

import logging

from map_solver_playground.main import MapSolverApp
from map_solver_playground.map.render.renderer_backend import RendererBackend


def main():
    """Run the SDL2-based MapSolverApp."""
    app = MapSolverApp(renderer_backend=RendererBackend.SDL2)
    app.run()


if __name__ == "__main__":
    main()
