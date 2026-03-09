# System Requirements

## Functional requirements

- Ingest account, holdings, cash, orders, and fills.
- Produce portfolio snapshots and watchlists.
- Generate trade suggestions with explanation and confidence.
- Track expected vs actual outcomes per trade and portfolio.
- Support paper mode, shadow mode, and supervised live mode.
- Support broker adapters beginning with Fidelity-compatible workflows.
- Expose APIs for frontend, AI services, and external automation.

## Non-functional requirements

- Reliability: recover from service failure without losing critical state.
- Security: protect secrets, auth boundaries, and audit logs.
- Observability: metrics, logs, traces, business dashboards.
- Explainability: every suggestion and trade must be reconstructable.
- Cost control: token budgets, model routing, and caching are mandatory.
- Modularity: independently deployable services.

## Data requirements

- Canonical models for order, fill, position, portfolio, trade thesis, and exit reason.
- Time-series store or durable event store for analytics.
- Journal store for decisions, approvals, and AI outputs.

## Integration requirements

- Broker API abstraction.
- Market data abstraction.
- AI provider abstraction.
- Cloud deployment abstraction across GCP and AWS.
