"""Runtime configuration loaded from environment."""
from __future__ import annotations
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    helius_webhook_secret: str
    solana_rpc_url: str
    redis_url: str
    reimbursement_vault: str
    log_level: str = "info"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            helius_webhook_secret=os.environ["HELIUS_WEBHOOK_SECRET"],
            solana_rpc_url=os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com"),
            redis_url=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
            reimbursement_vault=os.environ["REIMBURSEMENT_VAULT"],
            log_level=os.environ.get("LOG_LEVEL", "info"),
        )
