"""Pydantic schemas matching the Helius enhanced webhook payload."""
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field


class TokenTransfer(BaseModel):
    fromUserAccount: str
    toUserAccount: str
    mint: str
    tokenAmount: float


class WebhookEvent(BaseModel):
    """Subset of Helius enhanced tx — only fields we use."""
    type: str
    signature: str
    slot: int
    timestamp: int
    feePayer: str
    tokenTransfers: list[TokenTransfer] = Field(default_factory=list)


class LimitBreachedRecord(BaseModel):
    agent: str
    signature: str
    attempted_usdc: int
    limit_usdc: int
    spent_window_usdc: int
    at: int
    status: Literal["queued", "reimbursed", "skipped"] = "queued"
