"""
Utility functions for creating SDL2 textures without pygame dependency.
"""

import numpy as np
import sdl2
import sdl2.ext
from sdl2.ext.renderer import Texture
from PIL import Image


def create_texture_from_array(array: np.ndarray, renderer: sdl2.ext.Renderer) -> sdl2.ext.Texture:
    """
    Create an SDL2 texture directly from a numpy array.

    Args:
        array: A numpy array with shape (height, width, 3) or (height, width, 4) for RGB or RGBA data
        renderer: The SDL2 renderer to create the texture with

    Returns:
        An SDL2 texture
    """
    # Get array dimensions
    if len(array.shape) == 3:
        height, width, channels = array.shape
    else:
        raise ValueError("Array must have 3 dimensions (height, width, channels)")

    # Ensure the array is in the correct format (uint8)
    if array.dtype != np.uint8:
        array = array.astype(np.uint8)

    # Convert RGB to RGBA if needed
    if channels == 3:
        # Create a new RGBA array with full opacity
        rgba_array = np.zeros((height, width, 4), dtype=np.uint8)
        rgba_array[:, :, 0:3] = array  # Copy RGB channels
        rgba_array[:, :, 3] = 255  # Set alpha to fully opaque
        array = rgba_array
        channels = 4

    # Create an SDL2 surface with the appropriate format for RGBA
    rmask = 0x000000FF
    gmask = 0x0000FF00
    bmask = 0x00FF0000
    amask = 0xFF000000
    depth = 32
    pitch = width * 4

    # Create the SDL2 surface
    sdl_surface = sdl2.SDL_CreateRGBSurface(0, width, height, depth, rmask, gmask, bmask, amask)
    sdl_surface_contents = sdl_surface.contents

    # Get the raw pixel buffer from the surface
    pixels_ptr = sdl_surface_contents.pixels
    pixels_size = height * width * 4  # RGBA = 4 bytes per pixel

    # Create a ctypes array from the pixel buffer
    from ctypes import c_ubyte, cast, POINTER
    pixels_array = cast(pixels_ptr, POINTER(c_ubyte * pixels_size)).contents

    # Copy the pixel data from the numpy array to the surface
    # We need to convert from HWC format to a flat buffer in the correct order
    for y in range(height):
        for x in range(width):
            # Calculate the offset in the flat buffer
            offset = (y * width + x) * 4
            # Copy the pixel data (RGBA)
            pixels_array[offset] = array[y, x, 0]  # R
            pixels_array[offset + 1] = array[y, x, 1]  # G
            pixels_array[offset + 2] = array[y, x, 2]  # B
            if channels == 4:
                pixels_array[offset + 3] = array[y, x, 3]  # A
            else:
                pixels_array[offset + 3] = 255  # Full opacity

    # Create a texture from the surface
    from sdl2.ext.renderer import Texture
    texture = Texture(renderer, sdl_surface)

    # Free the surface (it's been copied to the texture)
    sdl2.SDL_FreeSurface(sdl_surface)

    return texture


def create_grayscale_texture(array: np.ndarray, renderer: sdl2.ext.Renderer) -> sdl2.ext.Texture:
    """
    Create an SDL2 texture from a grayscale numpy array.

    Args:
        array: A numpy array with shape (height, width) containing grayscale values
        renderer: The SDL2 renderer to create the texture with

    Returns:
        An SDL2 texture
    """
    # Get array dimensions
    if len(array.shape) == 2:
        height, width = array.shape
    else:
        raise ValueError("Array must have 2 dimensions (height, width)")

    # Normalize the array to 0-255 range if needed
    if array.dtype != np.uint8:
        if array.max() <= 1.0:
            array = (array * 255).astype(np.uint8)
        else:
            array = array.astype(np.uint8)

    # Convert grayscale to RGB
    rgb_array = np.stack([array] * 3, axis=-1)

    # Create texture from RGB array
    return create_texture_from_array(rgb_array, renderer)


