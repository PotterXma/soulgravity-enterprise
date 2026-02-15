import asyncio
import functools
import random
import logging

logger = logging.getLogger(__name__)

def retry(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: tuple = (Exception,)
):
    """
    Async decorator for retrying functions with exponential backoff.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_retries:
                        logger.error(f"Function {func.__name__} failed after {max_retries} retries. Error: {e}")
                        raise last_exception
                    
                    # Calculate wait time
                    wait_time = delay * (backoff_factor ** attempt)
                    if jitter:
                        wait_time += random.uniform(0, 0.5 * wait_time)
                    
                    logger.warning(f"Function {func.__name__} failed (attempt {attempt + 1}/{max_retries}). Retrying in {wait_time:.2f}s... Error: {e}")
                    await asyncio.sleep(wait_time)
            
            # Should not reach here
            raise last_exception
        return wrapper
    return decorator
