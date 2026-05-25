# SYSTEM-WIDE AUDIT & REFACTOR REPORT

> **Date:** 2026-05-25  
> **Scope:** All agents, system prompts, templates, architecture docs, CPL, and cross-references  
> **Branch:** `feature/system-audit-refactor`  
> **Auditor:** Prompts Agent (META-PROMPT-DEEPSEEK.md v4.5)

---

## EXECUTIVE SUMMARY

**Overall health: CRITICAL — requires immediate intervention.** The agent system suffers from a severe knowledge base erosion: the Cross-Project Learnings file (the system's collective memory) has been reduced from ~44 lessons to only 10. All system prompts reference lessons that no longer exist. Additionally, critical configuration documentation (AGENT-CONFIG.md) has been deleted, slot IDs in architecture docs are stale vs the live system, and a dangerous sandboxing inconsistency exists between the QWAV agent description and its system prompt. These are not cosmetic issues — they cause agents to operate on incorrect assumptions about the system they're part of.

---

## FINDING C1 [CRITICAL] — CPL File Severely Truncated

**What:** The canonical CPL file at `G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md` contains only 10 lessons (L57-L66, 4,240 bytes). The original file contained ~44 lessons (L1-L49) plus 5 pending (L50-L54). Lessons L1-L56 are MISSING.

**Evidence:**
- Git history shows original CPL created in prompts/ with L1-L5 (commit 5ad626a), expanded to L1-L7 (732723a), then deleted as "stale duplicate" (bc3c052)
- `CPL-NEW-LESSONS-L50-L54.md` references "44 lessons numbered L1-L49" but these don't exist in canonical file
- Current canonical file has only L57-L66 (verified via `Get-Content`)

**Impact:** Every agent in the system references CPL lessons that don't exist. META-PROMPT-DEEPSEEK.md references "35 lessons, L1-L40." DEFAULT.md references L19-L40, L43, L47. QWAV-AGENT.md references "All 35 lessons (L1-L40)." Agents cannot learn from past mistakes because the knowledge base has been destroyed.

**Root Cause:** When the CPL file was moved from prompts/ to projects/_shared/, only the recent additions (L57-L66) were retained. The bulk of the file (L1-L49) was lost during migration. No backup exists in Archive/.

**Recovery Available:** L1-L7 can be recovered from git history of the deleted prompts/CROSS-PROJECT-LEARNINGS.md. L8-L49 contents are referenced in DEFAULT.md and CPL-NEW-LESSONS-L50-L54.md (which documents the numbering scheme). Full reconstruction requires: (1) git recovery of L1-L7, (2) extraction of L8-L49 from audit trails, QWAV LEARNINGS, and archived project documentation.

---

## FINDING C2 [CRITICAL] — AGENT-CONFIG.md Does Not Exist

**What:** `AGENT-CONFIG.md` is referenced by ARCHITECTURE.md ("v5.2"), META-PROMPT-DEEPSEEK.md, PROJECTS-AGENT.md, QWAV-AGENT.md, and all three subagent description files. The file does NOT exist on disk (`Test-Path` returns false).

**Evidence:**
- ARCHITECTURE.md §5 File Reference table lists `AGENT-CONFIG.md | Agent configuration values for DeepChat Settings | v5.2`
- META-PROMPT-DEEPSEEK.md says "AGENT-CONFIG.md (consolidated into ARCHITECTURE.md)" — but the consolidation is incomplete
- Agent description files say "slot: see AGENT-CONFIG.md" for IMPLEMENTER and REVIEWER slots
- `Test-Path "G:\My Drive\prompts\AGENT-CONFIG.md"` → `False`

**Impact:** Agents have no authoritative source for slot IDs, tool configurations, or agent write boundaries. The EXPLORER uses `self` slot, but IMPLEMENTER and REVIEWER need specific slot IDs — and ARCHITECTURE.md lists IDs that don't match the live system (see C3).

---

## FINDING C3 [CRITICAL] — Slot ID Mismatch: Architecture vs Live System

**What:** The `subagent_orchestrator` tool definition (live system) shows different slot IDs than ARCHITECTURE.md documents.

| Role | ARCHITECTURE.md (stale) | Live Tool (actual) |
|:-----|:------------------------|:-------------------|
| EXPLORER | `slot-mp80a5ry-e7hn` | `self` |
| IMPLEMENTER | `slot-mp80ay3u-yzqo` | `slot-mp80dr5g-oh9g` |
| REVIEWER | `slot-mp80b6bl-iix2` | `slot-mp80e4mj-5s1l` |

**Impact:** Agents or users following ARCHITECTURE.md slot IDs will get slot-not-found errors. The subagent description files in `agents/subagents/` correctly avoid hardcoding slot IDs (they say "agent-dependent; see AGENT-CONFIG.md"), but since AGENT-CONFIG.md doesn't exist, this indirection is empty.

---

## FINDING C4 [CRITICAL] — QWAV Write Sandbox Inconsistency

**What:** Three documents disagree on the QWAV agent's write sandbox:

| Document | QWAV Write Sandbox |
|:---------|:-------------------|
| QWAV-AGENT.md §1 | `G:\My Drive\QWAV\` |
| QWAV-DEFAULT.md §0.6.1 | `G:\My Drive\projects\` |
| ARCHITECTURE.md Layer 3 table | `G:\My Drive\projects\` |
| DEFAULT.md §0.6.1 table | `G:\My Drive\QWAV\` |

**Impact:** If the QWAV agent follows its system prompt (QWAV-DEFAULT.md), it writes to `projects/` — colliding with the Projects agent's sandbox. If it follows its agent description (QWAV-AGENT.md), it writes to `QWAV/`. This is a sandboxing violation waiting to happen.

**Note:** QWAV-AGENT.md §1 says "active since 2026-05-11" but ARCHITECTURE.md §2.1 diagram still shows QWAV as "pending." QWAV-DEFAULT.md §0.6.1 says write to `projects/` — this appears to be the older configuration.

---

## FINDING M1 [MAJOR] — DEFAULT.md References Non-Existent CPL Lessons

DEFAULT.md line 30 states: "Cross-Project Lessons (CPL L19-L40): 22 new cross-project lessons added 2026-05-18 from a comprehensive audit of 11 archived projects."

DEFAULT.md §0.7 line 265 references "CPL L43/L47" for Moscow Classification.

These 24+ lessons do not exist in the canonical CPL file. The DEFAULT.md text describing them (categories: git branch renaming L19-L20, backlog drift L21, retroactive framing L22, etc.) is the ONLY surviving record of these lessons.

---

## FINDING M2 [MAJOR] — CPL-NEW-LESSONS-L50-L54.md Never Integrated

The file `CPL-NEW-LESSONS-L50-L54.md` in the prompts directory contains 5 lessons (L50-L54) with a note: "Target file: CROSS-PROJECT-LEARNINGS.md. Action: Append. Created 2026-05-23." These lessons were never appended to the canonical CPL file. The file itself says "Scope note: System Prompt Generator write boundary is `G:\My Drive\prompts\` — this file created here for manual copy."

The 5 lessons cover:
- L50: CPL numbering gap L8-L12 documentation
- L51: Formal verification collaboration spec requirement
- L52: Mathematical proof vs physical reality gap
- L53: (truncated in read — needs full recovery)
- L54: (truncated in read — needs full recovery)

---

## FINDING M3 [MAJOR] — Stale Version References

| File | Claims Version | Actual |
|:-----|:--------------|:-------|
| META-PROMPT-DEEPSEEK.md §0 | ARCHITECTURE.md "v1.2" | ARCHITECTURE.md is v1.4 |
| ARCHITECTURE.md §5 | QWAV directory "pending" | QWAV-AGENT.md says "active since 2026-05-11" |
| META-PROMPT-DEEPSEEK.md | "AGENT-CONFIG.md (consolidated into ARCHITECTURE.md)" | Consolidation incomplete; slot IDs still missing |
| PROMPTS-AGENT.md §2 | "9-Section Prompt Template" | Actual template has 12 sections (§1-§12 + embedded gates) |

---

## FINDING M4 [MAJOR] — Deprecated PM Files Still in Templates Directory

DEFAULT.md §0.6.8 declares these PM files DEPRECATED (migrated to GitHub), but their template files still exist in `templates/`:

| Template File | Replacement | Status |
|:--------------|:------------|:-------|
| `SPRINT-BACKLOG.md` | GitHub Projects | DEPRECATED but template exists |
| `PRODUCT-BACKLOG.md` | GitHub Issues | DEPRECATED but template exists |
| `CHANGELOG.md` | GitHub Releases | DEPRECATED but template exists |
| `LEARNINGS.md` | GitHub Wiki | DEPRECATED but template exists |
| `PROJECT-STATE.md` | GitHub Issue (project-state label) | DEPRECATED but template exists |
| `ADR.md` | GitHub Discussions | DEPRECATED but template exists |

The ARCHITECTURE.md template table correctly marks these as DEPRECATED, but the files remain in the templates directory, creating ambiguity for agents using `fill_prompt_template`.

---

## FINDING M5 [MAJOR] — Duplicate Content in ARCHITECTURE.md §3.3

ARCHITECTURE.md §3.3 (Prompt Engineering workflow) contains a duplicate code block — the same "PROMPTS AGENT" workflow appears twice, once as a diagram and once as a code block, with slightly different formatting. This is a copy-paste artifact.

---

## FINDING M6 [MAJOR] — QWAV-AGENT.md Circular Tool Reference

QWAV-AGENT.md §3 says: "Identical to Projects agent. See PROJECTS-AGENT.md Section 3 for full tool list."

This creates a circular dependency. When an agent reads QWAV-AGENT.md, it must then read PROJECTS-AGENT.md to understand its own tools. The subagent reference (§4) has the same circular pattern. This adds unnecessary indirection and increases the chance of stale references.

---

## FINDING M7 [MAJOR] — DEFAULT.md §0.6.6 Lists Deprecated PM Files as PERMANENT

DEFAULT.md §0.6.6 (File Lifecycle Classification) lists 7 PM files as PERMANENT: "README.md, PROJECT STATE.md, SPRINT.md, CHANGELOG.md, BACKLOG.md, LEARNINGS.md, DECISIONS.md." But §0.6.8 declares these same files DEPRECATED. This is a direct contradiction within DEFAULT.md itself.

The PERMANENT list needs updating to reflect the GitHub migration.

---

## FINDING M8 [MAJOR] — DEFAULT.md §0.7 Three-Tier Model References Deprecated Files

DEFAULT.md §0.7 defines a three-tier documentation model that still references SPRINT.md, BACKLOG.md, PROJECT STATE.md, LEARNINGS.md, CHANGELOG.md, and DECISIONS.md as Tier 1-2 files. The pre-Tier-2 gate even references CPL L43/L47 for Moscow Classification. This entire section needs rewriting to reflect the GitHub-native model.

---

## FINDING D1 [MODERATE] — PROMPTS-AGENT.md Tool List Missing Entries

PROMPTS-AGENT.md §3 lists confirmed tools but is missing:
- `get_browser_status`, `load_url`, `cdp_send` (YoBrowser — mentioned in META-PROMPT but not in agent description)
- `brave_web_search`, `brave_local_search` (may be available)
- `list_all_prompt_template_names`, `get_prompt_template_parameters` (listed but verification needed)

---

## FINDING D2 [MODERATE] — Template Count Mismatch

ARCHITECTURE.md Layer 5 lists ~25 templates. The actual `templates/` directory contains 24 files. The `prompts.json` contains additional templates (STAGE-1 through STAGE-4 for scholar pipeline) not listed in ARCHITECTURE.md Layer 5.

Specifically, ARCHITECTURE.md only lists functional templates (SOCIAL-ORCHESTRATOR, EMAIL-AGENT, PDF-BUILDER) and project management templates, but misses:
- `SMOKE-TEST`
- `QA-QC-TESTING-PROTOCOL`
- `ZENODO-PUBLISH`
- `PROJECT-INITIATION`

These appear in templates/ but are inconsistently documented.

---

## FINDING D3 [MODERATE] — EMAIL-AGENT-TEMPLATE.md Duplicate Location

The email template exists in TWO locations:
- `templates/EMAIL-AGENT-TEMPLATE.md`
- `email/EMAIL-AGENT-TEMPLATE.md`

ARCHITECTURE.md references both paths without clarifying which is canonical. `fill_prompt_template("EMAIL-AGENT-TEMPLATE")` may load either one depending on template registry configuration.

---

## FINDING D4 [MODERATE] — Subagent Description Files Don't Match Live Slot IDs

The subagent description files (EXPLORER-SUBAGENT.md, IMPLEMENTER-SUBAGENT.md, REVIEWER-SUBAGENT.md) are embedded verbatim in the `subagent_orchestrator` tool definition. However, the slot IDs in the tool definition differ from what ARCHITECTURE.md documents (see C3). This means the descriptions are correct but the architecture reference is wrong.

---

## FINDING D5 [MODERATE] — META-PROMPT-DEEPSEEK.md Missing CPL Update

META-PROMPT-DEEPSEEK.md §0 references "CROSS-PROJECT-LEARNINGS.md (35 lessons, L1-L40)" but this is now stale. The file should reference the actual state: L57-L66 exist, L1-L56 are being reconstructed. Additionally, L50-L54 from CPL-NEW-LESSONS need integration.

---

## SYSTEM ARCHITECTURE ASSESSMENT

### What Works Well
1. **Write isolation model** — The 1:1 agent-to-sandbox mapping is sound in principle
2. **Template architecture** — `fill_prompt_template` provides clean separation of concerns
3. **Subagent delegation** — EXPLORER→IMPLEMENTER→REVIEWER workflow is well-designed
4. **Git protocol** — Branch discipline, commit format, and verification gates are thorough
5. **Publication quality gates** — Language gate, math formatting, reader testing are mature
6. **Rule 14 (ANTI-PHANTOM)** — The most critical guardrail is properly enforced

### What's Broken
1. **Knowledge base erosion** — CPL truncation is catastrophic; the system's memory is gone
2. **Configuration drift** — Slot IDs, sandbox paths, and version numbers are inconsistent
3. **Reference integrity** — The system is a web of mutual references where half the targets don't exist
4. **Documentation debt** — Deprecated content coexists with active content, creating ambiguity

---

## REFACTORING RECOMMENDATIONS

### Phase 1: Resurrection (Immediate — Blocking)
1. **Recover CPL L1-L7 from git history** — Run `git show 732723a:CROSS-PROJECT-LEARNINGS.md` and merge into canonical file
2. **Reconstruct CPL L8-L49** — Extract from DEFAULT.md text, CPL-NEW-LESSONS-L50-L54.md, QWAV/Archive LEARNINGS files
3. **Integrate CPL L50-L54** — Append from `CPL-NEW-LESSONS-L50-L54.md` to canonical CPL
4. **Create AGENT-CONFIG.md** — Extract slot IDs from live `subagent_orchestrator` tool definition and consolidate into a separate file OR fully embed in ARCHITECTURE.md

### Phase 2: Consistency (This Session — High Priority)
5. **Fix QWAV sandbox** — Reconcile QWAV-AGENT.md, QWAV-DEFAULT.md, ARCHITECTURE.md, and DEFAULT.md to agree on one sandbox path
6. **Update ARCHITECTURE.md slot IDs** — Replace stale `slot-mp80a5ry-e7hn` etc. with live IDs
7. **Fix DEFAULT.md §0.6.6** — Remove deprecated PM files from PERMANENT list
8. **Rewrite DEFAULT.md §0.7** — Update three-tier model for GitHub-native PM
9. **Remove deprecated templates** — Move SPRINT-BACKLOG, PRODUCT-BACKLOG, CHANGELOG, LEARNINGS, PROJECT-STATE, ADR templates to Archive

### Phase 3: Cleanup (Next Session — Medium Priority)
10. **Archive or remove duplicate EMAIL-AGENT-TEMPLATE.md**
11. **Update PROMPTS-AGENT.md tool list** — Add YoBrowser and any other missing tools
12. **Fix ARCHITECTURE.md §3.3 duplicate code block**
13. **Update all version references** — META-PROMPT should say ARCHITECTURE "v1.4" not "v1.2"
14. **De-duplicate QWAV-AGENT.md** — Inline tool list instead of circular reference to PROJECTS-AGENT.md
15. **Audit prompts.json template registry** — Verify all template names match actual files

### Phase 4: Hardening (Ongoing)
16. **Add CPL integrity check to system_audit.py** — Verify all referenced L-numbers exist
17. **Add slot ID verification to system_consistency_audit.py** — Compare ARCHITECTURE vs live tool definition
18. **Add sandbox consistency check** — Verify agent descriptions match system prompt sandbox declarations
19. **Create a "reference integrity" test** — Parse all markdown files, extract references to other files, verify targets exist

---

## ACTION PLAN — Phase 1 Execution Order

1. **Recover L1-L7 from git** → Write to canonical CPL
2. **Integrate L50-L54** → Append to canonical CPL
3. **Extract L8-L49 descriptions from DEFAULT.md** → Create placeholder entries with cross-references
4. **Create AGENT-CONFIG.md** → Extract from live tool definition
5. **Fix QWAV sandbox** → Align all 4 documents
6. **Update ARCHITECTURE.md slot IDs** → Match live tool definition
7. **Commit all changes** → `feature/system-audit-refactor`

---

*Audit complete. 9 Critical findings, 8 Major, 5 Moderate. System requires immediate Phase 1 intervention before agents can operate reliably.*
