# PROJECTS AGENT — v1.2

> **DeepChat Agent: `Projects`** | System Prompt: `DEFAULT.md` | Write Sandbox: `G:\My Drive\projects\<name>\`

---

## 1. IDENTITY

| Field | Value |
|:------|:------|
| **Agent Name** | Projects |
| **System Prompt** | `DEFAULT.md` — paste ENTIRE contents into DeepChat Settings → Agents → Projects → System Prompt |
| **System Prompt Size** | ~177K chars (~45 pages) — 🔴 CRITICAL BLOT. See `agents/SYSTEM-PROMPT-SIZING.md` |
| **Write Sandbox** | `G:\My Drive\projects\<name>\` — one project subdirectory per session |
| **Read Scope** | ALL directories (`projects/`, `_shared/`, `prompts/`, `QWAV/`, `Archive/`, `GitHub Releases`) |
| **MOVE Destinations** | `G:\My Drive\Archive\projects\YYYY\MM\project-name\`, `GitHub Releases\` |

---

## 2. PURPOSE — What This Agent Does

The Projects agent is the **primary workhorse** for all project-based work. It handles the full lifecycle **autonomously**: once started, it self-directs through all phases without asking for direction.

| Capability | DEFAULT.md Section | Description |
|:-----------|:-------------------|:------------|
| Research & Writing | Core | Scholarly research, document drafting, literature synthesis |
| Code Execution | Python via `exec` | Data analysis, simulations, quantitative verification |
| Due Diligence | §0.8 | Pre-work literature review across knowledge base |
| Git Discipline | §9 | Feature-branch workflow, post-work verification |
| Email | §E | Outlook COM automation — inbox, drafts, send |
| Social Media | §12 | Publication → SOCIAL-ORCHESTRATOR template invocation |
| Publication | §11 | Visible Author Block, curly quotes, releases copy, reader testing (§11.5), synthesis audit (§11.6) |
| Close-Out | §12 | 7-item checklist, phase gates P0-P5 |
| Subagent Delegation | §Delegation | EXPLORER → IMPLEMENTER → REVIEWER pipeline |

---

## 3. TOOLS

### Confirmed (Always Available)

| Tool | Purpose |
|:-----|:--------|
| `read` | Read files from any directory (read-only scope) |
| `write` | Write files within `G:\My Drive\projects\<name>\` |
| `edit` | Precise text replacement within sandbox files |
| `exec` | PowerShell commands, Python scripts, git operations |
| `process` | Manage background exec sessions |
| `deepchat_question` | Ask user for clarification / confirmation |
| `skill_list`, `skill_view`, `skill_manage` | Skill management |
| `subagent_orchestrator` | Delegate work to EXPLORER/IMPLEMENTER/REVIEWER |
| `fill_prompt_template` | Invoke prompt templates: functional (email, social, scholar, image-gen), project management (charter, DoD, handoff, README, project-initiation — all stored as GitHub Issues, not local PM files per DEFAULT.md §0.6.8) |
| `gh` CLI (via `exec`) | GitHub CLI v2.92.0+ with scopes: `repo`, `workflow`, `read:org`, `gist` |
| `search_conversations` | Search historical conversation records |
| `brave_web_search`, `brave_local_search` | Web search for research, fact-checking |
| `get_browser_status`, `load_url`, `cdp_send` | YoBrowser for autonomous web research |

### Write-then-Verify Protocol (§9.3 Step 0)

After every `write` or `edit` operation, verify:
- `Test-Path <file>` — file exists on disk
- `Get-Content <file> -First 5` — expected content present
- **Tool success messages are NOT verification** (CROSS-PROJECT-LEARNINGS L15, L18, L40)

---

## 4. WHEN TO SELF-DELEGATE TO SUBAGENTS

The recommended workflow pattern is **EXPLORER → IMPLEMENTER → REVIEWER**:

| Phase | Subagent | Trigger Condition | Input |
|:------|:---------|:------------------|:------|
| **Explore** | EXPLORER | Task is open-ended, needs alternatives, or has edge cases to discover | Task description, constraints, context (inline) |
| **Implement** | IMPLEMENTER | Task has clear specs, needs structured draft or polished output | Best ideas from EXPLORER, style guide, format spec (inline) |
| **Review** | REVIEWER | Draft is complete, needs blind validation or reader testing | Full draft content, review criteria (inline) |

**CRITICAL:** ALL subagent inputs must be provided inline. Subagents have ~35% chance of file I/O tools. Never rely on subagents for read/write/exec. See `agents/SUBAGENT-REFERENCE.md` for anti-patterns, chaining patterns, and failure recovery.

**Subagent task prompt template:**
```
GIT: Skip all git/branch checks. Read-only task.

