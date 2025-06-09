"""
Color utilities for map_solver_playground.

This module provides color-related utilities that are backend-independent.
"""

# Define common colors as RGB tuples
COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "gray": (128, 128, 128),
    "light_gray": (192, 192, 192),
    "dark_gray": (64, 64, 64),
}

def get_color(color_name: str) -> tuple[int, int, int]:
    """
    Get an RGB color tuple by name.
    
    Args:
        color_name: The name of the color
        
    Returns:
        A tuple of (r, g, b) values
        
    Raises:
        ValueError: If the color name is not recognized
    """
    if color_name in COLORS:
        return COLORS[color_name]
    else:
        raise ValueError(f"Unknown color: {color_name}")