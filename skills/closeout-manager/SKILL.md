---
name: closeout-manager
description: Session close-out procedures — audit trail export, R2 state upload, archive operations, and handoff documentation. Use at the end of every session.
version: "1.0"
---

# CLOSEOUT MANAGER SKILL — v1.0

> **On-demand skill.** Load via `skill_view('closeout-manager')` at session end.
> Source: `CLOSEOUT-CHECKLIST.md` + DEFAULT.md §10 + QWAV-DEFAULT.md close-out checklist

---

## Session Close-Out Protocol (MANDATORY)

Execute these steps at the end of EVERY session:

### 1. Verify All Commits
```bash
git log -1 --oneline
git branch --show-current
```

### 2. Audit Trail Export to R2

Write session summary to temp file `YYYY-MM-DD-topic.md` containing:
- Agent name, session date, summary
- Decisions made (with rationale)
- Files changed, commits, issues referenced
- Infrastructure state changes
- Handoff notes for next session

Use `fill_prompt_template("CLOUDFLARE-AUDIT-EXPORT", {...})` for consistent format.

Upload to R2 (v4.95+ compatible):
```bash
npx wrangler r2 object put qnfo/audit/conversations/<file>.md --file=<path>
```

Verify upload:
```bash
npx wrangler r2 object get qnfo/audit/conversations/<file>.md
```

### 3. Update Decision Log

If new decisions were made:
```bash
# Download current log
npx wrangler r2 object get qnfo/audit/decisions/DECISION-LOG.md --file=<temp>

# Append new decisions to temp file

# Upload updated log
npx wrangler r2 object put qnfo/audit/decisions/DECISION-LOG.md --file=<temp>
```

### 4. Update Project State

```bash
# Upload state JSON
npx wrangler r2 object put qnfo/audit/state/<project>.json --file=<local-state-file>
```

### 5. Archive to Local Storage

```bash
Move-Item -Path "<project>" -Destination "G:\My Drive\Archive\projects\YYYY\MM\<name>\"
```

### 6. Clean Up Temporary Files

Remove temporary fix scripts and work files:
```bash
Remove-Item "G:\My Drive\QWAV\_fix_*.py" -ErrorAction SilentlyContinue
Remove-Item "G:\My Drive\QWAV\_temp_*" -ErrorAction SilentlyContinue
```

---

## Close-Out Checklist

Use `fill_prompt_template("CLOSEOUT-CHECKLIST")` for the full verification checklist:
- [ ] All commits verified
- [ ] Audit trail exported to R2
- [ ] Decision log updated
- [ ] Project state updated
- [ ] Archive completed
- [ ] Branch verified (NOT main/master)

---

## Handoff Document

When handing off to another agent:
```bash
fill_prompt_template("HANDOFF", {type: "Program->Project", scope: "...", ...})
```

---

## Reference Files

- Close-out checklist: `templates/CLOSEOUT-CHECKLIST.md`
- Audit export template: `templates/CLOUDFLARE-AUDIT-EXPORT.md`
- Handoff template: `templates/HANDOFF.md`
- Rebuild from scratch: `REBUILD-FROM-SCRATCH.md`

---

*closeout-manager skill v1.0 — Load on-demand via skill_view() at session end*
