"""
Map solver module.

This module provides the MapSolver class for solving map-related problems.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional, Union, List, override
import numpy as np

from map_solver_playground.maps.map_data import Map
from map_solver_playground.maps.types import MapLocation


class MapSolver(ABC):
    """
    An abstract class to solve map-related problems.

    This class is initialized with a Map object and automatically retrieves
    the small map. It also stores two location coordinates that can be used
    for pathfinding or other location-based operations.

    Subclasses must implement the solve method.
    """

    model_config = {
        "arbitrary_types_allowed": True,  # Allow arbitrary types like Map
    }

    def __init__(
        self,
        map_obj: Map,
        start_location: Optional[Union[Tuple[int, int], MapLocation]] = None,
        end_location: Optional[Union[Tuple[int, int], MapLocation]] = None,
    ):
        """
        Initialize a new MapSolver with the specified map and locations.

        Args:
            map_obj (Map): The map object to solve
            start_location (Optional[Union[Tuple[int, int], MapLocation]]): The starting location coordinates
            end_location (Optional[Union[Tuple[int, int], MapLocation]]): The ending location coordinates
        """
        self.map = map_obj
        self.small_map = self.map.submap  # Automatically retrieve the small map

        # Initialize locations
        self._start_location = None
        self._end_location = None

        # Set locations if provided
        if start_location is not None:
            self.set_start_location(start_location)
        if end_location is not None:
            self.set_end_location(end_location)

    @property
    def start_location(self) -> Optional[Tuple[int, int]]:
        """Get the start location as a tuple."""
        if self._start_location is None:
            return None
        return self._start_location.as_tuple()

    @property
    def end_location(self) -> Optional[Tuple[int, int]]:
        """Get the end location as a tuple."""
        if self._end_location is None:
            return None
        return self._end_location.as_tuple()

    def set_start_location(self, location: Union[Tuple[int, int], MapLocation]) -> None:
        """
        Sets the starting location for an entity, which can either be specified as a
        tuple of coordinates or a `MapLocation` object. If a tuple is provided, it is
        converted into a `MapLocation` instance. Validation is performed on the
        coordinates to ensure they comply with predefined constraints.

        :param location: The starting location, provided either as a tuple of two
           integers (representing x and y coordinates) or as a `MapLocation` object.
        :type location: Union[Tuple[int, int], MapLocation]
        :return: None
        """
        # Convert tuple to MapLocation if needed
        if isinstance(location, tuple):
            x, y = location
            # self.small_map.validate_location(x, y)
            self._start_location = MapLocation(x=x, y=y)
        else:
            # It's already a MapLocation
            # self.small_map.validate_location(location.x, location.y)
            self._start_location = location

    def set_end_location(self, location: Union[Tuple[int, int], MapLocation]) -> None:
        """
        Sets the end location of an entity within a map. The method ensures the location
        is valid and, if the input is a tuple, converts it to a `MapLocation` instance
        before assigning it to the internal `_end_location` attribute. This ensures
        consistency regardless of input type.

        :param location: The target end location. It can either be a tuple containing
                         the x and y coordinates or a `MapLocation` instance.
        :type location: Union[Tuple[int, int], MapLocation]
        """
        # Convert tuple to MapLocation if needed
        if isinstance(location, tuple):
            x, y = location
            # self.small_map.validate_location(x, y)
            self._end_location = MapLocation(x=x, y=y)
        else:
            # It's already a MapLocation
            # self.small_map.validate_location(location.x, location.y)
            self._end_location = location

    def __str__(self) -> str:
        """Return a string representation of the MapSolver."""
        return f"MapSolver(map={self.map}, start={self.start_location}, end={self.end_location})"

    def __repr__(self) -> str:
        """Return a string representation of the MapSolver."""
        return self.__str__()

    @abstractmethod
    def solve(self) -> List[Tuple[int, int]]:
        """
        Solve the path finding problem on the given map.

        Args:
            map_array (np.ndarray): The map as a numpy array
            start (Tuple[int, int]): The starting coordinates (x, y)
            goal (Tuple[int, int]): The goal coordinates (x, y)

        Returns:
            List[Tuple[int, int]]: A list of coordinates representing the path from start to goal
        """
        pass
