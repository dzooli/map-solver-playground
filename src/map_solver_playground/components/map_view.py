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
        self.map_generator: MapGenerator | None = None
        self.map_grayscale = self.map_image = None
        self.small_map_generator: MapGenerator | None = None
        self.small_map_grayscale = self.small_map_colored = self.small_map_image = None

        # Current view state
        self.current_view = 0  # 0 = original map, 1 = small map
        self.image_x = self.image_y = 0
        self.image = None

        # Flag positions and resources
        self.red_flag_pos = None
        self.green_flag_pos = None
        self.red_flag_img = None
        self.green_flag_img = None

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

    def is_within_safe_area(self, pos, sprite_width, sprite_height):
        """
        Check if the given position is within the safe area of the map.
        The safe area is defined as the area where a sprite can be placed without exceeding map boundaries.

        Args:
            pos: The (x, y) position to check
            sprite_width: The width of the sprite
            sprite_height: The height of the sprite

        Returns:
            tuple: (is_within_safe_area, is_within_map, rel_x, rel_y)
                is_within_safe_area: True if the position is within the safe area
                is_within_map: True if the position is within the map boundaries
                rel_x: The x-coordinate relative to the map's upper left corner
                rel_y: The y-coordinate relative to the map's upper left corner
        """
        # Check if click is within map boundaries
        map_width, map_height = self.image.get_width(), self.image.get_height()

        # Calculate the safe area where sprites can be placed without exceeding map boundaries
        # The sprite is centered on the click position, so we need to ensure it's at least half the sprite size away from edges
        safe_x_min = self.image_x + sprite_width // 2
        safe_x_max = self.image_x + map_width - sprite_width // 2
        safe_y_min = self.image_y + sprite_height // 2
        safe_y_max = self.image_y + map_height - sprite_height // 2

        # Check if position is within safe area
        is_within_safe_area = safe_x_min <= pos[0] <= safe_x_max and safe_y_min <= pos[1] <= safe_y_max

        # Check if position is within map boundaries
        is_within_map = (
            self.image_x <= pos[0] <= self.image_x + map_width and self.image_y <= pos[1] <= self.image_y + map_height
        )

        # Calculate coordinates relative to map's upper left corner
        rel_x = pos[0] - self.image_x
        rel_y = pos[1] - self.image_y

        return is_within_safe_area, is_within_map, rel_x, rel_y

    def screen_to_map_pos(self, rel_pos, sprite_width, sprite_height):
        """
        Convert relative map position to screen position for sprite placement.

        Args:
            rel_pos: The (x, y) position relative to the map's upper left corner
            sprite_width: The width of the sprite
            sprite_height: The height of the sprite

        Returns:
            tuple: The (x, y) screen position for the sprite
        """
        if rel_pos is None:
            return None

        screen_x = self.image_x + rel_pos[0] - sprite_width // 2
        screen_y = self.image_y + rel_pos[1] - sprite_height // 2
        return screen_x, screen_y

    def set_flag_images(self, red_flag_img, green_flag_img):
        """
        Set the flag images to be used for drawing.

        Args:
            red_flag_img: The red flag image
            green_flag_img: The green flag image
        """
        self.red_flag_img = red_flag_img
        self.green_flag_img = green_flag_img

    def set_flag_positions(self, red_flag_pos, green_flag_pos):
        """
        Set the positions of the flags.

        Args:
            red_flag_pos: The position of the red flag (x, y) relative to the map
            green_flag_pos: The position of the green flag (x, y) relative to the map
        """
        self.red_flag_pos = red_flag_pos
        self.green_flag_pos = green_flag_pos

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

        # Draw flags if in high resolution view and flag images are set
        if self.current_view == 0 and self.red_flag_img and self.green_flag_img:
            # Draw red flag if position is set
            if self.red_flag_pos:
                screen_pos = self.screen_to_map_pos(
                    self.red_flag_pos, self.red_flag_img.get_width(), self.red_flag_img.get_height()
                )
                self.screen.blit(self.red_flag_img, screen_pos)

            # Draw green flag if position is set
            if self.green_flag_pos:
                screen_pos = self.screen_to_map_pos(
                    self.green_flag_pos, self.green_flag_img.get_width(), self.green_flag_img.get_height()
                )
                self.screen.blit(self.green_flag_img, screen_pos)
