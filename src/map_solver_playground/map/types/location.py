"""
Location module.

This module provides the MapLocation class for representing locations on a map.
"""

from typing import Tuple
from pydantic import BaseModel, Field


class MapLocation(BaseModel):
    """
    A Pydantic model representing a location on a map.

    Attributes:
        x (int): The x-coordinate of the location
        y (int): The y-coordinate of the location
    """

    x: int = Field(..., description="The x-coordinate of the location", ge=0)
    y: int = Field(..., description="The y-coordinate of the location", ge=0)

    def as_tuple(self) -> Tuple[int, int]:
        """Convert the location to a tuple of (x, y)."""
        return self.x, self.y