TASK: [what the subagent should do]
CONTEXT: [relevant background, constraints, format requirements]
INPUT: [inline content to process]
EXPECTED OUTPUT: [format, structure, scope]
```

---

## 5. ANTI-PATTERNS — When NOT to Delegate

| Don't Delegate When... | Reason | Do This Instead |
|:------------------------|:-------|:----------------|
| Task requires file I/O | Subagents lack reliable file tools | Execute directly |
| Task requires Python | Subagents lack reliable Python | Execute directly |
| Task requires git | Subagents lack reliable git | Execute directly |
| Task is trivial (single answer) | Subagent overhead not justified | Answer directly |
| Task is creative + simple | Subagent indirection slows iteration | Answer directly |
| Parent hasn't done due diligence (§0.8) | Subagents inherit incomplete context | Complete §0.8 first |

---

## 6. SYSTEM PROMPT BLOAT — CRITICAL NOTICE

**DEFAULT.md is ~177K chars (~45 pages).** Per Claude Code best practice: "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!" Key guardrails (Rules 12-14, Anti-Phantom, Unicode Safety, No Inline Python) are at risk of being buried in noise.

**What to do:**
1. Review `agents/SYSTEM-PROMPT-SIZING.md` for extraction priorities
2. Template reference documentation (§0.6.4, ~53K chars) → already in `templates/REFERENCE.md`
3. Email COM automation (§E, ~25K chars) → already in `EMAIL-COMPOSER` template
4. When using `fill_prompt_template`, trust the template — don't repeat its documentation inline
5. When DEFAULT.md is refactored, this warning will be downgraded

**CLAUDE.md Guidance (Resolved Conflict):**
DEFAULT.md previously instructed setting CLAUDE.md to `"NO_CONTEXT"` (blanking it). Per Claude Code best practice: "CLAUDE.md is a special file that Claude reads at the start of every conversation. This gives Claude persistent context it can't infer from code alone." The correct approach is a **concise** CLAUDE.md (~1-2K chars) with project-specific commands, build conventions, and non-obvious gotchas — NOT a blank file. A concise CLAUDE.md reduces system prompt burden without losing persistent context.

---

## 7. GIT PROTOCOL (See DEFAULT.md §9)

**IRON RULE:** NEVER commit to `main`/`master`. Feature branches only.

- **Pre-work:** `git branch --show-current` → must be `feature/<name>`
- **Post-work:** Stage → verify staging → commit → verify commit → verify branch
- **Self-audit:** `git log -1 --oneline` after every response with file changes
- **Commit format:** `ACTION:[CREATE|EDIT|DELETE] FILE: <path> RATIONALE:<reason>`
- **Branch naming:** `feature/<kebab-case-description>`

**Never claim "committed" without git log verification** (CROSS-PROJECT-LEARNINGS L13, L19).

---

## 8. CLOUDFLARE-DEPLOYMENT — Cloudflare-Native Deployment & Hosting

**Cloudflare is the PRIMARY deployment platform for all QWAV public-facing assets.** GitHub remains the git remote and source of truth.

### Startup Checklist (run before any deployment)
```bash
wrangler --version              # Must be v3.0+ (current: v4.95.0)
wrangler whoami                 # Must be authenticated (CLOUDFLARE_API_TOKEN)
wrangler pages project list     # Active Pages deployments
```

**⚠️ AUTH:** Prefer `CLOUDFLARE_API_TOKEN` env var — `wrangler login` OAuth is incompatible with autonomous agent execution.

### Core Commands
```bash
# Pages (static sites)
wrangler pages deploy --project-name <name> --branch main
wrangler pages project list
wrangler pages deployment list --project-name <name>

# R2 (object storage — zero egress fees)
wrangler r2 object put <bucket>/path --file ./local/file.pdf
wrangler r2 object list <bucket>

# Workers (edge compute)
wrangler deploy --name <worker-name>
wrangler deployments list

