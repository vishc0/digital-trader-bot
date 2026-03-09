# Delivery Lead Custom Commands

These are reusable prompt commands for the `delivery-lead` agent during the development cycle.

## Usage pattern
Use a command name followed by compact context.

Example:
`/dl-plan-module module=execution_manager requirement="add approval-aware live order flow"`

## Command rules
- Keep inputs short and relevant.
- Reference files or modules when possible.
- Ask for bounded output.
- Prefer one command per objective.
- Reuse prior summaries instead of pasting large context repeatedly.

## Commands

### `/dl-plan-module`
Create a delivery plan for one module or service.

**Input**
- module
- requirement
- constraints

**Output**
- objective
- scope
- flow coverage
- MVP slice
- hardening tasks
- risks
- acceptance criteria
- next steps

### `/dl-flow-coverage`
Check whether happy path, failure path, edge cases, and boundary conditions are covered.

**Input**
- module
- feature
- relevant files

**Output**
- covered flows
- missing flows
- edge cases
- boundary conditions
- test recommendations

### `/dl-split-mvp`
Split work into MVP and production-hardening scope.

**Input**
- feature
- module
- current state

**Output**
- MVP scope
- deferred scope
- hardening scope
- release risks

### `/dl-acceptance-check`
Create or review acceptance criteria.

**Input**
- feature
- requirement
- module

**Output**
- acceptance criteria list
- pass or fail signals
- missing validation points

### `/dl-test-plan`
Create a targeted test strategy.

**Input**
- module
- feature
- risk areas

**Output**
- unit tests
- integration tests
- smoke tests
- regression checks
- failure-mode validation

### `/dl-dev-unblock`
Act as a hands-on developer to unblock delivery.

**Input**
- module
- issue
- expected outcome

**Output**
- likely cause
- smallest safe fix
- validation steps
- follow-up hardening

### `/dl-cicd-check`
Review CI/CD readiness and pipeline risks.

**Input**
- service
- pipeline stage
- recent failure or goal

**Output**
- failure points
- missing checks
- pipeline improvements
- release impact

### `/dl-release-readiness`
Assess whether a module or feature is ready for release.

**Input**
- feature
- module
- release target

**Output**
- readiness summary
- open blockers
- release gate status
- rollback readiness
- go or no-go recommendation

### `/dl-troubleshoot`
Investigate a delivery, deployment, test, or runtime issue.

**Input**
- symptom
- scope
- recent change
- logs or errors summary

**Output**
- issue classification
- likely causes
- immediate actions
- deeper fixes
- owner suggestions

### `/dl-support-runbook`
Create a short support runbook for likely delivery or production issues.

**Input**
- module
- issue type
- environment

**Output**
- symptoms
- checks
- likely causes
- recovery steps
- escalation path

### `/dl-risk-log`
Generate or refresh a delivery risk log.

**Input**
- release
- modules
- current blockers

**Output**
- risk list
- severity
- owner
- mitigation
- decision needed

### `/dl-status`
Produce a compact development-cycle status update.

**Input**
- milestone
- workstream
- current blockers

**Output**
- progress
- blockers
- risks
- next actions
- decisions needed

### `/dl-postrelease`
Support post-release stabilization.

**Input**
- release
- issue summary
- impacted module

**Output**
- stabilization plan
- immediate checks
- rollback trigger
- follow-up actions

### `/dl-token-audit`
Check whether the current delivery interaction is token-efficient.

**Input**
- current prompt or workflow summary

**Output**
- waste points
- tighter prompt version
- context reduction suggestions
- bounded output suggestion

## Recommended development-cycle sequence
1. `/dl-plan-module`
2. `/dl-flow-coverage`
3. `/dl-split-mvp`
4. `/dl-acceptance-check`
5. `/dl-test-plan`
6. `/dl-dev-unblock` or `/dl-cicd-check` as needed
7. `/dl-release-readiness`
8. `/dl-postrelease`

## Token-efficient command examples
- `/dl-status milestone=phase-2 workstream=state_manager blockers="redis auth not wired"`
- `/dl-troubleshoot symptom="execution-manager smoke test failing" scope="paper mode" recent change="approval validation added"`
- `/dl-cicd-check service=gateway pipeline stage=deploy recent failure="container healthcheck timeout"`
