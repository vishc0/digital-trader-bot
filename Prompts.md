# Digital Trader Bot Prompt Library

This file contains copy-paste prompt templates to help the project agents work together to design, build, harden, and deploy the full Digital Trader Bot platform.

## How to use this file

- Start with the orchestration prompts.
- Use the agent-selection prompts to choose the right specialist.
- Use the phase-based prompt packs in order.
- Keep prompts compact and scoped.
- Reuse summaries instead of pasting full repository context repeatedly.

## Global operating prompt

Use this first before deeper work:

> You are working on Digital Trader Bot, an AI-assisted trading platform. Follow the repository requirements and project-agent definitions as source of truth. Optimize token usage in all outputs. Keep safety before speed, preserve human approval for live execution, separate AI reasoning from deterministic controls, and do not design anything that bypasses broker, exchange, tax, regulatory, or pattern-day-trader rules. Prefer concise outputs using sections, bullets, checklists, matrices, schemas, and explicit next steps.

## MemoryPrint operating prompt

Use this before major multi-step work or when returning to the project after context switching:

> Before starting, read `.github/MemoryPrint/project-baseline.json` and `.github/MemoryPrint/latest-context.json` to restore project context. Use MemoryPrint as the compact machine-readable project memory source. After any meaningful change in architecture, delivery plan, strategy scope, observability design, broker integration, deployment plan, or governance understanding, update `.github/MemoryPrint/latest-context.json` and append a compact JSON line to `.github/MemoryPrint/checkpoints.jsonl`. Keep memory updates low-token, stable-keyed, and focused on durable project understanding.

---

## 1. Agent selection prompts

### 1.1 Pick the right agent

> /agent-pick objective="[describe the task]" scope="[module, feature, or workflow]" constraints="token efficient, safe, modular, auditable"

### 1.2 Route a multi-agent workflow

> /agent-route objective="Design, build, test, observe, and deploy [feature/platform slice]" scope="[modules involved]"

### 1.3 Compare candidate agents

> /agent-compare objective="[task]" candidate agents="ai-platform-orchestrator,trading-system-architect,delivery-lead,observability-sre,broker-integration-engineer,quant-strategy-analyst,risk-compliance-guardian"

### 1.4 Handoff from one agent to another

> /agent-handoff from agent="[current agent]" to agent="[next agent]" artifact="[plan, design, checklist, issue summary]" objective="[what the next agent should do]"

### 1.5 Refresh memory before choosing agents

> /memory-refresh task="[task]" scope="[scope]"

### 1.6 Save checkpoint after major progress

> /memory-checkpoint change type="[planning|architecture|delivery|implementation|deployment|troubleshooting|governance]" scope="[scope]" impact="[durable impact summary]"

---

## 2. Master orchestration prompts

### 2.1 Platform kickoff prompt

Use with `ai-platform-orchestrator`.

> Build the end-to-end delivery plan for Digital Trader Bot based on the repository requirements. Convert business goals into platform capabilities, functional requirements, modular architecture, delivery phases, and agent handoffs. Include portfolio monitoring, watchlists, recommendations, supervised trade execution, expected-vs-actual portfolio delta analysis, P&L analysis, exit-signal management, observability in GUI components, and deployment options for local, AWS, and GCP. Keep the output token-efficient and structured as: current understanding, capability map, phased plan, agent routing, risks, acceptance criteria, next steps.

### 2.2 Requirement sanity and feasibility review

Use with `ai-platform-orchestrator`.

> Review the current repository requirements and classify them into: feasible now, feasible later, ambiguous, unsafe to implement as written, and needs refinement. Preserve business intent but align recommendations with safety, compliance, auditability, and realistic engineering delivery. Keep the output compact and actionable.

### 2.3 Full platform work breakdown

Use with `ai-platform-orchestrator`.

> Break Digital Trader Bot into independently deliverable platform slices. For each slice, define objective, modules touched, user-facing outcomes, dependencies, specialist agent to use, measurable acceptance criteria, production-readiness concerns, and observability requirements. Keep token usage low and avoid repeating unchanged platform context.

---

## 3. Architecture prompt pack

### 3.1 Target platform architecture

Use with `trading-system-architect`.

> Design the target architecture for Digital Trader Bot as a modular AI-assisted portfolio operations platform. Cover frontend, gateway, state manager, strategy engine, data handler, execution manager, journaling service, decision-support/AI boundary, observability contract, and deployment shape. Make the design simple enough for phased delivery and safe enough for supervised trading. Include explicit state ownership, service contracts, failure modes, and observability requirements.

### 3.2 Domain model definition

Use with `trading-system-architect`.

