import asyncio
from typing import Any, Callable

# Minimal in-process queue abstraction. For production, replace with Redis/RQ/Celery.

class InMemoryQueue:
    def __init__(self):
        self._q = asyncio.Queue()

    async def put(self, item: Any):
        await self._q.put(item)

    async def worker(self, fn: Callable[[Any], Any]):
        while True:
            item = await self._q.get()
            try:
                await fn(item)
            except Exception:
                pass
            finally:
                self._q.task_done()
