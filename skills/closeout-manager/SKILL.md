---
name: closeout-manager
description: Execute project close-out procedures: archive, R2 audit trail export, PDF generation, GitHub Release creation, and state update. Use when the agent is completing a project or session. MANDATORY for every session end.
tools: exec, fill_prompt_template, write
---
# Closeout Manager v2.0 — With Cloudflare R2 Audit Trail

## When to Use
- Project work is complete
- Session is ending
- Agent needs to archive, release, and transition
- MANDATORY: Every session must export to Cloudflare R2 audit trail

## Workflow (7 Steps)

### 1. Complete All Pending Commits
```bash
git log -1 --oneline          # Verify last commit
git status                     # Check for uncommitted changes
Test-Path <changed-files>      # Filesystem verification before commit
Get-Content <file> -First 5    # Content verification
git add <files>
git commit -m "ACTION:... RATIONALE:..."
git log -1 --oneline          # Verify commit succeeded
```

### 2. Export Session to R2 Audit Trail (NEW — MANDATORY)
Create a structured session summary and upload to Cloudflare R2:
```
R2 Path: qnfo/audit/conversations/YYYY-MM-DD-description.md
```

**Session Summary Format:**
```markdown
# Session: [Brief Description]
**Date:** YYYY-MM-DD
**Agent:** [Agent Name] vX.Y
**User:** [Username]

## Summary
2-3 sentence summary of what was accomplished.

## Decisions Made
1. **Decision title** — Rationale, alternatives considered, status
2. ...

## Files Changed
- path/to/file.md (EDIT) — What changed and why
- path/to/new-file.py (CREATE) — Purpose

## Commits
- abc1234 ACTION:EDIT FILE: path RATIONALE:reason

## Infrastructure State Changes
- Workers: [deployed/modified/deleted]
- R2: [files uploaded]
- DNS: [records changed]
- Domains: [added/removed]

## Handoff Notes
- What the next agent/session needs to know
- Blocking issues
- Deferred items
```

**Upload Commands:**
```bash
# 1. Write session summary to temp file
# 2. Upload to R2
wrangler r2 object put qnfo/audit/conversations/YYYY-MM-DD-topic.md --remote --file=<temp-file>

# 3. Verify upload
wrangler r2 object get qnfo/audit/conversations/YYYY-MM-DD-topic.md --remote
```

### 3. Update Decision Log (If New Decisions Made)
```bash
# 1. Download current decision log
wrangler r2 object get qnfo/audit/decisions/DECISION-LOG.md --remote --file=./temp-decision-log.md

# 2. Read current log, prepend new decisions
# 3. Upload updated log
wrangler r2 object put qnfo/audit/decisions/DECISION-LOG.md --remote --file=./temp-decision-log.md

# 4. Verify
wrangler r2 object get qnfo/audit/decisions/DECISION-LOG.md --remote
```

### 4. Run Mandatory Close-Out Checklist
- [ ] All code committed: README.md reflects final documentation
- [ ] All tests pass: Python self-tests return success
- [ ] Git log verified: `git log -1 --oneline` confirms last commit
- [ ] **R2 audit trail exported: session summary + decisions updated** (NEW)
- [ ] Publication-ready docs copied to GitHub Releases
- [ ] Auto-archive to: `G:\My Drive\Archive\projects\YYYY\MM\<name>\`
- [ ] Auto-PDF: `gh workflow run pdf-release.yml --repo qnfo/<name>`
- [ ] GitHub Release: `gh release create vX.Y.Z --repo qnfo/<name> --title "..." --notes "..."`
- [ ] Project-state Issue updated with final status + archive location

### 5. Archive Project to Archive Directory
```bash
# Path convention
G:\My Drive\Archive\projects\YYYY\MM\<project-name>\

# Copy project files (not .git)
robocopy "G:\My Drive\projects\<name>" "G:\My Drive\Archive\projects\2026\05\<name>" /E /XD .git
```

### 6. Create GitHub Release
```bash
# For document projects with DOI/publication
gh release create v1.0.1 --repo qnfo/<name> \
  --title "Release v1.0.1" \
  --notes "$(cat CHANGELOG.md)"
gh release upload v1.0.1 ./output/paper.pdf --repo qnfo/<name>
```

### 7. Update Project-State Issue
```bash
gh issue comment <num> --repo qnfo/<name> --body "
## Session Complete
| Field | Value |
|:------|:------|
| Status | CLOSED (or ACTIVE if continuing) |
| Archive | G:\\My Drive\\Archive\\projects\\YYYY\\MM\\<name>\\ |
| R2 Audit | qnfo/audit/conversations/YYYY-MM-DD-topic.md |
| Release | https://github.com/qnfo/<name>/releases/tag/vX.Y.Z |
| PDF | Attached to Release |
"
```

---

## R2 Audit Trail Integration

The Cloudflare R2 audit trail captures EVERY agent session, decision, and infrastructure change. This is the system's memory — if your computer crashes, the audit trail survives on Cloudflare.

| R2 Path | Content | Updated By |
|:--------|:--------|:-----------|
| `qnfo/audit/conversations/` | Session summaries | closeout-manager (every session) |
| `qnfo/audit/github/latest/` | GitHub Issues | github-sync Worker (daily cron) |
| `qnfo/audit/decisions/DECISION-LOG.md` | All decisions | closeout-manager (when decisions made) |
| `qnfo/audit/infrastructure/` | CF state snapshots | closeout-manager (when infra changes) |

**Recovery:** New agent on new machine → queries R2 (`wrangler r2 object get qnfo/audit/... --remote`) → gets full context from last session.

---

## Social Media Trigger (If Publication Occurred)
```python
fill_prompt_template("SOCIAL-ORCHESTRATOR", {
    "platforms": "twitter, linkedin",
    "content": "New publication: [Title] | [DOI/URL]",
    "schedule": "now"
})
```

## Post-Close-Out Auto-Continue
1. Check GitHub Issues (label: project-state) for next active project
2. Prioritize: P0 > P1 > P2 > unfiled
3. If no projects: report "All projects closed out. Nothing pending."
4. If found: navigate to directory and begin session startup

---

*Closeout Manager v2.0 — Updated 2026-05-27 with mandatory Cloudflare R2 audit trail export. Every session ends with a survivable record on R2.*
