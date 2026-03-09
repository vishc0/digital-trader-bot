# MemoryPrint Commands

Use these commands to restore and save compact project memory in `.github/MemoryPrint`.

## Usage pattern
Use a command name followed by short structured context.

Example:
`/mem-read focus="architecture and delivery status"`

## Commands

### `/mem-read`
Read the MemoryPrint files and restore relevant project context.

**Input**
- focus

**Output**
- baseline summary
- latest context summary
- relevant risks
- relevant next actions

### `/mem-write`
Create a compact checkpoint after a material change.

**Input**
- change type
- scope
- durable facts
- decisions
- risks
- next

**Output**
- latest-context update proposal
- checkpoint JSONL entry

### `/mem-sync`
Refresh MemoryPrint after a multi-agent workflow.

**Input**
- completed work
- changed areas
- open gaps

**Output**
- consolidated latest-context changes
- checkpoint entry
- files or agents affected

### `/mem-diff`
Compare current work with the latest stored memory.

**Input**
- scope
- current summary

**Output**
- new facts
- outdated facts
- latest-context updates needed

### `/mem-compact`
Reduce a long project update into low-token memory format.

**Input**
- source summary

**Output**
- compact JSON fields
- stable keys
- reusable summary lines

## Recommended usage
1. `/mem-read` before major work.
2. Perform the task.
3. `/mem-write` or `/mem-sync` after durable project understanding changes.
4. `/mem-diff` when unsure what should be updated.

## Token-efficient examples
- `/mem-read focus="active architecture decisions and next delivery priorities"`
- `/mem-write change type="architecture" scope="gateway,state_manager" durable facts="gateway owns orchestration; state_manager owns approvals and limits" decisions="observability contract required per module" risks="journaling still not durable" next="define canonical order contract"`
- `/mem-sync completed work="expanded all project agents with memoryprint mandate" changed areas="project-agents, prompts, copilot instructions" open gaps="memory updates must be used consistently going forward"`
