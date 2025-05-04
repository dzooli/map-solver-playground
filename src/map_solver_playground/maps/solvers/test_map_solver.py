"""
Test script for the MapSolver class.
"""

from map_solver_playground.maps.map_data import Map
from map_solver_playground.maps.solvers import MapSolver


def test_map_solver():
    """Test the MapSolver class functionality."""
    # Create a test map
    test_map = Map(100, 100)

    # Test initialization without locations
    solver = MapSolver(test_map)
    print(f"MapSolver initialized: {solver}")
    print(f"Small map automatically retrieved: {solver.small_map is not None}")

    # Test setting locations
    solver.set_start_location((5, 5))
    solver.set_end_location((9, 9))
    print(f"After setting locations: {solver}")

    # Test initialization with locations
    solver2 = MapSolver(test_map, start_location=(2, 2), end_location=(8, 8))
    print(f"MapSolver initialized with locations: {solver2}")

    print("All tests passed!")


if __name__ == "__main__":
    test_map_solver()
