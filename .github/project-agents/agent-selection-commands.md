# Agent Selection Commands

Use these commands to choose the right project agent before starting work.

## Quick selector

### `/agent-pick`
Choose the best single agent for a task.

**Input**
- objective
- scope
- constraints

**Output**
- recommended agent
- why this agent
- expected output format
- suggested next command

### `/agent-compare`
Compare 2-3 candidate agents for the same task.

**Input**
- objective
- candidate agents

**Output**
- best fit
- second-best fit
- trade-offs
- handoff suggestion

### `/agent-route`
Route a task across multiple agents in the right order.

**Input**
- objective
- scope

**Output**
- agent sequence
- role of each agent
- handoff artifacts
- stopping conditions

### `/agent-stack`
Choose the minimum useful set of collaborating agents.

**Input**
- task
- delivery phase

**Output**
- required agents
- optional agents
- risks if skipped
- recommended first command

### `/agent-handoff`
Move work from one agent to another cleanly.

**Input**
- from agent
- to agent
- artifact
- objective

**Output**
- compact handoff packet
- assumptions
- open questions
- expected next output

### `/memory-refresh`
Refresh project context from MemoryPrint before choosing or routing agents.

**Input**
- task
- scope

**Output**
- relevant memory files
- current context summary
- likely stale areas
- recommended starting agent

### `/memory-checkpoint`
Create a compact MemoryPrint checkpoint after a material change.

**Input**
- change type
- scope
- impact

**Output**
- latest-context updates
- checkpoint entry
- affected agents
- next reads required

## Fast task-to-agent map

### Use `ai-platform-orchestrator` for
- turning business goals into work plans
- choosing other agents
- creating phased delivery plans
- aligning outputs to requirements

### Use `trading-system-architect` for
- system decomposition
- service boundaries and contracts
- domain models
- architecture decisions
- observability contracts at architecture level

### Use `delivery-lead` for
- turning plans into delivery slices
- flow coverage and acceptance criteria
- testing and release readiness
- CI/CD, troubleshooting, and support during delivery

### Use `observability-sre` for
- baked-in module telemetry
- GUI health and metric widgets
- alerts, traces, logs, and dashboards
- AI token and quality telemetry

### Use `broker-integration-engineer` for
- broker adapters
- field normalization
- paper/shadow/live flows
- reconciliation and broker troubleshooting

### Use `quant-strategy-analyst` for
- entry and exit strategy design
- strategy hypotheses and evaluation
- regime fit and drift review
- expected vs actual trade analysis

### Use `risk-compliance-guardian` for
- pre-trade and post-trade controls
- approval flow rules
- guardrail checks
- PDT and broker-policy review
- release compliance readiness

## Recommended selection flow
1. Use `/memory-refresh` to restore project context first.
2. Use `/agent-pick` if the task is narrow.
3. Use `/agent-route` if the task spans business, architecture, delivery, and controls.
4. Use `/agent-handoff` whenever one agent finishes and another should continue.
5. Use `/memory-checkpoint` after major changes or decisions.

## Token-efficient examples
- `/agent-pick objective="design metrics widgets for order approval flow" scope="frontend + gateway + state_manager" constraints="show status in GUI"`
- `/agent-route objective="replace fidelity mock with real integration safely" scope="adapter, risk checks, delivery, observability"`
- `/agent-compare objective="define expected vs actual portfolio delta capability" candidate agents="trading-system-architect,quant-strategy-analyst,delivery-lead"`