> /arch-domain-model domain area="portfolio monitoring, orders, fills, approvals, expected-vs-actual outcomes, exits, journal events" workflows="portfolio review, recommendation review, order approval, supervised execution, post-trade analysis"

### 3.3 Architecture simplification pass

Use with `trading-system-architect`.

> /arch-simplify current design="existing platform modules in repository" pain points="mock data, mock broker integration, missing durable journaling, missing canonical contracts, missing observability contracts"

### 3.4 Capability gap vs architecture

Use with `trading-system-architect`.

> /arch-gap-check target capability="full platform from requirements including GUI telemetry, portfolio analytics, recommendations, supervised execution, cloud deployment" current modules="frontend,gateway,state_manager,strategy_engine,execution_manager,data_handler,journaling_service,wisdom_builder,external_intelligence"

---

## 4. Delivery prompt pack

### 4.1 End-to-end delivery plan

Use with `delivery-lead`.

> Create the end-to-end delivery plan for the Digital Trader Bot platform. Split work into MVP, hardening, and production-readiness tasks. Ensure coverage of happy paths, failure paths, edge cases, CI/CD, observability, rollback notes, deployment steps, and supportability. Keep the output structured and token-efficient.

### 4.2 Module delivery planning

Use with `delivery-lead`.

> /dl-plan-module module="[module name]" requirement="[feature or workflow requirement]" constraints="safe, observable, testable, token-efficient"

### 4.3 Flow coverage review

Use with `delivery-lead`.

> /dl-flow-coverage module="[module]" feature="[feature]" relevant files="[files or folder paths]"

### 4.4 MVP vs hardening split

Use with `delivery-lead`.

> /dl-split-mvp feature="[feature]" module="[module]" current state="[brief status]"

### 4.5 Release readiness review

Use with `delivery-lead`.

> /dl-release-readiness feature="[feature or slice]" module="[module or modules]" release target="local pilot, AWS staging, GCP staging, supervised production"

---

## 5. Observability prompt pack

### 5.1 Bake observability into all modules

Use with `observability-sre`.

> Define baked-in observability for every major Digital Trader Bot module. I want both functional metrics and system metrics collected at module level and shown directly in operator-facing GUI components. Cover health, latency, stale data, approvals, orders, fills, recommendations, AI token usage, risk rejections, P&L, and expected-vs-actual outcomes. Keep the telemetry model simple, reusable, and production-oriented.

### 5.2 Module observability plan

Use with `observability-sre`.

> /obs-module-plan module="[module]" workflows="[critical workflows]" dependencies="[service dependencies]"

### 5.3 GUI telemetry widgets

Use with `observability-sre`.

> /obs-gui-widgets module="[module or workflow]" target page="[portfolio, dashboard, recommendations, approvals, operations]" operator goal="show first-hand health and workflow state"

### 5.4 End-to-end flow observability

Use with `observability-sre`.

> /obs-flow-map workflow="recommendation -> approval -> order placement -> fill -> expected-vs-actual review" services="frontend,gateway,state_manager,strategy_engine,execution_manager,journaling_service"

### 5.5 AI token telemetry

Use with `observability-sre`.

> /obs-token-cost workflow="recommendation generation, portfolio commentary, exit rationale, post-trade summary" model calls="rank,summarize,explain,review"

---

## 6. Risk and compliance prompt pack

### 6.1 Guardrail definition

Use with `risk-compliance-guardian`.

> Define the platform guardrails for Digital Trader Bot so the system stays safe, auditable, and compliant. Cover pre-trade checks, approval flow, exposure limits, drawdown controls, price sanity checks, stale-data behavior, exception handling, override logging, and policy rejection conditions. Ensure the design helps avoid rule violations but never evades them.

### 6.2 Pre-trade controls

Use with `risk-compliance-guardian`.

> /risk-pretrade workflow="approved live buy or sell order" constraints="human approval required, position/exposure limits, stale-data fail-safe, broker compliance checks"

### 6.3 PDT and broker-policy review

Use with `risk-compliance-guardian`.

> /risk-pdt-review workflow="AI-assisted portfolio maintenance, entry, exit, trim, sell" account context="retail brokerage context with supervised execution"

### 6.4 Release compliance gate

Use with `risk-compliance-guardian`.

> /risk-release-gate feature="[feature]" module="[module]"

---

## 7. Broker integration prompt pack

### 7.1 Fidelity-first integration plan

Use with `broker-integration-engineer`.

> Create a safe Fidelity-first broker integration plan for Digital Trader Bot. Start from the current mock adapter and define a path through paper mode, shadow mode, and supervised live readiness. Cover capability mapping, contract mapping, error handling, reconciliation, auditability, observability, approval-aware execution, and support runbooks.

### 7.2 Broker adapter design

Use with `broker-integration-engineer`.

