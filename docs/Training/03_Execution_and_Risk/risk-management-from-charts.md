# Risk Management from Charts

[Training Hub](../README.md) | [Section Index](./README.md) | [Foundations](../01_Chart_Foundations/README.md) | [Technical Deep Dive](../02_Technical_Deep_Dive/README.md)

You do not control market outcome; you control risk structure.

## Risk First Principles

- Capital protection is the first edge.
- One trade should not materially damage account equity.
- Position size is a function of stop distance and risk budget.

## Position Sizing Formula

Position Size = Risk Amount / Stop Distance

Example:

- Account risk per trade: $100
- Stop distance: $2
- Position size: 50 shares

If stop distance increases, position size must decrease.

## Stop Placement from Chart Structure

Preferred stop logic:

- Beyond meaningful swing (not inside noise).
- Optional ATR buffer beyond structural point.
- Aligned with setup invalidation, not pain tolerance.

## R-Multiple Framework

- 1R = amount risked.
- Evaluate outcomes in R, not dollars.
- Consistency in R reveals strategy quality.

## Expectancy Focus

Expectancy depends on:

- Win rate
- Average win size
- Average loss size

A strategy can be profitable with <50% win rate if wins are larger than losses.

## Drawdown Controls

- Daily max loss limit.
- Consecutive loss stop rule.
- Reduce size after drawdown threshold.

## Scenario 1: Same Setup, Different Volatility

- Setup appears in calm market: 1.2% stop.
- Same setup in volatile market: 2.4% stop.
- Keep risk constant by reducing position size in volatile regime.

## Scenario 2: Good Setup, Bad Reward

- Trigger valid but nearest resistance gives only 0.8R potential.
- Skip trade; risk/reward is not favorable.

## Professional Risk Checklist

Before entry:

1. What is exact invalidation?
2. What is stop distance?
3. What is size for fixed risk?
4. Is reward realistic before major barrier?
5. What is trade management plan?

No risk plan, no trade.
