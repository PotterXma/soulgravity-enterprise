import time
import asyncio
from typing import Dict

class RateLimiter:
    """
    Async Token Bucket Rate Limiter.
    """
    def __init__(self, rate: int, per: int):
        self.rate = rate
        self.per = per
        self.tokens = rate
        self.last_refill = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self):
        async with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            
            # Refill tokens
            refill = elapsed * (self.rate / self.per)
            self.tokens = min(self.rate, self.tokens + refill)
            self.last_refill = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            else:
                wait_time = (1 - self.tokens) * (self.per / self.rate)
                raise RateLimitExceeded(f"Rate limit exceeded. Try again in {wait_time:.2f}s")

class RateLimitExceeded(Exception):
    pass

# Simple in-memory registry for rate limiters
_limiters: Dict[str, RateLimiter] = {}

async def check_rate_limit(key: str, rate: int = 10, per: int = 60):
    """
    Check rate limit for a given key.
    Creates a new limiter if one doesn't exist for the key.
    """
    if key not in _limiters:
        _limiters[key] = RateLimiter(rate, per)
    
    await _limiters[key].acquire()
