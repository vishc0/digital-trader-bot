# Digital Trader Bot - Copilot Project Instructions

## Mission
Build a modular AI-assisted trading platform that helps a human operator monitor portfolios, evaluate trade ideas, review expected vs actual outcomes, and execute approved trades safely.

## Primary Goals
1. Safety before speed.
2. Token efficiency in all AI features.
3. Modular architecture with independently deployable services.
4. Paper-first validation before any live trading.
5. Full auditability for every AI recommendation and order.

## Token Usage Policy
- Treat token usage as a first-class non-functional requirement.
- Prefer compact prompts, structured inputs, and bounded outputs.
- Summarize large contexts before sending them to models.
- Use retrieval, caching, batching, and delta-updates instead of resending full history.
- Define max token budgets per workflow and fail safely when exceeded.
- Store reusable market summaries, portfolio summaries, and strategy summaries.
- Ask models for JSON or short bullet output when possible.
- Avoid duplicate AI calls across services.

## MemoryPrint Policy
- Treat `.github/MemoryPrint` as the compact machine-readable memory checkpoint folder for this project.
- Before major work, read the latest MemoryPrint files to restore project context quickly.
- After meaningful planning, architecture, delivery, implementation, deployment, troubleshooting, or governance changes, update the latest MemoryPrint and append a compact checkpoint entry.
- Prefer compact JSON or JSONL memory formats with stable keys and low-token summaries.
- Store only high-value project understanding: goals, constraints, active decisions, module state, risks, and next priorities.
- Avoid verbose narrative memory dumps; keep entries short, structured, and reusable across agents.

## Trading Safety Policy
- No feature may attempt to bypass broker rules, compliance controls, or pattern day trader protections.
- The system may help avoid policy breaches, but must never help evade them.
- Live execution requires explicit human approval until a later governance decision enables automation.
- All AI trade suggestions must pass risk, compliance, and price sanity validation.

## Current Platform Truth
- Existing code already supports modular services: gateway, state manager, strategy engine, execution manager, journaling, data handler, wisdom builder, external intelligence, frontend.
- Fidelity support is currently mock only.
- Market data and several analytics flows are still mock or placeholder based.
- Architecture is suitable for an AI-assisted platform, but not yet ready for production brokerage automation.

## Engineering Rules
- Prefer simple interfaces over deep service-to-service coupling.
- Keep state ownership explicit.
- Use typed request and response contracts.
- Add health checks, metrics, and audit events for each service.
- Separate recommendation generation from order execution.
- Separate AI reasoning from hard risk controls.

## Delivery Priorities
1. Documentation and design baseline.
2. Real platform capability map.
3. Observability and governance.
4. Real broker and portfolio integrations.
5. AI optimization and model cost controls.
6. Cloud deployment hardening.
