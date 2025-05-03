"""
Test script to verify that the map generators still work correctly after refactoring.
"""

import numpy as np

from map_solver_playground.maps.generators.diamond_square import DiamondSquareGenerator
from map_solver_playground.maps.generators.recursive_diamond_square import RecursiveDiamondSquareGenerator


def test_generators():
    """Test both map generators and verify their functionality."""
    # Parameters
    width, height = 256, 256

    # Create generators
    diamond_square = DiamondSquareGenerator(width, height)
    recursive_diamond_square = RecursiveDiamondSquareGenerator(width, height)

    # Generate maps
    print("Generating map with DiamondSquareGenerator...")
    ds_map = diamond_square.generate_map()

    print("Generating map with RecursiveDiamondSquareGenerator...")
    rds_map = recursive_diamond_square.generate_map()

    # Verify maps were created successfully
    print(f"DiamondSquareGenerator map shape: {ds_map.data.shape}")
    print(f"RecursiveDiamondSquareGenerator map shape: {rds_map.data.shape}")

    # Print some statistics about the maps
    print(f"DiamondSquareGenerator map min value: {ds_map.data.min()}")
    print(f"DiamondSquareGenerator map max value: {ds_map.data.max()}")
    print(f"DiamondSquareGenerator map mean value: {ds_map.data.mean()}")

    print(f"RecursiveDiamondSquareGenerator map min value: {rds_map.data.min()}")
    print(f"RecursiveDiamondSquareGenerator map max value: {rds_map.data.max()}")
    print(f"RecursiveDiamondSquareGenerator map mean value: {rds_map.data.mean()}")

    print("Test complete. Both generators are working correctly.")


if __name__ == "__main__":
    test_generators()
