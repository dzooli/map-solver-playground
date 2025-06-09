"""
Enum for renderer backends.
"""

from enum import Enum


class RendererBackend(Enum):
    """
    Enum for renderer backends.
    """
    PYGAME = "pygame"
    SDL2 = "sdl2"