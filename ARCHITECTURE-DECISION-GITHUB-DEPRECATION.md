# Architecture Decision: GitHub Deprecated for Non-Git Functions — Cloudflare-Native Migration

> **ADR-001** | **Date:** 2026-05-27 | **Author:** System Prompt Generator v4.6 + User Directive
> **Status:** ADOPTED — In Progress | **Supersedes:** DEFAULT.md §0.6.8 File Deprecation Map (GitHub-native)

---

## 1. Decision

**GitHub is deprecated for ALL non-git functions wherever Cloudflare can provide equivalent functionality.**

> **GitHub = source control ONLY (git push/pull/merge).** All project management, artifact storage, task tracking, publication hosting, CI/CD, and operational state is Cloudflare-native.

### Trigger Events

1. **QNFO Organization Flagged by GitHub** (QNFO/QWAV#62): The QNFO organization on GitHub is flagged, rendering `gh issue list`/`gh project`/`gh release` unreliable for QNFO repos. This proves GitHub is not a dependable platform for anything beyond git hosting.

2. **Cloudflare Infrastructure Maturity:** The Cloudflare platform (Pages, R2, Workers, D1, Vectorize) now covers all functions previously delegated to GitHub:
   - Pages → replaces GitHub Pages (✅ operational as of 2026-05-27)
   - R2 → replaces GitHub Releases for artifact storage (✅ operational)
   - Workers (Cron) → replaces GitHub Actions (✅ operational — `github-sync` Worker)
   - D1 → replaces GitHub Issues/Projects for structured state (planned P3)

3. **Single-Platform Risk:** GitHub controls git hosting, issue tracking, project management, release storage, wiki, discussions, CI/CD, and static hosting. If GitHub flags an org or account, ALL functions fail simultaneously. Decoupling into git-only on GitHub + everything else on Cloudflare eliminates this single point of failure.

---

## 2. Scope — What Is and Is NOT Deprecated

### DEPRECATED (moving to Cloudflare)

| GitHub Feature | Cloudflare Replacement | Status |
|:--------------|:----------------------|:-------|
| **Issues** | R2 `qnfo/audit/issues/` — JSON-based issue tracking via Workers API | Planned (P3) |
| **Projects (Kanban)** | Cloudflare Pages app backed by D1 or R2 state | Planned (P3) |
| **Releases** | **R2 `qnfo/releases/`** — artifact storage | ✅ OPERATIONAL |
| **Wiki** | Cloudflare Pages static site (per-project) | Trivial (not yet implemented) |
| **Discussions** | Deferred — not critical path | Deferred |
| **Pages** | **Cloudflare Pages** — `wrangler pages deploy` | ✅ OPERATIONAL |
| **Actions / CI** | **Workers Cron Triggers** — scheduled jobs | ✅ OPERATIONAL |

### RETAINED (Cloudflare cannot replace)

| GitHub Feature | Why Retained |
|:--------------|:-------------|
| **Git hosting** (push/pull/merge/branch/clone) | No Cloudflare equivalent for git protocol |
| **`gh auth`** | Required for git authentication |
| **Issue/PR URLs in commit messages** | Existing references remain valid; no migration needed |

---

## 3. Complete File Inventory — Every File That Must Be Updated

### 3.1 ALREADY UPDATED (This Session)

| File | Change | Commit |
|:-----|:-------|:-------|
| `scholar/STAGE-5-HOST.md` §13 | GitHub-Native PM → Cloudflare-Native Operations (§13) | `9c06e97` (on main due to CPL L19) |
| `scholar/STAGE-5-HOST.md` §0.5 | New 5-stage pipeline | `20f55fb` |
| `scholar/STAGE-4-PUBLISH.md` | Step 4 of 5 numbering + handoff note | `b6b8fc8` |
| `scholar/RESEARCH-PROTOCOL.md` | 1-4 → 1-5 stage reference | `b6b8fc8` |

### 3.2 NEEDS UPDATING — Core Prompts

| File | GitHub References to Remove/Replace | Priority |
|:-----|:-----------------------------------|:---------|
| **`DEFAULT.md`** | §0.6.8 File Deprecation Map (GitHub Issues/Projects/Releases/Wiki/Discussions as replacements), §13 GitHub-Native Project Management section, `gh issue`/`gh release`/`gh project` CLI commands throughout, "GitHub-Native Model (wiki)" reference in Essential Reading | **HIGH** |
| **`QWAV-DEFAULT.md`** | QWAV Program Board (GitHub Projects), `gh issue`/`gh release`/`gh project` commands, GitHub-native workflow references, QNFO org repo references (gh CLI operations on flagged org) | **HIGH** |
| **This prompt generator** | §0.5 Backlog Discipline (GitHub Issues with `meta` label), §5 template §13 GitHub-Native PM, §5 File Deprecation Map, Quick Reference table (GitHub-native PM in DO column) | **HIGH** |

### 3.3 NEEDS UPDATING — STAGE Prompts (1-4)

| File | GitHub References | Priority |
|:-----|:------------------|:---------|
| **`scholar/STAGE-1-SETUP.md`** | `GitHub Releases (via gh release)` in FileSystem Access (§0), "Step 1 of 4" → "Step 1 of 5" | **HIGH** |
| **`scholar/STAGE-2-DRAFT.md`** | `GitHub Releases (via gh release)` in FileSystem Access, "Step 2 of 4" → "Step 2 of 5" | **HIGH** |
| **`scholar/STAGE-3-REVIEW.md`** | `GitHub Releases (via gh release)` in FileSystem Access, "Step 3 of 4" → "Step 3 of 5" | **HIGH** |
| **`scholar/STAGE-4-PUBLISH.md`** | `GitHub Releases (via gh release)` references (Phase 5 User Approval Gate mentions), `gh release create` operations | **HIGH** (partial — already updated step numbering) |

### 3.4 NEEDS UPDATING — Templates

| File | GitHub References | Priority |
|:-----|:------------------|:---------|
| **`templates/CLOUDFLARE-DEPLOYMENT.md`** | May reference GitHub as source-of-truth for content | MEDIUM |
| **`templates/ZENODO-PUBLISH.md`** | May reference GitHub for artifact storage | MEDIUM |
| **`templates/PROJECT-INITIATION.md`** | Likely references GitHub Issues/Projects for project creation | MEDIUM |
| **`templates/DEFINITION-OF-DONE.md`** | May reference GitHub-native PM completion criteria | MEDIUM |
| **`templates/HANDOFF.md`** | May reference GitHub Issues for session handoff | MEDIUM |
| **`templates/PROJECT-CHARTER.md`** | May reference GitHub for project tracking | MEDIUM |
| **`templates/CLOSEOUT-CHECKLIST.md`** | May reference GitHub Issues for task tracking | MEDIUM |

### 3.5 NEEDS UPDATING — Skills

| File | GitHub References | Priority |
|:-----|:------------------|:---------|
| **`skills/cloudflare-deployer/SKILL.md`** | Already Cloudflare-native ✅ | NONE |
| **`skills/closeout-manager/SKILL.md`** | May reference `gh` CLI for closeout operations | MEDIUM |

### 3.6 DEPRECATED — Do NOT Update (Already Migrating to Cloudflare-Native)

| File | Why Skip |
|:-----|:--------|
| **`BACKLOG-ROADMAP.md`** | PM file already deprecated per new File Deprecation Map. Content should be migrated to R2 `qnfo/audit/backlog/` |
| **Any file named `PROJECT STATE.md`, `SPRINT.md`, `BACKLOG.md`, `CHANGELOG.md`, `LEARNINGS.md`, `DECISIONS.md`** | Already deprecated per File Deprecation Map |

---

## 4. Cloudflare-Native Infrastructure — Current State

### 4.1 Operational (Now)

```
Account ID: edb167b78c9fb901ea5bca3ce58ccc4b (quniverse)
Zone: 331e4363fd05e8e4fc123ea7d2775411 (qwav.tech)

R2 qnfo/
├── audit/
│   ├── conversations/     ← Conversation/session exports
│   ├── github/            ← GitHub issue mirrors (github-sync Worker)
│   ├── decisions/
│   │   └── DECISION-LOG.md ← Architecture decisions (populated 2026-05-27)
│   ├── state/             ← Project state (replaces PROJECT STATE.md)
│   │   └── <project>.json
│   └── backlog/           ← Backlog (replaces BACKLOG.md)
│       └── <project>.json
├── releases/              ← Artifact storage (replaces GitHub Releases)
│   └── CHANGELOG.json
├── deployments/           ← STAGE-5 deployment records
│   └── <project>-<date>.json
└── publications/          ← STAGE-5 publication PDFs
    └── <slug>/paper.pdf

Workers:
├── github-sync (daily cron 06:00 UTC) ← Mirrors GitHub Issues → R2
└── [future: issue-tracker API]        ← CRUD for R2-based issues

Pages:
├── deep.qwav.tech
├── primer.qwav.tech
├── archive.qnfo.org
└── [future: research.qwav.tech — STAGE-5 deployments]
```

### 4.2 Planned (Phase 3 — Needs Implementation)

| Capability | Cloudflare Implementation | Dependencies |
|:-----------|:--------------------------|:-------------|
| Issue Tracking (CRUD) | D1 database + Workers REST API | D1 schema design, Worker endpoint |
| Kanban Board | Cloudflare Pages app with D1 backend | Issue tracking API, UI design |
| Semantic Search | Vectorize `qwav-research` index (768d) populated with STAGE-5 `llms-full.txt` content | STAGE-5 deployed publications, embedding Worker |
| Wiki | Per-project Cloudflare Pages sites | Pages project creation automation |

---

## 5. Phased Migration Plan

### Phase 1 — IMMEDIATE (This Session / Next Session)
- [x] STAGE-5-HOST.md §13 updated to Cloudflare-Native ✅
- [x] STAGE-4-PUBLISH.md step numbering updated (4→5) ✅
- [x] RESEARCH-PROTOCOL.md updated (1-4→1-5) ✅
- [x] This ADR document created ✅
- [ ] Upload this ADR to R2 `qnfo/audit/decisions/ADR-001-GITHUB-DEPRECATION.md`
- [ ] Upload BACKLOG-ROADMAP.md content to R2 `qnfo/audit/backlog/`
- [ ] Merge both feature branches to main: `feature/agent-subagent-refactoring` (previous session) + `feature/github-deprecation-cloudflare-native` (this session)

### Phase 2 — CORE PROMPTS (Next Session)
- [ ] DEFAULT.md: Replace §0.6.8 File Deprecation Map, §13 GitHub-Native PM, `gh` CLI references
- [ ] QWAV-DEFAULT.md: Replace GitHub-native workflow with Cloudflare-native operations
- [ ] This prompt generator: Replace §5 template §13, §0.5 Backlog Discipline, File Deprecation Map

### Phase 3 — STAGE PROMPTS & TEMPLATES
- [ ] STAGE-1-SETUP.md: Remove `GitHub Releases (via gh release)`, update step numbering
- [ ] STAGE-2-DRAFT.md: Remove `GitHub Releases (via gh release)`, update step numbering
- [ ] STAGE-3-REVIEW.md: Remove `GitHub Releases (via gh release)`, update step numbering
- [ ] STAGE-4-PUBLISH.md: Replace `gh release create` with R2 upload, update GitHub Releases references
- [ ] All templates: Audit for `gh issue`/`gh release`/`gh project` references

### Phase 4 — INFRASTRUCTURE (Planned P3)
- [ ] Issue Tracking Worker (D1 + REST API)
- [ ] Kanban Board (Cloudflare Pages app)
- [ ] Vectorize population from STAGE-5 publications
- [ ] Per-project Wiki (Cloudflare Pages automation)

---

## 6. CPL L19 Incident — Branch Discipline Violation

**Date:** 2026-05-27 | **Session:** System Prompt Generator v4.6

### What Happened

1. Created `feature/research-publication-hosting` branch, committed STAGE-5-HOST.md (`20f55fb`) and pipeline updates (`b6b8fc8`)
2. A parallel session merged the feature branch to `main` via commit `58ac521` (RESEARCH-LAUNCH template + DEFAULT.md update)
3. Branch was deleted as part of merge
4. Subsequent commit (`9c06e97` — Cloudflare-Native Operations update) was made directly to `main` because the pre-commit branch check was not performed

### Root Cause

**CPL L19 guard was not executed:** The instruction "Verify branch name hasn't been renamed by a parallel process before every commit" was skipped between the parallel merge and the subsequent commit. Without the guard, the agent did not detect that it was operating on `main` instead of a feature branch.

### Impact

- One commit (`9c06e97`) on `main` instead of a feature branch
- Content is correct and consistent with the architectural directive
- No data loss or corruption — only branch discipline violation

### Resolution

- New feature branch `feature/github-deprecation-cloudflare-native` created immediately after detection
- This ADR documents the incident for future reference
- **Prevention:** Enforce pre-commit branch check in ALL generated prompts (already present in Git Protocol §12 — enforcement must be runtime, not just documented)

### Lesson

The CPL L19 guard ("Compare the current branch name against the branch name you recorded at session start") is effective only when **executed**. Documentation is not enforcement. All generated prompts should include an explicit pre-commit checkpoint that verifies `git branch --show-current` returns a `feature/*` branch — and ABORTS if not.

---

## 7. Design Principles — Cloudflare-Native Architecture

1. **GitHub is a git remote. Nothing more.** If an operation is not `git push`, `git pull`, `git merge`, or `git log`, it does not touch GitHub.

2. **All operational state lives in R2.** Deployments, issues, releases, decisions, backlogs — all JSON files in `qnfo/`. Workers provide structured CRUD access.

3. **Static content lives in Cloudflare Pages.** Publications, wikis, documentation sites — deployed via `wrangler pages deploy`.

4. **Scheduled work runs on Workers Cron.** Replaces GitHub Actions for automated jobs (sync, audit, indexing).

5. **Secrets live in Workers secrets.** `wrangler secret put` — never in environment variables or config files.

6. **No single-platform dependency.** If GitHub goes down, git operations pause but ALL project management, artifact access, and publication hosting continues on Cloudflare.

---

## 8. Related Documents

| Document | Path/Location |
|:---------|:-------------|
| QNFO Content License v1.1 | `G:\My Drive\prompts\LICENSE` + `https://github.com/QNFO/license` |
| STAGE-5-HOST.md | `G:\My Drive\prompts\scholar\STAGE-5-HOST.md` |
| Cloudflare Deployer Skill | `G:\My Drive\prompts\skills\cloudflare-deployer\SKILL.md` |
| Cloudflare Deployment Template | `G:\My Drive\prompts\templates\CLOUDFLARE-DEPLOYMENT.md` |
| DEFAULT.md | `G:\My Drive\prompts\DEFAULT.md` (needs updating — Phase 2) |
| QWAV-DEFAULT.md | `G:\My Drive\prompts\QWAV-DEFAULT.md` (needs updating — Phase 2) |
| BACKLOG-ROADMAP.md | `G:\My Drive\prompts\BACKLOG-ROADMAP.md` (deprecated — migrate to R2) |
| Cross-Project Learnings | https://github.com/rwnq8/prompts/wiki/Cross-Project-Learnings (L19 reference) |
| QNFO/QWAV#62 | QNFO Organization Flagged (canonical source via local files since GitHub API blocked) |

---

*ADR-001 v1.0 — Adopted 2026-05-27. GitHub = source control ONLY. Everything else = Cloudflare-native.*
