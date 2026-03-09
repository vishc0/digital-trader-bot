# Digital Trader Bot Kickoff Review

## Executive summary
The repository is a valid platform starter, but it is not yet ready for full feature implementation without a short gap-closing phase.

The rollout is now split as follows:
- MVP: built-in paper trading account inside the platform
- Phase 2: Fidelity market-account integration for supervised real-account workflows

Current code already gives you:
- modular backend services
- gateway and approval flow foundations
- frontend shell for operator workflows
- mock execution support
- initial health endpoints
- a project-agent system for AI-assisted delivery
- compact project memory in `.github/MemoryPrint`

Before kickoff, the most important gaps to close are:
- canonical domain models
- MVP paper-account design and Phase 2 Fidelity integration plan
- observability contract per module and GUI surface
- first implementation slice and release sequence
- compliance and approval boundaries for supervised trading

## Gap progress since review started

- MVP and Phase 2 rollout split is now frozen.
- Canonical MVP contract draft now exists in [docs/MVP_DOMAIN_CONTRACTS.md](docs/MVP_DOMAIN_CONTRACTS.md).
- Durable journaling for MVP is now implemented with SQLite in [platform/backend/journaling_service/journaling_service.py](platform/backend/journaling_service/journaling_service.py) and [platform/backend/journaling_service/main.py](platform/backend/journaling_service/main.py).
- MVP market-data provider is now locked to Twelve Data with mock fallback in [platform/backend/data_handler/data_handler.py](platform/backend/data_handler/data_handler.py) and [platform/backend/data_handler/main.py](platform/backend/data_handler/main.py).

## Frozen rollout decision

### MVP
- built-in paper trading account managed by the tool
- local-first deployment
- supervised workflow: portfolio view -> recommendation -> approval -> paper order -> fill simulation -> journal -> review
- no dependency on Fidelity for MVP completion

### Phase 2
- integrate Fidelity market accounts
- preserve human approval for real-account actions
- reuse the same contracts, journaling, observability, and approval flow proven in MVP

This means all current gap-closing work should favor abstractions that let the system swap from internal paper execution to Fidelity-backed execution without changing operator workflows.

## What is already strong
- Service decomposition is already present across [platform/backend](platform/backend), [platform/gateway](platform/gateway), and [platform/frontend](platform/frontend).
- Live execution is already partially guarded by approval logic in [platform/backend/state_manager/state_manager.py](platform/backend/state_manager/state_manager.py) and [platform/gateway/main.py](platform/gateway/main.py).
- Health endpoint patterns already exist across services.
- The project now has agent definitions, command catalogs, prompts, and MemoryPrint support in [.github/project-agents](.github/project-agents) and [.github/MemoryPrint](.github/MemoryPrint).

## Verified gaps before kickoff

### 1. Real data and broker connectivity gap
Status:
- MVP paper account is not yet defined as a first-class internal account model.
- Fidelity is still mock-only for Phase 2.
- Twelve Data is now the selected MVP market-data provider, with mock fallback when configuration is missing.
- Portfolio/account ingestion is not production-shaped.

Impact:
- Core product promise cannot be validated end to end.

Close this gap by:
- defining the internal paper account, balances, positions, orders, fills, and cash ledger behavior
- locking Fidelity as the first real broker target for Phase 2
- defining the account, balance, position, order, and fill contracts
- wiring the selected market-data path into strategy workflows and operator views

### 2. Durable journaling gap
Status:
- SQLite-backed durable journaling is now in place for MVP in [platform/backend/journaling_service/journaling_service.py](platform/backend/journaling_service/journaling_service.py).

Impact:
- MVP auditability is materially improved.
- Analytics projections and broader adoption across services still need follow-through.

Close this gap by:
- defining canonical event schemas
- separating trade events, execution metrics, AI decisions, and system health events consistently across services
- adding projection queries needed for expected-vs-actual and operator review screens

### 3. Canonical domain model gap
Status:
- Major workflows exist conceptually, but shared contracts are not yet locked.

Impact:
- Delivery will drift and integrations will become brittle.

Close this gap by defining:
- paper account model
- portfolio summary model
- holding and watchlist model
- recommendation model
- approval model
- order and fill model
- expected-vs-actual outcome model
- exit review model
- journal event model

### 4. Strategy maturity gap
Status:
- Strategy engine exists, but important indicator and signal paths are still placeholder-based.

