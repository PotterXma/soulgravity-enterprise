import functools
import time
import asyncio
from typing import Callable, Any, Type, Optional

class CircuitOpenError(Exception):
    pass

class CircuitBreaker:
    """
    Async Circuit Breaker.
    Prevents cascading failures by stopping execution for a period after a threshold of failures.
    """
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60, expected_exception: Type[Exception] = Exception):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.fail_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED (working), OPEN (blocking), HALF-OPEN (testing)

    async def call(self, func: Callable, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF-OPEN"
            else:
                raise CircuitOpenError(f"Circuit is open. Retrying in {self.recovery_timeout - (time.time() - self.last_failure_time):.2f}s")

        try:
            result = await func(*args, **kwargs)
            if self.state == "HALF-OPEN":
                self.state = "CLOSED"
                self.fail_count = 0
            return result
        except self.expected_exception as e:
            self.fail_count += 1
            self.last_failure_time = time.time()
            if self.fail_count >= self.failure_threshold:
                self.state = "OPEN"
            raise e

def circuit_breaker(failure_threshold: int = 5, recovery_timeout: int = 60, expected_exception: Type[Exception] = Exception):
    def decorator(func):
        # Store breaker instance on the function object itself to persist state across calls
        if not hasattr(func, "_circuit_breaker"):
             func._circuit_breaker = CircuitBreaker(failure_threshold, recovery_timeout, expected_exception)
        
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            return await func._circuit_breaker.call(func, *args, **kwargs)
        return wrapper
    return decorator
