# Best Practices

## AI best practices

- Use structured prompts with explicit goals, constraints, and output shape.
- Maintain reusable context summaries per service.
- Run evaluation suites on prompts before promoting changes.
- Capture prompt version, model, latency, and token cost for each critical call.

## Trading system best practices

- Separate signal generation, decision support, and execution.
- Use paper, shadow, and live modes.
- Measure expected vs actual fill quality.
- Make exits explicit, testable, and observable.

## Software best practices

- Prefer typed contracts.
- Add idempotency to all order-related writes.
- Store audit events before external execution where feasible.
- Keep mock and production code paths visible.

## Token best practices

- Prefer compact schemas over verbose natural language.
- Use retrieval filters before sending context.
- Batch related questions in one request when safe.
- Trim stale history aggressively.
- Cache stable outputs such as company profiles, strategy descriptions, and policy summaries.
