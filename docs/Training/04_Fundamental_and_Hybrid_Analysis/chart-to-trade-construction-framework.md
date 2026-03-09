# Chart to Trade Construction Framework

[Training Hub](../README.md) | [Section Index](./README.md) | [Chart Foundations](../01_Chart_Foundations/README.md) | [Execution and Risk](../03_Execution_and_Risk/README.md)

This module gives a repeatable way to construct trades directly from charts.

## The 8-Step Construction Process

1. Define market regime.
2. Mark key levels and liquidity zones.
3. Set directional thesis (long/short/neutral).
4. Select timeframe stack (anchor/setup/trigger).
5. Wait for trigger pattern.
6. Define invalidation and stop distance.
7. Compute position size from fixed risk.
8. Predefine target and management plan.

## Step-by-Step Detail

### Step 1: Regime

- Trending, ranging, or transitioning.
- Trade type must match regime.

### Step 2: Levels

- Prior day/week highs-lows.
- Support/resistance zones.
- Breakout boundaries and VWAP context.

### Step 3: Thesis

- One sentence max.
- Example: "Daily uptrend pullback into support likely continues if 1H reclaims local high."

### Step 4: Timeframes

Use professional stacks from [Professional Timeframe Combinations Guide](professional-timeframe-combinations-guide.md).

### Step 5: Trigger

Valid triggers:

- Breakout close + hold
- Engulfing at level
- Rejection + structure break

### Step 6: Invalidation

Invalidation is where thesis is wrong, not where pain begins.

### Step 7: Sizing

- Risk budget fixed per trade.
- Position size = risk / stop distance.

### Step 8: Targets and Management

- Target 1 at nearest logical barrier.
- Target 2 at extension or trailing structure.
- Time stop if no follow-through.

## Trade Construction Template

- Instrument:
- Regime:
- Thesis:
- Anchor/Setup/Trigger timeframes:
- Setup level:
- Trigger condition:
- Entry price:
- Invalidation:
- Stop:
- Position size:
- Target(s):
- Management rule:
- Abort condition:

## Scenario: ETF Swing Long

- Anchor (Daily): uptrend.
- Setup (4H): pullback to support + compression.
- Trigger (1H): bullish engulfing above compression high.
- Stop: below 1H structure low.
- Target: prior daily high then trail.

## Common Construction Errors

- Entering before trigger.
- No written invalidation.
- Position sizing from confidence, not stop distance.
- Changing trade type mid-trade.

## Performance Upgrade

Store each constructed trade in a journal and compare planned vs executed behavior weekly.
