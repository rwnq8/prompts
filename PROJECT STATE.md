# PROJECT STATE — Prompts Directory (Template Integration Wiring)

**Last Updated:** 2026-05-22
**Active Branch:** feature/template-integration-audit
**Current Phase:** P1 (Planning → Execution)

## What This Project Is

Wiring the 11 project management prompt templates (PROJECT-CHARTER, SPRINT-BACKLOG, DEFINITION-OF-DONE, PRODUCT-BACKLOG, RISK-REGISTER, RETROSPECTIVE, HANDOFF, README, CHANGELOG, ADR, CONTRIBUTING) into the agent system prompts so that new projects initiated by QWAV → Projects are scaffolded with template-driven documentation rather than manual ad-hoc files.

## Current Status

**Audit complete (S0):** 8 findings documented in `audit-reports/audit-2026-05-22_template-integration.md`. Core finding: 11/18 templates are dead code — registered and functional but never called by any agent workflow. DEFAULT.md, QWAV-DEFAULT.md, ARCHITECTURE.md, and PROJECTS-AGENT.md all lack references to project management templates.

**Active task (S1):** Wiring templates into DEFAULT.md §0.7 Startup Procedure. Current procedure says "If any are missing, create them" — must be replaced with `fill_prompt_template` calls for each file that has a template.

## Next Agent Handoff

1. Read SPRINT.md → identify S1 as active task
2. Read DEFAULT.md §0.7 (lines 134-159) → understand current startup procedure
3. Edit DEFAULT.md: replace manual "create them" with template-driven file generation
4. Commit with ACTION:EDIT RATIONALE
5. Update SPRINT.md: mark S1 complete, activate S2

## Constraints

| Constraint | Value |
|:-----------|:------|
| Write sandbox | `G:\My Drive\prompts\` only |
| Branch | `feature/template-integration-audit` |
| Merge target | `main` (after all P0 tasks complete + testing) |
| CPL enforcement | Must not violate CPL L1-L40, especially L19 (branch rename check), L21 (audit 7 docs), L40 (verify after every write) |

## Files Modified This Session

| File | Action | Status |
|:-----|:-------|:-------|
| `audit-reports/audit-2026-05-22_template-integration.md` | CREATE | Committed |
| `SPRINT.md` | CREATE | Pending commit |
| `PROJECT STATE.md` | CREATE | Pending commit |
