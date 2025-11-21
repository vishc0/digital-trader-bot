# Digital Trader Bot - System Architecture

**Version:** 1.0 (Level 5 Maturity - Stateful, Self-Correcting, Context-Aware)  
**Status:** MVP (Minimum Viable Product)  
**Infrastructure:** Google Cloud Platform + Redis + Firestore / AWS Equivalent

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Core Philosophy](#core-philosophy)
3. [Architecture Blueprint](#architecture-blueprint)
4. [Microservices](#microservices)
5. [Data Flow](#data-flow)
6. [Trading Strategies](#trading-strategies)
7. [Safety Mechanisms](#safety-mechanisms)
8. [Deployment](#deployment)

---

## System Overview

**Digital Trader Bot** is an autonomous trading platform designed for "Conservative Aggression":
- **Aggressive**: Hunt for profit maximization
- **Conservative**: Never incur catastrophic losses via hard-coded circuit breakers
- **Autonomous**: Self-learning system that adapts strategy parameters based on realized performance
- **Stateful**: Maintains memory of past failures to avoid repeating them

### Key Differentiators

1. **The Wisdom Module**: Unlike traditional bots, this system learns from every trade, adjusting confidence vectors nightly
2. **No Chatty Architecture**: Uses Redis + MsgPack (binary protocol) instead of HTTP microservices for ~80x efficiency gain
3. **Context-Aware**: Integrates external intelligence (news, sentiment) via Gemini LLM to detect regime changes
4. **Immutable Audit Trail**: Firestore journaling captures every signal, execution, and learning adjustment

---

## Core Philosophy

### Never Loss Mandate
- Every trade must pass an **Expected Value (EV)** mathematical filter before execution
- Formula: `EV = (Win_Rate × Avg_Win) - (Loss_Rate × Avg_Loss)`
- Only execute if EV > 0.5% (with margin for safety)

### Resilience Through Memory
- The "Wisdom Builder" runs nightly, analyzing all closed trades
- Adjusts strategy confidence scores based on realized P&L
- Implements parameter optimization (E1 learning) and regime detection (E2)

### Hard-Coded Safety
- Circuit Breaker: Stops all trading if daily losses exceed a set threshold (e.g., -$500)
- Tremor Filter: Ignores noisy data; requires strong conviction before acting
- Implementation Shortfall Tracking: Monitors slippage and latency to identify infrastructure decay

---

## Architecture Blueprint

### System Design Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│                    Central Brain (State Manager)                │
│                    ├─ Redis Memorystore                         │
│                    ├─ MsgPack Serialization                     │
│                    └─ Circuit Breaker Logic                     │
└──────────────────────────┬──────────────────────────────────────┘
                           │ (MsgPack Protocol - Low Latency)
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Strategy Engine │ │  Wisdom Builder │ │External Intel   │
│ (SES)           │ │  (Nightly)      │ │ (News/Sentiment)│
│ ├─A1: MR        │ │ ├─Reflect       │ │ ├─Gemini LLM   │
│ ├─A2: TF        │ │ ├─Optimize      │ │ ├─Regime Tags  │
│ ├─A3: StatArb   │ │ └─Drift Check   │ │ └─Alerts       │
│ └─Options       │ │                 │ │                │
└──────┬──────────┘ └────────┬────────┘ └─────────┬──────┘
       │                     │                    │
       └──────────────────────┼────────────────────┘
                              │
        ┌─────────────────────┼──────────────────┐
        │                     │                  │
        ▼                     ▼                  ▼
┌─────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│Data Handler     │ │Journaling Service│ │Execution Manager │
│├─Historical Data│ │(Firestore)       │ │(Broker APIs)     │
│├─BBO Handler    │ │├─Trade Events    │ │├─Order Placement │
│└─Normalization  │ │├─Wisdom Adjusts  │ │├─Slippage Track  │
│                 │ │└─Pattern Storage │ │└─Risk Mgmt       │
└─────────────────┘ └──────────────────┘ └──────────────────┘
```

### Technology Stack

| Component | Tech Stack | Rationale |
|-----------|-----------|-----------|
| **Central Brain** | Redis + MsgPack | Single source of truth; binary protocol for 80x efficiency |
| **Compute** | Python 3.9+ | Pandas, NumPy, TA-Lib for quant analysis |
| **Orchestration** | Cloud Run (GCP) / Lambda (AWS) | Serverless for cost efficiency |
| **State Storage** | Cloud Memorystore (Redis) | Sub-millisecond latency |
| **Persistence** | Firestore / DynamoDB | Immutable audit trail |
| **External Data** | Gemini LLM API | News/sentiment analysis |
| **CI/CD** | Cloud Build / GitHub Actions | Auto-deploy on git push |

---

## Microservices

### 1. **State Manager** (`src/state_manager/`)
**The Brain: Central Nervous System**

**Responsibilities:**
- Maintains Redis connection pool and MsgPack serialization
- Implements Circuit Breaker safety checks
- Stores/retrieves strategy confidence vectors
- Tracks daily P&L and risk metrics

**Key Methods:**
- `check_circuit_breaker()`: Validates if trading is allowed (hard stops on max daily loss)
- `get_strategy_vector(strategy_id)`: Retrieves confidence scores from memory
- `update_market_state(snapshot)`: Updates shared market awareness with TTL

**Safety Guarantees:**
- Raises `CircuitBreakerOpen` exception if risk thresholds breached
- Hard-coded daily loss limit (default: -$500)
- Connection pooling to prevent resource exhaustion

---

### 2. **Strategy Engine** (`src/strategy_engine/`)
**The Eyes & Hands: Signal Generation**

**Responsibilities:**
- Implements three core trading strategies (A1, A2, A3)
- Calculates technical indicators (RSI, MACD, Bollinger Bands, etc.)
- Filters signals through Expected Value (EV) gate
- Generates trade suggestions with entry/exit points

**Strategies:**

| Strategy | Name | Logic | Ideal Market |
|----------|------|-------|--------------|
| **A1** | Mean Reversion | RSI oversold (< 30) + price 2 ATR from SMA20 | Rangebound |
| **A2** | Trend Following | SMA50 > SMA200 + MACD momentum | Trending |
| **A3** | Statistical Arbitrage | Z-score pairs divergence (e.g., BABA/JD) | Neutral |
| **Options** | Premium Collection | Early exit at 75% of target (theta decay) | High IV |

**Key Features:**
- Expected Value calculation per strategy
- ATR-based dynamic stop losses
- Ratio-based take profit targets
- Options Greeks integration (delta, theta)

---

### 3. **Wisdom Builder** (`src/wisdom_builder/`)
**The Memory: Nightly Learning Engine**

**Responsibilities:**
- Analyzes closed trades each night (backtest-on-actuals)
- Updates strategy confidence vectors via neuroplasticity (adaptive learning)
- Detects drift and performance decay
- Suggests parameter optimizations (E1 learning)

**Learning Process:**
```python
# For each closed trade:
1. Fetch current strategy vector: [Confidence, Aggression, Risk_Aversion]
2. Calculate reward/punishment based on P&L
3. Update vector: new_vector = current + (delta * learning_rate)
4. Clip to [0.01, 0.99] range (normalized bounds)
5. Persist to Redis for next day's trading
```

**Key Adjustments:**
- Profitable trades: Increase confidence, slightly boost aggression
- Losing trades: Decrease confidence, increase risk aversion
- Win rate < historical: Tighten signal thresholds (safer entry)

---

### 4. **External Intelligence** (`src/external_intelligence/`)
**The Eyes & Ears: Market Regime Detection**

**Responsibilities:**
- Scans news feeds, earnings announcements, geopolitical events
- Uses Gemini LLM to convert text into mathematical regime vectors
- Detects market regime shifts (Bull, Bear, Sideways, Crisis)
- Flags catalysts for human review

**Regime Vector Format:**
```json
{
  "sentiment_score": -0.6,  // -1 (Bearish) to +1 (Bullish)
  "volatility_expectation": 0.8,  // 0 (Low) to 1 (High)
  "regime_label": "Bear/Crisis",
  "catalyst_detected": true
}
```

**LLM Integration:**
- Prompt: "Analyze market news and extract [sentiment, volatility, regime, catalyst]"
- Returns structured JSON for State Manager consumption
- Fallback mock logic ensures system stability if API fails

---

### 5. **Journaling Service** (`src/journaling_service/`)
**The Memory Bank: Immutable Audit Trail**

**Responsibilities:**
- Logs every trade event (SIGNAL, ORDER_SENT, FILL, CANCEL, REJECT)
- Captures execution metrics (slippage, latency)
- Stores wisdom adjustments with reasoning
- Maintains pattern repository for experimentation

**Collections in Firestore:**
```
artifacts/{appId}/users/{userId}/
├── trade_journal/ (All live trades)
├── shadow_journal/ (Shadow mode validation)
├── wisdom_insights/ (Post-mortems, drift analysis)
└── pattern_repository/ (Experimental strategies)
```

**Key Features:**
- Context-aware logging (includes market regime tag)
- Execution quality analysis (slippage, latency tracking)
- Post-mortem classification (MARKET_SHIFT, INFRA_FAILURE, STRATEGY_DECAY)
- Drift detection for risk management

---

### 6. **Data Handler** (`src/data_handler/`)
**The Senses: Data Ingestion & Normalization**

**Responsibilities:**
- Fetches historical and real-time market data
- Applies corporate action adjustments (splits, dividends)
- Implements BBO (Best Bid/Offer) handler for accurate pricing
- Provides clean snapshots to Strategy Engine

**Data Normalization:**
- Adjusts historical prices for stock splits (backward-looking)
- Applies dividend adjustments
- Fills gaps in sparse data
- Validates data quality with Z-score outlier detection

**BBO Handler:**
```python
# Real-time tick processing
1. Receive market tick: bid, ask, last_trade, timestamp
2. Calculate mid-price: (bid + ask) / 2
3. Enqueue for strategy analysis
4. Track bid-ask spread (slippage indicator)
```

---

## Data Flow

### Real-Time Trading Cycle (Every 15 Minutes)

```
1. DATA INGESTION (Data Handler)
   ├─ Fetch latest OHLCV from broker APIs
   ├─ Apply corporate action adjustments
   ├─ Process BBO stream (real-time ticks)
   └─ Create normalized data snapshot

2. SIGNAL GENERATION (Strategy Engine)
   ├─ Retrieve market regime from State Manager (Redis)
   ├─ Calculate TA indicators (RSI, MACD, SMA, ATR, etc.)
   ├─ Run A1 (Mean Reversion) strategy
   ├─ Run A2 (Trend Following) strategy
   ├─ Run A3 (Stat Arb) strategy
   ├─ Filter each signal through EV gate
   └─ Generate trade suggestions with entry/exit prices

3. RISK CHECK (State Manager)
   ├─ Validate circuit breaker status
   ├─ Check daily loss limit (hard-coded max)
   ├─ Verify strategy confidence vector (from Wisdom)
   └─ Allow/deny execution

4. JOURNALING (Journaling Service)
   └─ Log signal event to Firestore (immutable record)

5. EXECUTION (Broker Integration)
   ├─ Place order at calculated prices
   ├─ Monitor for fills
   └─ Log fill events with metrics

6. MONITORING
   ├─ Track slippage (expected vs actual price)
   ├─ Monitor latency (order->fill time)
   └─ Update daily P&L in State Manager
```

### Nightly Learning Cycle (11 PM Daily)

```
1. LOAD CLOSED TRADES (Journaling Service)
   └─ Retrieve all closed trades from past 24 hours

2. ANALYZE (Wisdom Builder)
   ├─ Calculate win rate, avg win, avg loss
   ├─ Detect drift vs backtest expectations
   └─ Identify root cause of underperformance

3. LEARN (E1 Adaptive Optimization)
   ├─ For each strategy:
   │  ├─ Fetch current confidence vector from Redis
   │  ├─ Calculate reward/punishment from P&L
   │  ├─ Apply neuroplasticity update
   │  └─ Store new vector in Redis
   └─ Disable strategies with confidence < 0.2

4. POST-MORTEM (Journaling Service)
   ├─ Log drift analysis
   ├─ Identify pattern failures
   └─ Flag for human review if major deviation

5. RESET STATE (State Manager)
   ├─ Clear daily P&L counter
   ├─ Reset circuit breaker if conditions met
   └─ Prepare for next trading day
```

---

## Trading Strategies

### A1: Mean Reversion

**Principle:** "The Rubber Band" - Exploits oversold/overbought conditions

**Entry Conditions:**
- RSI < 30 (oversold signal)
- Price is > 2 ATR below SMA20 (magnitude confirmation)

**Exit:**
- Take Profit: SMA20 (reversion target)
- Stop Loss: Current price - 1.5 ATR (trailing)

**Best For:** Rangebound markets, high volatility

**Example:**
```
AAPL oversold: RSI = 25, Price = $150, SMA20 = $155, ATR = $2
Entry Price: $150
Take Profit: $155 (SMA20)
Stop Loss: $147 ($150 - 1.5×$2)
Risk/Reward: 1:1.67 ✓
```

---

### A2: Trend Following

**Principle:** "The Surfer" - Captures sustained directional moves

**Entry Conditions:**
- SMA50 > SMA200 (long-term uptrend)
- MACD > Signal Line AND MACD > 0 (momentum confirmation)

**Exit:**
- Take Profit: Current Price + 3 ATR (trend extension)
- Stop Loss: SMA200 (trend break)

**Best For:** Strong trending markets

**Example:**
```
GOOGL trending: SMA50 = $140, SMA200 = $130, MACD = +2.5
Entry Price: $140
Take Profit: $146 ($140 + 3×$2 ATR)
Stop Loss: $130 (SMA200)
Risk/Reward: 1:2 ✓
```

---

### A3: Statistical Arbitrage

**Principle:** "The Twin" - Bets on pairs mean reversion

**Entry Conditions:**
- Z-Score > 2.0 (extreme divergence)
- Short overvalued leg, Long undervalued leg
- Example: Short BABA if it diverges > 2σ from JD

**Exit:**
- Take Profit: Z-Score = 0 (spread normalizes)
- Stop Loss: Z-Score = 3.0 (trend confirmation)

**Best For:** Mean-reverting pairs (e.g., tech stocks, commodities)

---

### Options Specialization

**Principle:** "Profit Taker" - Collects premium, exits early at 75% of max profit

**Execution:**
- Sell puts on bullish signals (high probability setup)
- Collect 1.5% premium per trade
- Exit at 75% of premium (early profit-taking)

**Advantage:** Theta decay works in seller's favor

---

## Safety Mechanisms

### 1. Circuit Breaker

**Trigger:** Daily cumulative loss ≤ -$500 (configurable)

```python
if daily_pnl <= MAX_DAILY_LOSS:
    trigger_circuit_breaker("Daily Loss Limit Hit")
    raise CircuitBreakerOpen()
```

**Effect:** ALL trading halted immediately. Cannot be overridden.

**Reset:** Manual intervention + Wisdom Builder nightly review

---

### 2. Expected Value Filter

**Formula:** `EV = (WinRate × AvgWin) - (LossRate × AvgLoss)`

**Requirement:** EV > 0.5% (with margin) to execute

**Example:**
- Strategy has 60% win rate, +2% average win, -1% average loss
- EV = (0.60 × 0.02) - (0.40 × 0.01) = 0.012 - 0.004 = 0.8% ✓ Pass
- If EV < 0.5%, signal is rejected

---

### 3. Tremor Filter

**Purpose:** Ignore noisy, low-conviction signals

**Implementation:**
- Require signal magnitude > 2 × ATR (not just crossing)
- Skip signals during extreme volatility (VIX > 30 threshold)
- Wait for confirmation across multiple indicators

---

### 4. Implementation Shortfall Tracking

**Metrics Tracked:**
- Slippage: `actual_fill - expected_price`
- Latency: `time_from_order_to_fill`
- Spread Cost: Bid-ask spread at execution time

**Used For:**
- Drift detection (if slippage increasing, infrastructure degrading)
- Strategy comparison (net of costs)
- Broker selection (low-cost execution)

---

### 5. Drift Detection

**Drift = (Realized Performance - Backtested Performance) / Backtested**

**Threshold:** If Drift > 20%, strategy is flagged

**Action:**
- Reduce position size
- Tighten signal thresholds
- Consider disabling if Drift > 50%

---

## Deployment

### GCP Deployment

1. **Cloud Run Services** (auto-scaling, serverless)
   ```bash
   gcloud run deploy state-manager \
     --image gcr.io/PROJECT/state-manager:latest \
     --memory 512Mi --cpu 1 \
     --update-env-vars REDIS_HOST=MEMORYSTORE_IP
   ```

2. **Cloud Memorystore** (Redis 7+)
   - 2GB capacity for initial MVP
   - High availability with automatic failover
   - Read replicas for HA

3. **Firestore** (NoSQL Database)
   - Multi-region replication
   - Automatic backups
   - Real-time change feeds

4. **Cloud Build** (CI/CD)
   - Triggers on `git push main`
   - Builds Docker images
   - Deploys to Cloud Run

### AWS Equivalent

- **Lambda** (compute) instead of Cloud Run
- **ElastiCache** (Redis) instead of Memorystore
- **DynamoDB** instead of Firestore
- **CodePipeline** instead of Cloud Build

### Local Development

```bash
# Start Redis locally
docker run -d -p 6379:6379 redis:7

# Install dependencies
pip install -r requirements-dev.txt

# Run state manager
python src/state_manager/main.py

# Run strategy engine
python src/strategy_engine/main.py

# Run wisdom builder (nightly)
python src/wisdom_builder/main.py
```

---

## Key Concepts Reference

| Term | Definition |
|------|-----------|
| **Circuit Breaker** | Hard-coded safety switch that halts all trading if risk limits breached |
| **Wisdom Vector** | [Confidence, Aggression, Risk_Aversion] tuple stored in Redis for each strategy |
| **Regime** | Market state (Bull, Bear, Sideways, Crisis) detected via LLM sentiment analysis |
| **EV (Expected Value)** | Mathematical probability of profit for a strategy |
| **Neuroplasticity** | Adaptive learning process that adjusts strategy parameters nightly |
| **Tremor Filter** | Rejection of noisy, low-conviction signals |
| **BBO** | Best Bid/Offer - real-time market quotes for accurate entry/exit pricing |
| **Slippage** | Difference between expected and actual fill price |
| **Drift** | Deviation of realized performance from backtested expectations |

---

## Next Steps

1. Deploy to GCP Cloud Run with Redis Memorystore
2. Connect to real broker APIs (e.g., Interactive Brokers, Alpaca)
3. Run extended backtests (6-12 months of data)
4. Implement MCP (Model Context Protocol) servers for LLM integration
5. Monitor live trading for first month (shadow mode)
6. Iterate on strategy parameters based on realized performance
7. Scale to additional markets (crypto, futures, forex)

---

**Last Updated:** November 2025  
**Author:** Digital Trading Team  
**License:** [See LICENSE file](./LICENSE)
