---
template: CLOSEOUT-CHECKLIST
version: "1.1"
---

# PROJECT CLOSE-OUT CHECKLIST — [PROJECT NAME]

> **⚠️ GITHUB-NATIVE v3.0:** All project management is GitHub-native. Do NOT create or update SPRINT.md, BACKLOG.md, CHANGELOG.md, LEARNINGS.md, DECISIONS.md, or PROJECT STATE.md — these files are PERMANENTLY DEPRECATED (DEFAULT.md §0.6.8). Use GitHub-native equivalents throughout.

**Date:** [YYYY-MM-DD]
**Phase Gate:** P5 — Close-Out
**GitHub Repo:** `qnfo/[repo-name]`
**GitHub Project State Issue:** `gh issue view --repo qnfo/[repo-name] [issue-number]`

Every item must be verified and marked `[x]` before the session ends. Items marked `[!]` indicate a blocker that prevents close-out.

## 1. FINAL REPORT / SYNTHESIS
- [ ] Comprehensive final document (or publication itself) summarizing: what was done, key results, what was NOT done, known limitations, lessons learned, and handoff recommendations for any continuation.

## 2. PUBLICATION DOCUMENT (if applicable)
- [ ] YAML frontmatter complete (title, authors, date, DOI, abstract)
- [ ] Curly/smart quotes verified (Python scan — zero straight quotes)
- [ ] Math formatting verified (Python scan — zero bare Unicode math)
- [ ] Descriptive filename (not versioned)
- [ ] Copied to GitHub Releases via `gh release create --repo qnfo/[repo-name]`
- [ ] Copy verified with `gh release view --repo qnfo/[repo-name]`

## 3. ALL GITHUB-NATIVE PROJECT STATE UPDATED
- [ ] **GitHub Issue (label: `project-state`):** Final status recorded — `gh issue comment --repo qnfo/[repo-name] [issue-number] --body "STATUS: CLOSED | DATE: [YYYY-MM-DD] | ARCHIVE: ..."`
- [ ] **GitHub Issues:** All tasks closed with `gh issue close` or triaged with labels
- [ ] **GitHub Project Board:** All items moved to `Done` column or archived
- [ ] **GitHub Releases:** Close-out release created — `gh release create --repo qnfo/[repo-name] v1.0.0 --title "Project Complete" --notes "Final deliverables and close-out summary"`
- [ ] **GitHub Wiki:** Final lessons recorded — `OWNER/REPO.wiki.git` updated with key findings
- [ ] **GitHub Discussions:** Final decisions documented
- [ ] **GitHub Issues (label: `backlog`):** Remaining items triaged (migrate, archive, or abandon)

## 4. GIT FINALIZED
- [ ] All changes committed on feature branch
- [ ] No uncommitted changes (`git status` clean)
- [ ] Branch merged to `main` (or ready for archival merge)
- [ ] Final commit message includes `PROJECT CLOSE-OUT` tag
- [ ] `git log -1 --oneline` confirms final commit exists

## 5. PUBLICATION WORKFLOW (if publication exists)
- [ ] User prompted: "Published to Zenodo? [YES/NO]"
- [ ] User prompted: "Published to ResearchGate? [YES/NO]"
- [ ] If both confirmed: trigger SOCIAL-ORCHESTRATOR template via `fill_prompt_template("SOCIAL-ORCHESTRATOR TEMPLATE v1.0", {...})`
- [ ] GitHub Release created with DOI link if available — `gh release create --repo qnfo/[repo-name] --notes "DOI: [doi]"`

## 6. ARCHIVING (CPL L44)
- [ ] Move project directory to `G:\My Drive\Archive\projects\YYYY\MM\` — use `Move-Item` or Python `shutil.move`
- [ ] Verify move succeeded: `Test-Path` at archive location returns True, original location returns False
- [ ] Update QWAV program state: comment on GitHub Issue (label: `project-state`) in qnfo/program repo to reflect archival
- [ ] Remove project from active GitHub Project boards (both project board and QNFO Program Board)
- [ ] Archive location documented in the project's GitHub Issue (label: `project-state`)
- [ ] Project directory is self-contained — a new agent from cold can read `README.md` and the GitHub Issue (project-state) and understand everything
- [ ] No broken references (verify all linked files exist)
- [ ] No temp files (scan for `_*.py`, `*.tmp`, `__pycache__`)
- [ ] `.gitignore` covers build artifacts

## 7. FINAL AUDIT
- [ ] Python script verifies: README.md exists and is non-empty
- [ ] Publication file exists in GitHub Releases (gh release view confirmed)
- [ ] `git worktree` clean
- [ ] No `__pycache__` or `.pyc` files in project directory
- [ ] `system_audit.py` run and reports PASS on all applicable checks
- [ ] GitHub Issue (label: `project-state`) reflects final CLOSED status

## Human Sign-Off
- [ ] Close-out checklist reviewed
- [ ] All blockers resolved
- [ ] Project approved for archive

---
*Generated from CLOSEOUT-CHECKLIST-TEMPLATE.md v3.0 — GitHub-Native*
