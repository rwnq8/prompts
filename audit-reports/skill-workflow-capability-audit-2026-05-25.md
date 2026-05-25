# DeepChat Skills vs GitHub Workflows — Capability Audit & Deprecation Roadmap

**Date:** 2026-05-25  
**Branch:** `feature/skill-workflow-capability-audit`  
**Trigger:** User identified GitHub workflow(s) not functioning correctly; requested deep-dive diagnostic/audit to identify gaps and determine which local DeepChat skills can be fully replicated server-side.  
**Source:** Conversation `8S4PFHlVuu2mtBANYU15x` (exported `G:\My Drive\Downloads\export_deepchat_2026-05-25_18-54-07.md`)

---

## 0. SUMMARY

**Three parallel capability stacks exist — local DeepChat skills, server-side prompt templates, and GitHub Workflows — with significant duplication, version mismatch, and broken references.** The canonical source of truth for scripts is fragmented across three paths:

| Layer | Location | Role |
|:------|:---------|:-----|
| **DeepChat Skills** | `C:\Users\LENOVO\.deepchat\skills\` | Local agent-capability extensions; invoked by the model at runtime |
| **Prompt Templates** | `G:\My Drive\prompts\templates\` | Server-side templates invoked via `fill_prompt_template` |
| **GitHub Workflows** | `G:\My Drive\prompts\.github\workflows\` | CI/CD automation triggered by git events |

**Key finding: At least 5 of 17 DeepChat skills have server-side equivalents (templates or workflows) and can be deprecated locally. However, 3 of those server-side equivalents have critical bugs or are significantly out of date.**

---

## 1. CURRENT STATE — Full Inventory

### 1.1 DeepChat Skills (17 total, at `C:\Users\LENOVO\.deepchat\skills\`)

| # | Skill | Has Server Equivalent? | Deprecatable? | Notes |
|:--|:------|:----------------------|:--------------|:------|
| 1 | `algorithmic-art` | No | No | Pure creative generation — no automation benefit server-side |
| 2 | `code-review` | No | No | Interactive code analysis — needs agent context |
| 3 | `deepchat-settings` | No | No | DeepChat UI settings — inherently local |
| 4 | `doc-coauthoring` | No | No | Interactive co-authoring workflow — needs agent context |
| 5 | `docx` | No | No | Document creation/editing — needs local file access |
| 6 | `frontend-design` | No | No | Interactive UI design — needs agent context |
| 7 | `git-commit` | Partial | Partial | Commit messages can be auto-generated; interactive use cannot |
| 8 | `infographic-syntax-creator` | No | No | DSL generation — no automation benefit |
| 9 | **`markdown-pdf`** | **Yes** | **YES** | Server equivalent: `PDF-BUILDER` template + `pdf-release.yml` workflow |
| 10 | `mcp-builder` | No | No | MCP server building — needs interactive context |
| 11 | `pdf` | No | No | PDF manipulation — needs local file access |
| 12 | `pptx` | No | No | Presentation creation — needs local file access |
| 13 | `skill-creator` | No | No | Meta-skill for creating skills — inherently local |
| 14 | `tufte-viz` | No | No | Visualization critique — needs agent context |
| 15 | `web-artifacts-builder` | No | No | Frontend building — needs agent context |
| 16 | `xlsx` | No | No | Spreadsheet manipulation — needs local file access |
| 17 | **`zenodo-publish`** | **Yes** | **YES** | Server equivalent: `ZENODO-PUBLISH` template + `zenodo-publish.yml` workflow |

### 1.2 Prompt Templates (at `G:\My Drive\prompts\templates\`)

| Template | File | Status |
|:---------|:-----|:-------|
| `ZENODO-PUBLISH` | `templates/ZENODO-PUBLISH.md` | **BROKEN** — references `G:\My Drive\projects\zenodo-automation\zenodo_publish.py` which does NOT exist |
| `PDF-BUILDER` | `templates/PDF-BUILDER-TEMPLATE.md` | OK — references `G:\My Drive\prompts\pdf\build_pdf.py` (valid) |
| Other 20+ templates | Various | Out of scope for this audit |

### 1.3 GitHub Workflows (at `G:\My Drive\prompts\.github\workflows\`)

| Workflow | File | Status | Issues |
|:---------|:-----|:-------|:-------|
| **`pdf-release.yml`** | Build + publish PDF on tag | **OUTDATED** | Uses raw Puppeteer/Node.js instead of canonical `build_pdf.py` pipeline |
| **`zenodo-publish.yml`** | Zenodo DOI on release | **FRAGILE** | Uses raw `curl` + `jq` commands instead of canonical `zenodo_publish.py` |
| **`gitbook-sync.yml`** | GitBook build + gh-pages deploy | **DEPRECATED** | Uses `gitbook-cli` (deprecated). Uses `peaceiris/actions-gh-pages@v3` |
| **`prompts-json-regen.yml`** | Rebuild prompts.json | **FRAGILE** | Inline `python -c` — fragile quoting, no error handling |
| **`system-audit-ci.yml`** | System audit on PR/push | OK | Runs `tools/system_audit.py` (valid path) |

---

## 2. ROOT CAUSE ANALYSIS — What's Actually Broken

### 2.1 F1: `zenodo_publish.py` — Path Does Not Exist (BLOCKING)

**The `ZENODO-PUBLISH` template references `G:\My Drive\projects\zenodo-automation\zenodo_publish.py`.** This directory does not exist. The only copy of `zenodo_publish.py` lives at `C:\Users\LENOVO\.deepchat\skills\zenodo-publish\scripts\zenodo_publish.py`.

**Impact:** When an agent invokes `fill_prompt_template` with `ZENODO-PUBLISH`, the generated instructions point to a non-existent path. The agent will fail at execution time with "file not found."

**Evidence:**
- `G:\My Drive\projects\zenodo-automation` — DOES NOT EXIST [CODE-EXECUTED]
- `zenodo_publish.py` exists ONLY at `C:\Users\LENOVO\.deepchat\skills\zenodo-publish\scripts\zenodo_publish.py` (MD5: `31325784e8a4efffccf191727edb861e`) [CODE-EXECUTED]

### 2.2 F2: `build_pdf.py` — Version Mismatch (MAJOR)

**The `build_pdf.py` in the DeepChat skill directory and the `build_pdf.py` in the prompts directory are DIFFERENT files.** Different MD5 hashes mean different code. The CSS files (`academic.css`, `minimal.css`, `modern.css`) ARE identical between the two locations.

| File | DeepChat Skill MD5 | Prompts Dir MD5 | Match? |
|:-----|:------------------|:----------------|:-------|
| `build_pdf.py` | `e931fa69d49e4a921125e0e9d6d3b1bd` | `48b09bc593e41f422ab37dcb1bb7c64a` | DIFFERENT |
| `academic.css` | `33e7adec154cada166a1aef78bd669d5` | `33e7adec154cada166a1aef78bd669d5` | IDENTICAL |
| `minimal.css` | `e6e1dee31555c1ba47e5805554c55e46` | `e6e1dee31555c1ba47e5805554c55e46` | IDENTICAL |
| `modern.css` | `2193e0a20920b4f31a5f00936b0e0d8e` | `2193e0a20920b4f31a5f00936b0e0d8e` | IDENTICAL |

**Impact:** Agents may get different PDF outputs depending on which `build_pdf.py` they invoke. The canonical version at `G:\My Drive\prompts\pdf\build_pdf.py` should be the single source of truth.

### 2.3 F3: `pdf-release.yml` — Doesn't Use Canonical Pipeline (MAJOR)

The workflow builds PDFs using raw Node.js/Puppeteer with inline CSS — completely bypassing the canonical `build_pdf.py` pipeline that includes:
- YAML frontmatter extraction (title, authors, ORCID, DOI, abstract)
- MathJax 3 LaTeX rendering
- Three CSS presets (academic, modern, minimal)
- Proper A4 formatting with margins

**Impact:** PDFs generated by the GitHub workflow are inferior to PDFs generated locally. The workflow is essentially a toy example, not a production pipeline.

### 2.4 F4: `zenodo-publish.yml` — Doesn't Use Canonical Script (MAJOR)

The workflow uses raw `curl` + `jq` to interact with Zenodo's REST API, bypassing the canonical `zenodo_publish.py` which handles:
- License resolution (YAML frontmatter to CLI flag to default QNFO-1.1)
- Custom license handling via `rights` field
- Sandbox-first testing with proper error messages
- ORCID integration
- Proper deposition lifecycle management

**Impact:** Two independent implementations of the same API surface exist — guaranteed to diverge. The `zenodo-publish.yml` workflow doesn't support custom licenses (QNFO-1.1) properly, doesn't read YAML frontmatter, and doesn't enforce sandbox-first.

### 2.5 F5: `gitbook-sync.yml` — Uses Deprecated Tooling (MINOR)

`gitbook-cli` has been deprecated since 2021. The `peaceiris/actions-gh-pages@v3` action is also outdated. This workflow likely fails silently or produces broken builds.

### 2.6 F6: Unicode Crashes in Local Script Execution (BLOCKING)

**From conversation evidence:** The `zenodo_publish.py` script crashed on Unicode characters (emoji) when invoked from PowerShell (conversation line 3187). This is a recurring issue documented in CROSS-PROJECT-LEARNINGS — the script needs a pre-execution Unicode safety scan (Rule 12).

### 2.7 F7: `ZENODO-PUBLISH` Template Returns Empty Parameters

Both `ZENODO-PUBLISH` and `PDF-BUILDER` return empty parameter lists from `get_prompt_template_parameters`. This may prevent proper parameter passing when templates are invoked programmatically.

### 2.8 F8: No `.zenodo_token` in Workflow Context

The `zenodo-publish.yml` workflow accesses `${{ secrets.ZENODO_SANDBOX_TOKEN }}` and `${{ secrets.ZENODO_TOKEN }}` — but the template instructs agents to read from `%USERPROFILE%\.zenodo_token`. These are different authentication paths. The workflow cannot access the local token file, and the local agent cannot access GitHub secrets. This creates an authentication gap where neither path fully works.

---

## 3. CAPABILITY MATRIX — Local vs Server-Side

| Capability | DeepChat Skill | Prompt Template | GitHub Workflow | Best Implementation |
|:-----------|:--------------|:----------------|:----------------|:--------------------|
| **Markdown to PDF** | `markdown-pdf` | `PDF-BUILDER` | `pdf-release.yml` (broken) | GitHub Workflow (after fix) |
| **Zenodo DOI** | `zenodo-publish` | `ZENODO-PUBLISH` (broken path) | `zenodo-publish.yml` (fragile) | GitHub Workflow (after fix) |
| **GitBook Build** | None | None | `gitbook-sync.yml` (deprecated) | Replace with modern static site generator |
| **System Audit** | None | None | `system-audit-ci.yml` | GitHub Workflow |
| **prompts.json Regen** | None | None | `prompts-json-regen.yml` (fragile) | GitHub Workflow (after fix) |
| **PDF Manipulation** | `pdf` | None | None | Local only (needs file access) |
| **Code Review** | `code-review` | None | None | Local only (needs context) |
| **Creative Generation** | `algorithmic-art`, `frontend-design`, etc. | None | None | Local only (creative tasks) |

---

## 4. DEPRECATION ROADMAP

### 4.1 Skills That CAN Be Fully Deprecated (Replace with Server-Side)

| Skill | Replacement | Prerequisite Fixes |
|:------|:------------|:-------------------|
| **`markdown-pdf`** | `PDF-BUILDER` template + fixed `pdf-release.yml` workflow | F2 (sync `build_pdf.py`), F3 (fix workflow) |
| **`zenodo-publish`** | `ZENODO-PUBLISH` template + fixed `zenodo-publish.yml` workflow | F1 (fix path), F4 (use canonical script), F8 (auth) |

**Deprecation mechanism:** Remove the SKILL.md files from `C:\Users\LENOVO\.deepchat\skills\` and ensure the server-side equivalents work correctly.

### 4.2 Skills That Should Remain Local

All 15 other skills (algorithmic-art, code-review, deepchat-settings, doc-coauthoring, docx, frontend-design, git-commit, infographic-syntax-creator, mcp-builder, pdf, pptx, skill-creator, tufte-viz, web-artifacts-builder, xlsx) require interactive agent context or local file access and cannot be replicated fully server-side.

### 4.3 Skills With Partial Server-Side Equivalents

| Skill | What Can Move Server-Side | What Must Stay Local |
|:------|:--------------------------|:---------------------|
| `git-commit` | Commit message generation rules | Interactive selection, multi-commit workflows |

---

## 5. ENHANCEMENT ROADMAP — Fixes Required

### 5.1 CRITICAL: Fix `ZENODO-PUBLISH` Template Path (F1)

**Action:** Update `templates/ZENODO-PUBLISH.md` to reference the canonical script path. Two options:

**Option A (Recommended):** Move `zenodo_publish.py` to `G:\My Drive\prompts\tools\zenodo_publish.py` and update template to reference `G:\My Drive\prompts\tools\zenodo_publish.py`.

**Option B:** Create `G:\My Drive\projects\zenodo-automation\` directory and copy script there.

**Preference:** Option A — keeps all tools in the `prompts` repo, which is the canonical source of truth.

### 5.2 CRITICAL: Sync `build_pdf.py` Versions (F2)

**Action:** The canonical version at `G:\My Drive\prompts\pdf\build_pdf.py` must be the single source of truth. Overwrite the skill copy at `C:\Users\LENOVO\.deepchat\skills\markdown-pdf\scripts\build_pdf.py` with the canonical version. Add a comment at the top of the skill copy noting "This is a synced copy. Canonical source: `G:\My Drive\prompts\pdf\build_pdf.py`."

### 5.3 CRITICAL: Fix `pdf-release.yml` to Use Canonical Pipeline (F3)

**Current:** Raw Node.js/Puppeteer with inline CSS.
**Target:** Install Python, install `markdown` library, run `python build_pdf.py --input ... --style ...`.

```yaml
# Proposed fix structure:
- uses: actions/setup-python@v5
  with: { python-version: '3.12' }
