"""
Flow field solver module.

This module provides the FlowFieldSolver class for solving map-related problems
using flow field pathfinding.
"""

from collections import deque
from typing import Tuple, List

import numpy as np

from map_solver_playground.maps.solvers.map_solver import MapSolver


class FlowFieldSolver(MapSolver):
    """
    A class to solve map-related problems using flow field pathfinding.

    Flow field pathfinding creates a vector field that points towards the goal
    from every accessible location on the map. This allows for efficient
    pathfinding from any point on the map to the goal.

    Example:

    ```python
        terrain = np.array([ [1, 1, 1], [2, 3, 1], [2, 2, 1] ])
        goal = (0, 2)
        start = (2, 0)
        came_from, cost_map = self._generate_flow_field_np(terrain, goal)
        path = self._extract_path_np(came_from, start, goal)
        total_energy = cost_map[start]
    ```

    """

    def energy_cost(self, from_h, to_h):
        delta = to_h - from_h
        if delta > 0:
            return delta * 2 + 1  # up
        elif delta < 0:
            return max(-1, delta)  # down
        else:
            return 1  # energy loss 1

    def _generate_flow_field_np(self) -> Tuple[np.ndarray, np.ndarray]:
        rows, cols = self.map.data.shape
        terrain = self.map.data
        cost_map = np.full((rows, cols), np.inf)
        came_from = np.full((rows, cols, 2), -1, dtype=int)

        gx, gy = self.end_location[0], self.end_location[1]
        cost_map[gx, gy] = 0
        queue = deque()
        queue.append((gx, gy))

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        while queue:
            x, y = queue.popleft()
            current_cost = cost_map[x, y]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    terrain_cost = self.energy_cost(terrain[x, y], terrain[nx, ny])
                    new_cost = current_cost + terrain_cost
                    if new_cost < cost_map[nx, ny]:
                        cost_map[nx, ny] = new_cost
                        came_from[nx, ny] = [x, y]
                        queue.append((nx, ny))
        return came_from, cost_map

    def _extract_path_np(self, came_from: np.ndarray):
        path = []
        goal = self.end_location
        x, y = self.start_location
        while (x, y) != goal:
            path.append((x, y))
            next_step = came_from[x, y]
            if tuple(next_step) == (-1, -1):
                return None
            x, y = next_step
        path.append(goal)
        return path

    def solve(self) -> List[Tuple[int, int]]:
        """
        Solve the path-finding problem on the given map using flow field pathfinding.

        Returns:
            List[Tuple[int, int]]: A list of coordinates representing the path from start to goal
        """
        came_from, _ = self._generate_flow_field_np()
        path = self._extract_path_np(came_from)
        return path
