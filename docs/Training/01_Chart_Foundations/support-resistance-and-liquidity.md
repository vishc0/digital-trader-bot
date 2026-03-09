# Support, Resistance, and Liquidity on Charts

[Training Hub](../README.md) | [Section Index](./README.md) | [Technical Deep Dive](../02_Technical_Deep_Dive/README.md)

Support/resistance is not a single line; it is a zone where order flow previously reacted.

## Core Concepts

- Support: area where demand previously defended price.
- Resistance: area where supply previously capped price.
- Flip zone: former resistance acts as support (or reverse) after acceptance.

## Liquidity Perspective

Price often moves toward liquidity before choosing direction.

Common liquidity pools:

- Equal highs (buy-side stops above)
- Equal lows (sell-side stops below)
- Prior day high/low
- Opening range extremes

## Rejection vs Acceptance at Levels

- Rejection: wick through level but close back inside zone.
- Acceptance: multiple closes beyond level with follow-through.

This distinction prevents many false breakout entries.

## Level Quality Score

A level is stronger when:

- It appears on higher timeframe.
- It has multiple historical reactions.
- It aligns with trend pullback zone.
- It coincides with high volume node or VWAP context.

## Scenario 1: Support Hold Long

- ETF in daily uptrend retraces to prior breakout support.
- 1h prints long-lower-wick rejection + bullish confirmation candle.
- Entry on confirmation break; stop below rejection wick.

## Scenario 2: Resistance Sweep Reversal

- Stock runs above obvious equal highs near resistance.
- Next candle closes back below level on strong volume.
- Interpretation: liquidity sweep and potential downside rotation.

## Practical Trading Rules

- Never place entries exactly at level without trigger.
- Use zone width, not razor-thin lines.
- Wait for candle close confirmation around major levels.

## Common Errors

- Drawing too many levels.
- Treating all levels equally.
- Ignoring market regime (trend vs range).

## Learning Exercise

On 30 past charts, tag:

- Support hold continuation
- Resistance rejection reversal
- Level break and successful retest

Record which context had highest quality outcomes.