> /broker-adapter-plan broker="Fidelity" capability scope="account summary, positions, orders, fills, cancels, balances" mode="paper -> shadow -> supervised live"

### 7.3 Field mapping

Use with `broker-integration-engineer`.

> /broker-field-map broker object="[broker object]" platform object="[platform entity]"

### 7.4 Broker troubleshooting prompt

Use with `broker-integration-engineer`.

> /broker-troubleshoot broker="[broker]" symptom="[symptom]" workflow="[workflow]"

---

## 8. Strategy prompt pack

### 8.1 Initial strategy portfolio

Use with `quant-strategy-analyst`.

> Define the initial strategy portfolio for Digital Trader Bot covering mean reversion, trend following, portfolio maintenance, and exit-signal management. For each strategy, define hypothesis, regime fit, inputs, entry logic, exit logic, invalidation, observability needs, expected-vs-actual review needs, and paper-trade gating. Keep the design simple, explainable, measurable, and token-efficient.

### 8.2 Strategy card prompt

Use with `quant-strategy-analyst`.

> /quant-strategy-plan strategy="[strategy name]" assetScope="[asset scope]" objective="[objective]"

### 8.3 Entry and exit logic prompt

Use with `quant-strategy-analyst`.

> /quant-entry-exit strategy="[strategy]" regime="[regime]"

### 8.4 Expected vs actual review

Use with `quant-strategy-analyst`.

> /quant-expected-actual strategy="[strategy]" expected summary="[expected thesis or target behavior]" actual summary="[real outcome summary]"

---

## 9. Application prompt pack by capability

### 9.1 Portfolio monitoring application

> Build the portfolio monitoring application slice for Digital Trader Bot. I want account summaries, holdings, cash, watchlists, position-level status, risk state, recommendation indicators, and first-hand GUI telemetry. Use existing modules where possible. Provide architecture, delivery plan, observability plan, risk controls, and deployment plan.

### 9.2 Recommendations application

> Build the recommendations and review workflow for Digital Trader Bot. I want watchlist analysis, per-holding recommendations, trade rationale, AI commentary, exit rationale, and expected-vs-actual tracking. Keep human approval in control for live actions. Include architecture, strategy logic, observability, and delivery plan.

### 9.3 Supervised execution application

> Build the supervised execution workflow for Digital Trader Bot. I want approval-aware trade execution with paper mode first, shadow mode support, journaling, risk checks, broker adapter boundary, and visible GUI state. Include architecture, controls, observability, delivery plan, and deployment notes.

### 9.4 Post-trade analytics application

> Build the post-trade analytics and learning workflow for Digital Trader Bot. I want realized and unrealized P&L, expected-vs-actual delta analysis, exit-quality review, and AI-assisted post-trade summaries. Include data model, observability, GUI components, delivery plan, and deployment notes.

### 9.5 Strategy knowledge ingestion application

> Design a compliant public-research ingestion workflow for Digital Trader Bot to collect and summarize legally accessible public market commentary, strategy notes, and public-source ideas. Do not copy protected material verbatim and do not assume unrestricted scraping rights. Focus on metadata, summaries, source references, strategy classification, and safe usage in research workflows.

---

## 10. GUI prompt pack

### 10.1 Operator control plane

> Design the operator GUI for Digital Trader Bot. I want portfolio summary, watchlists, recommendations, approvals, order status, P&L, exit signals, and observability widgets visible first-hand. Use backend telemetry as the source of truth and define component boundaries, states, refresh behavior, and drill-down flows.

### 10.2 GUI telemetry alignment

> Design the GUI so every critical platform module has an operator-visible status component. Show service health, stale data, workflow failures, AI usage, approvals pending, orders in flight, fills, risk state, and P&L metrics. Keep the UI practical, compact, and actionable.

### 10.3 Recommendation drill-down view

> Design the recommendation details page for a single holding. Show current state, recommendation, confidence, rationale, strategy inputs, exit logic, expected-vs-actual deltas if historical, and risk warnings. Include required backend contracts and observability signals.

---

## 11. Testing and hardening prompt pack

### 11.1 Full test strategy

> Create the full test strategy for Digital Trader Bot covering unit, integration, smoke, regression, observability validation, risk control validation, approval flow validation, broker adapter validation, and deployment smoke checks. Keep the plan modular and delivery-friendly.

### 11.2 Delivery unblock prompt

Use with `delivery-lead`.

> /dl-dev-unblock module="[module]" issue="[build, test, CI/CD, deployment, runtime issue]" expected outcome="[desired result]"

### 11.3 Troubleshooting prompt

Use with `delivery-lead` or `observability-sre` depending issue type.

> /dl-troubleshoot symptom="[symptom]" scope="[scope]" recent change="[recent change summary]"

