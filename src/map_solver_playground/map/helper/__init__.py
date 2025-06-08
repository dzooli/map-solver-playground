import time
import numpy as np


def calculate_random_offset(roughness, size=None):
    """
    Generate random offset values for terrain generation algorithms.

    Creates random values centered around zero (range from -roughness/2 to +roughness/2)
    by shifting the random distribution and scaling by the roughness factor.

    Args:
        roughness (float): The maximum displacement value. Higher values create more
                          jagged/rough terrain.
        size (int or tuple, optional): The shape of the returned array. If None, a single
                                      value is returned. Defaults to None.

    Returns:
        numpy.ndarray or float: Random offset values with the specified size.
    """
    seed = int(time.time() * 1000) & 0xFFFFFFFF  # Convert to milliseconds and limit to 32 bits
    rng = np.random.default_rng(seed)

    return (rng.random(size) - 0.5) * roughness
