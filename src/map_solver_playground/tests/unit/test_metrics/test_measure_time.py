import pytest
import time
from unittest.mock import patch
from map_solver_playground.profile.timing import measure_time


class TestMeasureTime:
    def test_measure_time_decorator_returns_function_result(self):
        # Mock time.time to return specific values
        with patch("map_solver_playground.profile.timing.time.time", side_effect=[0, 1]) as mock_time:

            @measure_time
            def sample_func():
                return 42

            result = sample_func()
            assert result == 42
            assert mock_time.call_count == 2

    def test_measure_time_decorator_records_execution_time(self):
        # Mock time.time to return specific values
        with patch("map_solver_playground.profile.timing.time.time", side_effect=[0, 2]) as mock_time:

            @measure_time
            def slow_func():
                return "done"

            result = slow_func()
            assert result == "done"
            # Mock shows 2 second execution time
            assert mock_time.call_count == 2

    def test_measure_time_decorator_with_args(self):
        # Mock time.time to return specific values
        with patch("map_solver_playground.profile.timing.time.time", side_effect=[0, 1]) as mock_time:

            @measure_time
            def func_with_args(x, y):
                return x + y

            result = func_with_args(2, 3)
            assert result == 5
            assert mock_time.call_count == 2

    def test_measure_time_decorator_with_kwargs(self):
        # Mock time.time to return specific values
        with patch("map_solver_playground.profile.timing.time.time", side_effect=[0, 0.5]) as mock_time:

            @measure_time
            def func_with_kwargs(x, y=10):
                return x + y

            result = func_with_kwargs(x=5, y=7)
            assert result == 12
            assert mock_time.call_count == 2