---
template: CLOSEOUT-CHECKLIST
version: "4.0"
---

# SESSION CLOSEOUT OPERATING PROCEDURE — [PROJECT/TOPIC]

> **GATE:** Mandatory before declaring ANY session complete. Verify all items/tasks/phases executed, implemented, complete, and tested/audited. Save, commit, merge, push, and document everything.
>
> **SCOPE:** Universal — applies to ALL session types (project work, prompt engineering, system maintenance, research).
>
> **GitHub-Native:** All project management is GitHub-native. Do NOT create or update SPRINT.md, BACKLOG.md, CHANGELOG.md, LEARNINGS.md, DECISIONS.md, or PROJECT STATE.md — these files are PERMANENTLY DEPRECATED (DEFAULT.md §0.6.8).
>
> **ERROR HANDLING:** All `gh` commands inherit QWAV-DEFAULT.md §0.9.1 retry strategy (3x with backoff). If a gh command fails after retries: mark `[!]` with rationale and continue. Do NOT block closeout on a single gh command failure — all items are independently verifiable.

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

- [ ] **Remote sync confirmed:** All local commits are on `origin/main` (or `origin/feature/name` if PR pending)
- [ ] **Verify with gh CLI:** `gh api repos/rwnq8/prompts/commits/main -q '.sha[0:7]'` matches local HEAD (or local HEAD is ahead by a PR)
- [ ] **PR created and merged** (if using feature branch): `gh pr view --repo [owner/repo] [number] --json state` returns `"MERGED"`
- [ ] **Feature branch deleted after merge:** `gh pr view` shows `--delete-branch` was used, or branch manually deleted
- [ ] **No orphan branches:** `git branch -a` shows no feature branches that should have been deleted after merge

**For project sessions:**
- [ ] **Project repo remote matches local:** `git log --oneline origin/main -3` matches local
- [ ] **All project repos pushed:** Every repo modified in this session has been pushed

**Blockers:** Unpushed commits, unmerged PRs, orphan feature branches, remote divergence.

---

## PHASE E: TRACKING & DOCUMENTATION `[CODE-EXECUTED]`

- [ ] **GitHub Issue tracking:** All work tracked via GitHub Issues with appropriate labels. Issue closed or updated with final status.
- [ ] **Project board updated:** Items moved to appropriate column (Done/Closed)
- [ ] **Wiki updated:** If methodology, learnings, or documentation was produced — Wiki pages created/updated
- [ ] **Labels created:** Any new labels needed for tracking were created (`gh label create`)
- [ ] **Project-state Issue updated:** Final status recorded on the project-state Issue with branch, commit, and summary
- [ ] **No stale documentation:** All referenced files, URLs, and paths are current and accessible

**For prompt engineering sessions:**
- [ ] **Wiki pages verified:** `gh api repos/rwnq8/prompts/wiki` (or browser load) confirms pages exist with correct content
- [ ] **New labels documented:** Any new GitHub labels created are noted in the project-state Issue

**Blockers:** Unclosed Issues, unupdated Wiki, undocumented changes.

---

## PHASE F: CLEANUP & FINAL STATE

- [ ] **All temp files deleted:** `Remove-Item` all `_*.py`, `_*.txt`, and other temporary artifacts
- [ ] **Working tree clean:** `git status --porcelain` returns empty (re-verified after cleanup)
- [ ] **QWAV-DEFAULT.md unstaged:** If QWAV-DEFAULT.md or DEFAULT.md was inadvertently modified (line endings, stash artifacts), restore with `git checkout`
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

**For sessions that produced a GitHub Release:**
- [ ] **PDF generated:** `gh run list --repo qnfo/<name> --workflow=pdf-release.yml --limit 1` confirms success OR `build_pdf.py` executed (DEFAULT.md Persistent Preference 12)
- [ ] **PDF in release:** `gh release view <tag> --repo qnfo/<name> --json assets` confirms PDF attached
- [ ] **GATE: If PDF is missing from release assets, close-out is BLOCKED.** Retroactively upload before completing.

---

## HUMAN SIGN-OFF

- [ ] All Phase A-G gates passed (zero `[!]` blockers)
- [ ] All deliverables verified on disk
- [ ] All remote repositories synced
- [ ] Session approved for closeout

---

*SESSION CLOSEOUT OPERATING PROCEDURE v4.0 — Universal | PROJECT, PROMPT-ENGINEERING, SYSTEM-MAINTENANCE, RESEARCH*

*Trigger: `fill_prompt_template("CLOSEOUT-CHECKLIST", {"topic": "<name>"})`*
