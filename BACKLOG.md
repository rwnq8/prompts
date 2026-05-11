# BACKLOG — Prompts

**Last prioritized:** 2026-05-11

---

## P0 — Must Do (Next Sprint)

| ID | Task | Why | Estimated Effort | Dependencies |
|:---|:-----|:----|:-----------------|:-------------|
| B1 | Create _shared/CROSS-PROJECT-LEARNINGS.md | Cross-project kaizen requires shared knowledge library. Currently blocked by write-access limitation. | 1 session | Human must create directory/file outside prompts/ |
| B2 | Seed LEARNINGS.md with cross-project lessons | Lessons from this session (git contamination, subagent overhead, isolation) apply to all projects. | 1 session | LEARNINGS.md exists (done) |

## P1 — Should Do (Soon)

| ID | Task | Why | Estimated Effort | Dependencies |
|:---|:-----|:----|:-----------------|:-------------|
| B3 | Audit DEFAULT.md for orchestration framework compliance | DEFAULT.md is the most-used prompt. It should reference the orchestration framework and kaizen practices. | 1 session | None |
| B4 | Add project assignment header to DEFAULT.md | Agents need to know which project they're assigned to at session start. Currently missing. | 0.5 session | B3 |
| B5 | Create PROJECT-TEMPLATE/ in _shared/ | New projects should start from a template with all mandatory files pre-populated. | 1 session | Human must create directory |
| B6 | Version-bump PROJECT-ISOLATION-ENFORCER to note supersession | v1.0 is subsumed by orchestration framework. Add deprecation notice or merge. | 0.25 session | None |

## P2 — Could Do (Later)

| ID | Task | Why | Estimated Effort | Dependencies |
|:---|:-----|:----|:-----------------|:-------------|
| B7 | Create automated documentation checker prompt | Agent that audits project directories for missing mandatory files and reports gaps. | 1 session | Framework stable |
| B8 | Create sprint planning assistant prompt | Agent that reads BACKLOG + CROSS-PROJECT-LEARNINGS and proposes sprint plans. | 1 session | Shared learnings exist |
| B9 | Create cross-project lesson curator prompt | Agent that scans project LEARNINGS.md files and proposes entries for CROSS-PROJECT-LEARNINGS.md. | 1.5 sessions | Multiple projects have LEARNINGS.md |
| B10 | Subagent kaizen: measure git pre-flight overhead | Quantify how much response budget subagents waste on irrelevant git checks. Use data to tune scoping. | 1 session | None |
| B11 | Standardize external search coordination format | All prompts include search request manifest format. Create a reusable template. | 0.5 session | None |

## P3 — Ideas (Someday)

| ID | Idea | Why |
|:---|:-----|:----|
| B12 | Agent performance metrics dashboard | Track task completion rate, lesson density, commit frequency per project |
| B13 | Cross-project "wisdom of the crowd" synthesis | Multiple agents independently review same output, synthesize findings |
| B14 | Prompt A/B testing framework | Compare prompt versions on same task, measure output quality differences |
| B15 | Kaizen maturity model | Score projects on documentation completeness, lesson density, cross-project contribution |

---

## Completed (from backlog)

| ID | Task | Completed | Sprint |
|:---|:-----|:----------|:-------|
| — | — | — | — |
