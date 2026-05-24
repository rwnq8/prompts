---
name: zenodo-publish
description: >
  Zenodo DOI registration via REST API. One-command publishing with mandatory sandbox-first testing.
  Use when the user needs to create a Zenodo deposition, register a DOI, publish a file
  (paper, dataset, poster, presentation, software), create new versions of existing records,
  or test Zenodo API integration. Triggers on: Zenodo, DOI registration, publish to Zenodo,
  Zenodo deposition, Zenodo upload, get a DOI, register DOI, Zenodo sandbox.
---

# Zenodo Publish — One-Command DOI Registration

## Quick Start

```bash
python scripts/zenodo_publish.py \
  --token $(Get-Content "$env:USERPROFILE\.zenodo_token") \
  --title "Title" --author "Last, First" --file "paper.pdf"
```

The script handles: deposition creation → metadata → file upload → publication.
Sandbox testing is **mandatory** before production. A real DOI is permanent.

## Workflow (HARD ORDER)

### 1. Verify Token
```powershell
Test-Path "$env:USERPROFILE\.zenodo_token"
```
If missing: see [token-setup.md](references/token-setup.md). Required scopes: `deposit:actions`, `deposit:write`.

### 2. Sandbox Test (NEVER SKIP)
```bash
python scripts/zenodo_publish.py --sandbox \
  --token $(Get-Content "$env:USERPROFILE\.zenodo_token") \
  --title "..." --author "..." --file "..." [--abstract "..."] [--keywords "kw1,kw2"]
```
Sandbox success: deposition ID displayed, file uploaded, script reports `[SANDBOX] Testing complete.`
If sandbox fails: fix issues. Do NOT proceed to production.

### 3. Production Publish
Remove `--sandbox`. Add `--upload-type` and `--license` if needed.
Script prompts: `Type 'PUBLISH' to confirm:` — requires explicit confirmation.
Success: DOI `10.5281/zenodo.XXXXXXXX` displayed.

### 4. New Versions
Pass existing DOI to create a new version (not a new record):
```bash
python scripts/zenodo_publish.py --token ... --doi "10.5281/zenodo.XXXXXXXX" ...
```

## Arguments

| Flag | Required | Default | Notes |
|:-----|:---------|:--------|:------|
| `--token` | Yes | — | Or set `ZENODO_TOKEN` env var |
| `--sandbox` | Phase 2 only | — | Use sandbox.zenodo.org (no real DOI) |
| `--title` | Yes | — | Publication title |
| `--author` | Yes | — | "Last, First" format |
| `--file` | Yes | — | Path to file to upload |
| `--abstract` | No | title | Publication abstract |
| `--keywords` | No | — | Comma-separated |
| `--upload-type` | No | publication | publication, poster, presentation, dataset, image, video, software, lesson, other |
| `--license` | No | QNFO-COL-v1.1 | License identifier (https://github.com/QNFO/license/) |
| `--orcid` | No | 0009-0002-4317-5604 | Author ORCID |
| `--date` | No | today | YYYY-MM-DD |
| `--doi` | No | — | Existing DOI for new version |

## Guardrails

- **Sandbox first, always.** Production DOIs cannot be deleted.
- **Never fabricate a DOI.** DOIs come only from `publish_deposition()` API response.
- **Token is NEVER hardcoded.** Read from `%USERPROFILE%\.zenodo_token` or env var.
- **Verify file exists** before publishing: `Test-Path` + `Get-Content -First 5`.
- **No placeholder content.** Scan for `[TODO]`, `[TBD]`, `########` before publishing.
- **API 500 is server-side.** Don't loop-retry. Report and wait.

## Failure Recovery

| Symptom | Action |
|:--------|:-------|
| `No Zenodo token` | Create token at zenodo.org/account/settings/applications/ → save to `.zenodo_token` |
| `File not found` | Verify path with `Test-Path`, use absolute path |
| `API Error [500]` | Server-side. Check status.zenodo.org. Retry later. |
| `API Error [401]` | Token expired/revoked. Generate new token. |
| Upload timeout | File >100MB may need Zenodo web UI |
| Sandbox vs production mixup | `--sandbox` flag controls this. Sandbox URL: sandbox.zenodo.org |

## Integration with DEFAULT.md

This skill adds Zenodo publishing capability without replacing DEFAULT.md.
DEFAULT.md provides Rules 1-6 (tool honesty), 12-13 (Unicode/PowerShell safety),
and general workflow patterns. This skill provides only the Zenodo-specific workflow
and the bundled `zenodo_publish.py` script for deterministic execution.
