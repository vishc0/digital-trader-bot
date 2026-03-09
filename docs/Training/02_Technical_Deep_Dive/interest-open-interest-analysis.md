# Interest (Open Interest) Analysis for Chart Traders

[Training Hub](../README.md) | [Section Index](./README.md) | [Foundations](../01_Chart_Foundations/README.md) | [Execution and Risk](../03_Execution_and_Risk/README.md)

This module explains how to use market interest data with charts.

For ETFs and stocks, Open Interest (OI) is most directly relevant in derivatives (index futures, stock futures, options, and perpetuals where available). Spot charts can still use participation proxies.

## What Open Interest Means

Open Interest = total outstanding derivative contracts not yet closed or delivered.

It helps answer: Is the move driven by new positioning or position unwinding?

## Core Price-Volume-OI Matrix

1. Price up + Volume up + OI up -> potential long buildup.
2. Price up + Volume up + OI down -> possible short covering.
3. Price down + Volume up + OI up -> potential short buildup.
4. Price down + Volume up + OI down -> potential long unwinding.

Use this only with chart context and structure.

## Why This Matters for Candlesticks

Same candle can imply different quality depending on OI:

- Bullish breakout candle + rising OI: stronger continuation bias.
- Bullish breakout candle + falling OI: possible squeeze that fades.

## ETF/Stock Context

- Cash equity charts do not have native OI for the underlying stock itself.
- Use options OI distribution, futures OI, and volume participation proxies where relevant.

## Options OI Practical Concepts

- High call OI near strike can act as pin/magnet near expiry.
- High put OI zones can reflect support/hedging behavior.
- Rapid OI changes near key strikes can alter intraday movement quality.

## Scenario 1: Breakout with OI Confirmation

- Index futures breakout above prior high.
- Volume and OI both expand.
- Retest candle holds and closes strong.
- Read: likely sustained positioning, not only forced covering.

## Scenario 2: Up Candle with OI Drop

- Large bullish candle into resistance.
- OI declines while volume spikes.
- Read: short-covering pop risk; continuation may be fragile.

## Scenario 3: Downside Continuation

- Support breaks on bearish engulfing.
- OI rises over next bars.
- Read: fresh shorts adding, downside continuation risk elevated.

## Practical Limits and Cautions

- OI source quality varies by exchange/vendor.
- OI can lag intraday depending data feed.
- Do not use OI in isolation without structure and volume.

## Professional Checklist

Before acting on OI-based read:

1. Is the level structurally meaningful?
2. Does candle close support thesis?
3. Is volume aligned?
4. Is OI behavior confirming or contradicting?
5. Is invalidation clear?

If 2+ answers are unclear, reduce size or skip.