def create_colored_texture_from_grayscale(
    array: np.ndarray, color_map: list, renderer: sdl2.ext.Renderer
) -> sdl2.ext.Texture:
    """
    Create a colored SDL2 texture from a grayscale numpy array using a color map.

    Args:
        array: A numpy array with shape (height, width) containing grayscale values
        color_map: A list of RGB tuples representing the color map
        renderer: The SDL2 renderer to create the texture with

    Returns:
        An SDL2 texture
    """
    # Get array dimensions
    if len(array.shape) == 2:
        height, width = array.shape
    else:
        raise ValueError("Array must have 2 dimensions (height, width)")

    # Convert color_map to a numpy array for faster indexing
    color_map_np = np.array(color_map, dtype=np.uint8)

    # Normalize the array to 0-1 range if needed
    if array.dtype != np.float32 and array.dtype != np.float64:
        array = array.astype(np.float32) / 255.0

    # Map the normalized values to indices in the color map
    # Scale to the range [0, len(color_map)-1] and clip to valid indices
    color_indices = np.clip((array * (len(color_map) - 1)).astype(np.int32), 0, len(color_map) - 1)

    # Create a new RGB array by mapping each index to its color
    mapped_colors = color_map_np[color_indices]

    # Create texture from RGB array
    return create_texture_from_array(mapped_colors, renderer)


def surface_to_pil_image(surface) -> Image.Image:
    """
    Convert an SDL2 surface to a PIL Image.

    Args:
        surface: The SDL2 surface to convert

    Returns:
        A PIL Image
    """
    # Get surface dimensions and format
    if hasattr(surface, "w") and hasattr(surface, "h"):
        width, height = surface.w, surface.h
    elif hasattr(surface, "contents") and hasattr(surface.contents, "w") and hasattr(surface.contents, "h"):
        width, height = surface.contents.w, surface.contents.h
    else:
        raise ValueError(f"Cannot determine dimensions of surface: {type(surface)}")

    # Create a numpy array to hold the pixel data
    pixel_data = np.zeros((height, width, 4), dtype=np.uint8)

    # Get the pixel data from the surface
    from ctypes import c_ubyte, cast, POINTER

    if hasattr(surface, "pixels"):
        pixels_ptr = surface.pixels
    elif hasattr(surface, "contents") and hasattr(surface.contents, "pixels"):
        pixels_ptr = surface.contents.pixels
    else:
        raise ValueError(f"Cannot access pixels of surface: {type(surface)}")

    # Calculate the size of the pixel buffer
    pixels_size = height * width * 4  # RGBA = 4 bytes per pixel

    # Create a ctypes array from the pixel buffer
    pixels_array = cast(pixels_ptr, POINTER(c_ubyte * pixels_size)).contents

    # Copy the pixel data to the numpy array
    for y in range(height):
        for x in range(width):
            # Calculate the offset in the flat buffer
            offset = (y * width + x) * 4
            # Copy the pixel data (RGBA)
            pixel_data[y, x, 0] = pixels_array[offset]      # R
            pixel_data[y, x, 1] = pixels_array[offset + 1]  # G
            pixel_data[y, x, 2] = pixels_array[offset + 2]  # B
            pixel_data[y, x, 3] = pixels_array[offset + 3]  # A

    # Create a PIL Image from the numpy array
    return Image.fromarray(pixel_data, 'RGBA')


def texture_to_pil_image(texture, renderer: sdl2.ext.Renderer) -> Image.Image:
    """
    Convert an SDL2 texture to a PIL Image.

    Args:
        texture: The SDL2 texture to convert
        renderer: The SDL2 renderer to use for rendering the texture

    Returns:
        A PIL Image
    """
    # Get texture dimensions
    if hasattr(texture, "size"):
        width, height = texture.size
    else:
        # Try to query the texture
        try:
            info = sdl2.SDL_QueryTexture(texture)
            width, height = info.w, info.h
        except Exception:
            # If we can't determine the size, use a default
            width, height = 100, 100
            print(f"Warning: Could not determine size of texture: {type(texture)}")

    # Create a target surface to render the texture to
    target_surface = sdl2.SDL_CreateRGBSurface(0, width, height, 32, 
                                              0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000)

    # Create a temporary renderer for the target surface
    target_renderer = sdl2.SDL_CreateSoftwareRenderer(target_surface)

    # Clear the target renderer
    sdl2.SDL_SetRenderDrawColor(target_renderer, 0, 0, 0, 0)
    sdl2.SDL_RenderClear(target_renderer)

    # Copy the texture to the target renderer
    sdl2.SDL_RenderCopy(target_renderer, texture, None, None)

    # Present the target renderer
    sdl2.SDL_RenderPresent(target_renderer)

    # Convert the target surface to a PIL Image
    pil_image = surface_to_pil_image(target_surface.contents)

    # Clean up
    sdl2.SDL_DestroyRenderer(target_renderer)
    sdl2.SDL_FreeSurface(target_surface)

    return pil_image
