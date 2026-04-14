"""HMAC verification of inbound Helius webhooks."""
from __future__ import annotations
import hmac
import hashlib


def verify_signature(secret: str, body: bytes, signature_header: str) -> bool:
    """Constant-time compare of `sha256=<hex>` against expected HMAC."""
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    received = signature_header.split("=", 1)[1]
    return hmac.compare_digest(expected, received)

# pass 4

# pass 21
