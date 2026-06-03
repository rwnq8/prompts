---
template: ZENODO-PUBLISH
version: "1.0"
date: 2026-06-03
---

# ZENODO-PUBLISH TEMPLATE v1.0
# Template for one-command Zenodo DOI registration via REST API
#
# Parameters:
#   title       — Publication title (required)
#   author      — Author name in "Last, First" format (required)
#   file        — Path to file to upload (required)
#   abstract    — Publication abstract (optional)
#   keywords    — Comma-separated keywords (optional)
#   upload_type — Zenodo type: publication|poster|presentation|dataset|image|video|software|lesson|other
#   license     — License identifier (default: QNFO-COL-v1.1 — https://github.com/QNFO/license/)
#   doi         — Existing DOI for creating new version (optional)
#   sandbox     — Set "true" for sandbox testing (default: false for production)
#
# Usage via fill_prompt_template:
#   templateName: ZENODO-PUBLISH
#   templateArgs: { "title": "...", "author": "...", "file": "...", ... }

## Zenodo DOI Registration — One-Command Publishing

You are about to register a DOI on Zenodo. The tool `zenodo_publish.py` handles the full pipeline:
deposition creation → metadata → file upload → publication.

**HARD RULES:**
1. **Sandbox first, production after.** Test with `--sandbox` before creating a real DOI.
2. **Never fabricate a DOI.** DOIs come only from the Zenodo API response.
3. **Token is NEVER hardcoded.** Primary: `ZENODO_TOKEN` environment variable. Fallback: `%USERPROFILE%\.zenodo_token` file.
4. **Verify file exists** before publishing: `Test-Path <file>` + `Get-Content <file> -First 5`.

### Phase 1: Token Verification

**Primary (env var — GitHub Actions compatible):**
```powershell
if ($env:ZENODO_TOKEN) {
    Write-Output "ZENODO_TOKEN env var set: YES"
} else {
    Write-Output "ZENODO_TOKEN env var: NOT SET — trying file fallback"
}
```

**Fallback (file — local machine only):**
```powershell
Test-Path "$env:USERPROFILE\.zenodo_token"
$token = Get-Content "$env:USERPROFILE\.zenodo_token"
```

If token missing: direct user to https://zenodo.org/account/settings/applications/
Required scopes: `deposit:actions`, `deposit:write`. Save to `%USERPROFILE%\.zenodo_token`.

### Phase 2: Sandbox Test (MANDATORY)

```powershell
$env:ZENODO_TOKEN = $env:ZENODO_TOKEN ?? (Get-Content "$env:USERPROFILE\.zenodo_token")

python "_zenodo_publish.py (pull from R2: `qnfo/tools/zenodo_publish.py`)" `
  --sandbox `
  --title "{{title}}" `
  --author "{{author}}" `
  --file "{{file}}" `
  {{#abstract}}--abstract "{{abstract}}"{{/abstract}} `
  {{#keywords}}--keywords "{{keywords}}"{{/keywords}}
```

**Success:** Deposition ID displayed, file uploaded, script reports `{{sandbox}} Testing complete.`
**If fails:** Fix issues before proceeding. Do NOT skip to production.

### Phase 3: Production Publication

Only after Phase 2 success. Remove `--sandbox`. Script will prompt `Type 'PUBLISH' to confirm:`.

```powershell
python "_zenodo_publish.py (pull from R2: `qnfo/tools/zenodo_publish.py`)" `
  --title "{{title}}" `
  --author "{{author}}" `
  --file "{{file}}" `
  {{#abstract}}--abstract "{{abstract}}"{{/abstract}} `
  {{#keywords}}--keywords "{{keywords}}"{{/keywords}} `
  {{#upload_type}}--upload-type "{{upload_type}}"{{/upload_type}} `
  {{#license}}--license "{{license}}"{{/license}} `
  {{#doi}}--doi "{{doi}}"{{/doi}}
```

**Success output:**
```
PUBLISHED SUCCESSFULLY
  Title: {{title}}
  DOI: 10.5281/zenodo.XXXXXXXX
  URL: https://doi.org/10.5281/zenodo.XXXXXXXX
  Zenodo: https://zenodo.org/records/XXXXXXXX
```

### Post-Publication

- **Capture the DOI** — it's in the script output
- **Document** in project CHANGELOG: DOI, deposition ID, date, file
- **For new versions:** pass `--doi <existing_doi>` to create a new version

### Failure Handling

| Error | Action |
|:------|:-------|
| No token | Direct user to create token at zenodo.org/account/settings/applications/ |
| File not found | Verify path with `Test-Path`, use absolute path |
| API 500 | Server-side. Check status.zenodo.org. Retry later. |
| API 401 | Token expired/revoked. Generate new token. |
| Script crash | Read `_zenodo_publish.py (pull from R2: `qnfo/tools/zenodo_publish.py`)` for error details |

### Source Labeling

- DOI from API response: `[CODE-EXECUTED: zenodo_publish.py]`
- Token status: `[EXTERNAL-SOURCE: %USERPROFILE%\.zenodo_token]`
- File verification: `[EXTERNAL-SOURCE: {{file}}]`
- All other claims: `[LLM-INFERRED]`
