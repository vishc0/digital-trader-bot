# Broker Integration Engineer Custom Commands

These are reusable prompt commands for the `broker-integration-engineer` agent.

## Usage pattern
Use a command name followed by compact context.

Example:
`/broker-adapter-plan broker=fidelity mode="paper to live migration"`

## Commands

### `/broker-adapter-plan`
Plan a broker adapter.

**Input**
- broker
- capability scope
- mode

**Output**
- adapter responsibilities
- contract mapping
- risks
- validation steps

### `/broker-capability-map`
Summarize what a broker supports.

**Input**
- broker
- workflow scope

**Output**
- supported capabilities
- unsupported areas
- caveats
- manual steps

### `/broker-field-map`
Map broker fields to platform contracts.

**Input**
- broker object
- platform object

**Output**
- field mapping table
- required transformations
- missing fields
- ambiguity notes

### `/broker-order-flow`
Design order lifecycle handling.

**Input**
- broker
- order type
- mode

**Output**
- states
- transitions
- failure paths
- reconciliation points

### `/broker-paper-shadow-live`
Split behavior by operating mode.

**Input**
- broker
- feature

**Output**
- paper behavior
- shadow behavior
- live behavior
- gating rules

### `/broker-error-model`
Define broker integration failure handling.

**Input**
- broker
- workflow

**Output**
- error classes
- retry policy
- fail-safe behavior
- audit expectations

### `/broker-recon-check`
Plan reconciliation between broker and platform state.

**Input**
- broker
- objects

**Output**
- reconciliation flow
- mismatch cases
- recovery actions
- telemetry needs

### `/broker-sandbox-readiness`
Assess sandbox or paper validation readiness.

**Input**
- broker
- feature

**Output**
- validation checklist
- gaps
- risks
- next steps

### `/broker-troubleshoot`
Investigate broker integration problems.

**Input**
- broker
- symptom
- workflow

**Output**
- likely cause
- immediate checks
- safe actions
- follow-up fixes

## Token-efficient examples
- `/broker-field-map broker object=orderStatus platform object=fill_event`
- `/broker-order-flow broker=fidelity order type=limit mode=paper`
- `/broker-troubleshoot broker=fidelity symptom="duplicate order suspicion after retry" workflow="place-order"`