- run: pip install markdown
- run: python pdf/build_pdf.py --input "${{ inputs.markdown_path }}" --style academic
```

### 5.4 CRITICAL: Fix `zenodo-publish.yml` to Use Canonical Script (F4)

**Current:** Raw `curl` + `jq` commands.
**Target:** Install Python, run `python tools/zenodo_publish.py` (after moving script to prompts/tools/).

The canonical `zenodo_publish.py` already handles:
- Sandbox vs production routing
- Custom license support via `rights` field
- YAML frontmatter license extraction
- Proper error handling and rate limiting

### 5.5 Fix `prompts-json-regen.yml` (F5)

**Current:** Inline `python -c "..."` with fragile quoting.
**Target:** Move the Python logic to a standalone script at `G:\My Drive\prompts\tools\rebuild_prompts_json.py` and invoke it:

```yaml
- run: python tools/rebuild_prompts_json.py
```

### 5.6 Fix `gitbook-sync.yml` (F6)

**Options:**
- Replace GitBook with mdBook (Rust-based, actively maintained)
- Replace with MkDocs + Material theme
- Replace with Hugo static site generator
- Deprecate entirely if GitBook no longer used

### 5.7 Add Unicode Safety to `zenodo_publish.py` (F7)

The script contains characters that crash on Windows cp1252 encoding. Add a pre-execution Unicode safety scan or replace all non-ASCII characters with ASCII-safe alternatives (per Rule 12).

### 5.8 Resolve Authentication Gap (F8)

Two paths exist for Zenodo authentication:
1. **Local agent:** Reads `%USERPROFILE%\.zenodo_token`
2. **GitHub Workflow:** Reads `${{ secrets.ZENODO_TOKEN }}`

**Fix:** The `zenodo_publish.py` script should accept `ZENODO_TOKEN` environment variable as primary, with file-based token as fallback. The workflow already sets this env var. Ensure the template also documents the env var approach.

---

## 6. RECOMMENDED ARCHITECTURE — Single Source of Truth

### 6.1 Script Canonical Locations

| Script | Canonical Path | Workflow Usage | Template Reference |
|:-------|:---------------|:---------------|:-------------------|
| `zenodo_publish.py` | `G:\My Drive\prompts\tools\zenodo_publish.py` | `zenodo-publish.yml` | `ZENODO-PUBLISH` template |
| `build_pdf.py` | `G:\My Drive\prompts\pdf\build_pdf.py` | `pdf-release.yml` | `PDF-BUILDER` template |
| `system_audit.py` | `G:\My Drive\prompts\tools\system_audit.py` | `system-audit-ci.yml` | N/A |
| `rebuild_prompts_json.py` | `G:\My Drive\prompts\tools\rebuild_prompts_json.py` | `prompts-json-regen.yml` | N/A |

### 6.2 Deprecated Skill Removal

After server-side equivalents are verified working:

1. Remove `C:\Users\LENOVO\.deepchat\skills\markdown-pdf\` (keep CSS files in `prompts/pdf/css/` as canonical)
2. Remove `C:\Users\LENOVO\.deepchat\skills\zenodo-publish\` (move scripts to `prompts/tools/`)
3. Update `fill_prompt_template` registrations to point to canonical paths

### 6.3 Verification Checklist

Before deprecating any local skill, verify:

- [ ] Server-side template returns valid instructions (test with `fill_prompt_template`)
- [ ] GitHub workflow completes successfully on a test commit
- [ ] Output quality matches or exceeds local skill output
- [ ] Authentication works end-to-end (sandbox to production)
- [ ] All edge cases handled (missing files, rate limits, API errors)
- [ ] Documentation updated to reflect new canonical paths

---

## 7. FAILURE MODES — What Can Go Wrong Post-Deprecation

| Failure | Detection | Recovery |
|:--------|:----------|:---------|
| Workflow silently fails (no notification) | Check Actions tab after push | Re-enable local skill temporarily |
| Workflow produces different output | Compare MD5 of PDF/DOI metadata | Fix workflow to use canonical script |
| GitHub Actions rate-limited | Workflow queued > 10 min | Use self-hosted runner or reduce frequency |
| Secrets rotation breaks workflow | Zenodo API returns 401 | Update GitHub Secrets, re-run |
| Agent invokes deprecated skill | `skill_view` returns empty/fails | Error message should redirect to template/workflow |
| `zenodo_publish.py` Unicode crash | Windows cp1252 encoding error | Pre-commit Unicode safety scan (Rule 12) |

---

## 8. IMMEDIATE NEXT ACTIONS

### Priority 1 — BLOCKING (Do First)

1. **Fix F1:** Create `G:\My Drive\prompts\tools\zenodo_publish.py` by copying from skill directory, then update `ZENODO-PUBLISH` template to reference new path
2. **Fix F2:** Overwrite `C:\Users\LENOVO\.deepchat\skills\markdown-pdf\scripts\build_pdf.py` with canonical version from `G:\My Drive\prompts\pdf\build_pdf.py`

### Priority 2 — MAJOR (Do Next)

3. **Fix F3:** Rewrite `pdf-release.yml` to use canonical `build_pdf.py`
4. **Fix F4:** Rewrite `zenodo-publish.yml` to use canonical `zenodo_publish.py`
5. **Fix F5:** Extract inline Python from `prompts-json-regen.yml` to standalone script

### Priority 3 — MINOR (Later)

6. **Fix F6:** Deprecate or modernize `gitbook-sync.yml`
7. **Fix F7:** Add Unicode safety scan to `zenodo_publish.py`
8. **Fix F8:** Resolve authentication gap (env var support)

### Priority 4 — DEPRECATION (After Verification)

9. Remove `markdown-pdf` skill after verifying `pdf-release.yml` works
10. Remove `zenodo-publish` skill after verifying `zenodo-publish.yml` works

---

## 9. APPENDIX — Evidence Log

### A1: Path Existence Verification

```
[CODE-EXECUTED] G:\My Drive\projects\zenodo-automation — DOES NOT EXIST
[CODE-EXECUTED] G:\My Drive\prompts\pdf\build_pdf.py — EXISTS (MD5: 48b09bc593e41f422ab37dcb1bb7c64a)
[CODE-EXECUTED] C:\Users\LENOVO\.deepchat\skills\zenodo-publish\scripts\zenodo_publish.py — EXISTS (MD5: 31325784e8a4efffccf191727edb861e)
[CODE-EXECUTED] C:\Users\LENOVO\.deepchat\skills\markdown-pdf\scripts\build_pdf.py — EXISTS (MD5: e931fa69d49e4a921125e0e9d6d3b1bd)
```

### A2: File Hash Comparison

```
[CODE-EXECUTED] build_pdf.py: Skill vs Prompts — DIFFERENT
[CODE-EXECUTED] academic.css: IDENTICAL
[CODE-EXECUTED] minimal.css: IDENTICAL
[CODE-EXECUTED] modern.css: IDENTICAL
```

### A3: Conversation Error Evidence

From `export_deepchat_2026-05-25_18-54-07.md`:
- Line 3187: `zenodo_publish.py` crashed on Unicode/emoji character
- Line 4359: zenodo-publish skill defaults to `cc-by-4.0` (should be QNFO-1.1)
- Lines 3090-3210: Multiple failed attempts to run `zenodo_publish.py` from PowerShell due to encoding issues

---

*Audit complete. Proceed to Priority 1 actions or request user decision on implementation order.*