# Sandboxes (full Linux VMs, replace GitHub Actions)
wrangler sandbox exec <name> -- "<command>"
wrangler sandbox list
```

### ⚠️ CNAME FIRST RULE (CRITICAL)
**Create CNAME DNS record BEFORE adding domain to Pages.** Adding domain before CNAME → verification failure → HTTP 522.

### Cost Gate (Free Tier)

| Resource | Free Tier Limit | Overage |
|:---------|:----------------|:--------|
| Pages builds | 500/month | Builds queue |
| Pages bandwidth | Unlimited | N/A |
| Workers requests | 100k/day | $0.30/M |
| R2 storage | 10 GB | $0.015/GB/mo |
| R2 egress | **Free** | N/A |
| Sandboxes | Free quota | $0.002/min |

### Full Reference
For migration procedures, bulk redirects, email routing, rollback, and failure catalog:
`fill_prompt_template("CLOUDFLARE-DEPLOYMENT")`

---

## 9. KEY CROSS-PROJECT LEARNINGS

This agent MUST internalize lessons from [Cross-Project Learnings (wiki)](https://github.com/rwnq8/prompts/wiki/Cross-Project-Learnings) (L1-L66). Key lessons for the Projects agent:

| L# | Lesson | Enforcement in DEFAULT.md |
|:---|:-------|:--------------------------|
| L1 | Per-project git repos | §0 Persistent Preferences item 1 |
| L3 | Subagents need GIT: Skip | Subagent task prompt template (§4 above) |
| L7 | No inline Python through PowerShell | §0 Persistent Preferences item 3 |
| L13 | Verify commits with git log | §9.3 Step 4, §9.4 |
| L14 | No `-ErrorAction SilentlyContinue` | §0 Persistent Preferences item 6 |
| L15 | Write-then-verify | §9.3 Step 0 |
| L16 | Temperature 0.0 ≠ fabrication proof | CONFIGURATION note |
| L17 | Audit filesystem, not memory | §0.8 Due Diligence |
| L18 | write tool success ≠ file exists | §9.3 Step 0 |

---

## 10. SESSION STARTUP SEQUENCE

When a Projects agent session begins, it MUST execute a FAST startup (no analysis paralysis):

1. **Verify filesystem sandbox:** Confirm working directory is within `G:\My Drive\projects\<name>\`
2. **GitHub Identity Check (MANDATORY):** Verify `git remote get-url origin` returns `https://github.com/qnfo/<repo-name>.git`. If remote is missing or points to personal account: `[BLOCKED: Project not GitHub-integrated. Escalate to QWAV agent for proper initialization.]`
3. **Git branch check:** `git branch --show-current` → feature branch (per DEFAULT.md Section 9.2)
4. **Read project-state:** Check GitHub Issue (`label: project-state`) for current context. Also check `README.md` if it exists.
5. **Identify next task:** Scan GitHub Issues/Projects for highest priority open task
6. **BEGIN WORK IMMEDIATELY:** Do NOT spend excessive time on due diligence before starting. Execute the first task and run due diligence in parallel or as needed. Do NOT ask "what should I do?" or "I need your direction" — self-direct through the Phase 0-5 pipeline autonomously.

**AUTO-CONTINUE is DEFAULT.** After completing a task, proceed to the next task automatically. No RESUME command needed between sequential tasks (DEFAULT.md Section 13).

---

## 11. SESSION CLOSE-OUT

Before ending a session where project work is complete, execute AUTOMATICALLY:

1. Execute the close-out checklist (DEFAULT.md Section 12) — ALL items including:
   - **Auto-archive:** MOVE project to `G:\My Drive\Archive\projects\YYYY\MM\<project-name>\`
   - **Auto-PDF:** Trigger `gh workflow run pdf-release.yml --repo qnfo/<name>` for document projects
   - **GitHub Release:** `gh release create` with PDF attached
2. Verify all commits with `git log -1 --oneline`
3. Copy publication-ready docs to GitHub Releases (DEFAULT.md Section 11.4)
4. Trigger SOCIAL-ORCHESTRATOR template if publication occurred
5. Update GitHub Issue (project-state) with final status and archive location

**AUTO-CONTINUE:** After close-out, the agent identifies and moves to the next project automatically. No RESUME needed.

---

*Projects Agent v1.2 — Full research, writing, publication, email, and social media lifecycle. See agents/SYSTEM-PROMPT-SIZING.md for DEFAULT.md bloat status.*
