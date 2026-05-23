# Zenodo DOI Registration — Install & Use Guide

> **One-command Zenodo DOI registration. No browser. No manual form-filling.**
> Skill + CLI tool that handles: deposition creation → metadata → file upload → publication.

---

## 0. What You Get

| Artifact | Location | Purpose |
|:---------|:---------|:--------|
| **Skill** | `zenodo-publish.skill` | Import into DeepChat — auto-triggers on Zenodo/DOI mentions |
| **CLI Tool** | `zenodo_publish.py` | Standalone Python script — use directly if preferred |
| **Template** | `templates/ZENODO-PUBLISH.md` | Procedural template for `fill_prompt_template` (future) |

All three do the same thing: publish a file to Zenodo with a permanent DOI. The skill is the recommended path — it auto-activates and bundles the script.

---

## 1. Prerequisites

| Requirement | How to Check |
|:------------|:-------------|
| **Python 3.7+** | `python --version` |
| **Zenodo account** | Sign up at https://zenodo.org/signup/ (free) |
| **Zenodo API token** | See §2 below |
| **DeepChat** (for skill) | The `.skill` file imports into DeepChat |
| **Windows** (for token persistence path) | `%USERPROFILE%\.zenodo_token` — adapt for Linux/Mac |

The CLI tool uses **zero external Python packages** — only `urllib`, `json`, `argparse`, `os`, `sys`, `time`, `datetime` from stdlib.

---

## 2. Token Setup (REQUIRED — Do This First)

### 2.1 Create a Zenodo API Token

1. Go to **https://zenodo.org/account/settings/applications/**
2. Under "Personal access tokens", click **"New token"**
3. Name it something recognizable (e.g., "CLI publishing")
4. Check **both** required scopes:
   - ☑ `deposit:actions` — create and manage depositions
   - ☑ `deposit:write` — upload files and publish
5. Click **"Create"**
6. **Copy the token immediately** — it is shown only once. It will look like a ~60-character string.

### 2.2 Save the Token (Windows)

Open PowerShell and run (replace `your-token-here` with the actual token):

```powershell
"your-token-here" | Out-File -FilePath "$env:USERPROFILE\.zenodo_token" -NoNewline -Encoding ASCII
```

### 2.3 Verify the Token

```powershell
# Should return True
Test-Path "$env:USERPROFILE\.zenodo_token"

# Should return ~60
(Get-Content "$env:USERPROFILE\.zenodo_token").Length
```

### 2.4 Alternative Methods

The script accepts tokens three ways (in priority order):
1. `--token` CLI flag: `python zenodo_publish.py --token YOUR_TOKEN ...`
2. `ZENODO_TOKEN` environment variable: `$env:ZENODO_TOKEN = "your-token"`
3. `%USERPROFILE%\.zenodo_token` file (auto-read if neither flag nor env var)

**Security note:** The token is stored as plaintext. Never commit it to git. Revoke and regenerate if compromised.

---

## 3. Installation

### Option A: Install the Skill (Recommended)

1. In DeepChat, click the **Skills** icon (puzzle piece)
2. Click **"Import Skill"**
3. Select `G:\My Drive\prompts\zenodo\zenodo-publish.skill`
4. The skill appears in your skill list as **"zenodo-publish"**

The skill auto-triggers whenever you mention: Zenodo, DOI registration, publish to Zenodo, Zenodo deposition, Zenodo upload, get a DOI, register DOI.

### Option B: Use the CLI Directly

No installation needed — the script is at:
```
G:\My Drive\projects\zenodo-automation\zenodo_publish.py
```
Run it with Python directly:
```bash
python "G:\My Drive\projects\zenodo-automation\zenodo_publish.py" --help
```

---

## 4. Quickstart — First Sandbox Test

**ALWAYS test in sandbox first.** Sandbox creates a test deposition at `sandbox.zenodo.org` — no real DOI, fully deletable.

### If Using the Skill:

Just say to DeepChat:
> "Sandbox-test publishing my paper: title 'Test Publication', author 'Smith, John', file 'C:\Users\LENOVO\Documents\test.pdf'"

The skill activates, reads your token, and runs the sandbox test.

### If Using the CLI Directly:

```powershell
python "G:\My Drive\projects\zenodo-automation\zenodo_publish.py" `
  --sandbox `
  --token (Get-Content "$env:USERPROFILE\.zenodo_token") `
  --title "Test Publication" `
  --author "Smith, John" `
  --file "C:\Users\LENOVO\Documents\test.pdf" `
  --abstract "A test of the Zenodo publishing pipeline." `
  --keywords "test, zenodo, pipeline"
