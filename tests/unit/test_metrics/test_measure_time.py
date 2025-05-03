import pytest
from map_solver_playground.metrics.timing import measure_time


class TestMeasureTime:
    def test_measure_time_decorator_returns_function_result(self, mocker):
        mock_time = mocker.patch("time.time", side_effect=[0, 1])

        @measure_time
        def sample_func():
            return 42

        result = sample_func()
        assert result == 42

    def test_measure_time_decorator_records_execution_time(self, mocker):
        mock_time = mocker.patch("time.time", side_effect=[0, 2])

        @measure_time
        def slow_func():
            return "done"

        result = slow_func()
        assert result == "done"
        # Mock shows 2 second execution time
        mock_time.assert_has_calls([mocker.call(), mocker.call()])

    def test_measure_time_decorator_with_args(self, mocker):
        mock_time = mocker.patch("time.time", side_effect=[0, 1])

        @measure_time
        def func_with_args(x, y):
            return x + y

        result = func_with_args(2, 3)
        assert result == 5

    def test_measure_time_decorator_with_kwargs(self, mocker):
        mock_time = mocker.patch("time.time", side_effect=[0, 0.5])

        @measure_time
        def func_with_kwargs(x, y=10):
            return x + y

        result = func_with_kwargs(x=5, y=7)
        assert result == 12
