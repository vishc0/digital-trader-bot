# Backtesting, Paper Trading, and Journaling

[Training Hub](../README.md) | [Section Index](./README.md) | [Foundations](../01_Chart_Foundations/README.md) | [Technical Deep Dive](../02_Technical_Deep_Dive/README.md)

Skill becomes strategy only when measured.

## Phase 1: Rule Definition

Before backtesting, define:

- Setup context
- Trigger
- Invalidation
- Exit rules
- Session/time constraints

Vague rules produce useless data.

## Phase 2: Backtesting

Collect at least 50-100 samples per setup.

Track:

- Win rate
- Average R per trade
- Max losing streak
- Max drawdown
- Time in trade

Segment by market regime (trend/range/high vol).

## Phase 3: Paper Trading

Purpose:

- Validate execution discipline in live conditions.
- Measure slippage and emotional deviations.

Run 20-40 paper trades before real capital.

## Phase 4: Journaling

For each trade, capture:

- Screenshot before entry and after exit.
- Setup type and timeframe stack.
- Entry, stop, target, and R outcome.
- Mistakes (if any) and correction rule.

## Error Taxonomy (Use in Journal)

- E1: Early entry before trigger.
- E2: Late chase after extension.
- E3: Invalid stop adjustment.
- E4: No-plan exit.
- E5: Overtrading low-quality context.

## Weekly Review Process

- Rank top 3 best setups by expectancy.
- Rank top 3 avoidable errors by frequency.
- Create one improvement rule for next week.

## Scenario: From Theory to Execution

- Backtest shows breakout-retest setup has +0.42R expectancy.
- Paper trading shows execution drift reduces to +0.10R.
- Journal finds repeated late entries.
- New rule: no entry if trigger candle >1.5x average range.

This is how edge is preserved in real-time trading.

## Daily 1-Hour Template

- 15 min review prior trades.
- 20 min chart replay/backtest samples.
- 15 min paper trade simulation planning.
- 10 min journal update and next-day focus rule.
