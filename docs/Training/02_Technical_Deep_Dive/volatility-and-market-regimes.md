# Volatility and Market Regimes on Charts

[Training Hub](../README.md) | [Section Index](./README.md) | [Foundations](../01_Chart_Foundations/README.md) | [Execution and Risk](../03_Execution_and_Risk/README.md)

Volatility determines how far price can move and how wide your risk must be.

## Regime Types

- Low volatility compression
- Normal volatility trend
- High volatility expansion/shock

Each regime needs different expectations and stop logic.

## Volatility Tools

- ATR (Average True Range)
- Bollinger Band width (optional)
- Candle range expansion vs rolling average

## Practical Effects on Trading

### Low Volatility

- More fakeouts in tight ranges.
- Need patience for confirmed expansion.

### High Volatility

- Larger candle swings and slippage risk.
- Stops must be wider; position size must be smaller.

## ATR-Based Planning

- Baseline stop = beyond structure + ATR buffer.
- In high volatility, reduce share size to keep fixed risk constant.

Example:

- Risk budget: $100.
- Stop distance doubles due to volatility.
- Position size should roughly halve.

## Regime Shift Clues on Charts

- Sudden series of wide candles after compression.
- Gap behavior and failed gap fills.
- Persistent range expansion over several bars.

## Scenario 1: Compression Breakout

- ETF trades in narrow band for 3 sessions.
- ATR contracts to monthly low.
- Expansion candle breaks range with high volume.
- Follow-through likely if regime shift sustains.

## Scenario 2: High-Volatility Trap

- Stock spikes on headline, then reverses inside prior range.
- ATR jumps sharply.
- Do not use old stop distance assumptions.

## Mistakes to Avoid

- Using fixed stop distances in all regimes.
- Chasing late in expanded candles during high-vol spikes.
- Ignoring event calendar impact on volatility.

## Training Drill

For 30 trades, log volatility regime at entry and compare expectancy by regime.
