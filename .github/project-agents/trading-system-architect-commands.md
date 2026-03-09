# Trading System Architect Custom Commands

These are reusable prompt commands for the `trading-system-architect` agent.

## Usage pattern
Use a command name followed by compact context.

Example:
`/arch-module-boundary module=state_manager requirement="own approvals, limits, and positions state"`

## Commands

### `/arch-module-boundary`
Define module boundaries and ownership.

**Input**
- module
- requirement
- related modules

**Output**
- responsibilities
- owned state
- interfaces
- dependencies
- boundary risks

### `/arch-domain-model`
Define canonical data models.

**Input**
- domain area
- workflows

**Output**
- entities
- key fields
- ownership
- lifecycle notes
- audit notes

### `/arch-interface-contract`
Define request, response, and event contracts.

**Input**
- source module
- target module
- workflow

**Output**
- contract shape
- required fields
- validation notes
- versioning notes
- failure modes

### `/arch-flow-design`
Design a critical workflow across modules.

**Input**
- workflow
- services
- constraints

**Output**
- step flow
- responsibilities
- decisions
- failure handling
- observability contract

### `/arch-simplify`
Reduce complexity in an existing design.

**Input**
- current design
- pain points

**Output**
- simplifications
- removed complexity
- trade-offs
- recommended shape

### `/arch-nfr-check`
Check architecture against NFRs.

**Input**
- module or workflow
- nfr focus

**Output**
- strengths
- gaps
- risks
- remediation steps

### `/arch-observability-contract`
Define observability requirements per module or flow.

**Input**
- module or workflow

**Output**
- health contract
- metrics
- logs
- traces
- GUI telemetry needs

### `/arch-gap-check`
Compare architecture to requirements and repository truth.

**Input**
- target capability
- current modules

**Output**
- aligned areas
- gaps
- risks
- next architecture decisions

### `/arch-decision-record`
Write a compact architecture decision.

**Input**
- topic
- options
- constraints

**Output**
- decision
- rationale
- trade-offs
- consequences

## Token-efficient examples
- `/arch-flow-design workflow="approved live order" services="frontend,gateway,state_manager,execution_manager,journaling_service"`
- `/arch-observability-contract module=execution_manager`
- `/arch-gap-check target capability="expected vs actual portfolio delta analysis" current modules="state_manager,journaling_service,frontend"`
