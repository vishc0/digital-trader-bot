# Wisdom Signals (Fundamentals-Oriented, Multibagger Heuristics)

Purpose: seed the Wisdom component with pragmatic, fundamentals-based factors inspired by common "multibagger" heuristics. These are starter rules to gate or weight ideas; refine as real data and research arrive.

## Core Factor Groups

### Growth Quality

- Revenue CAGR (3–5y): prefer >15–20%; penalize volatility.
- EPS CAGR (3–5y): prefer >15–20%; stable/expanding margins.
- Operating margin trend: expanding or stable over 3–5y.

### Capital Efficiency

- ROCE/ROIC: prefer >15%; exclude leverage-inflated ROCE.
- FCF conversion: CFO/EBITDA >70%; cumulative FCF positive over cycle.

### Balance Sheet Safety

- Net debt / EBITDA: prefer <1.5x (cap score above 2.5x).
- Interest coverage: prefer >5–8x.

### Capital Allocation

- Reinvestment rate: high reinvestment + high ROCE = strong; penalize diworsification (unrelated acquisitions).
- Buybacks/dividends: only positive if funded from FCF (not debt).

### Moat & Durability

- Structure: oligopoly/niche leadership, switching costs, network effects, brand.
- Customer metrics (if available): retention/churn, rising ARPU, efficient CAC/payback.

### Industry & Tailwinds

- Secular driver: clear long-term tailwind (e.g., digitization/formalization/infra capex).
- Cyclicality: apply discount in commodity/cyclical sectors unless balance sheet is strong and at cycle trough.

### Governance & Quality

- Insider/promoter holding: stable or rising; low/no pledging.
- Related-party red flags: frequent/large RPTs, auditor churn → penalty.
- Disclosure stability: penalize sudden metric-definition changes.

### Valuation & Risk

- Valuation tension: cap upside score if P/E or EV/EBIT is top-decile for sector without commensurate growth.
- Drawdown fragility: large past drawdowns on small news → fragility penalty.

## Quick Pass/Fail Heuristic (thin-data mode)

- Pass if: ROCE >15%, Rev/EPS CAGR >15% (3–5y), Net debt/EBITDA <1.5x, OPM stable/up, FCF positive over cycle, no governance red flags, valuation not top-decile for sector.
- Hard haircuts: net debt/EBITDA >2.5x AND interest cover <3x; governance red (pledging/auditor churn/large RPTs); negative cumulative FCF with ongoing dilution.

## Feature Vector Sketch (normalize 0–1)

- rev_cagr_5y, eps_cagr_5y, margin_trend
- roce, fcf_conv
- net_debt_ebitda, int_cov
- reinvest_rate, buyback_quality
- moat_score, tailwind_score, gov_score
- valuation_tension, cyclicality_penalty

## Scoring Guidelines

- Positive weights: growth, ROCE, FCF conversion, moat, tailwind, governance.
- Negative weights: leverage, valuation_tension, cyclicality_penalty.
- Rule gates: block/clip score if leverage/gov thresholds breached.

## Data Needs (minimal viable ingest)

- Financials: revenue/EBITDA/EPS history, cash flows, debt, interest.
- Capital allocation: capex vs. acquisitions; buyback/dividend history; funding source.
- Ownership: insider/promoter % and pledging; institutional trend if available.
- Industry tags: sector, cyclicality flag, tailwind descriptors.
- Valuation bands: sector-relative percentiles for P/E, EV/EBIT, EV/S.

## Integration Points

- State Manager: apply hard gates (leverage/governance) before allowing strategy confidence > X.
- Strategy Engine: modulate aggression/position size using wisdom score (e.g., scale exposure by normalized score).
- Wisdom Builder: update factor weights as realized performance accumulates; downweight factors that don’t correlate with outcomes.

## Next Steps

1) Choose data source for fundamentals (API or CSV) and map to the feature vector.
2) Implement normalization and gating logic in Wisdom/State Manager.
3) Add unit tests for scoring and gating edge cases.
4) Backtest factor impacts on historical picks to calibrate weights.

## When You Get Transcripts

- Re-run extraction to add any speaker-specific heuristics (e.g., sector filters, qualitative cues). Use them to adjust weights or add new moat/tailwind patterns.
