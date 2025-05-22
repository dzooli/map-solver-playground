"""
MapView component for displaying and managing map render in the application.
"""

from typing import List, Tuple, Optional, Dict

import pygame

from map_solver_playground.map.render.pygame_renderer import MapRenderer
from map_solver_playground.map.types import MapElement, Flag, GeoPath, Terrain
from map_solver_playground.map.generator import MapGenerator, DiamondSquareGenerator
from map_solver_playground.map.render.element import FlagRenderer, GeoPathRenderer
from map_solver_playground.map.render.element.renderer_factory import RendererFactory
from map_solver_playground.map.render.color_maps import ColorGradient, TerrainColorGradient

MAP_SIZE = 500
BLOCKS = 10


class MapView:
    """
    A UI component that handles the render and management of map.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        width: int,
        height: int,
        map_size: int = MAP_SIZE,
        block_size: int = 30,
        colormap: Optional[TerrainColorGradient] = None,
    ) -> None:
        """
        Initialize the map view component.

        Args:
            screen: The pygame screen to draw on
            width: The width of the screen
            height: The height of the screen
            map_size: The size of the map (width and height)
            block_size: The size of blocks for the small map
            colormap: The color gradient to use for map render
        """
        self.screen: pygame.Surface = screen
        self.width: int = width
        self.height: int = height

        # Map properties
        self.map_width: int = map_size
        self.map_height: int = map_size
        self.block_size: int = block_size
        self.colormap: TerrainColorGradient = colormap if colormap else ColorGradient.UNDEFINED

        # Map data and images
        self.map_generator: Optional[MapGenerator] = None
        self.map_grayscale: Optional[pygame.Surface] = None
        self.map_image: Optional[pygame.Surface] = None
        self.small_map_generator: Optional[MapGenerator] = None
        self.small_map_grayscale: Optional[pygame.Surface] = None
        self.small_map_colored: Optional[pygame.Surface] = None
        self.small_map_image: Optional[pygame.Surface] = None

        # Current view state
        self.current_view: int = 0  # 0 = original map, 1 = small map
        self.image_x: int = 0
        self.image_y: int = 0
        self.image: Optional[pygame.Surface] = None

        # Map elements
        self.map_elements: Dict[str, MapElement] = {}

        # Create initial map
        self.create_maps(self.colormap)
        self._center_image()

    def create_maps(
        self,
        colors: TerrainColorGradient,
        generator: Optional[MapGenerator] = None,
    ) -> None:
        """
        Create and render map with the specified color gradient.

        Args:
            :param colors: The color gradient to use for map render
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

    def switch_view(self) -> str:
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

    def _center_image(self) -> None:
        """
        Center the current image on the screen.
        """
        self.image_x = self.width // 2 - self.image.get_width() // 2
        self.image_y = self.height // 2 - self.image.get_height() // 2

    def get_map_info(self) -> str:
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

    @property
    def map(self):
        """
        Get the map object from the map generator.

        Returns:
            Map: The map object
        """
        if self.map_generator:
            return self.map_generator.map
        return None

    def is_within_safe_area(
        self, pos: Tuple[int, int], sprite_width: int, sprite_height: int
    ) -> Tuple[bool, bool, int, int]:
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
        # Check if the click is within map boundaries
        map_width, map_height = self.image.get_width(), self.image.get_height()

        # Calculate the safe area where sprites can be placed without exceeding map boundaries
        # The sprite is centered on the click position, so we need to ensure it's at least half the sprite size away from edges
        safe_x_min = self.image_x + sprite_width // 2
        safe_x_max = self.image_x + map_width - sprite_width // 2
        safe_y_min = self.image_y + sprite_height // 2
        safe_y_max = self.image_y + map_height - sprite_height // 2

        # Check if position is within safe area
        is_within_safe_area = safe_x_min <= pos[0] <= safe_x_max and safe_y_min <= pos[1] <= safe_y_max

        # Check if the position is within map boundaries
        is_within_map = (
            self.image_x <= pos[0] <= self.image_x + map_width and self.image_y <= pos[1] <= self.image_y + map_height
        )

        # Calculate coordinates relative to map's upper left corner
        rel_x = pos[0] - self.image_x
        rel_y = pos[1] - self.image_y

        return is_within_safe_area, is_within_map, rel_x, rel_y

    def screen_to_map_pos(
        self, rel_pos: Optional[Tuple[int, int]], sprite_width: int, sprite_height: int
    ) -> Optional[Tuple[int, int]]:
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

    def get_element(self, name: str) -> MapElement:
        """
        Get a map element by its name.

        Args:
            name: The name of the element to get

        Returns:
            MapElement: The map element with the specified name

        Raises:
            ValueError: If no element with the specified name is found
        """
        if name in self.map_elements:
            return self.map_elements[name]
        raise ValueError(f"No element found with name: {name}")

    def add_element(self, name: str, element: MapElement) -> None:
        """
        Add a map element to the map view.

        Args:
            name: The name to associate with the element
            element: The map element to add

        Raises:
            ValueError: If an element with the specified name already exists
        """
        if name in self.map_elements:
            raise ValueError(f"An element with name '{name}' already exists")
        self.map_elements[name] = element

    def draw(self) -> None:
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

        # Draw all map elements using the RendererFactory
        for element_name, element in self.map_elements.items():
            # Only draw flags in high resolution view
            if self.current_view != 0 and isinstance(element, Flag):
                continue

            # Use the RendererFactory to render the element
            RendererFactory.render(self.screen, element, self.image_x, self.image_y)
