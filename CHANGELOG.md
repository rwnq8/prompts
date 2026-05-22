# Prompts Workspace Changelog

## 2026-05-22 — Template Integration Wiring + QA/QC Overhaul + Scope Codification

**Source:** Template integration audit (`audit-reports/audit-2026-05-22_template-integration.md`) found 11/18 PM templates were dead code — registered but never invoked by any agent workflow.

### Sprint 1: Template Integration Wiring (S0-S7, 14 commits)

| File | Action | Description |
|:-----|:-------|:------------|
| `DEFAULT.md` | EDIT | §0.7 Startup Procedure replaced "create them" with template-driven file generation table. All 7 mandatory files mapped to templates via `fill_prompt_template`. §12.3 close-out generates from CLOSEOUT-CHECKLIST-TEMPLATE. §12.5 retrospective uses RETROSPECTIVE-TEMPLATE. |
| `QWAV-DEFAULT.md` | EDIT | §0.9 Project Initiation: 10-step template-driven initiation protocol replaces "scaffold all 7 docs." 13/16 PM templates wired. |
| `ARCHITECTURE.md` | EDIT | Layer 5 expanded 6→22 template rows (6 functional + 16 PM). Split into subgroups. |
| `agents/PROJECTS-AGENT.md` | EDIT | `fill_prompt_template` description expanded to full template inventory. |
| `tools/system_audit.py` | EDIT | Added Part F: Template Integration Check — scans DEFAULT + QWAV for template references, flags dead code. |
| `templates/` | CREATE (3) | PROJECT-STATE-TEMPLATE, LEARNINGS-TEMPLATE, CLOSEOUT-CHECKLIST-TEMPLATE. Now all 7 §0.7 mandatory files have templates. |
| `SPRINT.md`, `PROJECT STATE.md`, `BACKLOG.md` | CREATE | Prompts directory now complies with its own §0.7 mandate. |

### Sprint 2: QA/QC Process Overhaul (Q1-Q9, 4 commits)

| File | Action | Description |
|:-----|:-------|:------------|
| `templates/DEFINITION-OF-DONE-TEMPLATE.md` | EDIT | Expanded from 4 to 7 task types: CODE, CODE TEST, DOCUMENT (with reader testing), PUBLICATION, ANALYSIS, ANALYSIS TEST, WEB APP (14 checks). All test sections require re-execution evidence, not file existence. |
| `templates/WEB-APP-RELEASE-CHECKLIST.md` | CREATE | 9-section pre-deployment gate: functionality, error handling, cross-browser, accessibility, asset loading, test execution, documentation, deployment, post-deployment. |
| `templates/QA-QC-TESTING-PROTOCOL.md` | CREATE | Universal framework: deliverable type testing matrix (DOCUMENT/CODE/WEB APP/ANALYSIS), phase gate integration, test evidence standard, anti-patterns. |
| `templates/TEST-EVIDENCE-TEMPLATE.md` | CREATE | Standardized test execution evidence document with re-execution command, output capture, pass/fail count, root cause analysis. |
| `DEFAULT.md` | EDIT | §12.5 Phase Gates: P0 requires TEST PLAN, P2 requires TEST SUITE EXECUTED, P3 full QA/QC gate for all deliverable types, P5 TEST EVIDENCE AUDIT. WHAT'S NEXT? PROCEED: Step 2.5 audits completed tasks for test evidence. §0.6.4 sub-prompt access updated with WEB-APP-RELEASE-CHECKLIST and TEST-EVIDENCE-TEMPLATE. |
| `templates/SPRINT-BACKLOG-TEMPLATE.md` | EDIT | Verification column now requires "re-executed: [N] passed, [0] failed" for code tasks. |

### Scope Boundary Codification

| File | Action | Description |
|:-----|:-------|:------------|
| `META-PROMPT-DEEPSEEK.md` | EDIT | New §0.5 SCOPE BOUNDARY: 7 DO tasks, 6 DO NOT tasks with owning agents, 3-question boundary test, backlog discipline rule. |
| `agents/PROMPTS-AGENT.md` | EDIT | SCOPE BOUNDARY table: 6 out-of-scope tasks mapped to owning agents. Rule: output NOT saved to prompts/ → NOT your scope. |
| `BACKLOG.md` | EDIT | Header scope warning. All 15 META items complete. Zero remaining. SPINOFF removed — Projects agent scope. |

### Remaining META Items (P5-P9, 1 commit)

| File | Action | Description |
|:-----|:-------|:------------|
| `tools/system_audit.py` | EDIT | P5: Part A3 excludes known GitHub Pages deployment repos. P6: Part G template file content verification (all 19 .md files present + have content). First ALL-PASS audit in system history. |
| `templates/RISK-REGISTER-TEMPLATE.md` | EDIT | P9: Pre-populated CPL risks expanded from 6 to 13 lessons (L1, L3/L6, L7, L13, L14, L15/L17, L16, L18/L40, L19, L20, L21, L38, L39). |
| `BACKLOG.md` | EDIT | P7: Archived 55-project audit documented — 6/6 sampled have 7 mandatory docs (PASS), 0/6 have template-conformant docs (expected). P8: All 14 PM templates confirmed returning empty parameters. |

### System State After All Changes

- **6 new templates** created (PROJECT-STATE, LEARNINGS, CLOSEOUT-CHECKLIST, QA-QC-TESTING-PROTOCOL, TEST-EVIDENCE, WEB-APP-RELEASE-CHECKLIST)
- **3 existing templates** updated (DEFINITION-OF-DONE, SPRINT-BACKLOG, RISK-REGISTER)
- **16/16 PM templates wired** across DEFAULT + QWAV (Part F PASS)
- **Phase gates P0-P5** include QA/QC testing requirements
- **WHAT'S NEXT? PROCEED** Step 2.5 audits test evidence
- **System audit:** ALL 7 PARTS PASS (A-G) — first time in system history
- **ARCHITECTURE.md Layer 5:** 23 template rows (6 functional + 17 PM)
- **BACKLOG.md:** Zero remaining items (all 15 META complete)

---

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

