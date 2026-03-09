# Guidelines

## Collaboration guidelines

- Treat documentation as executable guidance.
- Capture decisions close to the affected module.
- Keep prompts and specs versioned.
- Prefer smaller, reviewable milestones.

## AI collaboration guidelines

- Use AI for synthesis, gap analysis, and draft generation.
- Use deterministic code for risk, accounting, and order state.
- Use standard templates for prompts, evaluations, and postmortems.
- Prefer model routing: cheap model first, expensive model only when needed.

## Token-efficient design guidelines

- Summarize portfolio state to only actionable holdings.
- Summarize market context by regime, watchlist, and exceptions.
- Use event deltas instead of full state refreshes.
- Keep prompt sections fixed so cache hits improve.
- Define stop conditions for multi-step reasoning.

## Architecture guidelines

- Frontend for control and visibility.
- Gateway for orchestration and policy enforcement.
- Backend services for stateful domain logic.
- Journaling as the source for audit and learning.
- AI services must consume curated views, not raw platform exhaust.
