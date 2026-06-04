---
template: CLOSEOUT-CHECKLIST
version: "5.0"
date: 2026-06-03
---
# SESSION CLOSEOUT OPERATING PROCEDURE — [PROJECT/TOPIC]

> **GATE:** Mandatory before declaring ANY session complete. Verify all items/tasks/phases executed, implemented, complete, and tested/audited. Save, commit, merge, push, and document everything.
>
> **AUTONOMOUS:** Do NOT wait for user to say "TERMINATE." Detect when all tasks are complete and auto-initiate closeout. The agent is responsible for recognizing completion and closing out without user prompting.
>
> **SCOPE:** Universal — applies to ALL session types (project work, prompt engineering, system maintenance, research).
>
> **Cloudflare-Native:** All project management is Cloudflare-native (R2, D1, Workers). Do NOT create or update SPRINT.md, BACKLOG.md, CHANGELOG.md, LEARNINGS.md, DECISIONS.md, or PROJECT STATE.md — these files are PERMANENTLY DEPRECATED (see File Deprecation Map — Cloudflare R2 replaces all PM files).
>
> **ERROR HANDLING:** All `wrangler` commands use standard retry strategy (3x with exponential backoff, 2s/4s/8s). If a wrangler command fails after retries: mark `[!]` with rationale and continue. Do NOT block closeout on a single wrangler command failure — all items are independently verifiable.

**Date:** [YYYY-MM-DD]
**Session Type:** [PROJECT / PROMPT-ENGINEERING / SYSTEM-MAINTENANCE / RESEARCH]
**Branch:** [feature/name]

Every item must be verified and marked `[x]` before the session ends. `[!]` = blocker. `[/]` = not applicable (document why).

---

## PHASE A: GIT STATE VERIFICATION `[CODE-EXECUTED]`

- [ ] **Working tree clean:** `git status --porcelain` returns empty (no uncommitted changes, no untracked files except intentional deliverables)
- [ ] **Correct branch:** `git branch --show-current` returns `main` (or the approved feature branch if merging is pending)
- [ ] **No stale branches:** `git branch` shows only `main` and the current feature branch. Delete all merged/abandoned feature branches.
- [ ] **No uncommitted merges:** `git status` shows no "You have unmerged paths" or rebase-in-progress
- [ ] **All changes committed:** `git log --oneline -5` shows all work committed. No `git stash list` items related to this session.

**Blockers:** Dirty working tree, stale branches, uncommitted merges, missing commits.

---

## PHASE B: FILE EXISTENCE & INTEGRITY VERIFICATION `[CODE-EXECUTED]`

- [ ] **All expected files on disk:** For each deliverable claimed in this session — `Test-Path <file>` returns `True`
- [ ] **File sizes non-zero:** For each deliverable — `(Get-Item <file>).Length -gt 0`
- [ ] **Content verified:** `Get-Content <file> -First 5` confirms file is readable and contains expected content
- [ ] **No stale temp files:** Scan for `_*.py`, `*.tmp`, `__pycache__`, `.pyc` — none should remain unless they are intentional deliverables
- [ ] **No broken references:** All `[EXTERNAL-SOURCE: filename]` and `[CODE-EXECUTED: script.py]` references resolve to existing files

**Blockers:** Missing files, zero-byte files, broken references.

---

## PHASE C: TEMPLATE & REGISTRY INTEGRITY `[CODE-EXECUTED]`

**For prompt engineering sessions (this repo):**
- [ ] **prompts.json rebuilt:** Run `python tools/rebuild_prompts_json.py` — confirms all templates registered, no stale references
- [ ] **New templates registered:** Any new `.md` files in `templates/`, `scholar/`, `email/`, or `agents/` appear in `prompts.json`
- [ ] **prompts.json committed:** `git log -1 -- prompts.json` shows a commit from this session if templates were added/modified
- [ ] **Fill template verification:** `fill_prompt_template` returns valid content for each new/updated template

**For project sessions:**
- [ ] **Fill template integrity:** All templates invoked during the session (`fill_prompt_template`) produced valid output
- [ ] **No stale template content:** Templates used contain the latest version (check against source `.md` files)

**Blockers:** prompts.json not rebuilt after template changes, new templates not registered.

