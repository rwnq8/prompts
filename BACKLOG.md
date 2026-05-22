# BACKLOG — Prompts Directory (System Prompt Engineering)

> **Purpose:** Prioritized queue of system prompt improvements, template updates, and cross-cutting QA/QC enhancements. All items here are universal — applicable to ANY project, not tied to specific projects.
> **Last Updated:** 2026-05-22

---

## ✅ COMPLETED — Sprint History

### Sprint 1: Template Integration Wiring (S0-S7)
14 project management templates wired into DEFAULT.md, QWAV-DEFAULT.md, ARCHITECTURE.md, and system_audit.py Part F. Three new templates created (PROJECT-STATE, LEARNINGS, CLOSEOUT-CHECKLIST).

### Sprint 2: QA/QC Process Overhaul (Q1-Q9 / P2-P4, P10-P15)
Universal QA/QC framework baked into the entire project lifecycle. Two new templates created (QA-QC-TESTING-PROTOCOL, TEST-EVIDENCE-TEMPLATE). One existing template updated (WEB-APP-RELEASE-CHECKLIST). Phase gates P0-P5 include testing requirements. WHAT'S NEXT? PROCEED Step 2.5 audits test evidence.

| # | Item | Status |
|:--|:-----|:-------|
| P1 | Merge feature/template-integration-audit to main | ✅ DONE |
| P2 | Add WEB APP DoD section to DEFINITION-OF-DONE-TEMPLATE | ✅ DONE |
| P3 | Create WEB-APP-RELEASE-CHECKLIST template | ✅ DONE |
| P4 | Wire web app templates into agent workflows | ✅ DONE |
| P10 | Create universal QA/QC Testing Protocol template | ✅ DONE |
| P11 | Wire QA/QC gates into DEFAULT.md phase workflow P0-P5 | ✅ DONE |
| P12 | Add test evidence requirement to SPRINT task format | ✅ DONE |
| P13 | Update DEFINITION-OF-DONE with test execution gates | ✅ DONE |
| P14 | Add testing gate to WHAT'S NEXT? PROCEED (Step 2.5) | ✅ DONE |
| P15 | Create TEST-EVIDENCE-TEMPLATE | ✅ DONE |

---

## 🟡 META — Remaining System Prompt Improvements

### P2 — Medium Priority

| # | Item | Description | Effort | Status |
|:--|:-----|:-----------|:-------|:-------|
| P5 | **Update system_audit.py Part A3 — exclude known .git contamination** | Projects deployed to GitHub Pages (e.g., ultrametric-game-of-life, polysynthetic-communication) have .git dirs by design in the projects tree. Audit should exclude these known deployment repos to eliminate false-positive FAIL. | 0.25h | [ ] |
| P6 | **Add template invocation audit to system_audit.py** | Beyond Part F's text-search (is template name present in agent prompts), add a check that actually calls `fill_prompt_template` for each template and verifies non-empty output — confirming templates are not just referenced but functional. | 0.5h | [ ] |
| P7 | **Retrofit archived projects with template-conformant docs** | Per CPL L21 (backlog drift): audit recently archived projects for structural consistency. Retrofit template-conformant documentation (CHARTER.md, DEFINITION-OF-DONE.md, RISK-REGISTER.md) where valuable for cross-project learning. | 2h | [ ] |

### P3 — Nice-to-Have

| # | Item | Description | Effort | Status |
|:--|:-----|:-----------|:-------|:-------|
| P8 | **Template parameter discovery** | Some PM templates return empty parameters from `get_prompt_template_parameters`. Consider whether formal parameters (project name, date) would improve utility vs inline `[PLACEHOLDER]` values being filled manually by agents. | 0.5h | [ ] |
| P9 | **CPL risk audit for RISK-REGISTER-TEMPLATE** | Verify pre-populated CPL risks (L7, L3/L6, L18/L40, L14, L39, L19) are current and complete against all 40 CPL lessons. Some lessons (L26-L28 reader testing, L38 null-byte, L39 subagent truncation) may need to be added as default risks. | 0.5h | [ ] |

---

## 🔴 CROSS-CUTTING — Universal QA/QC Lessons (Baked into System Prompts)

> **These are NOT project-specific backlog items.** They are universal patterns that have been (or will be) implemented in the system prompts to prevent across ALL future projects.

### Pattern 1: Test File Existence ≠ Test Execution

**Lesson:** Agents can write test files to disk without ever executing them. The system must distinguish "wrote test file" from "executed test suite" — check for execution OUTPUT, not file presence.

**Implemented in:** DEFINITION-OF-DONE-TEMPLATE (CODE TEST, ANALYSIS TEST sections require re-execution evidence), WHAT'S NEXT? PROCEED Step 2.5 (audit completed tasks for test evidence), SPRINT-BACKLOG-TEMPLATE (verification column requires "re-executed: [N] passed, [0] failed").

### Pattern 2: Definition of Done Must Cover All Deliverable Types

**Lesson:** A DoD that only covers CODE/DOC/PUBLICATION/ANALYSIS leaves WEB APP deliverables without any quality standard. Every deliverable type the system can produce must have a corresponding DoD section with type-appropriate verification criteria.

**Implemented in:** DEFINITION-OF-DONE-TEMPLATE now has 7 sections: CODE, CODE TEST, DOCUMENT, PUBLICATION, ANALYSIS, ANALYSIS TEST, WEB APP.

### Pattern 3: Phase Gates Must Gate on Testing, Not Just Completion

**Lesson:** "All tasks marked complete" is insufficient if tasks were completed without testing. Each phase gate must verify that testing appropriate to the deliverable type was executed, not just that files exist.

**Implemented in:** DEFAULT.md §12.5 Phase Gates — P0 requires TEST PLAN, P2 requires TEST SUITE EXECUTED, P3 is full QA/QC gate, P5 includes TEST EVIDENCE AUDIT.

### Pattern 4: Every Test Execution Must Produce Evidence

**Lesson:** Test execution is ephemeral — terminal output disappears. Every test run must produce a persisted evidence document that survives the session. "I remember the tests passing" is not evidence.

**Implemented in:** TEST-EVIDENCE-TEMPLATE (standardized evidence format), QA-QC-TESTING-PROTOCOL (mandates evidence capture for all deliverable types).

### Pattern 5: Pre-Deployment Gates Must Be Deliverable-Type-Specific

**Lesson:** A general close-out checklist designed for documents (CLOSEOUT-CHECKLIST) cannot gate a web app deployment (which needs cross-browser verification, asset loading checks, and live URL testing). Each release type needs its own pre-deployment checklist.

**Implemented in:** WEB-APP-RELEASE-CHECKLIST (9-section pre-deployment gate), DEFAULT.md §12.3 Step 1 (web app projects require web-specific checklist in addition to general close-out).

---

## Legend

| Domain | Color | Scope |
|:-------|:------|:------|
| 🟡 META | Yellow | System prompt engineering, templates, agent config (Prompts workspace scope) |
| 🔴 CROSS-CUTTING | Red | Universal QA/QC patterns implemented in system prompts for ALL projects |

---

*Generated from PRODUCT-BACKLOG-TEMPLATE.md v1.0*
