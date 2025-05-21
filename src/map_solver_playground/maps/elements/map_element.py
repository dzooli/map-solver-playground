"""
Abstract base class for map elements.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple


class MapElement(ABC):
    """
    Abstract base class for map elements like flags and paths.
    
    This class defines the interface that all map elements must implement.
    """

    def __init__(self, visible: bool = True) -> None:
        """
        Initialize a map element.
        
        Args:
            visible: Whether the element is visible
        """
        self._visible = visible
        self._properties: Dict[str, Any] = {}

    @property
    def visible(self) -> bool:
        """
        Get the visibility state of the element.
        
        Returns:
            bool: True if the element is visible, False otherwise
        """
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        """
        Set the visibility state of the element.
        
        Args:
            value: The new visibility state
        """
        self._visible = value

    def toggle_visibility(self) -> bool:
        """
        Toggle the visibility of the element.
        
        Returns:
            bool: The new visibility state
        """
        self._visible = not self._visible
        return self._visible

    def set_property(self, key: str, value: Any) -> None:
        """
        Set a property of the element.
        
        Args:
            key: The property key
            value: The property value
        """
        self._properties[key] = value

    def get_property(self, key: str, default: Any = None) -> Any:
        """
        Get a property of the element.
        
        Args:
            key: The property key
            default: The default value to return if the property doesn't exist
            
        Returns:
            Any: The property value or the default value
        """
        return self._properties.get(key, default)

    @abstractmethod
    def get_data(self) -> Any:
        """
        Get the data of the element.
        
        Returns:
            Any: The element data
        """
        pass