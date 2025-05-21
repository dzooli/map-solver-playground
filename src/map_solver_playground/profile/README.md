# Metrics Module

This module provides utilities for measuring and monitoring the metrics of functions in the map-solver-playground
project.

## Features

- `measure_time` decorator: Measures the execution time of a function and logs it as a debug message when a logger is
  provided. The log message includes the function's location (file path or module name), function name, and execution
  time.

## Usage

### Measuring Function Execution Time

#### Basic Usage

```python
from map_solver_playground.profile import measure_time


@measure_time
def my_function():
    # Your code here
    pass
```

When the decorated function is called, the execution time is measured but not logged (no logger provided).

To enable logging, you must provide a logger instance (see "Using a Custom Logger" below).

#### Using a Custom Logger

You can pass your own logger instance to the decorator:

```python
import logging
from map_solver_playground.profile import measure_time

# Create a custom logger
custom_logger = logging.getLogger("my_module")
custom_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
custom_logger.addHandler(handler)


# Use the custom logger with the decorator
@measure_time(logger_instance=custom_logger)
def my_function():
    # Your code here
    pass
```

This allows you to integrate the timing logs with your application's logging system.

### Example

See `metrics/example.py` for a complete example:

```python
import time
import logging
from map_solver_playground.profile.timing import measure_time


# Basic usage - no logging will occur
@measure_time
def example_function(sleep_time: float = 0.5) -> str:
    time.sleep(sleep_time)  # Simulate some work
    return f"Function completed after sleeping for {sleep_time} seconds"


# With custom logger - execution time will be logged
custom_logger = logging.getLogger("custom_timing")
custom_logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture timing logs


@measure_time(logger_instance=custom_logger)
def another_function(sleep_time: float = 0.3) -> str:
    time.sleep(sleep_time)  # Simulate some work
    return f"Another function completed after sleeping for {sleep_time} seconds"


# When called, only another_function will log the execution time
result1 = example_function(0.2)  # No logging
result2 = another_function(0.1)  # Will log execution time with location information

# Example log output:
# 2023-11-15 14:30:45,123 - custom_timing - DEBUG - Function 'D:\projects\python\map-solver-playground\src\map_solver_playground\profile\main.py:another_function' executed in 0.100123 seconds
```

## Configuration

When using a custom logger with the `measure_time` decorator, you need to ensure your logger is properly configured:

```python
import logging
from map_solver_playground.profile.timing import measure_time

# Create and configure a custom logger
custom_logger = logging.getLogger("my_timing_logger")
custom_logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture timing logs

# Add a handler to output logs
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
custom_logger.addHandler(handler)


# Use the custom logger with the decorator
@measure_time(logger_instance=custom_logger)
def my_function():
    # Your code here
    pass
```