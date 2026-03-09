# Project Agents

These are project-specific agent definitions for Digital Trader Bot.

## Purpose
Give AI clear specialist roles for this repository while keeping token usage disciplined.

## Suggested agents
- `ai-platform-orchestrator`
- `trading-system-architect`
- `broker-integration-engineer`
- `quant-strategy-analyst`
- `risk-compliance-guardian`
- `observability-sre`
- `delivery-lead`

## Usage
Use these files as role prompts for project-scoped AI sessions, or copy the content into a user-level custom agent setup.

Supporting command catalog:
- [agent-selection-commands.md](agent-selection-commands.md) - Commands to choose the right agent and hand off work cleanly
- [memoryprint-commands.md](memoryprint-commands.md) - Commands to restore and save compact project memory in `.github/MemoryPrint`
- [trading-system-architect-commands.md](trading-system-architect-commands.md) - Reusable architecture planning and contract commands for the `trading-system-architect` agent
- [broker-integration-engineer-commands.md](broker-integration-engineer-commands.md) - Reusable broker adapter and reconciliation commands for the `broker-integration-engineer` agent
- [quant-strategy-analyst-commands.md](quant-strategy-analyst-commands.md) - Reusable strategy design and evaluation commands for the `quant-strategy-analyst` agent
- [risk-compliance-guardian-commands.md](risk-compliance-guardian-commands.md) - Reusable control and guardrail commands for the `risk-compliance-guardian` agent
- [delivery-lead-commands.md](delivery-lead-commands.md) - Reusable development-cycle commands for the `delivery-lead` agent
- [observability-sre-commands.md](observability-sre-commands.md) - Reusable observability planning and GUI telemetry commands for the `observability-sre` agent

## Shared rules for all agents
- Optimize token use.
- Respect broker and compliance constraints.
- Use repository truth over assumption.
- Prefer concise outputs with action lists and risks.
- Read `.github/MemoryPrint/project-baseline.json` and `.github/MemoryPrint/latest-context.json` before major work when available.
- Update `.github/MemoryPrint/latest-context.json` and append a compact checkpoint to `.github/MemoryPrint/checkpoints.jsonl` after material changes in project understanding.
- Keep MemoryPrint entries machine-readable, compact, and low-token.
