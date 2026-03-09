# Digital Trader Bot - Platform IQ

> **The AI-Driven High-Frequency Trading Platform**

[![Platform Status](https://img.shields.io/badge/Platform-Active-success)](./REQUIREMENTS.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## ⚡ Overview

Digital Trader Bot is a comprehensive algorithmic trading platform designed for **Maximum Profit** through **AI Integration** and **Seamless Execution**. It connects to Top 10 global brokers and uses advanced reinforcement learning (Wisdom Builder) to adaptively optimize strategies.

it will have a paper account that can be used to try differnet trades and strategies internally in itself.
it will be connected to brokers for execution for some of them that will be realtime.
it will also have ability to provide current sttus of the portfolios it handles.
it will do backtesting and forward testing on the data it has collected and will provide insights on the strategies it has used.
it will evolve itself and suggest improvements. based on gaps it is able to understand. ==> this is a self development component.
i will need to develop a telemetry dashabord where i can monitor the status of thesystem all other telemetry items. so host this on one of the nodes.

## 📂 Platform Structure

The project is organized into a scalable "Platform" architecture:

| Directory | Layer | Purpose |
|-----------|-------|---------|
| `platform/frontend` | **Control Plane** | Real-time Dashboard & Strategy Management |
| `platform/gateway` | **Middleware** | Unified API Gateway (Websockets/REST) |
| `platform/backend/core` | **The Brain** | Strategy Engine, State Manager, AI Wisdom |
| `platform/backend/data` | **Memory** | Market Data Ingestion & Immutable Journaling |
| `platform/backend/connectors` | **The Hands** | Broker Integrations (IBKR, Alpaca, etc.) |

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.10+
- Node.js 18+

### Launch the Platform

```bash
# 1. Start all services
docker-compose up -d --build

# 2. Access the Dashboard
# Open http://localhost:3000

# 3. Check System Health
curl http://localhost:8000/health
```

## 🧠 AI & Strategies

- **Wisdom Builder**: Learns from every trade to improve future performance.
- **External Intelligence**: Scans news and sentiment to detect market regimes.
- **Circuit Breakers**: Hard-coded safety to prevent catastrophic loss.

## 📚 Documentation

- [REQUIREMENTS.md](./REQUIREMENTS.md) - Platform Vision & Broker Targets
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Technical Design & Data Flow
- [DEVELOPMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - How to contribute

---

**Version**: 2.0 (Platform Era)
**License**: MIT
