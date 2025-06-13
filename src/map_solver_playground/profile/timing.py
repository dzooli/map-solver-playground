"""
Timing decorators for measuring function execution time.
"""

import functools
import inspect
import time
from typing import Callable, Any, TypeVar, cast, Optional, Union
from loguru import logger as loguru_logger

# Type variable for generic function type
F = TypeVar("F", bound=Callable[..., Any])


def measure_time(
    func: Optional[F] = None, *, logger_instance: Optional[Any] = None
) -> Union[Callable[[F], F], F]:
    """
    Decorator that measures the execution time of a function and logs it as a debug message.
    If no logger instance is provided, no logging will occur.

    The log message includes the function's location (file path or module name), function name, and execution time.

    Args:
        func: The function to be measured
        logger_instance: Optional logger to use for logging execution time. If not provided, no logging occurs.
                         Can be either a loguru logger or a standard logging.Logger instance.

    Returns:
        The wrapped function with timing measurement

    Examples:
        # Basic usage (no logging)
        @measure_time
        def some_function():
            # function code

        # With loguru logger (logs execution time)
        from loguru import logger

        @measure_time(logger_instance=logger)
        def another_function():
            # function code
    """

    def decorator(fn: F) -> F:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            result = fn(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time

            # Log the execution time only if a logger instance was provided
            if logger_instance is not None:
                # Get the file path of the function
                try:
                    file_path = inspect.getfile(fn)
                except TypeError:
                    # If we can't get the file path, fall back to just the module name
                    file_path = fn.__module__

                logger_instance.debug(f"Function '{file_path}:{fn.__name__}' executed in {execution_time:.6f} seconds")

            return result

        return cast(F, wrapper)

    # Handle both @measure_time and @measure_time(logger_instance=...)
    if func is not None:
        return decorator(func)
    return decorator
