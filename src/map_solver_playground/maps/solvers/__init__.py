"""
Solvers package for map-related problem solving.

This package contains classes for solving various map-related problems.
"""

import importlib
import inspect

from map_solver_playground.maps.solvers.map_solver import MapSolver
from map_solver_playground.maps.solvers.flow_field_solver import FlowFieldSolver


class MapSolverFactory:
    """Factory class for creating MapSolver instances."""

    @staticmethod
    def create(solver_name: str, **kwargs) -> MapSolver:
        """
        Create a new instance of the specified MapSolver.

        Args:
            solver_name: Name of the solver class to instantiate
            **kwargs: Arguments to pass to the solver constructor

        Returns:
            MapSolver: An instance of the requested solver

        Raises:
            ValueError: If the solver class cannot be found or instantiated
        """
        try:
            module = importlib.import_module("map_solver_playground.maps.solvers")
            solver_class = getattr(module, solver_name)

            if not inspect.isclass(solver_class) or not issubclass(solver_class, MapSolver):
                raise ValueError(f"{solver_name} is not a valid MapSolver class")

            return solver_class(**kwargs)
        except (ImportError, AttributeError) as e:
            raise ValueError(f"Could not create solver {solver_name}: {str(e)}")


__all__ = ["MapSolver", "MapSolverFactory", "FlowFieldSolver"]
