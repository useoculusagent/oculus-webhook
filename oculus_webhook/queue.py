"""Redis-backed reimbursement queue.

Items are queued as JSON on a single list; a worker pops and processes them
with optimistic concurrency. The queue is durable but idempotent at the
signature level — a duplicate `LimitBreached` for the same signature
is dropped via a SET membership check.
"""
from __future__ import annotations
import json
from typing import Any
import redis.asyncio as redis

from .schemas import LimitBreachedRecord


class ReimbursementQueue:
    QUEUE_KEY = "oculus:reimbursement:queue"
    SEEN_KEY = "oculus:reimbursement:seen"

    def __init__(self, url: str) -> None:
        self.r = redis.from_url(url, decode_responses=True)

    async def enqueue(self, record: LimitBreachedRecord) -> bool:
        added = await self.r.sadd(self.SEEN_KEY, record.signature)
        if not added:
            return False
        await self.r.lpush(self.QUEUE_KEY, record.model_dump_json())
        return True

    async def dequeue(self, timeout_s: int = 5) -> LimitBreachedRecord | None:
        res: tuple[str, str] | None = await self.r.brpop(self.QUEUE_KEY, timeout=timeout_s)
        if not res:
            return None
        _, raw = res
        return LimitBreachedRecord.model_validate(json.loads(raw))

    async def size(self) -> int:
        return await self.r.llen(self.QUEUE_KEY)

# maintenance pass 1

# maintenance pass 4

# maintenance pass 7

# maintenance pass 10

# pass 9

# pass 13

# pass 18

# pass 31

# pass 47

# pass 50
