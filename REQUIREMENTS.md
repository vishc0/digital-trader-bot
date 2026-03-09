# Digital Trader Bot - Platform Requirements
>
> **Vision**: An AI-assisted trading platform that helps a human operator monitor portfolios, evaluate trade ideas, execute approved trades safely, and continuously improve with disciplined AI usage.

## 0. Primary goals

1. Safety before speed.
2. Token efficiency in all AI-enabled workflows.
3. Modular independently deployable services.
4. Paper-first validation before supervised live trading.
5. Full auditability for recommendations, approvals, and orders.

## 1. Top 10 Broker Integrations (Target)

The platform must support modular connectors for:

1. **Interactive Brokers (IBKR)** - Global equities & futures.
2. **Alpaca** - API-first stock trading.
3. **Charles Schwab / TDA** - Retail flow.
4. **E*TRADE** - Options specialization.
5. **Robinhood** - Simple equity access.
6. **Fidelity** - Institutional grade execution.
7. **Binance** - Crypto spot/futures.
8. **Coinbase Pro** - Crypto institutional.
9. **Kraken** - Crypto margin.
10. **Tastytrade** - Derivatives focused.

## 2. Platform Components

### Frontend (Control Plane)

Portfolio Page: 
- Portfolio summary of all the accounts and holdings in account. A single indicator to take action on certain assets.
- when actions is clicked it takes to recommendations page where it tells me what is the recommendation for that holding
- Mintain multiple Watch lists and perform analysis on each of these tickers to provide recomendations. 
- for each stock, apply strategies and come up with recomendations.
- Real-time dashboard ensuring "Maximum Profit" visibility.
- evaluating the original exit criteria, evaluate the actual movement of the stock and modify the exit strategy 
- scrape various internet bogs posts and tradinv view authors and ohter leading strategies websites to underatnd and documentthose stratgies.

 - Manual override controls (Kill Switch).
- AI Insight visualization (Sentiment, Regime).

### Middleware & Gateway

- **API Gateway**: Unified REST/WebSocket entry point.
- **Auth**: Secure API Key & JWT token management.
- **Rate Limiting**: Intelligent throttling to respect broker limits.

### Backend Core (The Brain)

- **AI Integration**:
  - **Wisdom Builder**: Reinforcement learning engine that optimizes parameters nightly.
  - **External Intelligence**: LLM-based news analysis (Gemini/GPT).
- **Strategy Engine**:
  - Mean Reversion, Trend Following, Stat Arb, Volatility.
  - Support for custom user strategies.
- **State Manager**:
  - Redis-backed persistent state.
  - Hard-coded risk limits (Circuit Breakers).

### Data Layer

- **Ingestion**: Normalizers for SIP, Crypto Feeds, and Broker APIs.
- **Journaling**: Immutable Firestore logs for every decision.

## 3. Key Non-Functional Requirements

- **Latency**: < 50ms internal processing time.
- **Reliability**: 99.9% Uptime during market hours.
- **Safety**: Never-loss mandates (EV > 0.5%).
