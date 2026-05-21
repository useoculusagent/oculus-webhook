# oculus-webhook

> Helius webhook ingestor + reimbursement queue for the Oculus policy engine.

[![CI](https://img.shields.io/badge/ci-passing-22c55e?style=flat-square)](../../actions)
[![License](https://img.shields.io/badge/license-MIT-d4d9e1?style=flat-square)](LICENSE)

## What it does

- Receives Helius enhanced webhooks for Solana agent wallets we monitor.
- Verifies HMAC signature against the shared secret.
- For every `LIMIT_BREACHED` event, enqueues a reimbursement record (deduplicated by signature).
- A worker dequeues records and triggers USDC refunds via an external signer.

```
helius ──▶ /webhook/helius ──▶ redis queue ──▶ worker ──▶ USDC refund
```

## Endpoints

| Method | Path              | Notes                       |
|--------|-------------------|-----------------------------|
| GET    | `/health`         | Liveness                    |
| POST   | `/webhook/helius` | HMAC-protected ingestion    |

## Run

```bash
uvicorn oculus_webhook.app:app --reload
python -m oculus_webhook.worker
```

## License

MIT

<!-- rev 9 -->

<!-- rev 12 -->

<!-- rev 11 -->

<!-- rev 40 -->

<!-- rev 63 -->
