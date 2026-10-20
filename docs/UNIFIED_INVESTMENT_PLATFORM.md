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


## Full-service investment and trading product scope (2026-10-20 expansion)

### Unified domain services
| Service | Required capabilities | Decision outputs |
| --- | --- | --- |
| Security master and corporate actions | Tickers, identifiers, exchanges, asset class, delistings, splits, dividends, mergers, point-in-time history | Canonical security and adjusted time series |
| Market intelligence | Quote timestamps, OHLCV, technical indicators, liquidity, spreads, volatility, breadth, correlation, regime | Market context with stale-data gate |
| Fundamentals and valuation | Standardized financials, peer multiples, DCF assumptions, returns on capital, earnings quality, revisions | Valuation ranges and uncertainty |
| Earnings intelligence | Calendar, consensus estimates, reported figures, surprise, guidance, transcripts, call Q&A, subsequent revisions | Earnings event brief, change versus thesis |
| News/event intelligence | Dated primary releases, secondary context, deduplication, entity attribution, novelty/materiality, source credibility | Event cards linked to revenue/cost/margin and risk |
| Analyst intelligence | Rating/target changes with firm/analyst/as-of dates, consensus and dispersion, revision history, historical forecast quality, conflicts and methodology | Contextual analyst view, never buy/sell solely on target |
| Macro and sector intelligence | Rate curve, inflation, employment, currency, energy, commodity drivers, sector leadership/flows, factor exposure, supply chains | Regime and sector allocation diagnostics |
| Screening and watchlists | Fundamental growth/value/quality, relative strength, trend, earnings windows, scenario constraints | Ranked research queue; saved filters |
| Portfolio management | Multi-account positions, cash/settlement, contributions, dividends, cost basis when accessible, targets, drift, exposure, rebalance candidates | Account-level holdings and policy-aware suggestions |
| Risk and scenario | Position/sector/theme concentration, look-through overlaps, drawdown, VaR with assumptions, stress tests, liquidity, correlation | Breach alerts and mitigation alternatives |
| Strategy research/backtesting | Hypothesis registry, lagged features, walk-forward, holdout, costs, survivorship bias, leakage tests | Research reports and promotion gates |
| Trade planning and execution tracking | Orders proposed vs approved vs placed vs filled; taxes/account restrictions; slippage, fees and fill reconciliation | Human-reviewed trade plan, audit trail |
| Performance and attribution | Time-weighted and money-weighted returns, corporate actions, benchmark total return, sector/factor/decision attribution | Verified performance and learning loop |
| Jobs and governance | Workflow dependencies, success/SLA, data coverage, idempotence, model-cost telemetry, secrets, role access, logs | Run health, alerting, replay and audit |

### Product surfaces and workflows
- **Home:** multi-account net value and allocations, job health, today's market regime, priority earnings/events, pending decisions.
- **Security 360:** price and volume, financial history, valuation, earnings surprise and guidance timeline, sourced news timeline, analyst revision timeline, industry peers, bull/base/bear case, risks, portfolio impact.
- **Sector 360:** performance/breadth and valuations; macro drivers, capital expenditure, supplier/customer chain, constituent overlap and prospective regime shifts.
- **Portfolio 360:** per-account holdings, SPAXX/cash vs securities, realized/unrealized P&L only when data supports it, TWR/MWR where appropriate, dividend and contribution tracking, sector/theme/country/factor exposure, benchmarks, target versus actual, concentration, available funds, rebalance recommendations ranked by benefit, risk and transaction cost.
- **Earnings Workbench:** pre-earnings expectations; post-earnings actual versus consensus and own thesis; revisions to valuation and watchlist status; account-specific earnings risk.
- **Decision Center:** candidate -> portfolio-fit analysis -> alternatives -> risks -> proposal -> owner approval -> manual execution confirmation -> review.
- **Strategy Lab:** separated long-term, swing, and quantitative experiments with reproducible data snapshot IDs and out-of-sample comparison.
- **Ops Console:** schedules, freshness, provider coverage, model routing, prompt/version, cost per report, failures and replay.

### Portfolio suggestion engine
1. Independently evaluate security quality, valuation and catalyst; retain unsupported inputs as unknown.
2. Read **the relevant account's** current positions, cash, constraints, tax treatment, approved strategy targets, contribution/withdrawal plan and pending transactions. If missing, generate diagnostic advice only, not trade-ready sizing.
3. Calculate holdings overlap across sectors and themes (e.g., AI chips, cloud platforms, AI-powered utilities), correlations, downside scenario exposure, cash buffer and transaction costs. Compare with alternatives: hold, add, trim, exit, reallocate and do nothing.
4. Rank **account-specific** suggestions on expected thesis merit, incremental diversification, concentration, opportunity cost, valuation, liquidity, tax/account rules and uncertainty. Show what evidence would invalidate each idea.
5. Produce proposal with account, symbol, snapshot, proposed dollar/share amounts only when verified, estimated post-trade weight, risk gates, thesis, downside scenario, source timestamps, expiry and required approval.
6. Require explicit human signoff for every order and external broker confirmation for filled status; preserve broker execution integrations disabled by default.

### Data model — minimum additional entities
`security_master, market_observation, corporate_action, fiscal_period, estimate_consensus, estimate_revision, earnings_event, transcript_segment, analyst_action, news_event, source_evidence, macro_observation, sector_snapshot, account, portfolio_snapshot, lot_optional, cash_ledger, benchmark_series, investment_thesis, scenario, strategy_version, signal_observation, model_run, job_run, proposal, order_tracking, fill_confirmation, attribution_run`.
Every fact carries observed_at, effective_at, source_published_at (where relevant), ingested_at, provider, immutable evidence reference, quality status, and revisions/version history. No single current-state row should overwrite point-in-time research history.

### Prioritized delivery order
- **Release 1: Portfolio and observability first.** Read-only separate Fidelity account holdings/cash, snapshot quality checks, Security 360 skeleton, news/earnings calendar, decision ledger and dashboard.
- **Release 2: Research intelligence.** Analyst actions, earnings vs consensus, sourced news and sector/macro comparisons, scoring rubric, company research cards.
- **Release 3: Portfolio guidance.** Risk exposures, benchmark-adjusted attribution, policy-aware portfolio-fit scoring, proposed rebalances and manual approval records.
- **Release 4: Strategy lab.** Swing/quant experimentation, rigorous backtests, scenario validation, paper trading only.
- **Release 5: Operational hardening.** Workflow scheduler, provider fallbacks, model evaluation, latency/cost budgets, integration tests, job SLA dashboards.

### Safety, evidence and financial fidelity
- Analyst ratings are opinions, not verified expected returns. Track dates and historical accuracy when licensing/data supports it.
- Historical price and earnings features must be point-in-time; do not train on future revisions.
- LLMs never calculate final portfolio values, fill prices or risk-limit compliance without deterministic independent checks.
- Paid data licenses, redistribution conditions, quotas, terms and audit requirements are deployment prerequisites.
- Portfolio analysis in custodial Roth accounts must respect account/custodian rules and cannot infer trading authority.
- Clarify whether capabilities are prototyped, tested, deployed and operating; documents alone do not count as deployment.
