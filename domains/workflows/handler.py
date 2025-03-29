import time
from functools import wraps
from loguru import logger


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    max_delay: float = 10.0,
):
    """
    Decorator to retry a function with exponential backoff.

    Args:
        max_retries (int): Maximum number of retries.
        initial_delay (float): Initial delay in seconds.
        backoff_factor (float): Factor by which the delay increases after each retry.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error in {func.__name__}: {e}")

                    if attempt < max_retries - 1:
                        sleep_time = min(delay, max_delay)
                        logger.warning(
                            f"Retrying {func.__name__} in {sleep_time:.2f} seconds (attempt {attempt + 1}/{max_retries})"
                        )
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        raise
        return wrapper

    return decorator
