"""
Example usage of the profile measurement utilities.
"""

import sys
import time
from loguru import logger

from map_solver_playground.profile.timing import measure_time

# Configure a custom logger
# Remove default handler
logger.remove()
# Add a handler with a specific format to match the previous logging format
custom_logger = logger.bind(name="custom_timing")
logger.add(sys.stderr, format="{time:YYYY-MM-DD HH:mm:ss} - {extra[name]} - {level} - {message}", level="DEBUG")


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
