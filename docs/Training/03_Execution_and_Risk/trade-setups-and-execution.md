# Trade Setups and Execution from Charts

[Training Hub](../README.md) | [Section Index](./README.md) | [Foundations](../01_Chart_Foundations/README.md) | [Technical Deep Dive](../02_Technical_Deep_Dive/README.md)

Professional reference: [Chart to Trade Construction Framework](../04_Fundamental_and_Hybrid_Analysis/chart-to-trade-construction-framework.md)

A setup is only professional if it includes trigger, invalidation, and management.

## Setup Architecture

Every setup must define:

- Context: trend/range + key level
- Trigger: objective candle/price event
- Invalidation: exact condition that proves idea wrong
- Target logic: where reward is extracted
- Management rule: partials, trailing, or time stop

## Core Setup Families

### 1) Trend Pullback Continuation

- Context: established trend.
- Trigger: rejection/engulfing at pullback zone.
- Invalidation: break of pullback structure.

### 2) Breakout and Retest

- Context: compression under/over major level.
- Trigger: breakout close + successful retest.
- Invalidation: close back inside range with follow-through.

### 3) Reversal at Exhaustion Zone

- Context: extended move into higher-timeframe level.
- Trigger: rejection candle + structure shift.
- Invalidation: reclaim of rejection extreme.

## Entry Methods

- Breakout entry (aggressive)
- Close confirmation entry (balanced)
- Retest entry (conservative, better R)

## Trade Management Models

- Fixed target model: 2R/3R objective.
- Scale-out model: partial at 1R, trail remainder.
- Structure trail: trail under higher lows / above lower highs.

## Scenario 1: Pullback Continuation

- ETF uptrend pulls back to support + 20EMA.
- Bullish engulfing trigger.
- Entry on break of trigger high.
- Stop below pullback low.
- Partial at prior high, trail rest.

## Scenario 2: Failed Breakout Reversal

- Stock breaks range high, then closes back below.
- Next candle confirms downside.
- Entry short on neckline break.
- Stop above failed breakout wick.

## Common Execution Errors

- Entering before trigger confirmation.
- Moving stop wider without plan.
- Taking profits randomly due to fear.

## Expert Rule

If invalidation is unclear, setup is incomplete; do not trade it.
