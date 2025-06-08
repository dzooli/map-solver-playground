"""
Terrain map element class.
"""

from typing import Optional, Tuple

import numpy as np
import pygame

from map_solver_playground.constants import DEFAULT_MAP_SIZE, DEFAULT_BLOCKS
from map_solver_playground.map.map_data import Map
from map_solver_playground.map.types.map_element import MapElement
from map_solver_playground.map.generator import MapGenerator
from map_solver_playground.map.generator.diamond_square import DiamondSquareGenerator
from map_solver_playground.map.render.color_maps import TerrainColorGradient
from map_solver_playground.map.render.renderer_backend import RendererBackend
from map_solver_playground.map.render.map_surface_renderer_factory import MapSurfaceRendererFactory


class Terrain(MapElement):
    """
    Terrain map element for representing terrain data on the map.
    """

    def __init__(
        self,
        map_data: Optional[Map] = None,
        visible: bool = True,
        map_size: int = DEFAULT_MAP_SIZE,
        block_size: int = 30,
        colormap: Optional[TerrainColorGradient] = None,
    ) -> None:
        """
        Initialize a terrain element.

        Args:
            map_data: The Map object containing terrain data
            visible: Whether the terrain is visible
            map_size: The size of the map (width and height)
            block_size: The size of blocks for the small map
            colormap: The color gradient to use for map render
        """
        super().__init__(visible)
        self._map_data = map_data
        self.map_width = map_size
        self.map_height = map_size
        self.block_size = block_size
        self.colormap = colormap

        # Map data and images
        self.map_generator: Optional[MapGenerator] = None
        self.map_grayscale: Optional[pygame.Surface] = None
        self.map_image: Optional[pygame.Surface] = None
        self.small_map_generator: Optional[MapGenerator] = None
        self.small_map_grayscale: Optional[pygame.Surface] = None
        self.small_map_colored: Optional[pygame.Surface] = None
        self.small_map_image: Optional[pygame.Surface] = None

    def create_maps(
        self,
        colors: TerrainColorGradient,
        generator: Optional[MapGenerator] = None,
        backend: RendererBackend = RendererBackend.PYGAME,
    ) -> None:
        """
        Create and render map with the specified color gradient.

        Args:
            :param colors: The color gradient to use for map render
            :param generator: The map generator to use for map generation, defaults to DiamondSquareGenerator
            :param backend: The renderer backend to use, defaults to PYGAME
        """
        if colors is None:
            raise ValueError("Color map must be provided")

        # Get the appropriate map surface renderer for the current backend
        renderer_class = MapSurfaceRendererFactory.get_map_surface_renderer(backend)

        # Create a map generator and generate a map
        # Use the instance variables map_width and map_height (already set in __init__)
        self.map_generator = (
            generator
            if isinstance(generator, MapGenerator)
            else DiamondSquareGenerator(self.map_width, self.map_height)
        )
        self.map_generator.generate_map()
        self.map_grayscale = renderer_class.to_surface(self.map_generator.map)
        # Apply color mapping to the grayscale image
        self.map_image = renderer_class.color_map(self.map_grayscale, colors)

        # Generate a smaller version of the map
        self.block_size = self.map_width // DEFAULT_BLOCKS
        self.small_map_generator = self.map_generator.generate_small_map(self.block_size)
        self.small_map_grayscale = renderer_class.to_surface(self.small_map_generator.map)
        # Apply color mapping to the small grayscale image
        self.small_map_colored = renderer_class.color_map(self.small_map_grayscale, colors)

        # Scale the small map to the original map's size for better visibility
        self.small_map_image = renderer_class.scale(self.small_map_colored, self.map_width, self.map_height)

        # Update the map_data property
        self._map_data = self.map_generator.map

    @property
    def map_data(self) -> Optional[Map]:
        """
        Get the map data of the terrain.

        Returns:
            Optional[Map]: The map data, or None if not set
        """
        return self._map_data

    @map_data.setter
    def map_data(self, value: Optional[Map]) -> None:
        """
        Set the map data of the terrain.

        Args:
            value: The new map data
        """
        self._map_data = value

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

    def get_map_info(self, current_view: int) -> str:
        """
        Get information about the current map view.

        Args:
            current_view: The current view index (0 for original, 1 for small map)

        Returns:
            str: Information about the current map view
        """
        if current_view == 0:
            return f"Original Map ({self.map_width}x{self.map_height}) with color mapping"
        else:
            small_width = self.map_width // self.block_size
            small_height = self.map_height // self.block_size
            return f"Small Map ({small_width}x{small_height}, block size: {self.block_size}) scaled to {self.map_width}x{self.map_height} with color mapping"

    def get_data(self) -> dict:
        """
        Get the data of the terrain.

        Returns:
            dict: The terrain data including map dimensions and visibility
        """
        if self._map_data is None:
            return {
                "width": 0,
                "height": 0,
                "visible": self.visible,
            }

        return {
            "width": self._map_data.width,
            "height": self._map_data.height,
            "visible": self.visible,
        }
