"""
MapView component for displaying and managing map visualization in the application.
"""

import pygame

from map_solver_playground.maps.generators import MapGenerator
from map_solver_playground.maps.generators.diamond_square import DiamondSquareGenerator
from map_solver_playground.maps.visualization.color_maps import ColorGradient
from map_solver_playground.maps.visualization.pygame_renderer import MapRenderer

MAP_SIZE = 500
BLOCKS = 10


class MapView:
    """
    A UI component that handles the visualization and management of maps.
    """

    def __init__(self, screen, width, height, map_size=MAP_SIZE, block_size=30, colormap=None):
        """
        Initialize the map view component.

        Args:
            screen: The pygame screen to draw on
            width: The width of the screen
            height: The height of the screen
            map_size: The size of the map (width and height)
            block_size: The size of blocks for the small map
            colormap: The color gradient to use for map visualization
        """
        self.screen = screen
        self.width = width
        self.height = height

        # Map properties
        self.map_width = self.map_height = map_size
        self.block_size = block_size
        self.colormap = colormap if colormap else ColorGradient.UNDEFINED

        # Map data and images
        self.map_generator = self.map_grayscale = self.map_image = None
        self.small_map_generator = self.small_map_grayscale = self.small_map_colored = self.small_map_image = None

        # Current view state
        self.current_view = 0  # 0 = original map, 1 = small map
        self.image_x = self.image_y = 0
        self.image = None

        # Create initial maps
        self.create_maps(self.colormap)
        self._center_image()

    def create_maps(
        self,
        colors,
        generator: MapGenerator = None,
    ):
        """
        Create and render maps with the specified color gradient.

        Args:
            :param colors: The color gradient to use for map visualization
            :param generator: The map generator to use for map generation, defaults to DiamondSquareGenerator
        """
        if colors is None:
            raise ValueError("Color map must be provided")

        # Create a map generator and generate a map
        self.map_width = self.map_height = MAP_SIZE
        self.map_generator = (
            generator
            if isinstance(generator, MapGenerator)
            else DiamondSquareGenerator(self.map_width, self.map_height)
        )
        self.map_generator.generate_map()
        self.map_grayscale = MapRenderer.to_pygame_image(self.map_generator.map)
        # Apply color mapping to the grayscale image
        self.map_image = MapRenderer.color_map(self.map_grayscale, colors)

        # Generate a smaller version of the map
        self.block_size = MAP_SIZE // BLOCKS
        self.small_map_generator = self.map_generator.generate_small_map(self.block_size)
        self.small_map_grayscale = MapRenderer.to_pygame_image(self.small_map_generator.map)
        # Apply color mapping to the small grayscale image
        self.small_map_colored = MapRenderer.color_map(self.small_map_grayscale, colors)

        # Scale the small map to the original map's size for better visibility
        self.small_map_image = MapRenderer.scale(self.small_map_colored, self.map_width, self.map_height)
        self.image = self.map_image

    def switch_view(self):
        """
        Switch between original and small map views.

        Returns:
            str: A message describing the current view
        """
        self.current_view = 1 - self.current_view
        if self.current_view == 0:
            self.image = self.map_image
            message = "Showing original"
        else:
            self.image = self.small_map_image
            message = "Showing small map"
        self._center_image()
        return message

    def _center_image(self):
        """
        Center the current image on the screen.
        """
        self.image_x = self.width // 2 - self.image.get_width() // 2
        self.image_y = self.height // 2 - self.image.get_height() // 2

    def get_map_info(self):
        """
        Get information about the current map view.

        Returns:
            str: Information about the current map view
        """
        if self.current_view == 0:
            return f"Original Map ({self.map_width}x{self.map_height}) with color mapping"
        else:
            small_width = self.map_width // self.block_size
            small_height = self.map_height // self.block_size
            return f"Small Map ({small_width}x{small_height}, block size: {self.block_size}) scaled to {self.map_width}x{self.map_height} with color mapping"

    def draw(self):
        """
        Draw the map view on the screen.
        """
        # Draw the image
        self.screen.blit(self.image, (self.image_x, self.image_y))

        # Draw a border around the map
        pygame.draw.rect(
            self.screen,
            pygame.color.THECOLORS["black"],
            (
                self.image_x,
                self.image_y,
                self.image.get_width(),
                self.image.get_height(),
            ),
            1,
        )
