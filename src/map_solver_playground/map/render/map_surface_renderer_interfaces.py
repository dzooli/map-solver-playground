"""
Base interfaces for map surface renderers.
"""

from abc import ABC, abstractmethod
from typing import Any, TypeVar

from map_solver_playground.map.map_data import Map
from map_solver_playground.map.render.color_maps import TerrainColorGradient

# Type variable for the renderer-specific surface type
SurfaceType = TypeVar('SurfaceType')


class BaseMapSurfaceRenderer(ABC):
    """
    Base interface for map surface renderers.
    
    This interface defines methods for converting map data to surfaces
    and applying visual effects.
    """
    
    @staticmethod
    @abstractmethod
    def to_surface(map_obj: Map) -> Any:
        """
        Convert a map to a surface suitable for drawing.
        
        Args:
            map_obj: The map to convert
            
        Returns:
            A surface representing the map (implementation-specific)
        """
        pass
        
    @staticmethod
    @abstractmethod
    def color_map(surface: Any, color_map_array: TerrainColorGradient) -> Any:
        """
        Map grayscale values in a surface to colors in a color map.
        
        Args:
            surface: The surface (implementation-specific)
            color_map_array: A list of RGB tuples representing the color map
            
        Returns:
            A new surface with mapped colors (implementation-specific)
        """
        pass
        
    @staticmethod
    @abstractmethod
    def scale(surface: Any, width: int, height: int) -> Any:
        """
        Scale a surface to the specified width and height.
        
        Args:
            surface: The surface (implementation-specific)
            width: The target width
            height: The target height
            
        Returns:
            The scaled surface (implementation-specific)
        """
        pass