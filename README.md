Digital Trader Bot (Level 5 Maturity)

Status: MVP
Infrastructure: Google Cloud Run + Redis + Firestore
Logic: Event-Driven Microservices

🧠 Architecture

State Manager: The central Redis brain enforcing safety (Circuit Breakers).

Strategy Engine: Python logic for Mean Reversion, Trend, and Stat Arb.

Wisdom Builder: Nightly learning loop that updates strategy confidence vectors.

External Intelligence: Gemini AI integration for news-based regime detection.

🚀 Deployment

Push to main branch triggers Google Cloud Build.

Details Version 2: 

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