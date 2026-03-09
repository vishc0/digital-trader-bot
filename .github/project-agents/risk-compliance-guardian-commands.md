# Risk and Compliance Guardian Custom Commands

These are reusable prompt commands for the `risk-compliance-guardian` agent.

## Usage pattern
Use a command name followed by compact context.

Example:
`/risk-pretrade workflow="live buy order" constraints="human approval required,max position 10%"`

## Commands

### `/risk-pretrade`
Define pre-trade checks.

**Input**
- workflow
- constraints

**Output**
- control points
- rejection conditions
- required approvals
- audit needs

### `/risk-posttrade`
Define post-trade checks and evidence.

**Input**
- workflow
- risk focus

**Output**
- post-trade controls
- monitoring points
- exception handling
- journal requirements

### `/risk-policy-map`
Map rules to a feature or workflow.

**Input**
- feature
- workflows

**Output**
- applicable policies
- enforced controls
- evidence needed
- gaps

### `/risk-exposure-check`
Review exposure and drawdown controls.

**Input**
- module or workflow
- portfolio context

**Output**
- controls present
- gaps
- fail-safe actions
- telemetry needs

### `/risk-approval-flow`
Design or review approval logic.

**Input**
- workflow
- actors

**Output**
- approval stages
- rejection path
- override logging
- audit expectations

### `/risk-pdt-review`
Check day-trading and broker-policy risk.

**Input**
- workflow
- account context

**Output**
- risk points
- policy exposure
- safe handling
- user guidance

### `/risk-guardrail-check`
Review a module against platform guardrails.

**Input**
- module
- feature

**Output**
- aligned controls
- missing guardrails
- release risks
- next fixes

### `/risk-exception-log`
Create a compact exception handling plan.

**Input**
- workflow
- exception type

**Output**
- trigger
- handling path
- logging needs
- approval needs

### `/risk-release-gate`
Assess risk and compliance readiness for release.

**Input**
- feature
- module

**Output**
- gate status
- unresolved risks
- evidence gaps
- go or no-go view

## Token-efficient examples
- `/risk-approval-flow workflow="enable live trading" actors="operator,admin,state_manager"`
- `/risk-guardrail-check module=execution_manager feature="shadow-to-live routing"`
- `/risk-pdt-review workflow="same-day entry and exit assist" account context="retail margin account"`
