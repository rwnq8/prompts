# AUDIT: "7 Mandatory Documentation Files" vs Actual Template Count (27)

**Date:** 2026-05-22
**Audit Trigger:** User flagged that agent startup says "7 mandatory documentation files" but there are now >7 templates.
**Scope:** All system prompts (DEFAULT.md, QWAV-DEFAULT.md, META-PROMPT-DEEPSEEK.md, ARCHITECTURE.md) and all 27 prompt templates.

---

## 1. EXECUTIVE SUMMARY

The system hardcodes "7 mandatory documentation files" in **27+ places** across 3 system prompts and 2 templates. However, the system now has **27 prompt templates**, with at least **10 additional file-generating templates** that are de facto expected during the project lifecycle.

**The "7" is technically still correct for ALWAYS-present files**, but the framing is misleading and causes agents to miss situational-but-expected documentation.

---

## 2. THE 7 MANDATORY FILES (currently defined in DEFAULT.md Section 0.7)

| # | File | Template |
|:--|:-----|:---------|
| 1 | `README.md` | README-TEMPLATE |
| 2 | `PROJECT STATE.md` | PROJECT-STATE-TEMPLATE |
| 3 | `SPRINT.md` | SPRINT-BACKLOG-TEMPLATE |
| 4 | `CHANGELOG.md` | CHANGELOG-TEMPLATE |
| 5 | `BACKLOG.md` | PRODUCT-BACKLOG-TEMPLATE |
| 6 | `LEARNINGS.md` | LEARNINGS-TEMPLATE |
| 7 | `DECISIONS.md` | ADR-TEMPLATE |

---

## 3. ADDITIONAL FILE-GENERATING TEMPLATES (NOT in the 7)

These templates generate files that are referenced/expected by the system but are NOT counted in "7 mandatory":

| # | Template | Generates | Referenced By | Expected When |
|:--|:---------|:----------|:--------------|:--------------|
| 8 | CLOSEOUT-CHECKLIST-TEMPLATE | `CLOSEOUT-CHECKLIST.md` | DEFAULT.md (5 refs), QA-QC-TESTING-PROTOCOL | **P5 Close-Out — always** |
| 9 | DEFINITION-OF-DONE-TEMPLATE | `DEFINITION-OF-DONE.md` | SPRINT-BACKLOG-TEMPLATE, CONTRIBUTING-TEMPLATE, PROJECT-CHARTER-TEMPLATE | **P0 Initiation — always** |
| 10 | CONTRIBUTING-TEMPLATE | `CONTRIBUTING.md` | DEFAULT.md mentions project-specific additions | **P0 Initiation — recommended** |
| 11 | RISK-REGISTER-TEMPLATE | `RISK-REGISTER.md` | PROJECT-STATE-TEMPLATE, CONTRIBUTING-TEMPLATE, QA-QC-TESTING-PROTOCOL | **P1 Planning — recommended** |
| 12 | PROJECT-CHARTER-TEMPLATE | `PROJECT-CHARTER.md` | None directly (standalone template) | **P0 Initiation — recommended** |
| 13 | QA-QC-TESTING-PROTOCOL | `QA-QC-TESTING-PROTOCOL.md` | DEFAULT.md references testing gates | **P2 Execution — when testing** |
| 14 | TEST-EVIDENCE-TEMPLATE | `test-evidence-*.md` | DEFAULT.md (2 refs), DEFINITION-OF-DONE, QA-QC-TESTING-PROTOCOL | **P2-P5 — when tests run** |
| 15 | WEB-APP-RELEASE-CHECKLIST | `RELEASE-CHECKLIST-*.md` | DEFAULT.md (3 refs), QA-QC-TESTING-PROTOCOL, DEFINITION-OF-DONE | **P4 Publication — web apps** |
| 16 | RETROSPECTIVE-TEMPLATE | `RETROSPECTIVE-*.md` | DEFAULT.md (1 ref), SPRINT-BACKLOG-TEMPLATE | **P3 Review — per sprint** |
| 17 | HANDOFF-TEMPLATE | `HANDOFF-*.md` | None directly (standalone) | **When delegating** |

