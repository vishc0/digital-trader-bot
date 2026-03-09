# Rules

## Immutable platform rules

1. Protect capital first.
2. Keep a human in control of live execution.
3. Never design to evade broker, tax, exchange, or compliance rules.
4. Log every material decision.
5. Keep AI advisory logic separate from enforcement logic.
6. Optimize token usage in every AI workflow.

## AI rules

- AI may suggest, summarize, classify, and rank.
- AI may not directly override risk controls.
- AI outputs must be treated as untrusted until validated.
- Prompts must exclude unnecessary secrets, noise, and duplicate context.
- Every AI workflow must define input budget, output budget, timeout, and fallback.

## Engineering rules

- One service owns one clear responsibility.
- All external calls must have timeouts and retries.
- Every service exposes health, metrics, and version endpoints.
- Every state mutation must be attributable to actor, reason, and trace ID.
- Mock adapters must be clearly labeled and isolated from live paths.

## Trading rules

- Paper trade first.
- Live trade only after checklist completion.
- Enforce position, exposure, and drawdown limits in code.
- Require explainability for trade suggestion, entry, hold, and exit.
- Keep PDT and broker compliance policies explicit in guardrails.
