# Digital Trader Bot - Platform Architecture

## System Overview

The **Digital Trader Bot** is a modular, event-driven trading platform designed for high-frequency trading across multiple brokers. It separates concerns into clear layers: **Frontend**, **Gateway**, and **Backend Services**.

## 🏗 System Architecture (Hybrid Deployment)

This platform uses a **Split-Node Architecture** to balance low-latency execution with high-compute AI processing, leveraging local hardware for zero cost.

```mermaid
graph TD
            StrategyEngine[Strategy Engine]
            WisdomBuilder[Wisdom Builder (AI)]
            ExtIntel[External Intelligence]
            DataHandler[Data Handler]
            Journaling[Journaling Service]
            TradeExecutor[Execution Manager]
            
            StrategyEngine -->|Signals| StateManager
            WisdomBuilder -->|Updates| StateManager
            ExtIntel -->|Regime Data| StateManager
            DataHandler -->|Snapshots| StrategyEngine
            Journaling -->|Logs| Firestore[(Firestore)]
            
            TradeExecutor -->|IBKR/Alpaca| BrokerAPI[External Broker]
        end
        
        StateManager -->|Risk Checks| TradeExecutor
        Redis[(Redis State)]
    end
```

## 📂 Directory Structure

### `platform/frontend`

The web-based control plane (Vite/React).

- **Dashboard**: Real-time P&L, Active Orders.
- **Controls**: Emergency Kill Switch, Strategy Toggles.

### `platform/gateway`

The unified entry point for all external traffic.

- Authenticates users.
- Routes requests to appropriate backend services.

### `platform/backend`

The core services operating the platform.

- **`state_manager`**: Holds the "Truth" (Positions, Risk Limits). Enforces Circuit Breakers.
- **`strategy_engine`**: Runs A1 (Mean Rev), A2 (Trend), A3 (Arb).
- **`wisdom_builder`**: The AI learning loop. Analyzes past trades to optimize parameters.
- **`external_intelligence`**: LLM integration for news/sentiment analysis.
- **`data_handler`**: Ingests market data (SIP, WebSocket).
- **`journaling_service`**: Writes immutable logs to Firestore.
- **`execution_manager`**: Routes orders to the correct connector (IBKR, Alpaca, etc.).

## 🚀 Tech Stack

- **Languages**: Python 3.10+ (Backend), TypeScript (Frontend).
- **Communication**: Redis Pub/Sub, gRPC/REST.
- **Storage**: Redis (Hot State), Firestore (Audit/Logs).
- **Infrastructure**: Docker, Cloud Run / Kubernetes.
