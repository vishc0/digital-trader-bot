# Consolidated Requirements & Philosophy

## 1. Core Mandates

* **Strict Profit Mandate:** "Always generate profit, hunt for minimizing losses."
* **Positive Expected Value ($E_V$):** Every trade must pass a mathematical expectation filter before execution.
* **Resilience:** The system must be "Stateful," remembering past failures to avoid repeating them.
* **Risk Management:** The system must be "Risk-Averse," never taking on risk that it cannot handle, or be bale to manage the risk it has.
* **Maturity:** The system must be evolving in its thinking, always as a human would do to learn fromt he past and information around it and be able to employ that info to various strategies and see fi the profitability can be impoeved based on past experiences of the syatem and others. "

## 2. Trading Strategy Archetypes (to start with and add to when discovered)

* **A1 (Mean Reversion):** Exploits oversold/overbought conditions (RSI + ATR deviation).
* **A2 (Trend Following):** Captures momentum (SMA Crossovers + MACD).
* **A3 (Stat Arb):** Pairs trading based on Z-Score co-integration.
* **Options Specialization:** "Early Quit" logic to capture theta/vega profits at 75% of target.

## 3. The "Wisdom" Module

* **Human-like Memory:** Stores confidence vectors for strategies. this persistant layer is seperated out from the programs that it executes as i want to turn on and off this system but be able to think better as it runs on the system and executes the programs. seperate the brains from the body.
* **Self-Correction:** If a strategy fails, its confidence score is mathematically degraded. the startegy and the execution will be analyzed and we will try to see if there is missing information so that it can be used later.
* **Data Hygiene:** Filters incoming "false ticks" using Z-Score outlier detection.
