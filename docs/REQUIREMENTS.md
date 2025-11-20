# Consolidated Requirements & Philosophy

## 1. Core Mandates
* **Strict Profit Mandate:** "Always generate profit, hunt for minimizing losses."
* **Positive Expected Value ($E_V$):** Every trade must pass a mathematical expectation filter before execution.
* **Resilience:** The system must be "Stateful," remembering past failures to avoid repeating them.

## 2. Trading Strategy Archetypes
* **A1 (Mean Reversion):** Exploits oversold/overbought conditions (RSI + ATR deviation).
* **A2 (Trend Following):** Captures momentum (SMA Crossovers + MACD).
* **A3 (Stat Arb):** Pairs trading based on Z-Score co-integration.
* **Options Specialization:** "Early Quit" logic to capture theta/vega profits at 75% of target.

## 3. The "Wisdom" Module
* **Human-like Memory:** Stores confidence vectors for strategies.
* **Self-Correction:** If a strategy fails, its confidence score is mathematically degraded.
* **Data Hygiene:** Filters incoming "false ticks" using Z-Score outlier detection.