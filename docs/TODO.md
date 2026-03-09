# 📝 System Technical Roadmap (TODO)

This document tracks long-term architectural improvements, separate from the immediate feature backlog.

## 🛡️ Security & Hardening

- [ ] **Redis Auth**: Enable `requirepass` on all Redis instances and update clients.
- [ ] **Secret Management**: Move hardcoded secrets (API Keys) to a `.env` file that is *not* committed to git, or use a Secret Manager (Vault/GSM).
- [ ] **Network Policy**: Restrict Redis port `6379` to only allow connections from the Tailscale Interface (`100.x.y.z`), rejecting public Internet traffic.

## 👁️ Telemetry & Observability

- [ ] **Health Dashboard**: Create a "Status Page" in the frontend showing:
  - Service Uptime (Green/Red dots).
  - Queue Depth (how many signals are waiting).
  - Node CPU/RAM usage.
- [ ] **Sanity Suite**: Implement a 5-minute cron job that:
  - Places a "Fake" Order.
  - Verifies it flows through Gateway -> State -> Execution.
  - Verifies it is logged in Journaling.
  - Reports success/failure to a notification channel (e.g., Discord/Slack).

## ♾️ DevOps & Pipelines

- [ ] **CI Pipeline**:
  - Linting (`pylint`, `black`).
  - Unit Tests (`pytest`).
  - Docker Build (Verify image creation).
- [ ] **CD Pipeline**:
  - Auto-deploy to "Staging" (Local VM).
  - Deployment to Production (Node 1/2) via SSH scripts.
- [ ] **Infrastructure as Code**:
  - Define the Tailscale ACLs and Node configs in Terraform or Ansible.

## 🧠 AI & Wisdom

- [ ] **Hallucination Validator**:
  - Before executing an AI trade, cross-reference the price with a live market feed.
  - If AI says "Buy AAPL at $100" but AAPL is $150, reject and log "Hallucination Detected".
- [ ] **Prompt Optimization**:
  - Feed "Actual Trade Outcomes" back into the prompt context to improve future suggestions.
