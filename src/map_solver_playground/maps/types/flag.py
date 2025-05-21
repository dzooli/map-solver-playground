"""
Flag map element class.
"""

from typing import Optional, Tuple

import pygame

from map_solver_playground.maps.types.map_element import MapElement


class Flag(MapElement):
    """
    Flag map element for marking locations on the map.
    """

    def __init__(
        self,
        position: Optional[Tuple[int, int]] = None,
        image: Optional[pygame.Surface] = None,
        flag_type: str = "default",
        visible: bool = True,
    ) -> None:
        """
        Initialize a flag element.

        Args:
            position: The (x, y) position of the flag on the map
            image: The image to use for the flag
            flag_type: The type of flag (e.g., "red", "green")
            visible: Whether the flag is visible
        """
        super().__init__(visible)
        self._position = position
        self._image = image
        self._flag_type = flag_type

    @property
    def position(self) -> Optional[Tuple[int, int]]:
        """
        Get the position of the flag.

        Returns:
            Optional[Tuple[int, int]]: The (x, y) position of the flag, or None if not set
        """
        return self._position

    @position.setter
    def position(self, value: Optional[Tuple[int, int]]) -> None:
        """
        Set the position of the flag.

        Args:
            value: The new (x, y) position of the flag
        """
        self._position = value

    @property
    def image(self) -> Optional[pygame.Surface]:
        """
        Get the image of the flag.

        Returns:
            Optional[pygame.Surface]: The flag image, or None if not set
        """
        return self._image

    @image.setter
    def image(self, value: Optional[pygame.Surface]) -> None:
        """
        Set the image of the flag.

        Args:
            value: The new flag image
        """
        self._image = value

    @property
    def flag_type(self) -> str:
        """
        Get the type of the flag.

        Returns:
            str: The flag type
        """
        return self._flag_type

    @flag_type.setter
    def flag_type(self, value: str) -> None:
        """
        Set the type of the flag.

        Args:
            value: The new flag type
        """
        self._flag_type = value

    def get_data(self) -> dict:
        """
        Get the data of the flag.

        Returns:
            dict: The flag data including position, type, and visibility
        """
        return {
            "position": self._position,
            "flag_type": self._flag_type,
            "visible": self.visible,
        }
