"""
Backend-independent image loading utilities for map_solver_playground.

This module provides functions for loading and processing images that work with any renderer backend.
"""

import importlib.resources
import tempfile
from typing import Any, Tuple, Optional

from map_solver_playground.map.render.element.renderer_factory import RendererFactory


class SDL2TextureWrapper:
    """Wrapper for SDL2 textures to provide a consistent interface."""

    def __init__(self, texture, width, height):
        self.texture = texture
        self._width = width
        self._height = height

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height


def wrap_sdl2_texture(image, target_size=None):
    """Wrap SDL2 texture in a wrapper that provides width and height methods."""
    from sdl2.ext.renderer import Texture

    if isinstance(image, Texture):
        width = target_size[0] if target_size else 30
        height = target_size[1] if target_size else 30
        return SDL2TextureWrapper(image, width, height)
    return image


def _process_image_with_pil(path_str, target_size):
    """Process image with PIL as a fallback method."""
    from PIL import Image

    img = Image.open(path_str)
    if target_size:
        img = img.resize(target_size)
    img = img.convert("RGBA")

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        tmp_path = tmp.name
    img.save(tmp_path)

    return tmp_path


def _load_and_wrap_image(renderer_class, path_str, target_size):
    """Load image with renderer and wrap it if it's an SDL2 texture."""
    image = renderer_class.load_image(path_str, target_size)
    if renderer_class.__name__ == "SDL2Renderer":
        return wrap_sdl2_texture(image, target_size)
    return image


def load_image_with_transparency(image_name: str, target_size: Optional[Tuple[int, int]] = None) -> Any:
    """
    Load a PNG image from assets package and create an image with transparency.
    This function works with any renderer backend.

    Args:
        image_name: Name of the image file (including .png extension)
        target_size: Optional tuple of (width, height) to resize the image

    Returns:
        An image object compatible with the current renderer backend

    Raises:
        ValueError: If the image cannot be loaded
    """
    with importlib.resources.path("map_solver_playground.assets", image_name) as path:
        path_str = str(path)
        renderer_class = RendererFactory.get_current_renderer()

        # First attempt: try direct loading
        try:
            return _load_and_wrap_image(renderer_class, path_str, target_size)
        except Exception as e:
            # Check if this is a transparency-related error
            error_msg = str(e)
            needs_transparency_fix = (
                "could not broadcast input array from shape" in error_msg
                and "3) into shape" in error_msg
                and "4)" in error_msg
            )

            if not needs_transparency_fix:
                raise ValueError(f"Failed to load image {image_name}: {error_msg}")

            # Second attempt: process with PIL for transparency
            try:
                tmp_path = _process_image_with_pil(path_str, target_size)
                return _load_and_wrap_image(renderer_class, tmp_path, target_size)
            except Exception as e2:
                raise ValueError(f"Failed to load image {image_name}: {str(e2)}")