---

## 12. Deployment prompt pack

### 12.1 Local deployment prompt

> Design the local deployment for Digital Trader Bot using the current repository structure. I want all core services runnable locally for development, testing, and paper-mode validation. Include container layout, environment files, health checks, observability, local dashboards, seed data or mock dependencies, and developer workflows.

### 12.2 AWS deployment prompt

> Design the AWS deployment for Digital Trader Bot as a modular, cost-aware, production-grade platform. Cover compute options, networking, secrets, data stores, observability, CI/CD, rollback, staged environments, and support model. Keep the design simple enough for phased delivery and include a migration path from local deployment.

### 12.3 GCP deployment prompt

> Design the GCP deployment for Digital Trader Bot as a modular, cost-aware, production-grade platform. Cover compute options, networking, secret management, managed data services, observability, CI/CD, rollback, staged environments, and migration path from local deployment. Keep the output concise and implementation-friendly.

### 12.4 Cloud comparison prompt

> Compare local, AWS, and GCP deployment options for Digital Trader Bot. Evaluate complexity, cost, observability, security, release operations, and support burden. Recommend the best path for phased rollout: local dev -> cloud staging -> supervised production.

### 12.5 Deployment readiness prompt

Use with `delivery-lead` and `observability-sre`.

> Assess whether the current platform slice is ready for local deployment, AWS staging, GCP staging, or supervised production. Include missing infrastructure, observability gaps, operational risks, rollback readiness, and next actions.

---

## 13. End-to-end collaboration prompt sets

### 13.1 Full platform build sequence

Run in this order:

1. `ai-platform-orchestrator`
	> Build the full phased plan for Digital Trader Bot from requirements to production-grade supervised platform. Route work to the right agents and keep the output token-efficient.

2. `trading-system-architect`
	> Design the target architecture and contracts for the first 2 platform phases, including observability and GUI telemetry requirements.

3. `risk-compliance-guardian`
	> Define platform guardrails, approval flow, capital protection logic, and release-time compliance gates for those phases.

4. `quant-strategy-analyst`
	> Define the initial strategy set, exit logic, expected-vs-actual review design, and paper-trade evaluation plan.

5. `broker-integration-engineer`
	> Define Fidelity-first adapter plan from mock to paper to shadow to supervised live readiness.

6. `observability-sre`
	> Define baked-in observability across modules and first-hand GUI telemetry components for the operator console.

7. `delivery-lead`
	> Convert all approved outputs into delivery slices, CI/CD, tests, release gates, deployment plan, and support runbooks.

### 13.2 New feature workflow

> /agent-route objective="Add [feature] to Digital Trader Bot with architecture, risk, observability, delivery, and deployment readiness" scope="[modules involved]"

### 13.3 Incident response workflow

> /agent-route objective="Diagnose and stabilize [issue] in Digital Trader Bot" scope="affected module, deployment, GUI, workflow"

Then use:
- `delivery-lead` for release-flow restoration
- `observability-sre` for telemetry diagnosis
- `risk-compliance-guardian` if control paths were impacted
- `broker-integration-engineer` if broker workflows were impacted

---

## 14. Token-efficient prompt hygiene

Use these rules in all prompts:

- Reference modules and workflows precisely.
- Ask for bounded output with named sections.
- Reuse prior summaries.
- Avoid pasting the full repo state unless the task is broad.
- Prefer one workflow per prompt.
- Prefer review prompts that ask for gaps, risks, and next steps.

### Good compact suffix

> Keep the output concise, modular, and token-efficient. Use only the minimum context needed. Prefer bullets, matrices, contracts, and checklists over narrative prose. Do not repeat unchanged platform facts.

---

## 15. Quick-start prompts

### 15.1 Start the whole project

> Build the full Digital Trader Bot roadmap from the current repository into a supervised, AI-assisted portfolio platform. Use the existing project agents together. Start with requirements alignment, then architecture, then delivery slices, then observability, then broker integration, then deployment plan for local, AWS, and GCP. Keep everything token-efficient and production-oriented.

### 15.2 Start just the architecture

> Design the complete target architecture for Digital Trader Bot from the current repo and requirements. Include modular services, observability contracts, GUI telemetry surfaces, risk boundaries, broker boundaries, and deployment shape for local, AWS, and GCP.

### 15.3 Start just the implementation plan

> Turn the Digital Trader Bot requirements into an implementation-ready phased delivery plan with module-level work items, acceptance criteria, tests, observability, CI/CD, deployment, and support readiness.

### 15.4 Start just the cloud deployment path

> Create the full deployment path for Digital Trader Bot from local development to AWS and GCP staging and then to supervised production. Include CI/CD, secrets, observability, rollback, and support model.
