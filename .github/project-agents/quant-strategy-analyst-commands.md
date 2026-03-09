# Quant Strategy Analyst Custom Commands

These are reusable prompt commands for the `quant-strategy-analyst` agent.

## Usage pattern
Use a command name followed by compact context.

Example:
`/quant-strategy-plan strategy="trend follow exit assist" assetScope="liquid large-cap stocks"`

## Commands

### `/quant-strategy-plan`
Define a strategy in compact form.

**Input**
- strategy
- assetScope
- objective

**Output**
- hypothesis
- regime fit
- inputs
- entry logic
- exit logic
- evaluation plan

### `/quant-hypothesis`
Write or refine a strategy hypothesis.

**Input**
- idea
- target outcome

**Output**
- one-line hypothesis
- assumptions
- measurable signals
- invalidation

### `/quant-feature-set`
Define the smallest useful feature set.

**Input**
- strategy
- regime

**Output**
- required features
- optional features
- observability needs
- noise reduction notes

### `/quant-entry-exit`
Specify entry and exit rules.

**Input**
- strategy
- regime

**Output**
- entry trigger
- hold logic
- trim logic
- exit logic
- invalidation

### `/quant-regime-fit`
Check when a strategy should or should not run.

**Input**
- strategy
- market context

**Output**
- suitable regimes
- unsuitable regimes
- warning signals
- gating guidance

### `/quant-backtest-plan`
Create a compact evaluation plan.

**Input**
- strategy
- available data

**Output**
- test slices
- key metrics
- drift checks
- pass or fail criteria

### `/quant-paper-review`
Review paper-trade behavior.

**Input**
- strategy
- observed outcomes

**Output**
- what worked
- what failed
- drift notes
- next recommendation

### `/quant-expected-actual`
Compare planned and realized outcomes.

**Input**
- strategy
- expected summary
- actual summary

**Output**
- deltas
- likely causes
- adjustments
- monitoring needs

### `/quant-prune`
Decide whether to keep, refine, pause, or retire a strategy.

**Input**
- strategy
- evidence summary

**Output**
- decision
- rationale
- next action
- review timing

## Token-efficient examples
- `/quant-hypothesis idea="mean reversion on oversold liquid names" target outcome="short-hold reversal capture"`
- `/quant-entry-exit strategy="portfolio trim winners" regime="concentration elevated, breadth weakening"`
- `/quant-expected-actual strategy="trend-follow signal" expected summary="3% target, low drawdown" actual summary="late exits, weaker breadth follow-through"`