---

## PHASE D: REMOTE SYNC & BRANCH MANAGEMENT `[CODE-EXECUTED]`

- [ ] **Remote sync confirmed:** All local commits are on `origin/main` (or `origin/feature/name` if merge pending)
- [ ] **Verify remote matches local:** `git log origin/main --oneline -1` matches `git log -1 --oneline` (or local HEAD is ahead awaiting merge)
- [ ] **Feature branch merged to main:** `git branch --merged main` includes the feature branch; `git log main..feature/name` returns empty (no unique commits)
- [ ] **Feature branch deleted after merge:** `git branch` shows no local `feature/name` branch; remote deleted with `git push origin --delete feature/name`
- [ ] **No orphan branches:** `git branch -a` shows no feature branches that should have been deleted after merge

**For project sessions:**
- [ ] **Project repo remote matches local:** `git log --oneline origin/main -3` matches local
- [ ] **All project repos pushed:** Every repo modified in this session has been pushed

**Blockers:** Unpushed commits, unmerged PRs, orphan feature branches, remote divergence.

---

## PHASE E: TRACKING & DOCUMENTATION `[CODE-EXECUTED]`

- [ ] **Cloudflare D1 task tracking:** All work tracked via Cloudflare D1 `qnfo-audit` with appropriate tags. Tasks closed or updated with final status in backlog.
- [ ] **Cross-project discovery executed:** Discovery Index re-pulled, ALL open handoffs checked for conflicts with this session's changes
- [ ] **Downstream impacts documented:** Any project that depends on resources modified this session has been noted in R2 audit trail
- [ ] **Discovery Index updated:** Any new/removed/modified resources registered, handoff statuses updated, project states current
- [ ] **No orphan records:** All handoffs this session created or updated are properly registered and cross-referenced
- [ ] **Project board updated:** Items moved to appropriate column (Done/Closed)
- [ ] **Wiki updated:** If methodology, learnings, or documentation was produced — Wiki pages created/updated
- [ ] **Labels created:** Any new labels needed for tracking were created (Cloudflare D1 tags or R2 metadata)
- [ ] **Project-state Issue updated:** Final status recorded on the project-state Issue with branch, commit, and summary
- [ ] **No stale documentation:** All referenced files, URLs, and paths are current and accessible

**For prompt engineering sessions:**
- [ ] **Wiki pages verified:** R2 `qnfo/audit/` or D1 `qnfo-audit` entries confirmed present with correct content
- [ ] **New labels documented:** Any new GitHub labels created are noted in the project-state Issue

**Blockers:** Unclosed Issues, unupdated Wiki, undocumented changes.

---

## PHASE F: CLEANUP & FINAL STATE — JIT ENFORCEMENT

