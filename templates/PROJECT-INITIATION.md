---
template: PROJECT-INITIATION
version: "1.0"
date: 2026-06-03
---

# Project Initiation Gate — [IDEA NAME]

> **Purpose:** Moscow classification + size gate BEFORE project creation. Per CPL L43 (not every idea needs a project) and CPL L47 (documentation must not outweigh the deliverable).
> **When to use:** Before ANY `git init` or directory creation for a new project. If this gate says BLOCK or BACKLOG-ONLY, do NOT create a local directory or R2 state.
> **⚠️ CLOUDFLARE-NATIVE v3.10:** All project management is Cloudflare-native from step zero (Project Initiation Protocol (§0.9.1)). Do NOT create SPRINT.md, BACKLOG.md, CHANGELOG.md, LEARNINGS.md, DECISIONS.md, or PROJECT STATE.md — these files are PERMANENTLY DEPRECATED (see File Deprecation Map — Cloudflare R2 replaces all PM files). Project state lives in R2 (`qnfo/audit/state/`), tasks in R2 (`qnfo/audit/backlog/`), decisions in R2 (`qnfo/audit/decisions/DECISION-LOG.md`). Git is version control ONLY.
> 
> **⚠️ ERROR HANDLING:** All `wrangler` commands in this template inherit the retry strategy from Project Initiation Protocol (§0.9.1) "Failure Handling & Retry Strategy." Authentication failures are blocking — escalate, do not retry.

---

## 1. IDEA SUMMARY

**What:** [One-sentence description]
**Why:** [Problem it solves or question it answers]
**Source:** [Strategy document, research finding, cross-project insight, user request]
**Program:** [QWAV | Ultrametricity | Tools | Research]
**Proposed Repo:** `qnfo/[repo-name]`

---

## 2. MOSCOW CLASSIFICATION (CPL L43) — SELECT ONE

Answer this question: **"What happens to the program if this project does NOT exist?"**

| Classification | Meaning | Action |
|:---------------|:--------|:-------|
| **🔴 M — MUST HAVE** | Program fails without it. Core deliverable of active sprint. | PROCEED → Cloudflare Foundation (QWAV §0.9.1 Phase A) → R2 state + backlog |
| **🟡 S — SHOULD HAVE** | Important. Program can succeed temporarily without it, but gap is significant. | PROCEED → Cloudflare Foundation (QWAV §0.9.1 Phase A) → R2 state + backlog |
| **🟢 C — COULD HAVE** | Nice to have. Adds value, not essential. Would be nice if resources permit. | BACKLOG ONLY — create R2 backlog object (`qnfo/audit/backlog/<name>.json`), do NOT create project directory |
| **⚪ W — WON'T HAVE** | Not now. Maybe never. Interesting idea but no current program alignment. | BLOCK — record in decision log only, do NOT create directory or R2 state |

**Classification:** [M / S / C / W]

**Justification:** [1-3 sentences explaining WHY this classification. Reference program goals, current sprint priorities, resource constraints.]

---

## 3. PROJECT SIZE GATE (CPL L47) — FOR M/S PROJECTS ONLY

Skip this section if classified C or W.

| Factor | Threshold | This Project | Gate |
|:-------|:----------|:-------------|:-----|
| Expected sessions | >5 = Large, ≤5 = Small | [Estimate] | [Large / Small] |
| Deliverable size | >20 KB = Large, ≤20 KB = Small | [Estimate] | [Large / Small] |
| Expected commits | >10 = Large, ≤10 = Small | [Estimate] | [Large / Small] |

**Size Classification:** [LARGE / SMALL]

**Cloudflare-Native Artifacts (NO LOCAL PM FILES):**

| Artifact | Location | Command |
|:---------|:---------|:--------|
| Project State | R2 object (`qnfo/audit/state/<name>.json`) | `npx wrangler r2 object put qnfo/audit/state/<name>.json --file=<local> --remote` |
| Task Tracking | R2 object (`qnfo/audit/backlog/<name>.json`) | `npx wrangler r2 object put qnfo/audit/backlog/<name>.json --file=<local> --remote` |
| Discovery Index | R2 object (`qnfo/discovery/index.json`) | `npx wrangler r2 object get qnfo/discovery/index.json --remote` → edit → `put` |
| Charter | Local PROJECT-CHARTER.md in project directory | `write` tool |
| Definition of Done | Section in R2 state file or PROJECT-CHARTER.md | Documented in charter |
| Decision Log | R2 object (`qnfo/audit/decisions/DECISION-LOG.md`) | Append to local copy → upload to R2 |
| Code Archive | R2 object (`qnfo/code/<name>.bundle`) | `git bundle create` → `npx wrangler r2 object put` |
| Releases | R2 object (`qnfo/releases/`) + Cloudflare Pages | `npx wrangler r2 object put` → `npx wrangler pages deploy` |

| If LARGE | If SMALL |
|:---------|:---------|
| Full R2 suite: state, backlog, code archive, releases, decision log entries | Core R2: state, backlog, decision log |
| R2 state labels: `active`, `delegated`, `blocked`, `complete`, `archived` | R2 state labels: `active`, `complete`, `archived` |

**⚠️ PERMANENTLY DEPRECATED — DO NOT CREATE:** SPRINT.md, BACKLOG.md, CHANGELOG.md, LEARNINGS.md, DECISIONS.md, PROJECT STATE.md. All replaced by Cloudflare-native R2 equivalents above.

---

## 4. ROUTING DECISION

Based on the gates above:

- [ ] **PROCEED** — M/S classification. Run QWAV Project Initiation Protocol §0.9.1: Phase A (Cloudflare Foundation C0-C5) → Phase B (Local Scaffolding L1-L7). All project management lives in R2.
- [ ] **BACKLOG ONLY** — C classification. Create R2 backlog object (`qnfo/audit/backlog/<name>.json`). Do NOT create project directory.
- [ ] **BLOCK** — W classification. Record in decision log only. Do NOT create directory or R2 state.

---

## 5. IF PROCEED — Pre-Flight Checklist

Before running QWAV §0.9.1 Phase A (Cloudflare Foundation):

- [ ] Moscow classification documented above
- [ ] Size gate documented above
- [ ] Cloudflare-native artifact set selected (FULL or CORE)
- [ ] Human sign-off obtained (for M/S projects affecting shared resources)
- [ ] Prior work checked via §0.8 Discovery (Discovery Index, R2 decision log, CPL lessons)
- [ ] `wrangler whoami` confirmed — Cloudflare authenticated

---

## 6. SIGN-OFF

- [ ] Moscow classification reviewed — not every idea needs a project
- [ ] If M/S: proceed to Cloudflare Foundation (QWAV §0.9.1 Phase A C0-C5) — create R2 state + backlog
- [ ] If C: R2 backlog object (`qnfo/audit/backlog/<name>.json`) created
- [ ] If W: idea captured in decision log only, no directory/R2 state created

---
*Generated from PROJECT-INITIATION-TEMPLATE.md v3.0 — Cloudflare-Native*
