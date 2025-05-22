"""
MapView component for displaying and managing map render in the application.
"""

from typing import Tuple, Optional, Dict

import pygame

from map_solver_playground.map.render.color_maps import ColorGradient, TerrainColorGradient
from map_solver_playground.map.render.element.renderer_factory import RendererFactory
from map_solver_playground.map.types import MapElement, Flag, Terrain

MAP_SIZE = 500
BLOCKS = 10
TERRAIN_ELEMENT_NAME = "terrain"


class MapView:
    """
    A UI component that handles the render and management of map.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        width: int,
        height: int,
        terrain: Terrain,
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
            terrain: The terrain element to use
            map_size: The size of the map (width and height)
            block_size: The size of blocks for the small map
            colormap: The color gradient to use for map render
        """
        self.screen: pygame.Surface = screen
        self.width: int = width
        self.height: int = height

        # Current view state
        self.current_view: int = 0  # 0 = original map, 1 = small map
        self.image_x: int = 0
        self.image_y: int = 0
        self.image: Optional[pygame.Surface] = None

        # Map elements
        self.map_elements: Dict[str, MapElement] = {}

        # Store the colormap
        self.colormap: TerrainColorGradient = colormap if colormap else ColorGradient.UNDEFINED

        # Add the terrain element to the map view
        self.add_element(TERRAIN_ELEMENT_NAME, terrain)

        # Initialize image
        self.image = None

    def switch_view(self) -> str:
        """
        Switch between original and small map views.

        Returns:
            str: A message describing the current view
        """
        self.current_view = 1 - self.current_view
        terrain = self.get_element(TERRAIN_ELEMENT_NAME)

        if self.current_view == 0:
            self.image = terrain.map_image
            message = "Showing original"
        else:
            self.image = terrain.small_map_image
            message = "Showing small map"

        self._center_image()
        return message

    def _center_image(self) -> None:
        """
        Center the current image on the screen.
        """
        if self.image is None:
            # Set default values for image position when image is not available yet
            self.image_x = self.width // 2
            self.image_y = self.height // 2
        else:
            self.image_x = self.width // 2 - self.image.get_width() // 2
            self.image_y = self.height // 2 - self.image.get_height() // 2

    def get_map_info(self) -> str:
        """
        Get information about the current map view.

        Returns:
            str: Information about the current map view
        """
        terrain = self.get_element(TERRAIN_ELEMENT_NAME)
        return terrain.get_map_info(self.current_view)

    @property
    def map(self):
        """
        Get the map object from the terrain element.

        Returns:
            Map: The map object
        """
        terrain = self.get_element(TERRAIN_ELEMENT_NAME)
        return terrain.map

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
        # Check if the image is available
        if self.image is None:
            # Return default values when image is not available
            return False, False, 0, 0

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
        for element_name, element in self.map_elements.items():
            # Only draw flags in high resolution view
            if self.current_view != 0 and isinstance(element, Flag):
                continue

            # Use the RendererFactory to render the element
            RendererFactory.render(self.screen, element, self.image_x, self.image_y, self.current_view)
