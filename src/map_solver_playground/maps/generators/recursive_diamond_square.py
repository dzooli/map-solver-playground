"""
Recursive Diamond-Square map generator module.

This module provides the RecursiveDiamondSquareGenerator class for generating maps
using a recursive implementation of the Diamond-Square algorithm.
"""

import math
import random

import numpy as np

from map_solver_playground.maps.generators.base_generator import MapGenerator, clamp_value
from map_solver_playground.maps.helpers import calculate_random_offset
from map_solver_playground.maps.map_data import Map


class RecursiveDiamondSquareGenerator(MapGenerator):
    """
    A map generator that uses a recursive implementation of the Diamond-Square algorithm.

    This class implements the MapGenerator interface to generate terrain
    using a recursive approach to the Diamond-Square algorithm.
    """

    def __init__(self, width: int, height: int, initial_roughness: float = 0.98):
        """
        Initialize a new Recursive Diamond-Square map generator.

        Args:
            width (int): The width of the map
            height (int): The height of the map
            initial_roughness (float): The initial roughness factor (default: 0.98)
        """
        super().__init__(width, height, initial_roughness)

    def generate_map(self) -> Map:
        """
        Generate a map using the recursive Diamond-Square algorithm.

        Returns:
            Map: The generated map
        """
        # Generate the heightmap using the recursive Diamond-Square algorithm
        map_data = self._generate_diamond_square()

        # Apply median filter and create map
        self.map = self._apply_median_filter(map_data)

        return self.map

    def _generate_diamond_square(self) -> np.ndarray:
        """
        Generate a heightmap using the recursive Diamond-Square algorithm.

        This is a recursive implementation of the Diamond-Square algorithm
        that generates terrain with height values between 0.0 and 1.0.

        Returns:
            np.ndarray: A 2D numpy array of height values between 0.0 and 1.0
        """
        # Calculate the size of the grid (power of 2 plus 1)
        size = self._calculate_grid_size()

        # Initialize the heightmap with random corner values
        heightmap = self._initialize_heightmap(size)

        # Start the recursive algorithm
        self._recursive_diamond_square(heightmap, 0, 0, size - 1, size - 1, self.initial_roughness)

        # Crop the heightmap to desired dimensions
        return self._crop_heightmap(heightmap, size)

    def _recursive_diamond_square(
        self, heightmap: np.ndarray, x1: int, y1: int, x2: int, y2: int, roughness: float
    ) -> None:
        """
        Recursively apply the diamond-square algorithm to a section of the heightmap.

        Args:
            heightmap (np.ndarray): The heightmap to modify
            x1 (int): The x-coordinate of the top-left corner
            y1 (int): The y-coordinate of the top-left corner
            x2 (int): The x-coordinate of the bottom-right corner
            y2 (int): The y-coordinate of the bottom-right corner
            roughness (float): The current roughness factor
        """
        # Calculate the width and height of the current section
        width = x2 - x1
        height = y2 - y1

        # Base case: if the section is too small, return
        if width <= 1 or height <= 1:
            return

        # Calculate the midpoint coordinates
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2

        random_offset = calculate_random_offset(self.initial_roughness, size=1)[0]

        # Diamond step: set the center point to the average of the four corners plus a random offset
        if math.isclose(heightmap[mid_y, mid_x], 0.0):  # Only set if not already set
            # Calculate average of the four corners
            avg_value = (heightmap[y1, x1] + heightmap[y1, x2] + heightmap[y2, x1] + heightmap[y2, x2]) / 4.0
            # Add random offset
            heightmap[mid_y, mid_x] = clamp_value(avg_value + random_offset)

        # Square step: set the midpoints of each edge
        # Top edge
        if math.isclose(heightmap[y1, mid_x], 0.0):
            # Calculate average of adjacent points
            avg_value = (heightmap[y1, x1] + heightmap[y1, x2] + heightmap[mid_y, mid_x]) / 3.0
            heightmap[y1, mid_x] = clamp_value(avg_value + random_offset)

        # Bottom edge
        if math.isclose(heightmap[y2, mid_x], 0.0):
            avg_value = (heightmap[y2, x1] + heightmap[y2, x2] + heightmap[mid_y, mid_x]) / 3.0
            heightmap[y2, mid_x] = clamp_value(avg_value + random_offset)

        # Left edge
        if math.isclose(heightmap[mid_y, x1], 0.0):
            avg_value = (heightmap[y1, x1] + heightmap[y2, x1] + heightmap[mid_y, mid_x]) / 3.0
            heightmap[mid_y, x1] = clamp_value(avg_value + random_offset)

        # Right edge
        if math.isclose(heightmap[mid_y, x2], 0.0):
            avg_value = (heightmap[y1, x2] + heightmap[y2, x2] + heightmap[mid_y, mid_x]) / 3.0
            heightmap[mid_y, x2] = clamp_value(avg_value + random_offset)

        # Reduce roughness for the next recursion level
        next_roughness = roughness * 0.5

        # Recursively apply the algorithm to the four sub-squares
        # Top-left square
        self._recursive_diamond_square(heightmap, x1, y1, mid_x, mid_y, next_roughness)
        # Top-right square
        self._recursive_diamond_square(heightmap, mid_x, y1, x2, mid_y, next_roughness)
        # Bottom-left square
        self._recursive_diamond_square(heightmap, x1, mid_y, mid_x, y2, next_roughness)
        # Bottom-right square
        self._recursive_diamond_square(heightmap, mid_x, mid_y, x2, y2, next_roughness)
