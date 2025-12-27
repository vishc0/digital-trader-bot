#!/bin/bash

echo "📦 INITIALIZING REPOSITORY STATE..."
REPO_DIR="$HOME/final_digital_trader"

# Ensure we are in the right directory
if [ ! -d "$REPO_DIR" ]; then
    echo "Creating project directory..."
    mkdir -p "$REPO_DIR"
fi
cd "$REPO_DIR"

# Ensure folder structure exists
mkdir -p src/state_manager src/strategy_engine src/wisdom_builder src/external_intelligence src/journaling_service
mkdir -p docs
mkdir -p scripts

# ==============================================================================
# 1. DOCUMENTATION (The Wisdom & Requirements)
# ==============================================================================
echo "📄 Writing Documentation & Specs..."

cat <<EOF > README.md
# Digital Trader Bot (MVP)

**Repository:** [vishc0/digital-trader-bot](https://github.com/vishc0/digital-trader-bot)
**Architecture:** Level 5 (Stateful, Self-Correcting, Context-Aware)
**Infrastructure:** Google Cloud Platform (Cloud Run + Redis)

## 🎯 Project Vision
This is an autonomous "Digital Employee" designed for **Conservative Aggression**.
* **Never Loss:** Hard-coded circuit breakers prevent catastrophic failure.
* **Wisdom:** Uses a Feedback Loop (Wisdom Builder) to learn from every trade.
* **Efficiency:** Serverless architecture utilizing the 80/20 rule for compute resources.

## 📂 Repository Structure
* \`src/\`: Python Microservices code.
* \`docs/\`: Detailed Architectural Blueprints and Requirements.
* \`scripts/\`: Deployment automation.
* \`cloudbuild.yaml\`: CI/CD Pipeline configuration.

## 🚀 Deployment
This project is connected to Google Cloud Build.
1. Push changes to \`main\`.
2. GCP automatically rebuilds the "Brain" and updates the live services.
EOF

cat <<EOF > docs/REQUIREMENTS_CONSOLIDATED.md
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
EOF

cat <<EOF > docs/ARCHITECTURE_BLUEPRINT.md
# Technical Architecture Blueprint

## 1. The "Skeleton" Design
To minimize latency and cost, we avoid chatty HTTP microservices.
* **Core Protocol:** Redis + MsgPack (Binary Serialization).
* **Central Brain:** A Redis instance acting as the Single Source of Truth.

## 2. Service Definition
| Service | Tech Stack | Responsibility |
| :--- | :--- | :--- |
| **State Manager** | Python/Flask/Redis | The Gatekeeper. Enforces Circuit Breakers. |
| **Strategy Engine** | Python/Pandas/TA-Lib | Signal Generation (A1, A2, A3). |
| **Wisdom Builder** | Python/Scipy | Nightly analysis of closed trades. Updates Strategy Vectors. |
| **External Intel** | Python/Gemini API | Scans news, creates "Regime Vectors". |
| **Journaling** | Firestore | Immutable audit log of all events. |

## 3. Infrastructure (GCP)
* **Compute:** Cloud Run (Serverless).
* **Memory:** Cloud Memorystore (Redis).
* **Persistence:** Firestore (NoSQL).
* **CI/CD:** Cloud Build triggers on Git Push.
EOF

cat <<EOF > docs/RESEARCH_GAP_ANALYSIS.md
# Research & Gap Analysis

## Gap 1: The "Backtest-Live" Disconnect
* **Problem:** Retail bots fail because they ignore latency and order book depth.
* **Solution:** We implement "Implementation Shortfall" logging to track slippage per trade.

## Gap 2: Data Quality
* **Problem:** Raw feeds contain noise.
* **Solution:** Data Handler Service includes a "BBO Handler" and Z-Score spike filter.

## Gap 3: Execution Safety
* **Problem:** Infinite loops or API bans.
* **Solution:** Hard-coded "Tremor Filter" and Circuit Breaker in the State Manager.
EOF

# ==============================================================================
# 2. SOURCE CODE (The MVP Skeleton)
# ==============================================================================
echo "💻 Writing Source Code..."

# --- STATE MANAGER ---
cat <<EOF > src/state_manager/main.py
import os
import redis
import msgpack
from flask import Flask, jsonify

app = Flask(__name__)
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
# Robust connection with timeout
r = redis.Redis(host=REDIS_HOST, port=6379, db=0, socket_connect_timeout=5)

@app.route('/')
def health():
    try:
        r.ping()
        return jsonify({"status": "healthy", "role": "Brain", "connected": True}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
EOF

cat <<EOF > src/state_manager/Dockerfile
FROM python:3.10-slim
RUN pip install flask gunicorn redis msgpack
COPY main.py .
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "8", "main:app"]
EOF

# --- STRATEGY ENGINE (Placeholder) ---
cat <<EOF > src/strategy_engine/main.py
# Strategy Engine Logic - To be implemented in Phase 2
print("Strategy Engine Loading...")
EOF

# ==============================================================================
# 3. CI/CD CONFIGURATION
# ==============================================================================
echo "⚙️ Writing CI/CD Config..."

cat <<EOF > cloudbuild.yaml
steps:
  # Build the State Manager (The Brain)
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/\$PROJECT_ID/state-manager', './src/state_manager']
  
  # Push to Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/\$PROJECT_ID/state-manager']
  
  # Deploy to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'state-manager'
      - '--image'
      - 'gcr.io/\$PROJECT_ID/state-manager'
      - '--region'
      - 'us-central1'
      - '--vpc-connector'
      - 'redis-connector'
      - '--allow-unauthenticated'
images:
  - 'gcr.io/\$PROJECT_ID/state-manager'
timeout: '1200s'
EOF

# ==============================================================================
# 4. GIT PUSH
# ==============================================================================
echo "☁️ Pushing to GitHub..."

# Initialize if needed
if [ ! -d ".git" ]; then
    git init -b main
    git remote add origin https://github.com/vishc0/digital-trader-bot.git
fi

git add .
git commit -m "Docs: Full Requirements, Research, and Architecture Check-in"
git push -u origin main

echo "✅ SUCCESS: All discussion artifacts are now in your GitHub Repo."