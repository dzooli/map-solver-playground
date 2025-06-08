"""
Diamond-Square map generator module.

This module provides the DiamondSquareGenerator class for generating map
using the Diamond-Square algorithm.
"""

import math
import time

import numpy as np

from map_solver_playground.map.generator.base_generator import MapGenerator, CORNER_COUNT, clamp_value
from map_solver_playground.map.helper import calculate_random_offset
from map_solver_playground.map.map_data import Map


class DiamondSquareGenerator(MapGenerator):
    """
    A map generator that uses the Diamond-Square algorithm.

    This class implements the MapGenerator interface to generate terrain
    using the Diamond-Square algorithm.
    """

    def __init__(self, width: int, height: int, initial_roughness: float = 0.98):
        """
        Initialize a new Diamond-Square map generator.

        Args:
            width (int): The width of the map
            height (int): The height of the map
            initial_roughness (float): The initial roughness factor (default: 0.98)
        """
        super().__init__(width, height, initial_roughness)

    def generate_map(self) -> Map:
        """
        Generate a map using the Diamond-Square algorithm.

        Returns:
            Map: The generated map
        """
        # Generate the heightmap using the Diamond-Square algorithm
        map_data = self._generate_diamond_square()

        # Apply median filter and create map
        self.map = self._apply_median_filter(map_data)

        return self.map

    def _generate_diamond_square(self) -> np.ndarray:
        """
        Generate a heightmap using the Diamond-Square algorithm.

        This is a numpy-based implementation that generates terrain
        with height values between 0.0 and 1.0.

        Returns:
            np.ndarray: A 2D numpy array of height values between 0.0 and 1.0
        """
        # Main algorithm execution
        size = self._calculate_grid_size()
        heightmap = self._initialize_heightmap(size)
        heightmap = self._apply_diamond_square_algorithm(heightmap, size, self.initial_roughness)

        # Crop the heightmap to desired dimensions
        return self._crop_heightmap(heightmap, size)

    def _apply_diamond_square_algorithm(self, heightmap: np.ndarray, size: int, roughness: float) -> np.ndarray:
        """
        Apply the diamond-square algorithm to the heightmap.

        This is a vectorized implementation that processes the map in decreasing step sizes.

        Args:
            heightmap: Initial heightmap with corner values set
            size: Size of the square heightmap
            roughness: Initial roughness factor

        Returns:
            np.ndarray: Heightmap with diamond-square algorithm applied
        """
        step_size = size - 1

        while step_size > 1:
            half_step = step_size // 2

            # Diamond step - set center points of each square
            self._perform_diamond_step(heightmap, size, step_size, half_step, roughness)

            # Square step - set midpoints of the edges of each square
            self._perform_square_step(heightmap, size, step_size, half_step, roughness)

            # Reduce roughness for the next iteration
            roughness *= 0.5
            step_size = half_step

        return heightmap

    def _perform_diamond_step(
        self, heightmap: np.ndarray, size: int, step_size: int, half_step: int, roughness: float
    ) -> None:
        """
        Perform the diamond step of the algorithm.

        Sets the center points of each square to the average of the four corners plus a random offset.

        Args:
            heightmap: Current heightmap
            size: Size of the square heightmap
            step_size: Current step size
            half_step: Half of the current step size
            roughness: Current roughness factor
        """
        # Create arrays of y and x coordinates for all diamond points
        y_coords = np.arange(half_step, size, step_size)
        x_coords = np.arange(half_step, size, step_size)

        # Create meshgrid for all diamond points
        y_grid, x_grid = np.meshgrid(y_coords, x_coords, indexing="ij")

        # Flatten the coordinate arrays for easier indexing
        y_flat = y_grid.flatten()
        x_flat = x_grid.flatten()

        if len(y_flat) > 0:  # Only proceed if there are points to process
            # Calculate the four corner indices for each diamond point
            top_left_y = y_flat - half_step
            top_left_x = x_flat - half_step

            top_right_y = y_flat - half_step
            top_right_x = x_flat + half_step

            bottom_left_y = y_flat + half_step
            bottom_left_x = x_flat - half_step

            bottom_right_y = y_flat + half_step
            bottom_right_x = x_flat + half_step

            # Get values at the four corners for each diamond point
            top_left_vals = heightmap[top_left_y, top_left_x]
            top_right_vals = heightmap[top_right_y, top_right_x]
            bottom_left_vals = heightmap[bottom_left_y, bottom_left_x]
            bottom_right_vals = heightmap[bottom_right_y, bottom_right_x]

            # Calculate average of the four corners
            avg_vals = (top_left_vals + top_right_vals + bottom_left_vals + bottom_right_vals) / CORNER_COUNT

            # Generate random offsets for all points at once
            random_offsets = calculate_random_offset(roughness, size=len(y_flat))

            # Set the values in the heightmap
            heightmap[y_flat, x_flat] = clamp_value(avg_vals + random_offsets)

    def _perform_square_step(
        self, heightmap: np.ndarray, size: int, step_size: int, half_step: int, roughness: float
    ) -> None:
        """
        Perform the square step of the Diamond-Square algorithm.
        Sets the midpoints of each edge to the average of adjacent points plus a random offset.

        Args:
            heightmap: Current heightmap
            size: Size of the square heightmap
            step_size: Current step size
            half_step: Half of the current step size
            roughness: Current roughness factor
        """
        # Identify unprocessed square points
        square_points = self._get_unprocessed_square_points(heightmap, size, step_size, half_step)

        if not square_points:
            return  # No points to process

        square_y, square_x = zip(*square_points)
        square_y = np.array(square_y)
        square_x = np.array(square_x)

        # Calculate average values from adjacent points
        avg_values = self._calculate_adjacent_point_averages(heightmap, square_y, square_x, half_step, size)

        # Apply random offsets and update heightmap
        random_offsets = calculate_random_offset(roughness, size=len(square_y))
        heightmap[square_y, square_x] = clamp_value(avg_values + random_offsets)
