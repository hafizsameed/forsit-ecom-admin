import time
from typing import Dict, List, Callable
from fastapi import Request, HTTPException, Depends


class RateLimiter:

    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.cache: Dict[str, List[float]] = {}

    def is_allowed(self, key: str) -> bool:
        current_time = time.time()
        if key not in self.cache:
            self.cache[key] = []

        self.cache[key] = [
            timestamp
            for timestamp in self.cache[key]
            if timestamp > current_time - self.period
        ]

        if len(self.cache[key]) < self.calls:
            self.cache[key].append(current_time)
            return True

        return False


default_limiter = RateLimiter(calls=100, period=60)


def rate_limit(
    limiter: RateLimiter = default_limiter,
    key_func: Callable[[Request], str] = lambda request: request.client.host,
):

    def dependency(request: Request):
        key = key_func(request)
        if not limiter.is_allowed(key):
            raise HTTPException(
                status_code=429, detail="Rate limit exceeded. Please try again later."
            )

    return Depends(dependency)
