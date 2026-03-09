# Observability SRE Custom Commands

These are reusable prompt commands for the `observability-sre` agent.

## Usage pattern
Use a command name followed by compact context.

Example:
`/obs-module-plan module=state_manager workflows="approvals,circuit_breaker,positions"`

## Command rules
- Keep inputs short and module-specific.
- Prefer naming the workflow, service, or GUI surface.
- Ask for bounded output.
- Reuse prior metric definitions instead of repeating context.

## Commands

### `/obs-module-plan`
Define baked-in observability for one module.

**Input**
- module
- workflows
- dependencies

**Output**
- instrumentation points
- functional metrics
- system metrics
- logs
- traces
- GUI surfaces
- alerts

### `/obs-flow-map`
Map observability to a functional workflow.

**Input**
- workflow
- services
- user touchpoints

**Output**
- flow stages
- emitted events
- trace spans
- metrics
- failure indicators
- GUI mapping

### `/obs-gui-widgets`
Design frontend components for operator-visible telemetry.

**Input**
- module or workflow
- target page
- operator goal

**Output**
- widget list
- displayed metrics
- states and thresholds
- refresh or staleness behavior
- drill-down suggestions

### `/obs-metric-set`
Define the minimum useful metric set.

**Input**
- module
- category=functional|system|ai|risk

**Output**
- metric name
- type
- description
- labels
- unit
- alert suitability

### `/obs-log-schema`
Define structured log requirements.

**Input**
- module
- workflow

**Output**
- required fields
- correlation IDs
- severity guidance
- redact or sensitive fields guidance

### `/obs-trace-plan`
Define end-to-end tracing points.

**Input**
- workflow
- services

**Output**
- span boundaries
- parent-child flow
- key attributes
- latency checkpoints
- failure markers

### `/obs-alert-plan`
Create actionable alert design.

**Input**
- module
- critical condition
- impact

**Output**
- alert name
- trigger
- threshold
- severity
- operator action
- runbook need

### `/obs-dashboard-plan`
Create a dashboard plan for backend and GUI views.

**Input**
- audience=operator|engineering|support|risk
- modules

**Output**
- dashboard sections
- top metrics
- trends
- alerts
- drill-down paths

### `/obs-coverage-check`
Review whether a module has enough observability.

**Input**
- module
- files
- workflows

**Output**
- covered areas
- missing telemetry
- GUI gaps
- release risks
- next fixes

### `/obs-staleness-check`
Define stale-data detection for metrics and GUI components.

**Input**
- data source
- consumers

**Output**
- freshness expectation
- stale thresholds
- alerts
- GUI stale indicators

### `/obs-runbook`
Create a short runbook for a likely failure mode.

**Input**
- module
- failure type
- environment

**Output**
- symptoms
- telemetry to check
- likely causes
- recovery steps
- escalation path

### `/obs-token-cost`
Create AI observability for token usage and quality.

**Input**
- workflow
- model calls

**Output**
- token metrics
- cost metrics
- latency metrics
- cache metrics
- GUI surfacing plan

## Recommended sequence
1. `/obs-module-plan`
2. `/obs-flow-map`
3. `/obs-metric-set`
4. `/obs-gui-widgets`
5. `/obs-log-schema`
6. `/obs-trace-plan`
7. `/obs-alert-plan`
8. `/obs-coverage-check`

## Token-efficient examples
- `/obs-module-plan module=execution_manager workflows="place-order,shadow-fill,live-approval"`
- `/obs-gui-widgets module=gateway target page=dashboard operator goal="see service and workflow health quickly"`
- `/obs-token-cost workflow="trade suggestion summary" model calls="rank, summarize, explain"`
