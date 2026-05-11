# DECISIONS LOG — Prompts

> **Purpose:** Record key architecture, design, and strategy decisions with rationale. Prevents re-litigating settled questions.

---

## Decision Registry

| D# | Date | Decision | Status |
|:---|:-----|:---------|:-------|
| D1 | 2026-05-11 | Per-project independent git repos (not shared parent repo) | ACTIVE |
| D2 | 2026-05-11 | Unified orchestration framework subsumes isolation enforcer | ACTIVE |
| D3 | 2026-05-11 | Standardized 7-file documentation set for every project | ACTIVE |
| D4 | 2026-05-11 | Cross-project learnings in _shared/ with human-in-the-loop curation | ACTIVE |
| D5 | 2026-05-11 | Subagent git-skip directive for read-only tasks | ACTIVE |
| D6 | 2026-05-11 | Machine-readable lesson format with cross-project flags | ACTIVE |

---

## Decisions

### D1: Per-project independent git repos (not shared parent repo)

- **Date:** 2026-05-11
- **Status:** ACTIVE
- **Context:** Multiple LLM agents working in sibling directories under `G:\My Drive\projects\` were committing to a single parent-level git repo. This caused cross-project commit contamination, branch collisions, and accidental file deletions. The root `.git/` at the parent level made all 6 projects share one git history.
- **Options Considered:**
  1. Keep shared parent repo, enforce branch-per-project discipline: Simpler migration, but doesn't prevent agents from seeing/modifying other projects' files in the working tree. Doesn't solve the fundamental isolation problem.
  2. Per-project independent repos: Each project directory gets its own `.git/`. Full isolation. Agents can only git-operate within their project. Migration required (each project must be git-init'd, existing history restructured).
- **Decision:** Option 2 — per-project independent repos. Full isolation is the only way to prevent cross-project contamination. The migration cost is acceptable (5 of 6 projects already have no `.git/`, so there's no history to lose).
- **Consequences:** Easier: git history is project-scoped, no cross-project merge conflicts, each project can have its own branching strategy. Harder: cannot `git log` across projects, cross-project file moves require explicit copy operations.
- **Revisit Trigger:** If a use case emerges requiring unified cross-project git history (e.g., monorepo tooling that needs atomic cross-project commits).

### D2: Unified orchestration framework subsumes isolation enforcer

- **Date:** 2026-05-11
- **Status:** ACTIVE
- **Context:** PROJECT-ISOLATION-ENFORCER-v1.0 was created to solve workspace confinement. During the same session, the scope expanded to include sprint management, kaizen learning loops, standardized documentation, and cross-project knowledge sharing. Two separate prompts (isolation + project management) would create fragmentation.
- **Options Considered:**
  1. Two separate prompts: isolation enforcer as a prependable module + separate project management prompt. Modular but increases prompt complexity and risk of inconsistent application.
  2. Single unified framework: All concerns (isolation, documentation, sprint lifecycle, kaizen, git) in one comprehensive prompt.
- **Decision:** Option 2 — unified PROJECT-ORCHESTRATION-FRAMEWORK. The isolation enforcer v1.0 is preserved as a simpler alternative for cases where the full framework is overkill, but new project work should use the unified framework.
- **Consequences:** Easier: one prompt to maintain, consistent application across projects. Harder: larger prompt (878 lines), may need to be split if it grows beyond practical token limits.
- **Revisit Trigger:** If the framework exceeds ~1500 lines or if isolation-only use cases become frequent enough to justify maintaining two prompts.

### D3: Standardized 7-file documentation set for every project

- **Date:** 2026-05-11
- **Status:** ACTIVE
- **Context:** Projects had inconsistent documentation. QWAV had SPRINT.md and CHANGELOG.md but embedded learnings in sprint narratives. Other projects had no project management files at all. The prompts/ directory had no CHANGELOG, SPRINT, BACKLOG, or LEARNINGS.
- **Options Considered:**
  1. Minimal set (SPRINT + CHANGELOG only): Less overhead but no structured lessons or backlog. QWAV's current approach.
  2. Full set (README, PROJECT STATE, SPRINT, CHANGELOG, BACKLOG, LEARNINGS, DECISIONS): More files but each has a distinct purpose with no overlap. Enables complete agent handoff.
- **Decision:** Option 2 — full 7-file set. Each file serves a distinct purpose. PROJECT STATE.md is the primary handoff (read-first). SPRINT.md is the active work tracker. LEARNINGS.md is the kaizen engine. The overhead is justified by eliminating context-transfer time between sessions.
- **Consequences:** Easier: agents always know where to find information, no re-explaining context between sessions. Harder: 7 files to maintain per project, risk of stale files if agents don't update them.
- **Revisit Trigger:** If file maintenance overhead measurably reduces task throughput without corresponding quality improvement.

### D4: Cross-project learnings in _shared/ with human-in-the-loop curation

- **Date:** 2026-05-11
- **Status:** ACTIVE
- **Context:** Lessons learned in one project (e.g., git contamination from shared repos) apply to all projects. But allowing agents to freely write to a shared directory creates its own contamination risk. Need a mechanism for cross-project knowledge sharing that doesn't compromise isolation.
- **Options Considered:**
  1. Agents write directly to _shared/: Fast propagation but reintroduces cross-project write contamination. Multiple agents could conflict.
  2. Human-only curation: Only the human writes to _shared/. Agents never touch it. Clean but slow — human becomes bottleneck.
  3. Agent-propose, human-approve: Agents propose entries from their project's LEARNINGS.md. Human reviews and writes to _shared/. Balanced.
- **Decision:** Option 3 — agent-propose, human-approve. Agents can read _shared/ freely (no contamination risk from reads). Writing requires explicit human approval. This maintains isolation while enabling cross-project learning.
- **Consequences:** Easier: agents benefit from other projects' lessons without write-access risk. Harder: human must actively curate (but this is a feature — quality gate on cross-project knowledge).
- **Revisit Trigger:** If proposal volume exceeds human capacity, consider automated filtering (e.g., only CRITICAL severity lessons auto-propagate).

### D5: Subagent git-skip directive for read-only tasks

- **Date:** 2026-05-11
- **Status:** ACTIVE
- **Context:** 20-invocation cross-slot audit confirmed subagents inherit the full system prompt including git discipline. Read-only subagent tasks (text synthesis, blind validation, reader testing) were wasting response budget on git pre-flight checks. Subagents have ~65% chance of lacking write/exec tools, making git operations impossible anyway.
- **Options Considered:**
  1. Remove git discipline from all prompts: Solves subagent problem but breaks git hygiene for parent agents.
  2. Conditional git section based on agent type: Complex to implement — prompts don't know if they're running as parent or subagent.
  3. Explicit git-skip directive in subagent task prompts: Simple, explicit, no prompt changes needed. First line of every subagent task is `GIT: Skip all git/branch checks. Read-only task.`
- **Decision:** Option 3 — explicit git-skip directive. Added to subagent task template in SUBAGENT_DESCRIPTIONS.md. Also added scoping section (7.2.1) to DEFAULT.md's git protocol for prompts that target read-only agents.
- **Consequences:** Easier: subagents don't waste budget on git, task completion rate improves. Harder: requires discipline to always include the directive in subagent task prompts.
- **Revisit Trigger:** If subagent architecture changes (e.g., subagents get their own prompt independent of parent).

### D6: Machine-readable lesson format with cross-project flags

- **Date:** 2026-05-11
- **Status:** ACTIVE
- **Context:** Lessons embedded in narrative text (QWAV's SPRINT.md approach) are not filterable, searchable, or propagatable across projects. Kaizen requires that agents can quickly find relevant lessons before starting work.
- **Options Considered:**
  1. Narrative format (embedded in SPRINT): Low overhead but not searchable or cross-project compatible. Status quo.
  2. Structured markdown with mandatory fields: Category, Severity, Cross-Project flag, Tags. Enables registry table, programmatic filtering, and cross-project propagation.
- **Decision:** Option 2 — machine-readable format. 10 standardized categories, 3 severity levels, YES/NO/CONDITIONAL cross-project flag, free-form tags. Registry table at top of LEARNINGS.md for quick scanning. Same format used in CROSS-PROJECT-LEARNINGS.md organized by category.
- **Consequences:** Easier: agents can filter lessons by category ("show me all GIT lessons"), cross-project propagation is deterministic. Harder: more fields to fill per lesson (but template reduces burden).
- **Revisit Trigger:** If the 10 categories prove insufficient or if agents routinely skip fields.
