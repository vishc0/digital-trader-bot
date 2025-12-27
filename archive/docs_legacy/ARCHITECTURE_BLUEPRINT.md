# Technical Architecture Blueprint

## 1. The "Skeleton" Design
To minimize latency and cost, we avoid chatty HTTP microservices.
* **Core Protocol:** Redis + MsgPack (Binary Serialization).
* **Central Brain:** A Redis instance acting as the Single Source of Truth.
# System Architecture Blueprint (Maturity Level 5)
* Central Brain: Redis + MsgPack
* Strategy: Python Microservices
* Infrastructure: GCP Cloud Run

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


# System Architecture Blueprint

## 1. Core Logic
* **Central Brain:** Redis + MsgPack. Single source of truth.
* **Safety:** Hard-coded 'Circuit Breaker' in State Manager.
* **Efficiency:** 80/20 Rule applied to compute resources.

## 2. Microservices
1.  **State Manager:** The Brain. Handles Redis connections and safety checks.
2.  **Strategy Engine:** Python-based logic (Mean Reversion, Trend, Stat Arb). Uses 'Expected Value' filters.
3.  **Wisdom Builder:** Nightly 'Dreaming' process. Adjusts confidence vectors based on realized PnL.
4.  **External Intelligence:** Connects to Gemini LLM to parse news into 'Regime Vectors'.

## 3. Data Flow
News -> Ext. Intel -> Redis (Regime) -> Strategy Engine -> Signal -> State Manager (Safety Check) -> Execution.