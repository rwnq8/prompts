---
template: PROJECT-INITIATION
version: "1.0"
---

# Project Initiation Gate — [IDEA NAME]

> **Purpose:** Moscow classification + size gate BEFORE GitHub repo creation. Per CPL L43 (not every idea needs a repo) and CPL L47 (documentation must not outweigh the deliverable).
> **When to use:** Before ANY `gh repo create` or `git init` for a new project. If this gate says BLOCK or BACKLOG-ONLY, do NOT create a GitHub repo or local directory.
> **⚠️ GITHUB-NATIVE v2.0:** All project management is GitHub-native from step zero (QWAV-DEFAULT.md §0.9.1 v3.0). Do NOT create SPRINT.md, BACKLOG.md, CHANGELOG.md, LEARNINGS.md, DECISIONS.md, or PROJECT STATE.md — these files are PERMANENTLY DEPRECATED (DEFAULT.md §0.6.8).

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
| **🔴 M — MUST HAVE** | Program fails without it. Core deliverable of active sprint. | PROCEED → GitHub Foundation (QWAV §0.9.1 Phase A) → Charter (GitHub Issue) |
| **🟡 S — SHOULD HAVE** | Important. Program can succeed temporarily without it, but gap is significant. | PROCEED → GitHub Foundation (QWAV §0.9.1 Phase A) → Charter (GitHub Issue) |
| **🟢 C — COULD HAVE** | Nice to have. Adds value, not essential. Would be nice if resources permit. | BACKLOG ONLY — create GitHub Issue (label: `backlog`) in qnfo/program repo, do NOT create project repo |
| **⚪ W — WON'T HAVE** | Not now. Maybe never. Interesting idea but no current program alignment. | BLOCK — record in GitHub Discussions only, do NOT create repo, directory, or Issue |

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

**GitHub-Native Artifacts (NO LOCAL PM FILES):**

| Artifact | Location | Command |
|:---------|:---------|:--------|
| Project State | GitHub Issue (label: `project-state`) | `gh issue create --repo qnfo/<name> --label "project-state"` |
| Task Tracking | GitHub Issues + Project board | `gh issue create` + `gh project item-create` |
| Sprint Board | GitHub Project (kanban) | `gh project create --owner qnfo` |
| Charter | GitHub Issue (label: `charter`) | `gh issue create --repo qnfo/<name> --label "charter"` |
| Definition of Done | GitHub Issue (label: `dod`) | `gh issue create --repo qnfo/<name> --label "dod"` |
| Risk Register | GitHub Issue per risk (label: `risk`) | `gh issue create --repo qnfo/<name> --label "risk"` |
| Changelog | GitHub Releases | `gh release create` |
| Learnings | GitHub Wiki | `OWNER/REPO.wiki.git` |
| Decisions | GitHub Discussions | `gh api graphql` for discussions |

| If LARGE | If SMALL |
|:---------|:---------|
| Full GitHub suite: Issues, Project board, Wiki, Discussions, Releases | Core GitHub: Issues, Project board, Releases |
| GitHub Issue labels: `project-state`, `charter`, `dod`, `risk`, `handoff`, `task`, `bug`, `blocked` | GitHub Issue labels: `project-state`, `task`, `dod`, `handoff` |
| + GitHub Discussions for architectural decisions | + GitHub Issues for decisions (use `decision` label) |

**⚠️ PERMANENTLY DEPRECATED — DO NOT CREATE:** SPRINT.md, BACKLOG.md, CHANGELOG.md, LEARNINGS.md, DECISIONS.md, PROJECT STATE.md, PROJECT-INITIATION.md (in project repo), CHARTER.md (in project repo), DEFINITION-OF-DONE.md (in project repo), RISK-REGISTER.md (in project repo). All replaced by GitHub-native equivalents above.

---

## 4. ROUTING DECISION

Based on the gates above:

- [ ] **PROCEED** — M/S classification. Run QWAV Project Initiation Protocol §0.9.1: Phase A (GitHub Foundation G0-G5) → Phase B (Local Scaffolding L1-L7). All project management lives in GitHub.
- [ ] **BACKLOG ONLY** — C classification. Create GitHub Issue (label: `backlog`) in qnfo/program repo. Do NOT create project repo or local directory.
- [ ] **BLOCK** — W classification. Record in GitHub Discussions only. Do NOT create repo, directory, or Issue.

---

## 5. IF PROCEED — Pre-Flight Checklist

Before running QWAV §0.9.1 Phase A (GitHub Foundation):

- [ ] Moscow classification documented above
- [ ] Size gate documented above
- [ ] GitHub-native artifact set selected (FULL or CORE)
- [ ] Human sign-off obtained (for M/S projects affecting shared resources)
- [ ] Prior work checked via §0.1.4 Discovery (Archive search, CPL lessons, releases)
- [ ] `gh auth status` confirmed with `repo, workflow, read:org, gist` scopes

---

## 6. SIGN-OFF

- [ ] Moscow classification reviewed — not every idea needs a repo
- [ ] If M/S: proceed to `gh repo create qnfo/<name>` (QWAV §0.9.1 Phase A)
- [ ] If C: GitHub Issue (label: `backlog`) created in qnfo/program
- [ ] If W: idea captured in GitHub Discussions, no repo/Issue/directory created

---
*Generated from PROJECT-INITIATION-TEMPLATE.md v2.0 — GitHub-Native*