---

## 4. FULL HARDCODED "7" REFERENCE MAP

### 4.1 DEFAULT.md — 8 locations, ~19 individual references

| Line | Context | Text |
|:-----|:--------|:-----|
| 115 | §0.6 File Lifecycle | `Mandatory documentation: README.md, PROJECT STATE.md, SPRINT.md, CHANGELOG.md, BACKLOG.md, LEARNINGS.md, DECISIONS.md` |
| 153 | §0.7 Startup Procedure Step 1 | `Verify all 7 mandatory documentation files exist.` |
| 225 | Phase C Final Integrity Sweep | `ALL 7 mandatory documentation files audited for stale references` |
| 252 | File Naming Exception | `These 7 files use fixed names and are never versioned` |
| 368 | §0.8.2 Due Diligence Startup | `Verify ALL 7 documentation files exist` |
| 623 | §9.3 Step 0 Verification | `Verify all 7 mandatory documentation files exist` |
| 1428 | §12.2 Close-Out Checklist Item 3 | `ALL 7 MANDATORY DOCS UPDATED` |
| 1448 | §12.2 Close-Out Checklist Item 7 | `all 7 docs exist and are non-empty` |
| 1497 | Phase table P0 | `7 mandatory docs, git repo, SPRINT.md with tasks` |
| 1701 | Agent description footer | `mandatory 7-file documentation standards` |

### 4.2 QWAV-DEFAULT.md — 5 locations, ~7 individual references

| Line | Context |
|:-----|:--------|
| 122 | Startup procedure: `Verify ALL 7 files exist` |
| 160 | File naming: `These 7 files use fixed names` |
| 276 | Due diligence startup: `Verify ALL 7 documentation files` |
| 563 | Session start verification: `Verify all 7 mandatory documentation files` |
| 1178 | Close-out checklist: `ALL 7 MANDATORY DOCS UPDATED` |
| 1198 | Final audit: `all 7 docs exist and are non-empty` |
| 1245 | Phase table: `7 mandatory docs` |

### 4.3 META-PROMPT-DEEPSEEK.md — 1 location

| Line | Context |
|:-----|:--------|
| 9 | CPL L21: `audit all 7 documentation files for stale references` |

### 4.4 Template Content — 2 templates with hardcoded "7"

| Template | References |
|:---------|:-----------|
| CLOSEOUT-CHECKLIST-TEMPLATE | `ALL 7 MANDATORY DOCS UPDATED`, `all 7 docs exist and are non-empty` |
| RISK-REGISTER-TEMPLATE | CPL L21: `7 mandatory docs become stale` |

### 4.5 Other Hardcoded "7" (Different Context — Not Documentation Files)

| Template | Reference |
|:---------|:----------|
| EMAIL-AGENT-TEMPLATE | `7-point checklist` (email pre-send validation) |
| STAGE-1-SETUP | `Identify exactly 7 distinct gaps` (gap analysis categories) |

---

## 5. TEMPLATE ECOSYSTEM (27 total)

### File-Generating Templates (17)

| # | Template | Output File | Mandatory Set? |
|:--|:---------|:------------|:---------------|
| 1 | README-TEMPLATE | `README.md` | Yes (always) |
| 2 | PROJECT-STATE-TEMPLATE | `PROJECT STATE.md` | Yes (always) |
| 3 | SPRINT-BACKLOG-TEMPLATE | `SPRINT.md` | Yes (always) |
| 4 | CHANGELOG-TEMPLATE | `CHANGELOG.md` | Yes (always) |
| 5 | PRODUCT-BACKLOG-TEMPLATE | `BACKLOG.md` | Yes (always) |
| 6 | LEARNINGS-TEMPLATE | `LEARNINGS.md` | Yes (always) |
| 7 | ADR-TEMPLATE | `DECISIONS.md` | Yes (always) |
| 8 | CLOSEOUT-CHECKLIST-TEMPLATE | `CLOSEOUT-CHECKLIST.md` | No (de facto: P5) |
| 9 | DEFINITION-OF-DONE-TEMPLATE | `DEFINITION-OF-DONE.md` | No (de facto: P0) |
| 10 | CONTRIBUTING-TEMPLATE | `CONTRIBUTING.md` | No |
| 11 | RISK-REGISTER-TEMPLATE | `RISK-REGISTER.md` | No |
| 12 | PROJECT-CHARTER-TEMPLATE | `PROJECT-CHARTER.md` | No |
| 13 | QA-QC-TESTING-PROTOCOL | `QA-QC-TESTING-PROTOCOL.md` | No |
| 14 | TEST-EVIDENCE-TEMPLATE | `test-evidence-*.md` | No |
| 15 | WEB-APP-RELEASE-CHECKLIST | `RELEASE-CHECKLIST-*.md` | No |
| 16 | RETROSPECTIVE-TEMPLATE | `RETROSPECTIVE-*.md` | No |
| 17 | HANDOFF-TEMPLATE | `HANDOFF-*.md` | No |