**HARD RULE:** This machine is a thin client. The ONLY files that persist locally are the import surface (`G:\My Drive\prompts\`). Everything else MUST be cleaned up.

- [ ] **Orphan `_*` files scan and removal:** `Get-ChildItem -File -Name | Where-Object { $_ -match '^_' } | ForEach-Object { Remove-Item $_ }` — verify with `Test-Path` that ZERO `_*` files remain
- [ ] **Python cache cleanup:** `if (Test-Path "__pycache__") { Remove-Item -Recurse -Force "__pycache__" }`
- [ ] **All temp files deleted:** `Remove-Item` all `_*.py`, `_*.txt`, and other temporary artifacts. Verify with `Test-Path` — do NOT use `-ErrorAction SilentlyContinue`
- [ ] **Working tree clean:** `git status --porcelain` returns empty (re-verified after cleanup)
- [ ] **QWAV-DEFAULT.md unstaged:** If QWAV-DEFAULT.md or DEFAULT.md was inadvertently modified (check `git diff --name-only`) (line endings, stash artifacts), restore with `git checkout`
- [ ] **Only main branch exists:** `git branch` shows `* main` as the only local branch
- [ ] **Stash empty:** `git stash list` shows no items from this session

---

## PHASE G: QUANTITATIVE CLOSEOUT VERIFICATION `[CODE-EXECUTED]`

Run a Python script that verifies:
- [ ] **Test-Path chain:** Every file claimed in this session's outputs exists on disk
- [ ] **Git log integrity:** All commits claimed in this session appear in `git log`
- [ ] **prompts.json integrity:** Template count matches expected, new entries have valid `content` field
- [ ] **Remote consistency:** Remote HEAD matches or is within 1 commit of local (accounting for CI auto-commits)
- [ ] **Test evidence:** Any test suite claimed as "passed" re-executes and produces the same result

**Verification script output:**
```
[CODE-EXECUTED]
Files: 5/5 present
Commits: 3/3 verified
Templates: 26/26 registered  
Remote: synced
Tests: 10/10 passing
```

---

**For sessions that produced a publication/release:**
- [ ] **PDF generated:** `pdf-builder` skill executed successfully (`skill_view('pdf-builder')`) OR manual PDF generation confirmed (Persistent Preference — PDF attached to releases)
- [ ] **PDF in release:** `npx wrangler r2 object get qnfo/releases/<project>/<version>/paper.pdf --remote` confirms PDF exists
- [ ] **GATE: If PDF is missing from release assets, close-out is BLOCKED.** Retroactively upload before completing.

---

## PHASE H: PROJECT HANDOFF VERIFICATION `[CODE-EXECUTED]`

Before terminating the session, verify that ALL projects in `G:\My Drive\projects\` have up-to-date handoff documents:

- [ ] **All projects scanned:** `Get-ChildItem -Path "G:\My Drive\projects" -Directory` enumerated. Every project directory checked for `HANDOFF.md`.
- [ ] **No missing handoffs:** Zero projects return "NO HANDOFF.md." Any missing handoff created via `fill_prompt_template("HANDOFF", {...})`.
- [ ] **Handoff content non-trivial:** All HANDOFF.md files > 100 bytes. Verify with `(Get-Item <path>).Length -gt 100`.
- [ ] **Current project handoff updated:** The project worked on in this session has HANDOFF.md updated with: session date, agent, work completed, current state, next steps, blockers, branch reference.
- [ ] **All handoffs read-verified:** `Get-Content <path> -First 3` on every HANDOFF.md confirms readability.

**Blockers:** Any project missing HANDOFF.md, zero-byte handoff, handoff not updated for current session's project.

---

## PHASE I: TASK EXECUTION AUDIT `[CODE-EXECUTED]`

Verify that ALL planned tasks were actually EXECUTED — not just claimed in text:

- [ ] **Planned vs executed comparison:** Every task from the session's plan (Issue, backlog, or prior HANDOFF) has a corresponding execution artifact (file, commit, test output).
- [ ] **No phantom claims:** Audit response text for action claims without tool invocation. Any "I will..." or "PROCEED" without corresponding tool call → `[!]` BLOCKER. Remove from response.
- [ ] **File write verification:** Every file claimed as written → `Test-Path <file>` returns True AND `Get-Content <file> -First 3` matches expected content.
- [ ] **Commit verification:** Every commit claimed → `git log --oneline` contains the commit hash.
- [ ] **Python execution verification:** Every script claimed as run → re-execute and confirm output matches claim.
- [ ] **Test verification:** Every test claimed as "passed" → re-run and confirm exit code 0 with matching output.
- [ ] **Unexecuted items documented:** Any planned-but-unexecuted item has `[DEFERRED: reason]` or `[BLOCKED: reason]` documentation in the handoff.
- [ ] **No silent omissions:** Review the full session plan. Every line item has a status: `[x]` done, `[!]` blocked, `[/]` N/A, or `[→]` deferred.

**Blockers:** Any executed task with no evidence, any phantom claim in response text, any planned item with no status.

---

## HUMAN SIGN-OFF

- [ ] All Phase A-I gates passed (zero `[!]` blockers)
- [ ] All deliverables verified on disk
- [ ] All remote repositories synced
- [ ] All projects have updated HANDOFF.md
- [ ] Closeout complete — session ready to end

---

*SESSION CLOSEOUT OPERATING PROCEDURE v5.0 — Universal | PROJECT, PROMPT-ENGINEERING, SYSTEM-MAINTENANCE, RESEARCH*

*Trigger: `fill_prompt_template("CLOSEOUT-CHECKLIST", {"topic": "<name>"})` — or auto-triggered by closeout-manager skill v2.0 when all tasks complete.*
