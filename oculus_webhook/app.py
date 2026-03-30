"""FastAPI app — inbound webhook + health endpoints."""
from __future__ import annotations
import structlog
from fastapi import FastAPI, Header, HTTPException, Request

from .config import Settings
from .verify import verify_signature
from .queue import ReimbursementQueue
from .schemas import WebhookEvent, LimitBreachedRecord

log = structlog.get_logger()
settings = Settings.from_env()
queue = ReimbursementQueue(settings.redis_url)

app = FastAPI(title="oculus-webhook", version="0.1.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "version": "0.1.0"}


@app.post("/webhook/helius")
async def helius_webhook(
    request: Request,
    x_helius_signature: str = Header(default=""),
) -> dict[str, int]:
    body = await request.body()
    if not verify_signature(settings.helius_webhook_secret, body, x_helius_signature):
        raise HTTPException(401, "invalid signature")

    payload = await request.json()
    events = [WebhookEvent.model_validate(e) for e in payload]
    enqueued = 0
    for ev in events:
        if ev.type != "LIMIT_BREACHED":
            continue
        record = LimitBreachedRecord(
            agent=ev.feePayer,
            signature=ev.signature,
            attempted_usdc=int(ev.tokenTransfers[0].tokenAmount * 1_000_000) if ev.tokenTransfers else 0,
            limit_usdc=0,
            spent_window_usdc=0,
            at=ev.timestamp,
        )
        if await queue.enqueue(record):
            enqueued += 1
            log.info("queued.reimbursement", agent=record.agent, sig=record.signature)
    return {"received": len(events), "enqueued": enqueued}

# maintenance pass 2

# maintenance pass 8

# pass 5
