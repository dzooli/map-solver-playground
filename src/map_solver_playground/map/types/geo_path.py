"""
GeoPath map element class.
"""

from typing import List, Optional, Tuple

from map_solver_playground.map.types.map_element import MapElement


class GeoPath(MapElement):
    """
    GeoPath map element for representing paths on the map.
    """

    def __init__(
        self,
        path_points: Optional[List[Tuple[int, int]]] = None,
        color: Tuple[int, int, int] = (0, 0, 255),  # Default blue color
        width: int = 2,
        visible: bool = True,
    ) -> None:
        """
        Initialize a geo path element.

        Args:
            path_points: List of (x, y) points that make up the path
            color: RGB color tuple for the path
            width: Width of the path line
            visible: Whether the path is visible
        """
        super().__init__(visible)
        self._path_points = path_points if path_points is not None else []
        self._color = color
        self._width = width

    @property
    def path_points(self) -> List[Tuple[int, int]]:
        """
        Get the points that make up the path.

        Returns:
            List[Tuple[int, int]]: List of (x, y) points
        """
        return self._path_points

    @path_points.setter
    def path_points(self, value: List[Tuple[int, int]]) -> None:
        """
        Set the points that make up the path.

        Args:
            value: New list of (x, y) points
        """
        self._path_points = value

    def add_point(self, point: Tuple[int, int]) -> None:
        """
        Add a point to the path.

        Args:
            point: The (x, y) point to add
        """
        self._path_points.append(point)

    def clear_points(self) -> None:
        """
        Clear all points from the path.
        """
        self._path_points = []

    @property
    def color(self) -> Tuple[int, int, int]:
        """
        Get the color of the path.

        Returns:
            Tuple[int, int, int]: RGB color tuple
        """
        return self._color

    @color.setter
    def color(self, value: Tuple[int, int, int]) -> None:
        """
        Set the color of the path.

        Args:
            value: New RGB color tuple
        """
        self._color = value

    @property
    def width(self) -> int:
        """
        Get the width of the path line.

        Returns:
            int: Line width
        """
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        """
        Set the width of the path line.

        Args:
            value: New line width
        """
        self._width = value

    def get_data(self) -> dict:
        """
        Get the data of the geo path.

        Returns:
            dict: The path data including points, color, width, and visibility
        """
        return {
            "path_points": self._path_points,
            "color": self._color,
            "width": self._width,
            "visible": self.visible,
        }

    def is_empty(self) -> bool:
        """
        Check if the path is empty (has no points).

        Returns:
            bool: True if the path has no points, False otherwise
        """
        return len(self._path_points) == 0
