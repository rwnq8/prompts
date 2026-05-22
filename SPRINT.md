# Sprint Backlog — Template Integration Wiring

**Sprint Goal:** Wire all 11 project management templates into agent workflows so new projects are initiated with template-driven documentation, not manual ad-hoc scaffolding.
**Started:** 2026-05-22
**Target End:** 2026-05-22
**Status:** Active

## Active Tasks

| ID | Task | DoD Criteria | Est. Effort | Status | Assignee |
|:---|:-----|:-------------|:------------|:-------|:---------|
| S1 | Wire templates into DEFAULT.md §0.7 Startup Procedure | DOCUMENT: file passes Publication Language Gate, curly quotes, committed | 1h | [x] | Agent |
| S2 | Wire templates into QWAV-DEFAULT.md §0.9 Project Initiation | DOCUMENT: structured template sequence replaces "scaffold all 7 docs" | 1h | [~] | Agent |
| S3 | Update ARCHITECTURE.md Layer 5 — add all 11 PM templates | DOCUMENT: template table complete | 0.5h | [ ] | Agent |
| S4 | Update PROJECTS-AGENT.md tool description | DOCUMENT: fill_prompt_template purpose expanded | 0.25h | [ ] | Agent |
| S5 | Add Part F (Template Integration) to system_audit.py | CODE: detects unwired templates, passes/fails correctly | 0.5h | [ ] | Agent |
| S6 | Create PROJECT-STATE-TEMPLATE.md and LEARNINGS-TEMPLATE.md | DOCUMENT: two new templates for uncovered required files | 0.5h | [ ] | Agent |
| S7 | Create CLOSEOUT-CHECKLIST-TEMPLATE.md | DOCUMENT: template for §12.5 P5 gate referenced but non-existent file | 0.25h | [ ] | Agent |

## Completed (Retained for Audit)

| ID | Task | Completed | Verification |
|:---|:-----|:----------|:-------------|
| S1 | Wire templates into DEFAULT.md §0.7 Startup Procedure | 2026-05-22 | Test-Path DEFAULT.md + git log confirmed: 5 PM templates (README, SPRINT-BACKLOG, CHANGELOG, PRODUCT-BACKLOG, ADR) now wired into §0.7 |
| S0 | Template integration audit — 8 findings, 10 recommendations | 2026-05-22 | Test-Path audit-reports/audit-2026-05-22_template-integration.md + git log confirmed |

## Blocked

| ID | Task | Blocked By | Resolution |
|:---|:-----|:-----------|:-----------|
| — | — | — | — |

## Sprint Health

- Tasks completed: 2/8
- DoD verified: 1/7 remaining
- Blocked items: 0
- Retrospective filed: No

---
*Generated from SPRINT-BACKLOG-TEMPLATE.md v1.0*
