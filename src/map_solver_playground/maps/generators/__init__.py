"""
Generators module for map data.

This module provides algorithms for generating map data.
"""

from map_solver_playground.maps.generators.base_generator import MapGenerator
from map_solver_playground.maps.generators.diamond_square import DiamondSquareGenerator
from map_solver_playground.maps.generators.recursive_diamond_square import RecursiveDiamondSquareGenerator


class MapGeneratorFactory:
    """Factory class for creating map generator instances."""

    @staticmethod
    def create(generator_type: str, **kwargs) -> MapGenerator:
        """Create a map generator instance based on the generator type.

        Args:
            generator_type: Name of the generator class to instantiate.

        Returns:
            An instance of the specified map generator.

        Raises:
            ValueError: If the generator type is not recognized.
        """
        generators = {
            "DiamondSquareGenerator": DiamondSquareGenerator,
            "RecursiveDiamondSquareGenerator": RecursiveDiamondSquareGenerator,
        }

        if generator_type not in generators:
            raise ValueError(f"Unknown generator type: {generator_type}")

        return generators[generator_type](**kwargs)


__all__ = ["MapGenerator", "DiamondSquareGenerator", "RecursiveDiamondSquareGenerator", "MapGeneratorFactory"]
