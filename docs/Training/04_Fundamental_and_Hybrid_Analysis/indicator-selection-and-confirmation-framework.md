# Indicator Selection and Confirmation Framework

[Training Hub](../README.md) | [Section Index](./README.md) | [Technical Deep Dive](../02_Technical_Deep_Dive/README.md) | [Execution and Risk](../03_Execution_and_Risk/README.md)

This module explains why specific indicators are used as primary signals vs confirmation signals.

## Indicator Philosophy

- Price structure is primary.
- Indicators are evidence layers.
- Use a small, non-redundant stack.

## Primary vs Confirmation Indicators

### Primary (Trade Direction and Trigger Context)

1. Trend Structure + Moving Averages (20/50/200 EMA)
   - Reason: identifies direction and pullback zones in a way many participants also track.

2. VWAP (intraday)
   - Reason: institutional benchmark for session value; useful for ETF/large-cap intraday bias.

3. Volume/RVOL
   - Reason: validates whether breakout/reversal has participation.

### Confirmation (Improve quality, not replace thesis)

1. RSI
   - Reason: momentum regime filter (above/below 50) and divergence context.

2. MACD
   - Reason: momentum phase shift and trend continuation timing.

3. ATR
   - Reason: volatility-aware stop and sizing, not direction prediction.

## Why These Indicators (Fundamental Logic)

- MA/VWAP: capture behavior of broad market participants and execution benchmarks.
- Volume: a move without participation is less durable.
- RSI/MACD: momentum confirmation reduces poor-quality entries.
- ATR: controls risk relative to regime conditions.

## Professional Indicator Sets by Setup Type

### Trend Pullback Setup

- Primary: structure + 20/50 EMA + volume contraction/expansion.
- Confirmation: RSI staying in bullish/bearish regime.

### Breakout Setup

- Primary: level break + RVOL expansion + close quality.
- Confirmation: MACD histogram expansion and no immediate divergence warning.

### Reversal Setup

- Primary: rejection candle at key level + structure shift.
- Confirmation: RSI divergence + volume spike + failed follow-through in old trend direction.

## Avoid Redundancy

Do not stack multiple indicators that measure nearly the same thing.

Example of redundancy:

- MACD + Stoch + RSI + CCI all trying to signal momentum overbought/oversold.

Prefer clarity:

- One trend tool, one participation tool, one momentum confirmer, one risk tool.

## Indicator Decision Grid

Before trade, answer:

1. Which indicator is my primary evidence?
2. Which one confirms (not leads) this idea?
3. Is any indicator contradicting the setup strongly?
4. If yes, reduce size or skip.

## Example Workflow

- Daily uptrend and support hold.
- 4H pullback into 20 EMA.
- 1H bullish engulfing with RVOL > 1.5.
- RSI reclaims > 50.

Trade is accepted because structure + participation + momentum confirmation align.

## Final Rule

If an indicator gives the signal before price structure is valid, ignore it. Structure first, indicators second.