```

### Expected Sandbox Output:

```
============================================================
ZENODO SANDBOX (testing) PUBLICATION
============================================================
  Title: Test Publication
  Author: Smith, John
  File: C:\Users\LENOVO\Documents\test.pdf
  Environment: SANDBOX (testing)
============================================================

Step 1: Creating deposition...
  Created deposition ID: 123456

Step 2: Setting metadata...
  [OK] Metadata updated

Step 3: Uploading file...
  Uploading: test.pdf (12,345 bytes)
  Bucket: https://sandbox.zenodo.org/api/files/.../test.pdf
  [OK] Uploaded: test.pdf

Step 4: [SANDBOX] Would publish here. Testing complete.
  Deposition ID: 123456
  View at: https://sandbox.zenodo.org/deposit/123456
```

---

## 5. Full Workflow — Sandbox → Production

### Phase 1: Verify Everything

```powershell
# Check token
Test-Path "$env:USERPROFILE\.zenodo_token"

# Check file exists and is non-empty
Test-Path "your-file.pdf"
Get-Content "your-file.pdf" -First 5
```

### Phase 2: Sandbox Test (MANDATORY)

Run with `--sandbox` flag (see Quickstart above). Verify:
- [ ] Deposition ID is returned
- [ ] File uploaded successfully
- [ ] Metadata set correctly
- [ ] Script reports "Testing complete"

**If sandbox fails:** Fix the issue. Do NOT proceed to production. Common fixes:
- Token invalid → regenerate at zenodo.org/account/settings/applications/
- File not found → use absolute path
- API 500 → server-side, retry later (check status.zenodo.org)

### Phase 3: Production Publication

Remove `--sandbox`. Add full metadata:

```powershell
python "G:\My Drive\projects\zenodo-automation\zenodo_publish.py" `
  --token (Get-Content "$env:USERPROFILE\.zenodo_token") `
  --title "My Research Paper" `
  --author "Smith, John" `
  --file "C:\Users\LENOVO\Documents\paper.pdf" `
  --abstract "A comprehensive analysis of..." `
  --keywords "machine learning, optimization, convergence" `
  --upload-type "publication" `
  --license "cc-by-4.0"
```

**The script will prompt:**
```
⚠️  WARNING: You are about to PUBLISH to Zenodo PRODUCTION.
  This will create a real DOI that cannot be deleted.
  Type 'PUBLISH' to confirm:
```

Type `PUBLISH` (exactly, case-sensitive) and press Enter.

### Phase 4: Capture the DOI

```
============================================================
PUBLISHED SUCCESSFULLY
============================================================
  Title: My Research Paper
  DOI: 10.5281/zenodo.12563842
  URL: https://doi.org/10.5281/zenodo.12563842
  Zenodo: https://zenodo.org/records/12563842
============================================================
```

**The DOI is permanent.** Save it immediately. Add it to your paper's YAML frontmatter, project CHANGELOG, and any citations.

---

## 6. New Versions

To create a new version of an existing record (rather than a new record):

```powershell
python zenodo_publish.py --token ... --doi "10.5281/zenodo.12563842" --file "paper-v2.pdf" ...
```

Zenodo creates a new version linked to the original record. The original DOI resolves to the latest version.

---

## 7. All CLI Arguments

| Flag | Required | Default | Example |
|:-----|:---------|:--------|:--------|
| `--token` | Yes | — | `--token YOUR_TOKEN` |
| `--sandbox` | Phase 2 | `False` | `--sandbox` (flag only) |
| `--title` | Yes | — | `--title "Paper Title"` |
| `--author` | Yes | — | `--author "Smith, John"` |
| `--file` | Yes | — | `--file "paper.pdf"` |
| `--abstract` | No | title text | `--abstract "We show that..."` |
| `--keywords` | No | — | `--keywords "kw1, kw2, kw3"` |
| `--upload-type` | No | `publication` | `--upload-type dataset` |
| `--license` | No | `cc-by-4.0` | `--license mit` |
| `--orcid` | No | `0009-0002-4317-5604` | `--orcid 0000-0002-1825-0097` |
| `--date` | No | today | `--date 2026-05-15` |
| `--doi` | No | — | `--doi 10.5281/zenodo.XXXXXXXX` |

Valid `--upload-type` values: `publication`, `poster`, `presentation`, `dataset`, `image`, `video`, `software`, `lesson`, `other`.

---

## 8. Trigger Phrases (for the Skill)

The `zenodo-publish` skill auto-activates when you use any of these in DeepChat:

| Trigger | Example |
|:--------|:--------|
| "publish to Zenodo" | "Publish this paper to Zenodo" |
| "DOI registration" | "I need DOI registration for my dataset" |
| "Zenodo deposition" | "Create a Zenodo deposition for this file" |
| "Zenodo upload" | "Upload this poster to Zenodo" |
| "get a DOI" | "Get a DOI for my presentation" |
| "register DOI" | "Register a DOI for this software release" |
| "Zenodo sandbox" | "Test this in Zenodo sandbox first" |

---

## 9. Files Reference — What's Where

```
G:\My Drive\prompts\zenodo\
├── GUIDE.md                          ← THIS FILE — human-readable install/use guide
├── zenodo-publish.skill              ← Packaged skill (import into DeepChat)
├── zenodo_publish.py                 ← CLI tool (standalone, zero dependencies)
└── skill/zenodo-publish/             ← Skill source directory
    ├── SKILL.md                      ← Skill instructions (for AI agent, not human)
    ├── scripts/zenodo_publish.py     ← Bundled copy of the CLI tool
    └── references/token-setup.md     ← Token creation guide (loaded by AI agent)

