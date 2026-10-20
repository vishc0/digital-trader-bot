# Portfolio policy MVP

The initial implementation is deliberately **read-only**. No broker order submission exists here. Keep production trading disabled until broker-side permission verification, authoritative settled buying-power ingestion, open-order reconciliation, persistence, security controls, and integration testing are complete.

## Run tests
```bash
python -m unittest discover -s tests -p 'test_portfolio_core.py' -v
```

## Core modules
- `Account`: per-account broker, legal category and verified permission flags; never store credentials here.
- `Proposal`: a candidate order; never an approved order.
- `evaluate()`: account-mismatch, asset eligibility, verified cash and position checks; ALWAYS returns `execution_enabled=False`.
- `summarize()`: position values with price dates.
- `reconcile()`: expected versus observed positions, explicitly treating missing observations as missing, not zero.

## Next iteration
1. Obtain source-verified broker capabilities, legal registration and custodian roles for Fidelity custodial Roth accounts, Schwab IRA and E*TRADE brokerage.
2. Read-only connectors with freshness checks, order holds, settled/unsettled cash and broker truth.
3. Immutable decision journal, approval state machine, account-level allocation dashboards, dividend and corporate action reconciliation.
4. Integrate earnings/news/analyst/sector data with source citations and as-of dates.
5. Add property-based and integration tests, CI, and release controls. Do not deploy an execution adapter until a separate explicit authorization and production review.
