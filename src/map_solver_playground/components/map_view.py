"""
MapView component for displaying and managing map render in the application.
"""

from typing import Tuple, Optional, Dict

from map_solver_playground.components.widget import Widget
from map_solver_playground.constants import DEFAULT_MAP_SIZE, DEFAULT_BLOCKS
from map_solver_playground.map.render.color_maps import ColorGradient, TerrainColorGradient
from map_solver_playground.map.render.element.renderer_factory import RendererFactory
from map_solver_playground.map.types import MapElement, Flag, Terrain

TERRAIN_ELEMENT_NAME = "terrain"


class MapView(Widget):
    """
    A UI component that handles the render and management of map.
    """

    def __init__(
        self,
        renderer,
        screen_width: int,
        screen_height: int,
        terrain: Terrain,
        map_size: int = DEFAULT_MAP_SIZE,
        block_size: int = 30,
        colormap: Optional[TerrainColorGradient] = None,
        x: int = 0,
        y: int = 0,
    ) -> None:
        """
        Initialize the map view component.

        Args:
            renderer: The renderer to use for drawing
            screen_width: The width of the screen
            screen_height: The height of the screen
            terrain: The terrain element to use
            map_size: The size of the map (width and height)
            block_size: The size of blocks for the small map
            colormap: The color gradient to use for map render
            x: The x-coordinate of the MapView's position on the screen
            y: The y-coordinate of the MapView's position on the screen
        """
        position = (x, y)
        size = (screen_width, screen_height)  # Using screen dimensions as default size
        super().__init__(renderer, screen_width, screen_height, position, size)

        # For backward compatibility, maintain x and y properties
        self._x: int = x
        self._y: int = y

        # Current view state
        self.current_view: int = 0  # 0 = original map, 1 = small map

        # Map elements
        self.map_elements: Dict[str, MapElement] = {}

        # Store the colormap
        self.colormap: TerrainColorGradient = colormap if colormap else ColorGradient.UNDEFINED

        # Add the terrain element to the map view
        self.add_element(TERRAIN_ELEMENT_NAME, terrain)

    @property
    def x(self) -> int:
        """Get the x-coordinate of the MapView's position."""
        return self.position[0]

    @x.setter
    def x(self, value: int) -> None:
        """Set the x-coordinate of the MapView's position."""
        self._x = value
        self.position = (value, self.position[1])

    @property
    def y(self) -> int:
        """Get the y-coordinate of the MapView's position."""
        return self.position[1]

    @y.setter
    def y(self, value: int) -> None:
        """Set the y-coordinate of the MapView's position."""
        self._y = value
        self.position = (self.position[0], value)

    def switch_view(self) -> str:
        """
        Switch between original and small map views.

        Returns:
            str: A message describing the current view
        """
        self.current_view = 1 - self.current_view

        if self.current_view == 0:
            message = "Showing original"
        else:
            message = "Showing small map"

        return message

    def set_view(self, view_index: int) -> None:
        """
        Set the current view to the specified index.

        Args:
            view_index: The view index to set (0 for original, 1 for small map)
        """
        if view_index in (0, 1):
            self.current_view = view_index

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
        # Adjust position to be relative to the MapView's position
        adjusted_pos = (pos[0] - self.position[0], pos[1] - self.position[1])

        # Calculate the safe area where sprites can be placed without exceeding map boundaries
        # The sprite is centered on the click position, so we need to ensure it's at least half the sprite size away from edges
        if self.map is not None:
            map_width = self.map.width
            map_height = self.map.height
            safe_x_min = sprite_width // 2
            safe_x_max = map_width - sprite_width // 2
            safe_y_min = sprite_height // 2
            safe_y_max = map_height - sprite_height // 2
        else:
            # If no map is available, use the MapView dimensions
            safe_x_min = sprite_width // 2
            safe_x_max = self.screen_width - sprite_width // 2
            safe_y_min = sprite_height // 2
            safe_y_max = self.screen_height - sprite_height // 2

        # Check if position is within safe area
        is_within_safe_area = (
            safe_x_min <= adjusted_pos[0] <= safe_x_max and safe_y_min <= adjusted_pos[1] <= safe_y_max
        )

        # Check if the position is within map boundaries
        if self.map is not None:
            map_width = self.map.width
            map_height = self.map.height
            # Account for sprite size to ensure it's fully within map boundaries
            is_within_map = (
                sprite_width // 2 <= adjusted_pos[0] <= map_width - sprite_width // 2
                and sprite_height // 2 <= adjusted_pos[1] <= map_height - sprite_height // 2
            )
        else:
            # If no map is available, use the MapView dimensions
            is_within_map = (
                sprite_width // 2 <= adjusted_pos[0] <= self.screen_width - sprite_width // 2
                and sprite_height // 2 <= adjusted_pos[1] <= self.screen_height - sprite_height // 2
            )

        # Calculate coordinates relative to map's upper left corner (which is now at 0,0)
        rel_x = adjusted_pos[0]
        rel_y = adjusted_pos[1]

        return is_within_safe_area, is_within_map, rel_x, rel_y

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
        if not self.visible:
            return

        for element_name, element in self.map_elements.items():
            # Only draw flags in high resolution view
            if self.current_view != 0 and isinstance(element, Flag):
                continue

            # Use the RendererFactory to render the element
            # image_x and image_y are now 0, representing the origin of the upper-left corner of the view
            RendererFactory.render(self.renderer, element, self.position[0], self.position[1], self.current_view)
