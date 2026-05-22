---
template: CLOSEOUT-CHECKLIST
version: "1.0"
---

# PROJECT CLOSE-OUT CHECKLIST — [PROJECT NAME]

**Date:** [YYYY-MM-DD]
**Phase Gate:** P5 — Close-Out

Every item must be verified and marked `[x]` before the session ends. Items marked `[!]` indicate a blocker that prevents close-out.

## 1. FINAL REPORT / SYNTHESIS
- [ ] Comprehensive final document (or publication itself) summarizing: what was done, key results, what was NOT done, known limitations, lessons learned, and handoff recommendations for any continuation.

## 2. PUBLICATION DOCUMENT (if applicable)
- [ ] YAML frontmatter complete (title, authors, date, DOI, abstract)
- [ ] Curly/smart quotes verified (Python scan — zero straight quotes)
- [ ] Math formatting verified (Python scan — zero bare Unicode math)
- [ ] Descriptive filename (not versioned)
- [ ] Copied to `G:\My Drive\Obsidian\releases\YYYY\MM\`
- [ ] Copy verified with `Test-Path`

## 3. ALL CORE + PHASE DOCS UPDATED
- [ ] `PROJECT STATE.md` — final state recorded
- [ ] `SPRINT.md` — all tasks marked `[x]`, `[-]`, or triaged
- [ ] `CHANGELOG.md` — close-out entry added
- [ ] `LEARNINGS.md` — final lessons recorded
- [ ] `DECISIONS.md` — final decisions documented
- [ ] `BACKLOG.md` — remaining items triaged (migrate, archive, or abandon)
- [ ] `README.md` — project summary updated

## 4. GIT FINALIZED
- [ ] All changes committed on feature branch
- [ ] No uncommitted changes (`git status` clean)
- [ ] Branch ready for merge to main or archival
- [ ] Final commit message includes `PROJECT CLOSE-OUT` tag

## 5. PUBLICATION WORKFLOW (if publication exists)
- [ ] User prompted: "Published to Zenodo? [YES/NO]"
- [ ] User prompted: "Published to ResearchGate? [YES/NO]"
- [ ] If both confirmed: trigger SOCIAL-ORCHESTRATOR template via `fill_prompt_template("SOCIAL-ORCHESTRATOR TEMPLATE v1.0", {...})`

## 6. ARCHIVING
- [ ] Project directory is self-contained — a new agent from cold can read `PROJECT STATE.md` and understand everything
- [ ] No broken references (verify all linked files exist)
- [ ] No temp files (scan for `_*.py`, `*.tmp`, `__pycache__`)
- [ ] `.gitignore` covers build artifacts

## 7. FINAL AUDIT
- [ ] Python script verifies: all core docs exist and are non-empty
- [ ] Publication file exists in releases (Test-Path confirmed)
- [ ] `git worktree` clean
- [ ] No `__pycache__` or `.pyc` files
- [ ] `system_audit.py` run and reports PASS on all applicable checks

## Human Sign-Off
- [ ] Close-out checklist reviewed
- [ ] All blockers resolved
- [ ] Project approved for archive

---
*Generated from CLOSEOUT-CHECKLIST-TEMPLATE.md v1.0*