G:\My Drive\prompts\templates\
└── ZENODO-PUBLISH.md                 ← Template for future fill_prompt_template use

G:\My Drive\projects\zenodo-automation\
├── zenodo_publish.py                 ← Canonical CLI tool (production copy)
├── test_plan.py                      ← 22-test verification script
├── index.html                        ← Pipeline status dashboard
├── README.md                         ← Project overview
├── SPRINT.md                         ← Sprint tracker
├── CHANGELOG.md                      ← Change log
└── PROJECT STATE.md                  ← Project state summary
```

---

## 10. Troubleshooting

### "ERROR: No Zenodo token provided"

**Fix:** You haven't saved a token. Follow §2 (Token Setup) above. Verify:
```powershell
Test-Path "$env:USERPROFILE\.zenodo_token"
```

### "ERROR: File not found: <path>"

**Fix:** The file path is wrong. Check:
```powershell
Test-Path "<your-file-path>"
```
Use absolute paths. Check for typos, missing extensions, or wrong drive letter.

### "API Error [500]: ..."

**Fix:** This is a Zenodo server-side issue. You cannot fix it from your end.
- Check https://status.zenodo.org/ for service status
- Wait and retry later
- The script and token are fine — do not change them

### "API Error [401]: Unauthorized"

**Fix:** Your token is invalid, expired, or revoked.
- Generate a new token at https://zenodo.org/account/settings/applications/
- Save to `%USERPROFILE%\.zenodo_token` (overwrite the old one)
- Verify with `(Get-Content "$env:USERPROFILE\.zenodo_token").Length` (~60 chars)

### "Upload failed [413]: ..."

**Fix:** File is too large for the upload endpoint.
- For files >100MB, use the Zenodo web UI at https://zenodo.org/uploads
- The CLI tool does not currently support chunked uploads

### Sandbox vs Production Confusion

**Prevention:** Always use `--sandbox` for testing. The environment is clearly labeled in the output.
- Sandbox URL: `https://sandbox.zenodo.org/` — test depositions only
- Production URL: `https://zenodo.org/` — real DOIs, permanent

**If you accidentally created a real DOI when testing:** DOIs cannot be deleted. Contact Zenodo support.

### Unicode/Encoding Errors

**Fix (Windows):** Set console to UTF-8 before running:
```powershell
chcp 65001
python zenodo_publish.py ...
```

### Skill Doesn't Trigger

**Fix:** Make sure the skill is installed (check Skills panel in DeepChat). Use explicit trigger phrases from §8. If still not triggering, use the CLI directly:
```powershell
python "G:\My Drive\projects\zenodo-automation\zenodo_publish.py" --help
```

---

## 11. The Iron Rule

> **Sandbox first. Always.**
>
> A real Zenodo DOI is permanent. There is no undo. Test in sandbox every time, even if you've used the tool before. The `--sandbox` flag takes 2 extra seconds and prevents permanent mistakes.
>
> Only type `PUBLISH` when you are certain the right file is uploaded with the right metadata.

---

*Zenodo DOI Registration v1.0 — One command. Sandbox first. Permanent DOI.*
