# Unified Investment Intelligence Platform — Implementation Blueprint
Status: architecture proposal, not a deployed trading system. Updated: 2026-10-20.

## Scope and preservation
Consolidate Digital Trader Bot, Growth Rotation, swing-trading education/research, ORIA multi-model validation, and Fidelity reporting into a modular research and decision platform. Preserve all existing code; migrate via adapters and tests, not wholesale replacement.
Three isolated strategy namespaces: `growth_rotation` (separate Shivam/Shourya custodial IRA accounts), `swing_research`, and `quant_lab`. Common evidence, security master, market data, run ledger and dashboard; separate portfolio ledgers, policies, strategies, benchmarking and experiment results.
No unattended live orders. All Fidelity orders are placed manually by the account custodian. Approval != order != confirmed fill.

## Architecture modules
1. `platform/backend/data`: as-of timestamped price, corporate action, holdings, settlement cash, filings, news and fundamentals adapters; source provenance, immutable snapshots, stale/coverage flags; licensed-provider rules.
2. `platform/backend/core`: strategy registry, benchmark returns, 100-point fundamental scoring, portfolio optimizer, exposure graph, risk policy evaluator, decision ledger.
3. `platform/backend/research` (new): deterministic financial ratios, point-in-time feature store, source-verified event extraction, multi-model thesis/counterargument review.
4. `platform/backend/backtest` (new): reproducible walk-forward/backtest; delistings, historical universe, transaction costs, slippage, earnings and execution lag, unseen holdout. Anti-look-ahead tests required before strategy promotion.
5. `platform/backend/connectors`: Fidelity read-only data import/connector if available; simulated execution for labs. Never infer read-only reporting access is broker trading access.
6. `platform/gateway` and `platform/frontend`: strategy-separated console, data health, allocations, thesis cards, job status, human approval/confirmation and audit log.
7. Scheduler: orchestrate via existing deployed stack only after inventory; retries idempotent, backfills, durable state, source freshness alerts.

## Task-to-model routing (configurable, no hard-coded vendor dependency)
| Task | Default | Escalation |
| --- | --- | --- |
| Data ingestion, prices, math, risk gates | Deterministic Python/SQL | Never trust LLM for authoritative numerical state |
| Classification/dedup, routine brief | Small local/inexpensive text model | Escalate when sources contradict |
| Source retrieval/filing extraction | Search/retrieval plus structured validation | Stronger reasoning model for ambiguous document interpretation |
| Valuation, adversarial thesis, portfolio interactions | High-reasoning cloud model with cited evidence | Human review and independent calculation |
| Coding/tests and optimization | Coding-focused model in separate review loop | Human PR review |
| Backtests | Versioned Python engine | Stronger model may critique design but never substitute statistical validation |

Record model ID/version, cost, latency, prompt/template version, evidence refs, quality checks in every AI-assisted run. Tier by task, not headline model ranking.

## Approved investment context
- Accounts: Fidelity Shivam and Shourya custodial Roth IRAs, segregated.
- Oct 1 latest framework: eventually 80% individual stocks / 20% cash; research envelopes AI/technology 25%, cybersecurity 15%, power/infrastructure 15%, oil/gas/refining 15%, established pharma 10%. These sum to the proposed stock sleeve and are not forced deployment budgets.
- No company-specific targets or trade orders approved. Earlier ETF mixes and Oct 5 one-off ticker allocation superseded.
- Proposed, not approved, guards: typical position 2–4%, review above 6%, theme/sector review 30%, 3-trading-day pre-earnings blackout, 10% monthly sale turnover review. No options/leverage in this sleeve.
- Score growth 20, guidance 15, FCF/margin/efficiency 15, valuation 15, momentum 15, industry 10, catalyst 5, balance sheet 5; missing inputs remain N/A.
- Performance requires matched-period, cash-flow-adjusted benchmark against SPY total return, not price-only.

## Job catalog and recommended cadence
- `daily_investment_brief`: 08:00 ET daily. Check holdings and source freshness; compare previous close and only material news; short exceptions and HOLD/INVESTIGATE/PROPOSE states. Currently implemented in ChatGPT Automations as 'Unified Investment Morning Brief'. It is not this repository's cron job.
- `deep_portfolio_review`: first and third Wednesday ET, after market close; rerun risk/exposure/valuation for material holdings, prepare non-executing review.
- `monthly_research_refresh`: last trading close, point-in-time ranking and thesis refresh; store score coverage and drift.
- `nightly_ingest_check`: scheduled after source publication, verify timestamps, completeness, schema, idempotence, price split/corporate actions and provider failures.
- `weekly_strategy_validation`: research only; rolling out-of-sample metrics, stability, turnover and leakage checks.
Do not activate further automations until their source feeds and ownership are tested; avoid duplicate notifications.

## Decision ledger schema
`decision_id, account_id, strategy_id, symbol, snapshot_id, thesis_id, source_timestamps, target_weight_nullable, current_weight_nullable, shares_nullable, available_cash_nullable, earnings_date_nullable, risk_checks, counterargument, expires_at, state, placed_at_nullable, filled_at_nullable, fill_ref_nullable`.
State transitions: RESEARCH -> PROPOSED -> APPROVED -> PLACED -> FILLED; REJECTED/CANCELLED/EXPIRED available. A manual broker fill confirmation is required for FILLED.

## MVP acceptance criteria
1. Read-only holdings snapshots with per-account as-of times and explicit incomplete-coverage states, tested missing/stale/zero cases.
2. Immutable sourced evidence cards, deterministic 100-point score with missing inputs reported N/A.
3. Data/risk gate prevents execution-ready proposals without buying power, approved security targets, dated prices, earnings date and explicit user approval.
4. Matching period total-return performance and cash-flow treatment tested against synthetic fixtures.
5. Replayable daily brief with decision IDs, source citation ledger, model/cost telemetry and idempotent reruns.
6. Backtest engine proves no look-ahead on fixture tests and produces transaction-cost-sensitive out-of-sample reports.
7. No broker execution credential or live order endpoints enabled.

## Phased delivery
P0 inventory dependencies, secret handling and existing job definitions; baseline tests. P1 data adapters, evidence schema, accounts and decision ledger. P2 existing Growth Rotation scorecard/dashboard integration. P3 swing/quant research and backtest connectors. P4 scheduler, model routing evaluation and observable production hardening. Each phase requires tests, backout, budget ceiling, and human signoff.
