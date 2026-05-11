# PROMPTS — PROJECT STATE

**For LLM Agents:** Read this first. Complete handoff. No prior context needed.

**Last updated:** 2026-05-11 | **Session:** Kaizen Framework Deployment | **Changelog:** CHANGELOG.md

---

## 1. PROJECT IDENTITY

**Prompts** is the system prompt engineering repository for the LLM Agent DevOps ecosystem. It produces, audits, and versions the system prompts that govern all other agents operating in `G:\My Drive\projects\`. This includes the general-purpose research agent (DEFAULT.md), the prompt compiler (META-PROMPT-DEEPSEEK.md), the social media orchestrator (SOCIAL-ORCHESTRATOR-v4.0.md), the workspace isolation enforcer, and the project orchestration framework.

**Outputs are prompts, not end-user content.** The prompts/ agent produces the instructions that other agents follow.

---

## 2. CURRENT STATUS SNAPSHOT

| Dimension | Status |
|:----------|:-------|
| **Active prompts** | 6 (DEFAULT, META-PROMPT-DEEPSEEK, SOCIAL-ORCHESTRATOR, PROJECT-ISOLATION-ENFORCER, PROJECT-ORCHESTRATION-FRAMEWORK, image-gen-banner-prompt) |
| **Active sprint** | Sprint 1: Kaizen Documentation Infrastructure |
| **Git branch** | feature/social-v4-fix |
| **Repo status** | Clean working tree, 4 prior commits on this branch |
| **Cross-project status** | CROSS-PROJECT-LEARNINGS.md not yet created at _shared/ level |

---

## 3. KEY CONSTRAINTS

| Constraint | Rationale |
|:-----------|:----------|
| **Write only to `G:\My Drive\prompts\`** | This is the only writable directory for the prompts agent |
| **All prompts must include Rules 1-6 verbatim** | Core operating rules are non-negotiable |
| **All prompts must follow 9-section template** | Structural consistency across all generated prompts |
| **Git discipline mandatory** | Feature branches only, never commit to main/master |
| **No web search in any prompt** | Agents have no web access; all search must be external coordination |

---

## 4. WHAT'S BEEN TRIED

### 4.1 Subagent Architecture (2026-05-11)

| Item | Outcome | Date |
|:-----|:--------|:-----|
| 20-invocation cross-slot audit | Confirmed subagents inherit full system prompt (including git discipline) | 2026-05-11 |
| Subagent git pre-flight overhead | Subagents waste ~65% chance of lacking write/exec tools. Read-only subagents burn budget on irrelevant git checks. | 2026-05-11 |
| SELF-CLONE slot configured | Working for text synthesis with git-skip directive | 2026-05-11 |
| Removed unreliable subagent slots | PROJECTS slot (~40% file I/O) and ARCHIVE slot (0% file I/O) deleted | 2026-05-11 |

### 4.2 Prompt Evolution

| Prompt | Version | Status | Date |
|:-------|:--------|:-------|:-----|
| DEFAULT.md | v3.1 (inferred) | Active — general-purpose research agent | Ongoing |
| META-PROMPT-DEEPSEEK.md | v4.1 | Active — prompt compiler/auditor | Ongoing |
| SOCIAL-ORCHESTRATOR-v4.0.md | v4.0 | Active — social media orchestration | 2026-05-10 |
| image-gen-banner-prompt.md | v1.0 | Active — banner generation | 2026-05-10 |
| PROJECT-ISOLATION-ENFORCER-v1.0.md | v1.0 | Active — workspace isolation | 2026-05-11 |
| PROJECT-ORCHESTRATION-FRAMEWORK-v1.0.md | v1.0 | Active — kaizen project management | 2026-05-11 |
| SUBAGENT_DESCRIPTIONS.md | v3.1 | Active — agent/subagent configuration | 2026-05-11 |

---

## 5. CURRENT STATE

- **Active sprint:** Sprint 1: Kaizen Documentation Infrastructure
- **Completed tasks:** 1 (Orchestration framework drafted)
- **Open tasks:** 4 (CHANGELOG, SPRINT, BACKLOG, LEARNINGS creation for prompts/)
- **Blockers:** None — only constraint is write access limited to `G:\My Drive\prompts\`

---

## 6. IMMEDIATE NEXT STEPS (for next agent)

1. Complete creation of CHANGELOG.md, SPRINT.md, BACKLOG.md, LEARNINGS.md for prompts/ directory
2. Create `G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md` (requires human to execute — write access is outside prompts/)
3. Seed LEARNINGS.md with key lessons from this session (cross-project git contamination, subagent git overhead, isolation enforcement)
4. Audit DEFAULT.md for compliance with new orchestration framework standards
5. Plan Sprint 2: Cross-project kaizen propagation mechanism

---

## 7. LEARNINGS REGISTER (summary)

| L# | Category | Lesson | Status |
|:---|:---------|:-------|:-------|
| L1 | GIT | Shared parent repo causes cross-project contamination; per-project repos required | DOCUMENTED |
| L2 | ISOLATION | Without path confinement, agents freely access sibling project directories | DOCUMENTED |
| L3 | METHODOLOGY | Subagents inherit full system prompt (including git discipline) — read-only subagents need git-skip directive | DOCUMENTED |
| L4 | FILE-MGMT | Standardized documentation (SPRINT, CHANGELOG, LEARNINGS) enables agent handoff across sessions | DOCUMENTED |
| L5 | METHODOLOGY | Kaizen requires machine-readable lesson format for cross-project filtering | IN PROGRESS |
