# HANDOFF: Prompts R2 Migration — 2026-06-05

> **Status:** MIGRATION EXECUTED | **By:** META-PROMPT v6.5 | **Handoff to:** Next agent session

---

## What Happened

All prompt-defining files were migrated from local `G:\My Drive\prompts\` to Cloudflare R2 as the canonical source. This completes the Thin-Client Model — R2 is now the single source of truth for ALL QNFO assets.

### Files Migrated to `qnfo/prompts/`

| Category | Count | R2 Path |
|:---------|:-----:|:--------|
| Core Prompts | 4 | `qnfo/prompts/DEFAULT.md`, `QWAV-DEFAULT.md`, `META-PROMPT-DEEPSEEK.md`, `PLATFORM-GAPS.md` |
| Prompt JSON | 2 | `qnfo/prompts/prompts.json`, `prompts_bare.json` |
| Skills | 14 | `qnfo/prompts/skills/<name>/SKILL.md` + `scripts/` + `references/` |
| Templates | 21 | `qnfo/prompts/templates/*.md` |
| Agents | 3 | `qnfo/prompts/agents/*.md` |
| Tools | 3 | `qnfo/prompts/_deploy.py`, `_system_audit.py`, `_bootstrap_from_r2.py` |
| Config | 3 | `qnfo/prompts/config/*.json` |
| Architecture | — | `qnfo/prompts/architecture/*.md` |

### Bootstrap Script

A new `_bootstrap_from_r2.py` is available at `qnfo/prompts/_bootstrap_from_r2.py`. Agents should use this to pull all prompt files from R2 when starting a cold session:

```bash
# Pull from R2
npx wrangler r2 object get qnfo/prompts/_bootstrap_from_r2.py --remote --file=_bootstrap_from_r2.py
python _bootstrap_from_r2.py              # Pull all prompts
python _bootstrap_from_r2.py --dry-run    # Preview
python _bootstrap_from_r2.py --skills-only  # Skills only
```

### Updated Scripts

| Script | Version | Change |
|:-------|:-------:|:-------|
| `_deploy.py` | v2.2 | Target `.deepchat`, full-dir sync, text-normalized hashes |
| `_bootstrap_from_r2.py` | v1.0 | NEW — pulls all prompts from R2 |
| Discovery Index | updated | New `prompts_r2_migration` section |

### Discovery Index

Updated with new `prompts_r2_migration` section documenting:
- All file categories and their R2 paths
- Bootstrap script location
- Migration timestamp

### Git Status

- Branch: `main` (ahead of `origin/main` by 8 commits)
- All migration scripts committed
- **PUSH PENDING** — run `git push origin main` to back up

### Local File Cleanup

⚠️ **USER ACTION REQUIRED:** Local prompt-defining files should be deleted after confirming R2 uploads are verified. Run:

```powershell
# VERIFY first:
python _bootstrap_from_r2.py --dry-run

# Then delete local files (after confirming R2 has everything):
# (The user should execute this after verification)
```

### What the Next Agent Must Do

1. **Pull from R2:** `python _bootstrap_from_r2.py` (if local files are gone)
2. **Deploy skills:** `python _deploy.py --skills-only`
3. **Restart DeepChat** to pick up skill changes
4. **Verify:** `python _deploy.py --dry-run --skills-only` should show all UNCHANGED

### Known Issues

- **EPERM on pdf-builder import:** DeepChat's import UI cannot rename `pdf-builder` directory due to file locks. Workaround: use `_deploy.py` (direct write, no rename). Never use DeepChat UI import for QNFO skills.
- **Git line-ending churn:** `_deploy.py` v2.2 uses text-normalized hash comparison to eliminate false WOULD_UPDATE from `core.autocrlf`.
- **npx PATH in Python:** `npx` is a PowerShell script at DeepChat's runtime path. Python's `subprocess` must use `shell=True` to invoke it.

---
*HANDOFF-MIGRATION-2026-06-05.md — Prompts R2 Migration Handoff*
