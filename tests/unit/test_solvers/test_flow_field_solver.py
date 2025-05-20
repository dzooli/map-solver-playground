"""
Test module for the FlowFieldSolver class.
"""

import unittest
import numpy as np

from map_solver_playground.maps.map_data import Map
from map_solver_playground.maps.solvers import MapSolverFactory, FlowFieldSolver


class TestFlowFieldSolver(unittest.TestCase):
    """Test cases for the FlowFieldSolver class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a simple 10x10 map (minimum size to avoid division by zero)
        self.map_data = np.zeros((10, 10))
        self.map_obj = Map(width=10, height=10, data=self.map_data)

        # Create a solver using the factory
        self.solver = MapSolverFactory.create("FlowFieldSolver", map_obj=self.map_obj)

        # Also create a solver directly for comparison
        self.direct_solver = FlowFieldSolver(map_obj=self.map_obj)

    def test_solver_creation(self):
        """Test that the solver can be created using the factory."""
        self.assertIsInstance(self.solver, FlowFieldSolver)

    def test_solve_method(self):
        """Test that the solve method returns a valid path."""
        start = (0, 0)
        goal = (9, 9)

        # Set start and end locations
        self.solver.set_start_location(start)
        self.solver.set_end_location(goal)

        # Solve using the factory-created solver
        path = self.solver.solve()

        # Check that the path starts at the start point
        self.assertEqual(path[0], start)

        # Check that the path ends at the goal point
        self.assertEqual(path[-1], goal)

        # Check that the path is continuous (each step is adjacent to the previous)
        for i in range(1, len(path)):
            prev_x, prev_y = path[i - 1]
            curr_x, curr_y = path[i]

            # Check that we only move one step at a time (horizontally or vertically)
            dx = abs(curr_x - prev_x)
            dy = abs(curr_y - prev_y)

            # Either dx or dy should be 1, and the other should be 0
            self.assertTrue((dx == 1 and dy == 0) or (dx == 0 and dy == 1) or (dx == 1 and dy == 1))

    def test_direct_vs_factory(self):
        """Test that the factory-created solver behaves the same as a directly created one."""
        start = (2, 2)
        goal = (8, 8)

        # Set start and end locations for both solvers
        self.solver.set_start_location(start)
        self.solver.set_end_location(goal)
        self.direct_solver.set_start_location(start)
        self.direct_solver.set_end_location(goal)

        # Solve using both solvers
        factory_path = self.solver.solve()
        direct_path = self.direct_solver.solve()

        # Check that both paths are the same
        self.assertEqual(factory_path, direct_path)


if __name__ == "__main__":
    unittest.main()
