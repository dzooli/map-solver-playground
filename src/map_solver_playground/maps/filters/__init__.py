"""
Map filter functions module.

This module provides filter functions for map data processing.
"""

from typing import List, Union

import numpy as np
from scipy import ndimage


def median_filter(data: Union[List[List[float]], np.ndarray], kernel_size: int = 3) -> np.ndarray:
    """
    Apply a median filter to the map data to reduce noise.

    Args:
        data (Union[List[List[float]], np.ndarray]): The 2D map data to filter.
            If a list is provided, it will be converted to a numpy array.
            If a numpy array is provided, it will be used directly without copying.
        kernel_size (int): Size of the filter kernel (must be odd). Defaults to 3.

    Returns:
        np.ndarray: The filtered map data
    """
    if kernel_size % 2 == 0:
        kernel_size += 1  # Ensure kernel size is odd

    # Convert to a numpy array if it's a list
    if isinstance(data, list):
        data_array = np.array(data, dtype=np.float64)
    else:
        # Use the array directly without copying
        data_array = data

    # Use scipy's optimized median filter implementation
    filtered_data = ndimage.median_filter(data_array, size=kernel_size, mode="reflect")

    return filtered_data
