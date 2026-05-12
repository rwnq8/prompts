# CROSS-PROJECT LEARNINGS

> **Purpose:** Lessons applicable across all projects. Read this at session start.
> **How it works:** Agents read this file (read-only). When an agent discovers a cross-project lesson, it tells you. You decide what gets added here.

---

## By Category

| L# | Category | Source | Lesson |
|:---|:---------|:-------|:-------|
| L1 | GIT | prompts/ | Shared parent repo causes cross-project contamination — each project needs its own `.git/` |
| L2 | ISOLATION | prompts/ | Without path confinement, agents access sibling project directories |
| L3 | METHODOLOGY | prompts/ | Subagents inherit full system prompt including git — read-only subagents need `GIT: Skip` directive |
| L4 | FILE-MGMT | prompts/ | Standardized 7-file documentation enables agent handoff across sessions |
| L5 | TOOL-USE | prompts/ | Windows PowerShell rejects `&&` — use `;` or separate commands |

---

## Lessons

### L1: Per-project git repos (not shared parent)

- **Category:** GIT
- **Issue:** Multiple agents committed to a single `.git/` at `G:\My Drive\projects\`, mixing QWAV, Ultrametric Synthesis, and other projects on the same branches. Cross-project file deletions occurred.
- **Solution:** Each project directory gets its own `git init`. The parent is a container, not a repo.
- **Prevention:** Agent startup checks `git rev-parse --show-toplevel` — must equal project path, not parent. See DEFAULT.md Phase 0.1.6.

### L2: Workspace path confinement

- **Category:** ISOLATION
- **Issue:** Agents read and wrote files in sibling project directories without restriction.
- **Solution:** Hard path verification before every file operation. Forbidden: sibling dirs, parent dir, any path outside assigned project. Violation = hard stop with `[ISOLATION-VIOLATION]`.
- **Prevention:** See DEFAULT.md Section 0.6.

### L3: Subagent git overhead

- **Category:** METHODOLOGY
- **Issue:** SELF-CLONE subagents inherit the full system prompt including git discipline. Read-only text tasks waste response budget on branch checks (~65% of subagents lack write/exec tools anyway).
- **Solution:** Every subagent task prompt starts with: `GIT: Skip all git/branch checks. Read-only task.`
- **Prevention:** Use the subagent task template in SUBAGENT_DESCRIPTIONS.md.

### L4: Standardized documentation for agent handoff

- **Category:** FILE-MGMT
- **Issue:** Agents starting new sessions on the same project had no way to know what was done, what's next, or what failed. Human had to re-explain context every time.
- **Solution:** 7 mandatory files per project: README, PROJECT STATE, SPRINT, CHANGELOG, BACKLOG, LEARNINGS, DECISIONS. Agents read STATE → SPRINT → LEARNINGS → CHANGELOG at session start.
- **Prevention:** See DEFAULT.md Section 0.7.

### L5: PowerShell command syntax

- **Category:** TOOL-USE
- **Issue:** Commands using `&&` (bash chaining) fail on Windows PowerShell. Example: `cd "path" && git status` → parser error.
- **Solution:** Use `Set-Location "path"; command1; command2` or run commands separately.
- **Prevention:** Always use PowerShell-compatible syntax on Windows.
