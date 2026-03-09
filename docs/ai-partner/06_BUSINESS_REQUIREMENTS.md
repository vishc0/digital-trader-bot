# Business Requirements

## Product vision

An AI-assisted portfolio operations platform that helps a user monitor accounts, evaluate trades, execute approved orders, and manage exits with minimal research overhead.

## Business outcomes

- Reduce manual research time.
- Improve decision quality through structured AI support.
- Maintain strong safety, auditability, and explainability.
- Support gradual progression from paper trading to supervised live trading.
- Keep operating cost low, including AI token spend.

## In-scope capabilities

- Portfolio monitoring and snapshots.
- Trade idea generation and ranking.
- Expected vs actual portfolio delta analysis.
- P&L analysis at position and portfolio level.
- Exit and sell-off signal support.
- Built-in paper trading account and simulation for MVP.
- Broker integration in Phase 2, starting with Fidelity market-account workflows.

## Delivery phases

### MVP

- Built-in paper trading account inside the tool.
- Portfolio monitoring, recommendations, approval workflow, paper execution, journaling, and review.
- Local-first operation with strong observability and bounded AI/token usage.

### Phase 2

- Fidelity market-account integration.
- Reuse the same operator workflows, approval gates, journal model, and observability contracts from MVP.
- Supervised real-account execution only after paper-path validation.

## Out of scope for initial release

- Fully autonomous production trading.
- Multi-broker high-frequency execution.
- Complex options automation.
- Any attempt to bypass compliance constraints.

## Success criteria

- A human can understand why a trade is suggested.
- A human can compare expected and realized outcomes.
- A human can approve or reject live actions quickly.
- AI costs remain bounded and measurable.
