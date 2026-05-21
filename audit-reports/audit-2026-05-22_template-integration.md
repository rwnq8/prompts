# TEMPLATE INTEGRATION AUDIT — 2026-05-22

> **Question:** Are new projects initiated with Projects Agent / DEFAULT system prompt making full use of latest project management templates (custom prompts)?

## Executive Summary

**Answer: NO.** The project management templates exist and are registered but are **dead code** — they are never invoked by any agent workflow. New projects are initiated with manually-scaffolded documentation that does not use the 11 available project management templates. The templates are listed in README.md and accessible via `fill_prompt_template` but are **not wired** into DEFAULT.md, QWAV-DEFAULT.md, ARCHITECTURE.md, or PROJECTS-AGENT.md.

**Severity: MAJOR** — The system has the _intent_ (18 templates, defined DoD, PMBOK/Agile phase gates) but lacks the _wiring_. Every new project misses out on structured chartering, sprint tracking, risk registration, retrospectives, and consistent DoD enforcement that the templates were designed to provide.

---

## SCOPE AND LIMITATIONS

**Verified (from within `G:\My Drive\prompts\`):**
- All 18 prompt templates and their content
- DEFAULT.md (Projects agent system prompt) — full content scan
- QWAV-DEFAULT.md (QWAV agent system prompt) — full content scan
- ARCHITECTURE.md (system taxonomy) — Layer 5 template listing
- PROJECTS-AGENT.md, PROMPTS-AGENT.md, QWAV-AGENT.md — full content
- tools/system_audit.py — check coverage
- Git history — all commits referencing project management templates
- README.md — template inventory

**Not Verified (sandbox constraint — `G:\My Drive\prompts\` only):**
- Actual project files in `G:\My Drive\projects\` or `G:\My Drive\Archive\`
- Whether recent projects _happen_ to have template-conformant documentation by coincidence
- Whether project files in Archive match template structure

---

## FINDINGS

### F1: Project Management Templates Exist (18 Total)

**Status: PRESENT, REGISTERED, FUNCTIONAL**

| Template | File | fill_prompt_template Test |
|:---------|:-----|:--------------------------|
| ADR-TEMPLATE | `templates/ADR-TEMPLATE.md` | Produces correct ADR structure |
| CHANGELOG-TEMPLATE | `templates/CHANGELOG-TEMPLATE.md` | Produces keepachangelog.com format |
| CONTRIBUTING-TEMPLATE | `templates/CONTRIBUTING-TEMPLATE.md` | Produces CONTRIBUTING.md |
| DEFINITION-OF-DONE-TEMPLATE | `templates/DEFINITION-OF-DONE-TEMPLATE.md` | Produces CODE/DOC/PUBLICATION/ANALYSIS checklists |
| HANDOFF-TEMPLATE | `templates/HANDOFF-TEMPLATE.md` | Produces handoff document |
| PRODUCT-BACKLOG-TEMPLATE | `templates/PRODUCT-BACKLOG-TEMPLATE.md` | Produces P0-P3 prioritized backlog |
| PROJECT-CHARTER-TEMPLATE | `templates/PROJECT-CHARTER-TEMPLATE.md` | Produces charter with scope/success/constraints |
| README-TEMPLATE | `templates/README-TEMPLATE.md` | Produces README with deps/architecture/usage |
| RETROSPECTIVE-TEMPLATE | `templates/RETROSPECTIVE-TEMPLATE.md` | Produces start/stop/continue + action items |
| RISK-REGISTER-TEMPLATE | `templates/RISK-REGISTER-TEMPLATE.md` | Produces risk register with CPL pre-populated risks |
| SPRINT-BACKLOG-TEMPLATE | `templates/SPRINT-BACKLOG-TEMPLATE.md` | Produces sprint tracking with DoD references |

**Plus 7 functional templates** (EMAIL-AGENT, SOCIAL-ORCHESTRATOR, 4 scholar pipeline, image-gen-banner) — these ARE wired and used.

**All 18 templates pass `fill_prompt_template` invocation.** The templates themselves are correct and complete.

---

### F2: DEFAULT.md Never Calls Project Management Templates

**Status: CONFIRMED GAP — Zero references**

A full text search of DEFAULT.md (127,759 chars) for `fill_prompt_template` found only:

| Line | Reference | Template |
|:-----|:----------|:---------|
| 90 | `fill_prompt_template("EMAIL-AGENT TEMPLATE v1.2", {...})` | EMAIL-AGENT |
| 91 | `fill_prompt_template("SOCIAL-ORCHESTRATOR TEMPLATE v1.0", {...})` | SOCIAL-ORCHESTRATOR |
| 496 | Subagent description (informational) | — |
| 1427 | Close-out → social orchestration | SOCIAL-ORCHESTRATOR |
| 1455 | Email drafting protocol | EMAIL-AGENT |
| 1465 | Social media protocol | SOCIAL-ORCHESTRATOR |

**Zero references to ANY project management template** (PROJECT-CHARTER, SPRINT-BACKLOG, DEFINITION-OF-DONE, PRODUCT-BACKLOG, RISK-REGISTER, RETROSPECTIVE, HANDOFF, README, CHANGELOG, ADR, CONTRIBUTING).

Instead, §0.7 instructs the agent to **manually scaffold** 7 documentation files:
```
1. Verify ALL 7 files exist in the project directory. If any are missing, create them.
2. Read PROJECT STATE.md → understand current status
3. Read SPRINT.md → identify the active task
4. Read LEARNINGS.md → avoid repeating past mistakes
5. Read CHANGELOG.md (last entry) → know what just changed
```

The agent is told to "create them" — without using templates. This means every project gets ad-hoc manual documentation.

---

### F3: QWAV-DEFAULT.md Also Excludes Them

**Status: CONFIRMED GAP**

QWAV-DEFAULT.md (the QWAV Strategy Program Manager responsible for project initiation) contains the same pattern:

- References `fill_prompt_template` for EMAIL-AGENT and SOCIAL-ORCHESTRATOR only
- §0.9 says: "Initiate new projects: Create project directory under `G:\My Drive\projects\`, scaffold all 7 mandatory docs (§0.7), write initial SPRINT.md with prioritized tasks, create handoff documents for the Projects agent"
- No instruction to use PROJECT-CHARTER-TEMPLATE, SPRINT-BACKLOG-TEMPLATE, DEFINITION-OF-DONE-TEMPLATE, or HANDOFF-TEMPLATE

The QWAV agent creates project documentation **from scratch.**

---

### F4: ARCHITECTURE.md Layer 5 Is Incomplete

**Status: CONFIRMED GAP**

ARCHITECTURE.md §1 (Layer 5: Prompt Templates) documents only:

| Template | Parameters | Called From | Produces |
|:---------|:-----------|:------------|:---------|
| SOCIAL-ORCHESTRATOR TEMPLATE v1.0 | publicationTitle, etc. | Projects agent | Social media post |
| EMAIL-AGENT TEMPLATE v1.2 | recipient, subject, etc. | Projects agent | Email draft command |
| Research Planning Agent — Step 1 | — | Research pipeline | Project setup plan |
| Research Writing Agent — Step 2 | — | Research pipeline | Research draft |
| Research Review Agent — Step 3 | — | Research pipeline | Quality review |
| Research Publication Agent — Step 4 | — | Research pipeline | Final publication |

**The 11 project management templates are absent from the architecture.** This means anyone reading ARCHITECTURE.md to understand the system would not know these templates exist.

---

### F5: PROJECTS-AGENT.md Excludes Project Management Templates

**Status: CONFIRMED GAP**

PROJECTS-AGENT.md §3 (Tools) lists `fill_prompt_template` with purpose: "Invoke prompt templates (email, social, scholar)"

"scholar" appears to refer to the 4-stage research pipeline templates. Project management templates are not mentioned.

---

### F6: system_audit.py Has No Template Integration Check

**Status: CONFIRMED GAP**

The system health audit (`tools/system_audit.py`) checks:
- PART A: Git contamination ✓
- PART B: Prompt consistency (subagent refs, slot IDs) ✓
- PART C: CPL lesson count ✓
- PART D: Archive integrity ✓
- PART E: Cross-file version consistency ✓

**No check for whether project management templates are referenced in DEFAULT.md or QWAV-DEFAULT.md.** The audit would pass even if all 11 templates were deleted.

---

### F7: Template History Shows Fragility

**Status: CONFIRMED PATTERN**

Git history reveals a deletion-restoration cycle:

```
c06a005 CREATE FILE: templates/{10 templates} — "Recreate 10 template files deleted in cleanup"
d6eaf7b EDIT FILE: templates/{11 templates} — "Restore ORIGINAL template content from prompts.json registry.
         Previous recreations were fabricated from memory and completely different from originals."
```

The templates were:
1. Originally created (unknown commit)
2. Deleted during a cleanup
3. Recreated from memory (incorrectly — fabricated content)
4. Restored from `prompts.json` backup (correct originals)

**Root cause:** With zero usage, nobody noticed the templates were missing or incorrect. If agents were actually calling `fill_prompt_template("PROJECT-CHARTER-TEMPLATE", ...)`, the deletion would have caused immediate failures.

---

### F8: §0.7 Required Files vs. Template Coverage — Partial Overlap

**Status: PARTIAL GAP**

DEFAULT.md §0.7 requires 7 files. Template coverage:

| Required File | Template Available | Template Name | Overlap |
|:-------------|:-------------------|:--------------|:--------|
| README.md | YES | README-TEMPLATE | Template exists, not used |
| PROJECT STATE.md | NO | — | No template; HANDOFF-TEMPLATE is closest |
| SPRINT.md | PARTIAL | SPRINT-BACKLOG-TEMPLATE | Template exists (different filename convention) |
| CHANGELOG.md | YES | CHANGELOG-TEMPLATE | Template exists, not used |
| BACKLOG.md | YES | PRODUCT-BACKLOG-TEMPLATE | Template exists, not used |
| LEARNINGS.md | NO | — | No template |
| DECISIONS.md | YES | ADR-TEMPLATE | Template exists (different granularity — ADR vs decisions log) |

Additional templates with no required-file counterpart:
- PROJECT-CHARTER-TEMPLATE → no required "CHARTER.md"
- DEFINITION-OF-DONE-TEMPLATE → no required "DEFINITION-OF-DONE.md"
- RISK-REGISTER-TEMPLATE → no required "RISK-REGISTER.md"
- RETROSPECTIVE-TEMPLATE → no required retrospective file
- CONTRIBUTING-TEMPLATE → no required "CONTRIBUTING.md"
- HANDOFF-TEMPLATE → related to PROJECT STATE.md but separate

**This shows two layers of misalignment:**
1. Some required files have templates (but templates aren't used)
2. Some templates exist for files that aren't required (orphan templates)

---

## IMPACT ASSESSMENT

### What Actually Happens When a New Project Starts

1. QWAV agent receives instruction to create a project
2. QWAV-DEFAULT.md §0.9 says: "scaffold all 7 mandatory docs (§0.7), write initial SPRINT.md"
3. Agent manually creates 7 files — no template invocation
4. Projects agent picks up the handoff, reads manually-created files
5. Throughout the project, documentation is maintained manually per §0.7 procedures
6. No charter is filed (PROJECT-CHARTER-TEMPLATE unused)
7. No risk register is maintained (RISK-REGISTER-TEMPLATE unused)
8. No formal DoD checklist is applied per task (DEFINITION-OF-DONE-TEMPLATE unused)
9. No structured retrospective is filed per sprint (RETROSPECTIVE-TEMPLATE unused)
10. CLOSE-OUT procedure in §12 references a "CLOSEOUT-CHECKLIST.md" but no template exists

### What SHOULD Happen

1. QWAV agent creates project directory
2. Calls `fill_prompt_template("PROJECT-CHARTER-TEMPLATE", {...})` → writes CHARTER.md
3. Calls `fill_prompt_template("DEFINITION-OF-DONE-TEMPLATE", {...})` → writes DEFINITION-OF-DONE.md
4. Calls `fill_prompt_template("RISK-REGISTER-TEMPLATE", {...})` → writes RISK-REGISTER.md
5. Calls `fill_prompt_template("SPRINT-BACKLOG-TEMPLATE", {...})` → writes SPRINT.md
6. Calls `fill_prompt_template("PRODUCT-BACKLOG-TEMPLATE", {...})` → writes BACKLOG.md
7. Calls `fill_prompt_template("README-TEMPLATE", {...})` → writes README.md
8. Writes PROJECT STATE.md, LEARNINGS.md, DECISIONS.md from templates or defined formats
9. Throughout project: tasks verified against DEFINITION-OF-DONE.md criteria
10. Sprint boundaries: RETROSPECTIVE-TEMPLATE invoked, RISK-REGISTER reviewed
11. Close-out: all templates produce consistent, auditable documentation

---

## RECOMMENDATIONS

### Priority 0 (BLOCKING — Fix Immediately)

**R1: Wire templates into DEFAULT.md §0.7 Startup Procedure**

Replace the manual "create them" instruction with explicit `fill_prompt_template` calls for each of the 7 required files that have templates. Add CHANGELOG-TEMPLATE invocation to the session close procedure.

**R2: Wire templates into QWAV-DEFAULT.md §0.9 Project Initiation**

Replace "scaffold all 7 mandatory docs" with a structured initiation sequence that invokes PROJECT-CHARTER, DEFINITION-OF-DONE, RISK-REGISTER, SPRINT-BACKLOG, PRODUCT-BACKLOG, and README templates. Add HANDOFF-TEMPLATE invocation for the handoff to Projects agent.

### Priority 1 (HIGH — Fix This Sprint)

**R3: Update ARCHITECTURE.md Layer 5**

Add all 11 project management templates to the template table with their parameters, calling agents, and produced outputs.

**R4: Update PROJECTS-AGENT.md Tool Description**

Change `fill_prompt_template` purpose from "email, social, scholar" to "email, social, scholar, project management (charter, sprint, backlog, DoD, risk register, retrospective, handoff, ADR, README, CHANGELOG, CONTRIBUTING)".

**R5: Add template integration check to system_audit.py**

Add PART F: TEMPLATE INTEGRATION CHECK — verify that DEFAULT.md references all registered project management templates via `fill_prompt_template` calls.

### Priority 2 (MEDIUM — Address Within 3 Sprints)

**R6: Align required files with template coverage**

Either:
- Add templates for PROJECT STATE.md, LEARNINGS.md, DECISIONS.md
- Or define standardized formats for files without templates

**R7: Add Close-Out Checklist template**

DEFAULT.md §12 references `CLOSEOUT-CHECKLIST.md` but no template exists. Create one and wire it into the close-out procedure.

**R8: Retrofit existing projects**

Audit recent archived projects and retrofit template-conformant documentation where valuable. Apply CPL L21 (backlog drift) — ensure documentation structure is consistent across projects.

### Priority 3 (LOW — Backlog)

**R9: Template parameter refinement**

Some templates return empty parameters from `get_prompt_template_parameters` (all project management templates). Consider whether parameters would improve template utility (e.g., project name, start date as formal parameters rather than inline placeholders).

**R10: Pre-populated CPL risks in RISK-REGISTER-TEMPLATE**

Verify that the CPL pre-populated risks (L7, L3/L6, L18/L40, L14, L39, L19) are current and complete against all 35 CPL lessons.

---

## VERIFICATION

### Test: Can project management templates be invoked?

```python
# All 11 templates return correct structure from fill_prompt_template
# Tested: PROJECT-CHARTER, DEFINITION-OF-DONE, SPRINT-BACKLOG, etc.
# Result: ALL PASS — templates are functional
```

### Test: Do DEFAULT.md and QWAV-DEFAULT.md reference them?

```python
# Search for fill_prompt_template + project management template names
# DEFAULT.md: 0 results for any PM template
# QWAV-DEFAULT.md: 0 results for any PM template
# Result: CONFIRMED GAP — templates exist but are not called
```

### Test: Does ARCHITECTURE.md document them?

```python
# Layer 5 template table: 6 entries (EMAIL, SOCIAL, 4 scholar)
# Project management templates: 0 entries
# Result: CONFIRMED GAP — 11 templates undocumented in architecture
```

---

## SYSTEM HEALTH CHECK CONTEXT

The most recent system health audit (2026-05-22 01:27) shows:

| Check | Status |
|:------|:-------|
| PART A: Git contamination | FAIL (2 pre-existing `.git` dirs in projects tree) |
| PART B: Prompt consistency | PASS |
| PART C: CPL lessons (35) | PASS |
| PART D: Archive integrity (647 release docs) | PASS |
| PART E: Cross-file version consistency | PASS |

**This template integration gap is NOT detected by the current system_audit.py.** The health check would show all PASS even though 11/18 templates are dead code.

---

## CONCLUSION

**The project management template system is a ghost town.** 11 well-designed templates sit in the `templates/` directory, properly registered and functionally correct, but with zero integration into any agent workflow. New projects are initiated and managed with manual, ad-hoc documentation despite a complete, tested template infrastructure being available.

The templates were designed for exactly the workflow the system attempts — PMBOK/Agile hybrid with phase gates, sprint tracking, risk management, retrospectives, and structured close-out. But the bridge between the templates and the agents that should use them was never built.

**The fix is straightforward:** wire `fill_prompt_template` calls into the project initiation (§0.7), sprint management (§12.5), and close-out (§12) procedures in both DEFAULT.md and QWAV-DEFAULT.md. The templates are ready. The procedures are defined. Only the invocation is missing.

---

*Audit performed 2026-05-22 from within `G:\My Drive\prompts\` sandbox. Archive/project directory contents not directly verified due to sandbox constraints. Template functionality verified via `fill_prompt_template` and `get_prompt_template_parameters` calls.*
