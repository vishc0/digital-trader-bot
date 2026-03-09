# Software Architect Guide

## Architecture target

Keep the platform modular, event-driven where useful, and simpler than a full trading mesh until real integrations justify more complexity.

## Recommended platform shape

- Frontend: operator console, approvals, dashboards.
- Gateway: authentication, orchestration, aggregation, policy checks.
- State manager: source of truth for positions, limits, approvals, and feature flags.
- Strategy engine: deterministic strategy evaluation.
- Decision support service: AI summaries, ranking, rationale, and portfolio commentary.
- Execution manager: broker-agnostic order routing and execution state.
- Journaling service: immutable audit and analytics feed.
- Data handler: market data and account data normalization.

## Simplification guidance

- Avoid introducing more services until ownership is clear.
- Keep broker-specific code inside adapters.
- Keep AI provider calls in a dedicated boundary.
- Prefer one shared event schema over many ad hoc payloads.
- Use one observability approach across all services.

## Immediate architecture gaps

- Fidelity integration is mock only.
- Market data is mock in key paths.
- Strategy indicators contain random placeholders.
- Journaling is in-memory rather than durable.
- Redis security and secret management need hardening.

## Architecture decisions to make next

1. Canonical domain model.
2. Durable audit store.
3. Portfolio and P&L analytics pipeline.
4. Real broker integration plan.
5. AI orchestration and token budget policy.
