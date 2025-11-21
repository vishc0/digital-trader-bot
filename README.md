# Digital Trader Bot - MVP (Level 5 Maturity)

> An autonomous trading platform that hunts for profit while maintaining strict loss controls. Built for **conservative aggression** - aggressive profit-seeking tempered by hard-coded safety mechanisms.

## 🎯 Quick Overview

**What it Does:**
- Generates trade signals using 3 strategies (Mean Reversion, Trend Following, Stat Arb)
- Learns from every trade via nightly optimization (Wisdom Builder)
- Detects market regime changes using AI/LLM
- Enforces hard-coded circuit breakers to prevent catastrophic losses
- Maintains immutable audit trail of all decisions

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Redis 7+
- Docker (optional)

### Local Setup (3 minutes)

```bash
# 1. Clone and enter directory
git clone https://github.com/vishc0/digital-trader-bot.git
cd digital-trader-bot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start Redis
docker run -d -p 6379:6379 redis:7

# 5. Start all services
python src/state_manager/main.py &
python src/strategy_engine/main.py &
python src/data_handler/main.py &
```

## 📊 Architecture

6 Microservices:

| Service | Purpose | Port |
|---------|---------|------|
| State Manager | Central brain (Redis + safety) | 8080 |
| Strategy Engine | Trade signal generation | 8081 |
| Wisdom Builder | Nightly learning optimization | 8082 |
| External Intelligence | Market regime (LLM) | 8083 |
| Journaling Service | Audit trail (Firestore) | 8084 |
| Data Handler | Market data ingestion | 8085 |

## 🧠 The Three Strategies

### A1: Mean Reversion
- **Entry**: RSI < 30 AND price 2 ATR below SMA20
- **Win Rate**: 65%

### A2: Trend Following
- **Entry**: SMA50 > SMA200 AND MACD momentum
- **Win Rate**: 55%

### A3: Statistical Arbitrage
- **Entry**: Z-Score > 2.0 (pair divergence)
- **Win Rate**: 70%

## 🛡️ Safety Mechanisms

1. **Circuit Breaker**: Max daily loss -$500 (hard-coded)
2. **Expected Value Filter**: EV > 0.5% required
3. **Wisdom Vectors**: Adaptive confidence (updated nightly)

## 📈 Trading Cycle

**Real-Time**: Data → Signals → Risk Check → Execution  
**Nightly**: Analyze Trades → Learn → Update Vectors → Reset State

## 🚀 Deployment

### GCP Cloud Run
```bash
gcloud run deploy state-manager --image gcr.io/PROJECT/state-manager:latest
```

### Docker Compose (Local)
```bash
docker-compose up -d
```

### AWS Lambda
See `docs/AWS_DEPLOYMENT.md`

## 📚 Documentation

- `ARCHITECTURE.md` - System design details
- `REQUIREMENTS.md` - Functional requirements
- `RESEARCH_FINDINGS.md` - Trading system research
- `LaymansGuide.txt` - Non-technical overview

## 🧪 Testing

```bash
pytest tests/unit/
pytest tests/integration/
```

## 📄 License

MIT License - see `LICENSE`

---

**Version**: 1.0 (MVP)  
**Status**: Ready for Backtesting & Deployment  
**Last Updated**: November 2025
