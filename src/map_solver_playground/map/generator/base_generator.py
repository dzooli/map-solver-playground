"""
Base map generator module.

This module provides the abstract base class for map generator.
"""

from abc import ABC, abstractmethod
import math
import numpy as np

from map_solver_playground.map.filter import median_filter
from map_solver_playground.map.map_data import Map
from map_solver_playground.map.helper import calculate_random_offset

# Constants
CORNER_COUNT = 4
RANDOM_SEED = 42

# Helper functions
clamp_value = lambda value: np.clip(value, 0.0, 1.0)


class MapGenerator(ABC):
    """
    Abstract base class for map generator.

    This class defines the interface for map generator and provides
    common functionality.
    """

    def __init__(self, width: int, height: int, initial_roughness: float = 0.98):
        """
        Initialize a new map generator with the specified dimensions.

        Args:
            width (int): The width of the map
            height (int): The height of the map
            initial_roughness (float): The initial roughness factor (default: 0.98)
        """
        self.width = width
        self.height = height
        self.initial_roughness = initial_roughness
        self.map = None

    @abstractmethod
    def generate_map(self) -> Map:
        """
        Generate a map using the specific algorithm.

        Returns:
            Map: The generated map
        """
        pass

    def _calculate_grid_size(self) -> int:
        """
        Calculate the size of the grid (power of 2 plus 1).

        Returns:
            int: Grid size that will fit the map dimensions
        """
        power = 0
        while 2**power < max(self.width, self.height):
            power += 1
        return 2**power + 1

    def _initialize_heightmap(self, size: int) -> np.ndarray:
        """
        Initialize the heightmap with zeros and set random corner values.

        Args:
            size: Size of the square heightmap

        Returns:
            np.ndarray: Initialized heightmap with random corner values
        """
        heightmap = np.zeros((size, size), dtype=np.float64)
        # Set the four corners to random values
        rnd_gen = np.random.default_rng(RANDOM_SEED)
        corners = rnd_gen.random(CORNER_COUNT)

        heightmap[0, 0] = corners[0]
        heightmap[0, size - 1] = corners[1]
        heightmap[size - 1, 0] = corners[2]
        heightmap[size - 1, size - 1] = corners[3]

        return heightmap

    def _get_unprocessed_square_points(self, heightmap: np.ndarray, size: int, step_size: int, half_step: int) -> list:
        """
        Find all unprocessed square points in the heightmap.

        Args:
            heightmap: Current heightmap
            size: Size of the square heightmap
            step_size: Current step size
            half_step: Half of the current step size

        Returns:
            List of (y, x) coordinates for unprocessed square points
        """
        square_points = []
        for y in range(0, size, half_step):
            x_start = half_step if y % step_size == 0 else 0
            for x in range(x_start, size, step_size):
                if math.isclose(heightmap[y, x], 0.0):  # Only process unset points
                    square_points.append((y, x))
        return square_points

    def _calculate_adjacent_point_averages(
        self, heightmap: np.ndarray, y_coords: np.ndarray, x_coords: np.ndarray, half_step: int, size: int
    ) -> np.ndarray:
        """
        Calculate the average values of valid adjacent points for each coordinate.

        Args:
            heightmap: Current heightmap
            y_coords: Array of y coordinates
            x_coords: Array of x coordinates
            half_step: Half of the current step size
            size: Size of the square heightmap

        Returns:
            Array of average values
        """
        # Create masks for valid adjacent points in each direction
        top_valid = y_coords - half_step >= 0
        bottom_valid = y_coords + half_step < size
        left_valid = x_coords - half_step >= 0
        right_valid = x_coords + half_step < size

        # Initialize arrays for sums and counts
        total_values = np.zeros(len(y_coords))
        valid_point_counts = np.zeros(len(y_coords))

        # Add values from valid adjacent points
        if np.any(top_valid):
            total_values[top_valid] += heightmap[y_coords[top_valid] - half_step, x_coords[top_valid]]
            valid_point_counts[top_valid] += 1

        if np.any(bottom_valid):
            total_values[bottom_valid] += heightmap[y_coords[bottom_valid] + half_step, x_coords[bottom_valid]]
            valid_point_counts[bottom_valid] += 1

        if np.any(left_valid):
            total_values[left_valid] += heightmap[y_coords[left_valid], x_coords[left_valid] - half_step]
            valid_point_counts[left_valid] += 1

        if np.any(right_valid):
            total_values[right_valid] += heightmap[y_coords[right_valid], x_coords[right_valid] + half_step]
            valid_point_counts[right_valid] += 1

        # Calculate and return averages
        return total_values / valid_point_counts

    def _crop_heightmap(self, heightmap: np.ndarray, size: int) -> np.ndarray:
        """
        Crop the heightmap to the desired dimensions.

        Args:
            heightmap: The heightmap to crop
            size: The size of the heightmap

        Returns:
            np.ndarray: The cropped heightmap
        """
        return heightmap[: min(self.height, size), : min(self.width, size)]

    def _apply_median_filter(self, map_data: np.ndarray) -> Map:
        """
        Apply median filter to the map data to reduce noise.

        Args:
            map_data: The map data to filter

        Returns:
            Map: The filtered map
        """
        # Create a new Map instance with the generated data
        map_obj = Map(self.width, self.height, map_data)

        # Apply median filter to reduce noise
        return map_obj.apply_filter(lambda data: median_filter(data, kernel_size=5))

    def generate_small_map(self, block_size: int) -> "MapGenerator":
        """
        Generate a smaller version of the map by averaging blocks of cells.

        Args:
            block_size (int): The size of each block to average

        Returns:
            MapGenerator: A new MapGenerator instance with the smaller map
        """
        if self.map is None:
            self.generate_map()

        # Create a smaller map by averaging blocks
        small_map = self.map.create_submap(block_size)

        # Create a new generator of the same type with the smaller map
        generator_class = self.__class__
        small_generator = generator_class(small_map.width, small_map.height)
        small_generator.map = small_map

        return small_generator
