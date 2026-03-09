# Software Delivery Lead Guide

## Delivery principles

- Document first, then implement.
- Release small slices with observable outcomes.
- Keep every milestone demoable.
- Track token spend as a delivery KPI.

## Suggested phases

### Phase 1: Documentation and alignment

- Finalize platform intent.
- Confirm current gaps.
- Define service contracts and glossary.
- Freeze rollout split: built-in paper trading MVP, Fidelity market-account integration in Phase 2.

### Phase 2: Foundation hardening

- Secure Redis and secrets.
- Add health, metrics, and tracing.
- Make journaling durable.
- Define internal paper account, cash ledger, position ledger, order, and fill lifecycle.

### Phase 3: Core portfolio workflows

- Account ingestion.
- Portfolio monitoring.
- Trade suggestion review.
- Expected vs actual analysis.
- Deliver the operator control plane against the built-in paper account.

### Phase 4: Broker and execution workflows

- Replace Fidelity mock with real adapter for Phase 2.
- Preserve MVP paper path while adding Fidelity-backed supervised execution controls.
- Add approval and compliance checks.

### Phase 5: Cloud deployment and optimization

- GCP or AWS reference deployment.
- Cost controls, auto-scaling, dashboards.

## Release gates

- Docs updated.
- Tests passing.
- Dashboard visibility available.
- Token budgets defined.
- Rollback path documented.
