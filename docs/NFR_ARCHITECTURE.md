# 🏗 Non-Functional Requirements (NFR) Architecture

**System Architect**: Antigravity
**Scope**: TradeSenseAI / Digital Trader Bot Hybrid Cluster

This document outlines how the system architecture addresses critical quality attributes.

## 1. Reliability & Availability

> **Requirement**: "The system must recover from failures without data loss."

* **Architecture Decision**: **Separation of Compute and Storage**.
* **Implementation**:
  * **Compute**: Docker Containers are ephemeral. They can crash, be deleted, or upgraded without impact.
  * **Storage (Persistence Layer)**: All stateful data (Redis DB, Logs) is mapped to **Bind Mounts** on the underlying Host OS (Node 1 SSD).
  * *Docker Config*: `volumes: - ./redis_data:/data` ensures data survives `docker-compose down`.
* **Recovery**: In case of container panic, Docker `restart: always` policy attempts immediate recovery. In case of Node failure, `DISASTER_RECOVERY.md` protocols apply.

## 2. Scalability

> **Requirement**: "Ability to grow with more strategies and complexity."

* **Architecture Decision**: **Split-Node / Microservices**.
* **Implementation**:
  * **Vertical Scaling**: Heavy compute (AI/Strategies) is isolated on Node 2 ("Muscle"). We can upgrade Node 2's hardware independently of Node 1.
  * **Horizontal Scaling**: We can add a "Node 3" and simply deploy another replica of `strategy_engine` to it, pointing to the same Redis.

## 3. Maintainability (DevOps)

> **Requirement**: "Iterative development and safe pipelines."

* **Architecture Decision**: **Containerization Protocol**.
* **Implementation**:
  * **One Artifact**: The generic `platform` code is the single source of truth.
  * **Configuration as Code**: all behavior differences are defined in `docker-compose.yml` and `.env` files, not code.
  * **Pipeline Vision**: (See `TODO.md`) We will implement a CI/CD pipeline that builds a Docker Image once and pushes it to a registry, ensuring "Build Once, Run Anywhere".

## 4. Observability

> **Requirement**: "Transparency and visibility at systemic and business levels."

* **Architecture Decision**: **Centralized Telemetry**.
* **Implementation**:
  * **Systemic**: Docker Healthchecks + Dashboard for CPU/RAM.
  * **Functional**: `Journaling Service` captures the "Why" of every trade.
  * **Business**: Real-time P&L calculation on every tick updates.

## 5. Security

> **Requirement**: "Secure access and secret management."

* **Architecture Decision**: **Zero-Trust Principles** (In Progress).
* **Implementation**:
  * **Boundary**: Tailscale Mesh prevents public internet access.
  * **Internal**: Moving towards authenticated Redis and Gateway-validated Requests.
  * **Secrets**: Defined in `SECURITY_ASSESSMENT.md`, improving storage from Environment Variables to Secret Managers.
