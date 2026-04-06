import asyncio
import time


class RateLimiter:
    def __init__(self, min_interval: float) -> None:
        self.min_interval = min_interval
        self._lock = asyncio.Lock()
        self._last_req_time = 0.0

    async def acquire(self):
        async with self._lock:
            elapsed = time.monotonic() - self._last_req_time
            if elapsed < self.min_interval:
                time_left = self.min_interval - elapsed
                await asyncio.sleep(time_left)

            self._last_req_time = time.monotonic()