### Non-File Templates (10)

| Template | Purpose |
|:---------|:--------|
| STAGE-1-SETUP | Research planning (4-stage pipeline) |
| STAGE-2-DRAFT | Research drafting (4-stage pipeline) |
| STAGE-3-REVIEW | Research review (4-stage pipeline) |
| STAGE-4-PUBLISH | Research publication (4-stage pipeline) |
| EMAIL-AGENT-TEMPLATE | Email drafting from project context |
| SOCIAL-ORCHESTRATOR-TEMPLATE | Social media content from publications |
| image-gen-banner-prompt | Image generation banner |
| "1. What explicit choices..." | Retrospective question template |
| "A first-principles convergence..." | Document template |
| "Cleanup Actions..." | Cleanup actions template |

---

## 6. IMPACT ASSESSMENT

### 6.1 Current Behavior

When an agent starts a project and reads DEFAULT.md §0.7, it:
1. Creates exactly 7 files (the "mandatory" set)
2. Does NOT create DEFINITION-OF-DONE.md (which SPRINT-BACKLOG-TEMPLATE references)
3. Does NOT create RISK-REGISTER.md (which PROJECT-STATE-TEMPLATE references)
4. Does NOT create CLOSEOUT-CHECKLIST.md until P5 (correct behavior, but the close-out checklist itself says "ALL 7 MANDATORY DOCS")

### 6.2 Cross-Reference Failures

The following templates reference files that are NOT in the "7 mandatory" set:

| Template | References | File NOT in 7 |
|:---------|:-----------|:--------------|
| SPRINT-BACKLOG-TEMPLATE | `DoD Criteria: Ref to DEFINITION-OF-DONE.md` | DEFINITION-OF-DONE.md |
| PROJECT-STATE-TEMPLATE | `Risk ID: R# from RISK-REGISTER.md` | RISK-REGISTER.md |
| CONTRIBUTING-TEMPLATE | `DoD criteria beyond standard ones in DEFINITION-OF-DONE.md` | DEFINITION-OF-DONE.md |
| CONTRIBUTING-TEMPLATE | `Pre-populated risks from RISK-REGISTER-TEMPLATE.md` | RISK-REGISTER.md |
| PROJECT-CHARTER-TEMPLATE | `DoD Reference: DEFINITION-OF-DONE.md` | DEFINITION-OF-DONE.md |

### 6.3 User-Observed Symptom

The user's observed agent behavior (shown in the triggering message):
> "I need to: Create the 7 mandatory documentation files"

The agent only knows about 7 files from DEFAULT.md. It does not know about the full template catalog, leading to:
- Missing DEFINITION-OF-DONE.md (referenced by SPRINT tasks)
- Missing RISK-REGISTER.md (referenced by PROJECT STATE)
- Missing CONTRIBUTING.md (project-specific rules)

---

## 7. PROPOSED FIX

### Option A: Tiered Documentation Model (RECOMMENDED)

Replace the single "7 mandatory" concept with a 3-tier model:

**Tier 1: CORE INITIALIZATION FILES (7 — always created at P0)**
- README.md, PROJECT STATE.md, SPRINT.md, CHANGELOG.md, BACKLOG.md, LEARNINGS.md, DECISIONS.md

