# Prompts Workspace Changelog

## 2026-05-19 — Role Boundary Amendments (QWAV/Projects Fork)

**Source:** QWAV handoff documents `QWAV/strategy/0.10.md` (diagnosis) and `QWAV/strategy/0.11.md` (handoff to Prompts agent)

### Problem
The QWAV and Projects agents shared the same `DEFAULT.md` system prompt, which positioned the agent as a generalist ("equally capable of creative ideation, rigorous research, structured writing"). This caused the QWAV agent to repeatedly cross into Project Executor territory — writing technical specifications, suggesting implementation details, micro-managing what a Projects thread should do. See `QWAV/LEARNINGS.md` L20 for the incident report.

### Changes Applied

| File | Action | Description |
|:-----|:-------|:------------|
| `DEFAULT.md` | EDIT | Added §0.9 PROJECTS AGENT ROLE: Independent Project Executor — defines what Projects does (research, computation, code, data analysis), what it doesn't do (update QWAV docs, make portfolio decisions), handoff protocol, and sub-handoff capability |
| `QWAV-DEFAULT.md` | CREATE | Forked from `DEFAULT.md` with QWAV-specific §0.9: Strategy Program Manager — defines portfolio-level scope, boundary rule ("DO NOT start executing project work"), delegation protocol, and initiation-vs-execution test |
| `AGENT-CONFIG.md` | EDIT | v5.2 → v5.3: QWAV agent now loads `QWAV-DEFAULT.md` instead of `DEFAULT.md`. Updated design note to explain the fork. |
| `ARCHITECTURE.md` | EDIT | v1.2 → v1.3: Updated agent table (removed "(TBD)" from QWAV-DEFAULT.md), added QWAV-DEFAULT.md to system prompts table, updated Layer 7 QWAV-AGENT.md reference, updated footer |
| `agents/QWAV-AGENT.md` | EDIT | v1.1 → v1.2: Updated system prompt reference from `DEFAULT.md` to `QWAV-DEFAULT.md`, updated design note and footer |

### Design Decision: Fork vs. Conditional

Both QWAV and Projects previously shared `DEFAULT.md`. The handoff recommended forking into two separate files (`QWAV-DEFAULT.md` and `DEFAULT.md` for Projects). This was chosen over a conditional/runtime mechanism because:
- Cleaner separation — each agent loads exactly the prompt it needs
- No runtime parameter complexity
- Aligned with ARCHITECTURE.md's existing anticipation of `QWAV-DEFAULT.md (TBD)`
- Both forks share identical capabilities (email, social media, due diligence, sandboxing); only §0.9 differs

### Verification Tests (to be run by QWAV thread)

| Agent | Test Input | Expected Behavior |
|:------|:-----------|:------------------|
| QWAV | "Build a tree-walk training simulation" | Creates handoff document, delegates to Projects, pauses |
| QWAV | "What's the next sprint task?" | Reads SPRINT.md, identifies task, frames it (QWAV scope) |
| Projects | "Update QWAV SPRINT.md" | Refuses — "QWAV documentation is managed by the QWAV agent" |
| Projects | "Which project should we work on next?" | Defers — "Project prioritization is QWAV strategy scope" |

