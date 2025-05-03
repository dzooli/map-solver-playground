"""
Map data representation module.

This module provides the Map class for representing 2D map data.
"""

from typing import List, Union

import numpy as np


class Map:
    """
    A class to represent 2D map data.

    This class stores a 2D numpy array of height values and provides methods
    for manipulating and accessing the map data.
    """

    def __init__(self, width: int, height: int, data: Union[List[List[float]]] | np.ndarray = None):
        """
        Initialize a new map with the specified dimensions.

        Args:
            width (int): The width of the map
            height (int): The height of the map
            data (Optional[Union[List[List[float]], np.ndarray]]): Initial map data, if provided.
                If a numpy array is provided, it will be used directly without copying.
                This means changes to the Map will affect the original array.
        """
        self.width: int = width
        self.height: int = height
        self.small_map = None

        if data is not None:
            # Convert list to numpy array if needed
            if isinstance(data, list):
                # Validate data dimensions
                if len(data) != height or any(len(row) != width for row in data):
                    raise ValueError("Data dimensions do not match specified width and height")
                self.data = np.array(data, dtype=np.float64)
            elif isinstance(data, np.ndarray):
                # Validate numpy array dimensions
                if data.shape != (height, width):
                    raise ValueError("Data dimensions do not match specified width and height")
                # Store the array directly without copying
                self.data = data
            else:
                raise TypeError("Invalid data type. Must be a list or numpy array.")
        else:
            # Initialize with zeros
            self.data = np.zeros((height, width), dtype=np.float64)

    def create_submap(self, block_size: int) -> "Map":
        """
        Create a smaller version of the map by averaging blocks of cells.

        Args:
            block_size (int): The size of each block to average

        Returns:
            Map: A new Map instance with the smaller map
        """
        # Calculate the dimensions of the smaller map
        small_width = self.width // block_size
        small_height = self.height // block_size

        # Create a new map for the smaller map
        self.small_map = Map(small_width, small_height)

        # Use numpy's reshape and mean functions for efficient block averaging
        # Handle the case where the map dimensions are not exact multiples of block_size
        valid_height = small_height * block_size
        valid_width = small_width * block_size

        # Extract the valid portion of the data that can be evenly divided into blocks
        valid_data = self.data[:valid_height, :valid_width]

        # Reshape the data to group blocks together, then compute the mean of each block
        # This reshapes the data to (small_height, block_size, small_width, block_size)
        # Then takes the mean over the block_size dimensions
        reshaped = valid_data.reshape(small_height, block_size, small_width, block_size)
        self.small_map.data = reshaped.mean(axis=(1, 3))

        return self.small_map

    @property
    def submap(self) -> np.ndarray | None:
        if not self.small_map:
            self.create_submap(self.width // 10)
        return self.small_map

    def apply_filter(self, filter_func):
        """
        Apply a filter function to the map data.

        Args:
            filter_func: A function that takes the map data (numpy array) and returns filtered data (numpy array)

        Returns:
            Map: A new Map instance with the filtered data
        """
        filtered_data = filter_func(self.data)
        return Map(self.width, self.height, filtered_data)

    def __str__(self) -> str:
        """Return a string representation of the map."""
        return f"Map({self.width}x{self.height})"

    def __repr__(self) -> str:
        """Return a string representation of the map."""
        return self.__str__()
