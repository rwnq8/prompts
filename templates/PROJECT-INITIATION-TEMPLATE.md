---
template: PROJECT-INITIATION
version: "1.0"
---

# Project Initiation Gate — [IDEA NAME]

> **Purpose:** Moscow classification + size gate BEFORE project directory creation. Per CPL L43 (not every idea needs a repo) and CPL L47 (documentation must not outweigh the deliverable).
> **When to use:** Before ANY `scaffold_template` or `git init` for a new project. If this gate says BLOCK or BACKLOG-ONLY, do NOT create a project directory.

---

## 1. IDEA SUMMARY

**What:** [One-sentence description]
**Why:** [Problem it solves or question it answers]
**Source:** [Strategy document, research finding, cross-project insight, user request]
**Program:** [QWAV | Ultrametricity | Tools | Research]

---

## 2. MOSCOW CLASSIFICATION (CPL L43) — SELECT ONE

Answer this question: **"What happens to the program if this project does NOT exist?"**

| Classification | Meaning | Action |
|:---------------|:--------|:-------|
| **🔴 M — MUST HAVE** | Program fails without it. Core deliverable of active sprint. | PROCEED → Charter → Scaffold |
| **🟡 S — SHOULD HAVE** | Important. Program can succeed temporarily without it, but gap is significant. | PROCEED → Charter → Scaffold |
| **🟢 C — COULD HAVE** | Nice to have. Adds value, not essential. Would be nice if resources permit. | BACKLOG ONLY — add to BACKLOG.md, do NOT create directory |
| **⚪ W — WON'T HAVE** | Not now. Maybe never. Interesting idea but no current program alignment. | BLOCK — record in strategy notes only, do NOT create directory or backlog item |

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

**Documentation Set:**

| If LARGE | If SMALL |
|:---------|:---------|
| Full Tier 1 (7 files): README, PROJECT STATE, SPRINT, CHANGELOG, BACKLOG, LEARNINGS, DECISIONS | Reduced set (4 files): README, PROJECT STATE, SPRINT, DEFINITION-OF-DONE |
| + Phase docs: DEFINITION-OF-DONE, CHARTER, RISK-REGISTER | + Optional: CHARTER (if stakeholder-facing) |
| + Situational: CONTRIBUTING, RETROSPECTIVE, HANDOFF, etc. | DO NOT create: BACKLOG, CHANGELOG, LEARNINGS, DECISIONS, CONTRIBUTING, RISK-REGISTER (bloat for small projects) |

---

## 4. ROUTING DECISION

Based on the gates above:

- [ ] **PROCEED** — M/S classification, proceed to PROJECT-CHARTER-TEMPLATE, then scaffold with [FULL / REDUCED] documentation set
- [ ] **BACKLOG ONLY** — C classification, add to BACKLOG.md with `[COULD HAVE]` tag, do NOT create project directory
- [ ] **BLOCK** — W classification, record in strategy notes only, do NOT create project directory or backlog item

---

## 5. IF PROCEED — Pre-Flight Checklist

Before running `scaffold_template`:

- [ ] Moscow classification documented above
- [ ] Size gate documented above
- [ ] Documentation set selected (FULL or REDUCED)
- [ ] Human sign-off obtained (for M/S projects affecting shared resources)
- [ ] Prior work checked via §0.1.4 Discovery (Archive search, CPL lessons, releases)

---

## 6. SIGN-OFF

- [ ] Moscow classification reviewed — not every idea needs a repo
- [ ] If M/S: project scope is clear enough for a charter
- [ ] If C: backlog entry is sufficient for now
- [ ] If W: idea is captured in strategy notes, no project directory created

---
*Generated from PROJECT-INITIATION-TEMPLATE.md v1.0*