Impact:
- Recommendations are not yet trustworthy.

Close this gap by:
- limiting the initial strategy set
- defining paper-first evaluation rules
- requiring explicit exit logic and observability per strategy

### 5. Observability contract gap
Status:
- Health endpoints exist, but module telemetry and GUI-first observability are not yet systematically baked in.

Impact:
- Troubleshooting and operator confidence will be weak during development and release.

Close this gap by:
- defining required metrics per module
- defining GUI health widgets and workflow-status components
- adding staleness, latency, failure, and token metrics

### 6. Deployment target gap
Status:
- Local, AWS, and GCP are all desired, but only local-first is currently locked.

Impact:
- Infra planning and CI/CD will stay vague.

Close this gap by:
- choosing local-first as the initial mandatory environment
- choosing one cloud staging target before dual-cloud hardening
- defining minimal deployment architecture for each stage

### 7. Scope management gap
Status:
- Requirements include a broad long-term vision, including many brokers and large capability breadth.

Impact:
- Kickoff can become too wide.

Close this gap by freezing the first release scope to one supervised portfolio workflow.

## Decisions to lock before writing major code
1. First delivery slice
   - locked: portfolio monitoring + recommendations + approval-aware built-in paper execution
2. MVP execution model
   - locked: internal paper trading account built directly into the tool
3. First real broker target
   - locked for Phase 2: Fidelity market accounts
4. First durable journal store
   - locked for MVP: SQLite event store
5. First market/account data path
   - locked for MVP: Twelve Data
   - still open: operator configuration, rate-limit handling, and strategy adoption details
6. First cloud staging target
   - choose AWS or GCP after local-first baseline
7. Canonical domain model ownership
   - architect owns contracts, delivery lead owns adoption plan
8. GUI first-page scope
   - recommended: dashboard, portfolio, recommendations, approvals, operations health

## Recommended kickoff scope

### Kickoff slice A: Platform foundation hardening
- canonical contracts
- built-in paper account contract and ledger rules
- durable journaling implementation on SQLite
- observability contract per module
- MemoryPrint usage in workflow
- CI/CD and local deployment baseline

### Kickoff slice B: Operator control plane MVP
- portfolio summary page
- watchlist support
- recommendation indicator and details drill-down
- approval status panel
- first-hand health widgets

### Kickoff slice C: Supervised paper execution MVP
- recommendation -> approval -> paper order -> fill -> journal flow
- expected-vs-actual storage and review hook
- risk and compliance checks in path

## Gap handling policy for this project phase
- I should try to close each identified gap directly in code or docs where possible.
- I should only ask for user choices when a decision changes architecture, compliance posture, storage technology, or deployment direction.
- When a choice is required, I should present a small option set with a recommended default.
- Until a later decision changes it, MVP work should optimize for the built-in paper account path and preserve compatibility with a future Fidelity adapter.

## What should wait until after kickoff
- multi-broker rollout
- advanced autonomous trading
- broad internet strategy ingestion at scale
- complex derivatives automation
- cross-cloud production hardening on both AWS and GCP at once

## Recommended first agent sequence
1. `ai-platform-orchestrator`
   - freeze first delivery slice and phase plan
2. `trading-system-architect`
   - lock canonical contracts and module boundaries
3. `risk-compliance-guardian`
   - define control points for supervised paper and supervised live progression
4. `observability-sre`
   - define baked-in module and GUI telemetry contract
5. `delivery-lead`
   - turn the above into build-ready work packages and local release path
6. `broker-integration-engineer`
   - shape Fidelity-first paper/shadow adapter plan
7. `quant-strategy-analyst`
   - define the first limited strategy set and evaluation rules

## Kickoff done criteria
Kickoff is complete when:
- first delivery slice is frozen
- canonical data contracts are documented
- first local deployment path is documented
- journaling direction is chosen
- observability contract exists for all core modules
- supervised paper execution path is mapped end to end
- risk and approval gates are explicit
- MemoryPrint reflects the new baseline

## Recommended immediate next step
Use the kickoff prompt in [Prompts.md](Prompts.md) to generate the first phased plan, but constrain the outcome to:
- local-first deployment
- one supervised portfolio workflow
- built-in paper trading account for MVP
- Fidelity market-account integration in Phase 2
- baked-in observability in backend and GUI
- durable journaling decision before deeper implementation
