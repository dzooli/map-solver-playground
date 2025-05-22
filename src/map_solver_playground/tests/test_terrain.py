"""
Test script for the Terrain class and TerrainRenderer.
"""

import pygame
import numpy as np

from map_solver_playground.map.map_data import Map
from map_solver_playground.map.types import Terrain
from map_solver_playground.components.map_view import MapView


def test_terrain():
    """
    Test the Terrain class and TerrainRenderer.
    """
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Terrain Test")

    # Create a map with some terrain data
    map_size = 256
    map_data = Map(map_size, map_size)

    # Generate some simple terrain data (a gradient)
    for y in range(map_size):
        for x in range(map_size):
            # Create a simple gradient pattern
            height = (x + y) / (2 * map_size)
            map_data.data[y, x] = height

    # Create a terrain element
    terrain = Terrain(map_data)

    # Create a map view with the terrain element
    map_view = MapView(screen, 800, 600, terrain)

    # Main loop
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the map view
        map_view.draw()

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    test_terrain()
