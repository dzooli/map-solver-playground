"""
Image loading utilities for map_solver_playground.

This module provides functions for loading and processing images.
"""

import importlib.resources
import pygame


def load_image_with_transparency(image_name: str, target_size: tuple[int, int] = None) -> pygame.Surface:
    """
    Load a PNG image from assets package and create a pygame surface with transparency.

    Args:
        image_name: Name of the image file (including .png extension)
        target_size: Optional tuple of (width, height) to resize the image

    Returns:
        pygame.Surface with transparency enabled
    """
    with importlib.resources.path("map_solver_playground.assets", image_name) as path:
        image = pygame.image.load(str(path))
        if target_size:
            image = pygame.transform.scale(image, target_size)
        # Get color of top-left pixel
        transparent_color = image.get_at((0, 0))
        # Set that color as transparent
        image.set_colorkey(transparent_color)
        return image