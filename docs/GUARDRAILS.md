# 🚧 System Guardrails

**Purpose**: This document defines the *immutable laws* of the Platform. No strategy or AI recommendation can override these rules.

## 1. Capital Protection (Hard Limits)

These checks are enforced by the **State Manager** before any order is sent to the Execution Manager.

* **Max Drawdown Per Day**: `5%` of Total Equity.
  * *Action*: If reached, trigger **Kill Switch** (Close all positions, stop trading).
* **Max Position Size**: `10%` of Total Equity per symbol.
* **Max Open Orders**: `20` active orders max to prevent rate-limit bans.

## 2. AI Safety (The "Hallucination" Firewall)

* **Price Sanity Check**:
  * AI Order Price must be within `2%` of the last traded price from the Data Handler.
  * *Action*: Reject order if price deviates > 2%.
* **Ticker Validation**:
  * AI can only trade symbols in the `Approved_Universe` list (e.g., S&P 500).
  * *Action*: Reject unknown tickers (prevents trading "fake" or "delisted" stocks).

## 3. Operational Logic

* **The "Fat Finger" Check**:
  * Max Notional Value per Trade: `$10,000` (adjustable).
  * *Action*: Reject trade if size > Limit.
* **Kill Switch Manual Override**:
  * Administrator (You) can hit the physical/digital red button at any time.
  * *System Response*: Immediate `CancelAll` broadcast to all brokers.

## 4. Compliance & Logging

* **Immutable Logs**: Every "Decision" (Strategy Signal and Risk Check result) must be logged to Firestore/Journal *before* execution.
* **Audit Trail**: The specific code version (Git Hash) and Model Version must be recorded with every trade.
