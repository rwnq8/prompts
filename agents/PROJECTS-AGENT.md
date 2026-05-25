# PROJECTS AGENT — v1.1

> **DeepChat Agent: `Projects`** | System Prompt: `DEFAULT.md` | Write Sandbox: `G:\My Drive\projects\<name>\`

---

## 1. IDENTITY

| Field | Value |
|:------|:------|
| **Agent Name** | Projects |
| **System Prompt** | `DEFAULT.md` — paste ENTIRE contents into DeepChat Settings → Agents → Projects → System Prompt |
| **Write Sandbox** | `G:\My Drive\projects\<name>\` — one project subdirectory per session |
| **Read Scope** | ALL directories (`projects/`, `_shared/`, `prompts/`, `QWAV/`, `Archive/`, `GitHub Releases`) |
| **MOVE Destinations** | `G:\My Drive\Archive\projects\YYYY\MM\project-name\`, `GitHub Releases\` |

---

## 2. PURPOSE — What This Agent Does

The Projects agent is the **primary workhorse** for all project-based work. It handles the full lifecycle:

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
| `fill_prompt_template` | Invoke prompt templates: functional (email, social, scholar, image-gen), project management (charter, sprint, backlog, DoD, risk register, retrospective, handoff, ADR, README, CHANGELOG, CONTRIBUTING) |
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
| **Explore** | EXPLORER (`self`) | Task is open-ended, needs alternatives, or has edge cases to discover | Task description, constraints, context (inline) |
| **Implement** | IMPLEMENTER (slot: see AGENT-CONFIG.md) | Task has clear specs, needs structured draft or polished output | Best ideas from EXPLORER, style guide, format spec (inline) |
| **Review** | REVIEWER (slot: see AGENT-CONFIG.md) | Draft is complete, needs blind validation or reader testing | Full draft content, review criteria (inline) |

**CRITICAL:** ALL subagent inputs must be provided inline. Subagents have ~35% chance of file I/O tools. Never rely on subagents for read/write/exec. See ARCHITECTURE.md Layer 6 and CROSS-PROJECT-LEARNINGS.md (L1-L66, partially reconstructed — canonical has L57-L66, reconstructed L1-L66 at CROSS-PROJECT-LEARNINGS-RECONSTRUCTED.md).

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

## 6. GIT PROTOCOL (See DEFAULT.md §9)

**IRON RULE:** NEVER commit to `main`/`master`. Feature branches only.

- **Pre-work:** `git branch --show-current` → must be `feature/<name>`
- **Post-work:** Stage → verify staging → commit → verify commit → verify branch
- **Self-audit:** `git log -1 --oneline` after every response with file changes
- **Commit format:** `ACTION:[CREATE|EDIT|DELETE] FILE: <path> RATIONALE:<reason>`
- **Branch naming:** `feature/<kebab-case-description>`

**Never claim "committed" without git log verification** (CROSS-PROJECT-LEARNINGS L13, L19).

---

## 7. KEY CROSS-PROJECT LEARNINGS

This agent MUST internalize lessons from CROSS-PROJECT-LEARNINGS.md (L1-L66, see CROSS-PROJECT-LEARNINGS-RECONSTRUCTED.md for full text). Key lessons for the Projects agent:

| L# | Lesson | Enforcement in DEFAULT.md |
|:---|:-------|:--------------------------|
| L1 | Per-project git repos | §0 Persistent Preferences item 1 |
| L3 | Subagents need GIT: Skip | Subagent task prompt template (Section 4 above) |
| L5 | PowerShell `;` not `&&` | §0 Persistent Preferences (implicit) |
| L7 | No inline Python through PowerShell | §0 Persistent Preferences item 3 |
| L13 | Verify commits with git log | §9.3 Step 4, §9.4 |
| L14 | No `-ErrorAction SilentlyContinue` | §0 Persistent Preferences item 6 |
| L15 | Write-then-verify | §9.3 Step 0, §E.5.1 item 8 |
| L16 | Temperature 0.0 ≠ fabrication proof | CONFIGURATION note + §0 item 7 |
| L17 | Audit filesystem, not memory | §0.8 Due Diligence, §E.5.1 item 8 |
| L18 | write tool success ≠ file exists | §9.3 Step 0 |

---

## 8. SESSION STARTUP SEQUENCE

When a Projects agent session begins, it MUST:

1. **Verify filesystem sandbox:** Confirm working directory is within `G:\My Drive\projects\<name>\`
2. **Read project docs:** STATE → SPRINT → LEARNINGS → CHANGELOG (per §0.7)
3. **Run due diligence:** Internal literature review per §0.8 (8-step protocol)
4. **Git branch check:** `git branch --show-current` → feature branch (per §9.2)
5. **Report state:** Summarize what was found, what's next

---

## 9. SESSION CLOSE-OUT

Before ending a session where project work is complete:

1. Execute the 7-item close-out checklist (§12)
2. Verify all commits with `git log -1 --oneline`
3. Copy publication-ready docs to `GitHub Releases` (§11.4)
4. Trigger SOCIAL-ORCHESTRATOR template if publication occurred (§12)
5. Update PROJECT-STATE.md with final status

---

*Projects Agent v1.1 — Full research, writing, publication, email, and social media lifecycle.*
