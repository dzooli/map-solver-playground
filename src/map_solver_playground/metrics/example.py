"""
Example usage of the metrics measurement utilities.
"""

import logging
import time

from map_solver_playground.metrics.timing import measure_time

# Configure a custom logger
custom_logger = logging.getLogger("custom_timing")
custom_logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture the timing logs
custom_logger.propagate = False  # Prevent propagation to the root logger to avoid duplicate logs
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
custom_logger.addHandler(handler)


@measure_time
def example_function(sleep_time: float = 0.5) -> str:
    """
    Example function that sleeps for a specified amount of time.
    No logging occurs as no logger is provided to the decorator.

    Args:
        sleep_time: Time to sleep in seconds

    Returns:
        A message indicating the function has completed
    """
    time.sleep(sleep_time)  # Simulate some work
    return f"Function completed after sleeping for {sleep_time} seconds"


@measure_time(logger_instance=custom_logger)
def custom_logger_function(sleep_time: float = 0.3) -> str:
    """
    Example function that sleeps for a specified amount of time.
    Uses a custom logger passed to the decorator.

    Args:
        sleep_time: Time to sleep in seconds

    Returns:
        A message indicating the function has completed
    """
    time.sleep(sleep_time)  # Simulate some work
    return f"Custom logger function completed after sleeping for {sleep_time} seconds"


def main():
    """Run example to demonstrate the measure_time decorator."""
    print("\n1. Running example function without a logger (no logging will occur)...")
    result = example_function(0.2)
    print(f"Result: {result}")

    # Run again with different sleep time
    result = example_function(0.1)
    print(f"Result: {result}")

    print("\n2. Running example function with custom logger (will log execution time)...")
    result = custom_logger_function(0.2)
    print(f"Result: {result}")

    # Run again with different sleep time
    result = custom_logger_function(0.1)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