**Tier 2: PHASE-GATED FILES (created at specific phases)**
- P0: DEFINITION-OF-DONE.md, PROJECT-CHARTER.md, CONTRIBUTING.md, RISK-REGISTER.md
- P5: CLOSEOUT-CHECKLIST.md

**Tier 3: SITUATIONAL FILES (created when applicable)**
- QA-QC-TESTING-PROTOCOL.md (when testing planned)
- TEST-EVIDENCE-*.md (when tests executed)
- WEB-APP-RELEASE-CHECKLIST (for web app projects)
- RETROSPECTIVE-*.md (per sprint)
- HANDOFF-*.md (when delegating)

### Option B: Just Fix the Language

Change "7 mandatory documentation files" to "7 core initialization files" and add a reference to the full template catalog. This is a minimal fix but doesn't solve the cross-reference problem.

### Option C: Expand the Mandatory Set

Add DEFINITION-OF-DONE.md and RISK-REGISTER.md to the mandatory set (9 files). This fixes the cross-reference failures but may be overkill for simple projects.

---

## 8. FILES REQUIRING UPDATES

If Option A is chosen, the following files need updates:

| File | Changes Needed |
|:-----|:---------------|
| DEFAULT.md §0.7 | Replace "7 mandatory" with tiered model; reference full template catalog |
| DEFAULT.md (all 8 locations) | Change "7 mandatory documentation files" to "7 core initialization files" or tiered reference |
| QWAV-DEFAULT.md (all 5 locations) | Same updates |
| META-PROMPT-DEEPSEEK.md (1 location) | Update CPL L21 reference |
| CLOSEOUT-CHECKLIST-TEMPLATE | Change "ALL 7 MANDATORY DOCS" to "ALL CORE DOCS" + reference additional phase docs |
| RISK-REGISTER-TEMPLATE | Update CPL L21 description |

---

## 9. RESOLUTION (2026-05-22)

**Implemented Option A: Tiered Documentation Model**

### Files Updated

| File | Changes |
|:-----|:--------|
| `DEFAULT.md` | §0.7 rewritten with 3-tier model + full template catalog. All 19 hardcoded "7" references replaced. |
| `QWAV-DEFAULT.md` | All 7 hardcoded "7" references replaced with tiered language. |
| `META-PROMPT-DEEPSEEK.md` | CPL L21: "audit all 7 documentation files" -> "audit ALL documentation files (Tier 1-3)" |
| `projects/_shared/CROSS-PROJECT-LEARNINGS.md` | L21: "update all 7 docs" -> "update all Tier 1-3 docs" |
| `tools/system_consistency_audit.py` | NEW - Proactive audit tool that catches hardcoded count drift |

### New Tiered Model

| Tier | Count | Description | Examples |
|:-----|:------|:-----------|:---------|
| Tier 1: Core Init | 7 | Always created at P0 | README, SPRINT, CHANGELOG |
| Tier 2: Phase-Gated | 5 | Created at specific phases | DEFINITION-OF-DONE (P0), CLOSEOUT-CHECKLIST (P5) |
| Tier 3: Situational | 5 | Created when applicable | WEB-APP-RELEASE-CHECKLIST, TEST-EVIDENCE |
| Non-file templates | 10 | Process/analysis only | STAGE-1 through STAGE-4, EMAIL-AGENT |
| Total | 27 | | |

### Proactive Audit System

`tools/system_consistency_audit.py` checks:
- A. Hardcoded numeric claims vs actual counts
- B. Template count claims accuracy
- C. Cross-references between templates
- D. Template registry completeness
- E. CPL lesson reference staleness

Trigger: `python tools/system_consistency_audit.py` or integrated into `system_audit.py`.

### Template Content Note

Two templates (CLOSEOUT-CHECKLIST-TEMPLATE, RISK-REGISTER-TEMPLATE) still contain "7" in stored content. These are managed by the template system. Generated files will be correct because `fill_prompt_template` returns templates with `[PLACEHOLDER]` markers that agents fill from the updated DEFAULT.md tiered model.
