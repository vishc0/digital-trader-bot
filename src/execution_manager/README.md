# Execution Manager

## Overview

The Execution Manager is the centralized microservice responsible for turning trade signals into orders. It enforces mode gating (paper / shadow / live), validates trading permissions via the State Manager (circuit breaker), ensures idempotent placement, and records fills to the Journaling Service.

This component is intentionally the single place to implement broker adapters and protections for real-money trading.

Port: `8086`

---

## Responsibilities

- Accept order placement requests from Strategy Engine or an API Gateway.
- Check `State Manager` for circuit breaker and risk permissions before placing orders.
- Support execution modes:
  - `paper` (default): simulate fills locally with configurable slippage/delay.
  - `shadow`: send the order into journaling and simulation while also sending the same payload to a broker in read-only/simulated account (future).
  - `live`: place orders with a configured broker adapter (disabled by default until approval).
- Provide idempotency for order requests (via `Idempotency-Key` header).
- Publish fills/events to the `Journaling Service`.
- Expose `/health` for orchestration.

---

## Environment Variables

- `PORT` (default `8086`) — service port.
- `EXECUTION_MODE` (`paper` | `shadow` | `live`) — execution mode; default `paper` for safety.
- `STATE_MANAGER_HOST` — optional custom host for State Manager (defaults to `state-manager` in compose).
- `JOURNALING_HOST` — optional custom host for Journaling Service (defaults to `journaling-service`).
- Broker-specific secrets (for live mode) — should be provided through a secrets manager in production.

Do not store API keys or secrets in Git or plaintext environment files. Use GCP Secret Manager / AWS Secrets Manager or Docker secrets.

---

## API Endpoints

### `GET /health`
- Response: `{ status: 'healthy', service: 'execution-manager', mode: '<paper|shadow|live>' }`

### `POST /place-order`
- Request JSON fields (example):
  {
    "ticker": "AAPL",
    "side": "buy",          // buy | sell
    "qty": 10,
    "price": 150.0,
    "order_type": "limit"  // limit | market
  }
- Optional header: `Idempotency-Key: <uuid or client-generated key>`
- Responses:
  - 200: `{ status: 'ok', result: { trade_id, ticker, qty, fill_price, status }}`
  - 500: `{ error: 'message' }`

Notes on Idempotency:
- If the client supplies `Idempotency-Key`, the Execution Manager must deduplicate repeated calls with the same key and return the original result.
- In the skeleton, idempotency is implemented per-process using the provided key. Production should store keys in Redis with TTL to provide dedup across restarts and replicas.

---

## Internal Behavior (Skeleton Implementation)

- `is_trading_allowed()` calls `GET /circuit-breaker` on the State Manager. If State Manager is unreachable or returns `trading_allowed: false`, the Execution Manager disallows trading (fail-safe).

- `place_order(order, idempotency_key)`:
  - Validates trading allowed.
  - Uses provided `idempotency_key` or generates one.
  - In `paper` mode: simulates a fill (`_simulate_fill`) with a small slippage and timestamps, then sends a `FILL` event to Journaling Service via `/trade-event`.
  - In `live` mode: placeholder `_place_live_order` to be implemented with broker adapter.

- `_simulate_fill` implements a minimal slippage model and immediate fill. This can be improved to model order book, partial fills, time-in-force, and realistic latency.

---

## Integration Points

- State Manager (`/circuit-breaker`, `/strategy-vector`, `/daily-pnl`) — used to check permissions and update PnL.
- Journaling Service (`/trade-event`, `/execution-metrics`) — used to record fill events and execution quality metrics.
- API Gateway / Strategy Engine — callers of the Execution Manager.

Integration best practices:
- Propagate a `Trace-ID` header for end-to-end observability between services.
- Use short timeouts for state checks, and implement retry/backoff.

---

## Approval Workflow (Live Enablement)

To prevent accidental live trading, the platform must require a manual, auditable operator approval process before `EXECUTION_MODE=live` is ever enabled in production.

Recommended flow:
1. Operator A requests enabling live trading via the Admin UI or API (writes a request to State Manager as `live_enable_request` with metadata).
2. Operator B reviews and approves the request.
3. State Manager toggles `ENABLE_LIVE_TRADING` flag and logs the approvers and timestamp in the Journaling Service.
4. Deployment pipeline updates service configuration to `EXECUTION_MODE=live` or the Execution Manager reads the `ENABLE_LIVE_TRADING` flag and only transitions modes after the stored approvals are valid.

Implement a policy that requires at least two distinct human approvals and an approval TTL.

---

## Security Considerations

- Run the Execution Manager in a private network where only trusted services (Strategy Engine, API Gateway) can call it.
- Use mTLS or signed JWTs for inter-service auth in production.
- Store broker secrets in a dedicated secret manager; load them into the Execution Manager at runtime, not via source.
- Rate-limit `/place-order` to detect accidental loops.

---

## Observability

- Add structured logging with `trade_id`, `trace_id`, `service`, `level`.
- Expose metrics (Prometheus) for:
  - orders_placed_total
  - orders_filled_total
  - orders_failed_total
  - avg_execution_latency_ms
- Add OpenTelemetry traces and propagate trace IDs across calls.

---

## Testing

Unit tests to add:
- `test_simulate_fill_returns_expected_fields`
- `test_is_trading_disallowed_when_state_manager_unreachable`
- `test_idempotency_returns_same_result_for_same_key` (requires in-memory store or mocked Redis)

Integration tests:
- Start state-manager and journaling-service in docker-compose test profile and verify full lifecycle: place-order -> journaling entry -> daily_pnl update.

---

## Deployment

- Dockerfile included. Compose entry is configured to run the service on `8086` with `EXECUTION_MODE=paper`.
- In production, run behind an API Gateway or internal load balancer and configure secrets and service accounts.

---

## Extensibility & Next Steps

- Implement `broker_adapters/` folder with a clear BrokerAdapter interface and an example mock adapter for Alpaca/IB.
- Implement persistent idempotency store (Redis) and dedup logic.
- Add `shadow` mode that mirrors live orders into a non-executing environment for comparison.
- Add tests and chaos scenarios (broker downtime, partial fills, rejections).

---

## Developer Notes

- File layout:
  - `execution_manager.py` — core logic class.
  - `main.py` — Flask entrypoint.
  - `Dockerfile`, `requirements.txt` — packaging.
  - `README.md` — this document.

- To run locally with all services:
```powershell
docker-compose up --build -d
curl http://localhost:8086/health
```

---

## License & Ownership

Part of the `digital-trader-bot` project. Follow the project's LICENSE file for contribution and distribution rules.
