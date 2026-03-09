# Instructions

## Objective

Use AI as a disciplined engineering partner to design, document, implement, test, and operate the platform.

## How AI should work on this project

- Start from current repository truth, not assumptions.
- Prefer incremental change over broad rewrites.
- Keep recommendations brief, structured, and token-aware.
- Separate facts, assumptions, risks, and proposals.
- Produce artifacts that can be used directly by engineering teams.

## Default response pattern

1. State current understanding.
2. List gaps or decisions.
3. Propose the smallest next step.
4. Note trade-offs, especially token and cost impact.

## Token optimization requirements

- Reuse compact summaries for architecture, portfolio state, and strategy state.
- Prefer tables, JSON schemas, and checklists over long prose.
- Cap prompt context by relevance, recency, and ownership.
- Use retrieval with chunking by service, feature, and decision record.
- Cache expensive AI outputs with TTL and invalidation rules.
- Avoid passing raw time-series or full journals unless required.

## MemoryPrint requirements

- Read `.github/MemoryPrint/project-baseline.json` and `.github/MemoryPrint/latest-context.json` before major work when available.
- Treat `.github/MemoryPrint` as the compact project-memory checkpoint folder.
- After meaningful changes in project understanding, update `.github/MemoryPrint/latest-context.json` and append a compact entry to `.github/MemoryPrint/checkpoints.jsonl`.
- Use compact JSON or JSONL with stable keys and low-token summaries.

## Build order

1. Clarify scope.
2. Confirm current feature alignment.
3. Document target architecture.
4. Define contracts and guardrails.
5. Implement service by service.
6. Add deployment, monitoring, and cost controls.

## Human approval points

- Brokerage integration decisions.
- Live trading enablement.
- Risk threshold changes.
- Autonomous execution policy changes.
- Model/provider changes that affect cost or latency.
