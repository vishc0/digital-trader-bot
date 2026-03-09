# MemoryPrint

This folder stores compact machine-readable project memory for Digital Trader Bot.

## Purpose
Enable AI agents to quickly restore project context with low token usage when returning to this repository.

## Core files
- [project-baseline.json](project-baseline.json) - Stable project identity, goals, constraints, and module map.
- [latest-context.json](latest-context.json) - Current working context, active priorities, decisions, risks, and next actions.
- [checkpoints.jsonl](checkpoints.jsonl) - Append-only compact history of meaningful checkpoints.
- [checkpoint-template.json](checkpoint-template.json) - Template for new checkpoint entries.

## Rules
- Keep entries compact and machine-readable.
- Prefer JSON and JSONL with stable keys.
- Store only high-value reusable understanding.
- Update after meaningful planning, architecture, delivery, implementation, deployment, troubleshooting, or governance changes.
- Read the latest MemoryPrint before major work.

## Suggested update flow
1. Read [project-baseline.json](project-baseline.json).
2. Read [latest-context.json](latest-context.json).
3. Perform the task.
4. Update [latest-context.json](latest-context.json) if the durable project understanding changed.
5. Append one compact object line to [checkpoints.jsonl](checkpoints.jsonl).
