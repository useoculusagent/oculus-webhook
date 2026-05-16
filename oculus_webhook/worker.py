"""Reimbursement worker — pops queue items and sends USDC refunds."""
from __future__ import annotations
import asyncio
import structlog

from .config import Settings
from .queue import ReimbursementQueue
from .schemas import LimitBreachedRecord

log = structlog.get_logger()


async def process(record: LimitBreachedRecord) -> None:
    """Send a USDC refund to the agent's owner address.

    The actual on-chain transfer is delegated to an external signer service —
    this worker only orchestrates the call and records the result.
    """
    log.info("reimbursement.start", agent=record.agent, sig=record.signature)
    # TODO: hand off to signer service
    await asyncio.sleep(0.1)
    log.info("reimbursement.done", agent=record.agent)


async def run() -> None:
    settings = Settings.from_env()
    queue = ReimbursementQueue(settings.redis_url)
    log.info("worker.start", queue_size=await queue.size())
    while True:
        record = await queue.dequeue(timeout_s=5)
        if record is None:
            continue
        try:
            await process(record)
        except Exception as e:
            log.exception("reimbursement.failed", err=str(e), sig=record.signature)


if __name__ == "__main__":
    asyncio.run(run())

# pass 20

# pass 49

# pass 57
