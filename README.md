# Digital Trader Bot - Platform IQ

> **The AI-Driven High-Frequency Trading Platform**

[![Platform Status](https://img.shields.io/badge/Platform-Active-success)](./REQUIREMENTS.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## ⚡ Overview

Digital Trader Bot is an AI-assisted trading platform for **safe portfolio monitoring, trade evaluation, supervised execution, and post-trade learning**. Token efficiency is treated as a first-class requirement for every AI workflow.

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

- [REQUIREMENTS.md](./REQUIREMENTS.md) - Platform vision and broker targets
- [docs/ai-partner/README.md](./docs/ai-partner/README.md) - AI partner operating model, requirements, and roles
- [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) - Technical design and data flow
- [docs/DEPLOYMENT_GUIDE.md](./docs/DEPLOYMENT_GUIDE.md) - How to contribute

---

**Version**: 2.0 (Platform Era)
**License**: MIT
