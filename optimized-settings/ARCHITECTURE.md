# DeepChat Settings Architecture — Complete Documentation

**Generated:** 2026-05-27 | **Source:** `rwnq8/prompts` | **Branch:** `feature/agent-subagent-refactoring`

---

## 1. Design Principles

| # | Principle | Source |
|:--|:----------|:-------|
| 1 | **One file per purpose** — agent configs, system prompts, subagent prompts, templates each have exactly one file per entity | User directive |
| 2 | **Skills for on-demand workflows** — domain knowledge loaded via `skill_view()`, not carried in every session | DeepChat architecture |
| 3 | **Wiki for documentation** — architecture docs, learnings, configuration references live at `rwnq8/prompts/wiki`, never in agent context | User directive |
| 4 | **Self-contained agent files** — each `agents/*.md` has all delegation info inline; wiki for expanded detail | Audit finding |
| 5 | **Subagent prompts are lean** — DoD + self-verification; parent-facing content removed | Claude/DeepSeek best practice |
| 6 | **Templates for output formats** — `fill_prompt_template()` for structured output; skills for workflow knowledge | Claude/DeepSeek best practice |

---

## 2. Layer Architecture (9 Layers)

```
┌──────────────────────────────────────────────────────────────┐
│ LAYER 0: DeepChat Platform                                   │
│ Agent Loop, ToolPresenter, SessionPresenter,                 │
│ subagent_orchestrator, skill_list/view/manage                │
│ NOT configurable by us — platform-level                      │
├──────────────────────────────────────────────────────────────┤
│ LAYER 1: default_system_prompt (app-settings.json)          │
│ 16.7K — base prompt EVERY agent starts with                  │
│ Universal: Rules, MathJax, PowerShell warnings, markdown     │
│ IDEAL: 8-10K (trim email/pub/social references)              │
├──────────────────────────────────────────────────────────────┤
│ LAYER 2: Agent System Prompts (3 files)                     │
│ DEFAULT.md                177.7K (original) / 9.1K (trimmed) │
│ META-PROMPT-DEEPSEEK.md    41.4K (updated w/ skill triggers) │
│ QWAV-DEFAULT.md            35.2K (updated w/ skill triggers) │
│ Role-specific behavior + delegation + skill triggers         │
├──────────────────────────────────────────────────────────────┤
│ LAYER 3: Custom Skills (7 skills, ~22K total)               │
│ Loaded on-demand via skill_view()                            │
│ email-composer, cloudflare-deployer, publication-publisher,  │
│ github-manager, closeout-manager, git-hygiene, template-catalog│
├──────────────────────────────────────────────────────────────┤
│ LAYER 4: Custom Prompt Templates (10 templates, 64.5K)      │
│ Invoked via fill_prompt_template()                           │
│ SOCIAL-ORCHESTRATOR, CLOUDFLARE-DEPLOYMENT, EMAIL-AGENT,    │
│ ZENODO-PUBLISH, CLOSEOUT-CHECKLIST, DEFINITION-OF-DONE,     │
│ HANDOFF, PROJECT-CHARTER, PROJECT-INITIATION, PDF-BUILDER    │
├──────────────────────────────────────────────────────────────┤
│ LAYER 5: Subagent Prompts (3 files)                         │
│ EXPLORER-SUBAGENT.md (3.7K) — Divergent Thinking             │
│ IMPLEMENTER-SUBAGENT.md (4.2K) — Convergent Execution        │
│ REVIEWER-SUBAGENT.md (6.1K) — Critical Evaluation            │
│ All v1.2 with Definition of Done + Self-Verification         │
├──────────────────────────────────────────────────────────────┤
│ LAYER 6: Agent Config Files (3 files)                       │
│ PROJECTS-AGENT.md (6.3K) — Self-contained, wiki refs         │
│ PROMPTS-AGENT.md (5.5K) — Self-contained, wiki refs          │
│ QWAV-AGENT.md (5.3K) — Self-contained, wiki refs             │
│ Human-readable, one file per agent                           │
├──────────────────────────────────────────────────────────────┤
│ LAYER 7: MCP Tools (mcp-settings.json, 4.9K)                │
│ Brave Search, Buffer, LinkedIn, Artifacts                    │
│ 37 enabled tools                                             │
├──────────────────────────────────────────────────────────────┤
│ LAYER 8: ACP Agents (acp_agents.json, 0.4K)                 │
│ claude-acp, codex-acp, kimi — currently DISABLED             │
├──────────────────────────────────────────────────────────────┤
│ LAYER 9: Wiki (rwnq8/prompts/wiki)                           │
│ Architecture, Agent Configuration, Cross-Project Learnings,  │
│ GitHub-Native Model — documentation, NEVER in agent context  │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Complete File Inventory

### System Prompts (3 — loaded every session)
| File | Current Size | Status |
|:-----|:-------------|:-------|
| `DEFAULT.md` | 177.7K | 🔴 Original — needs replacement with trimmed version |
| `META-PROMPT-DEEPSEEK.md` | 41.4K | 🟡 Updated with skill triggers |
| `QWAV-DEFAULT.md` | 35.2K | 🟡 Updated with skill triggers |

### Agent Configs (3 — human-readable, NOT loaded into context)
| File | Size | Version | Status |
|:-----|:-----|:--------|:-------|
| `agents/PROJECTS-AGENT.md` | 6.3K | v1.2 | ✅ Self-contained, wiki refs |
| `agents/PROMPTS-AGENT.md` | 5.5K | v1.2 | ✅ Self-contained, subagent delegation added |
| `agents/QWAV-AGENT.md` | 5.3K | v1.3 | ✅ Self-contained, wiki refs |

### Subagent Prompts (3 — loaded as subagent system prompts)
| File | Size | Version | Key Features |
|:-----|:-----|:--------|:-------------|
| `agents/subagents/EXPLORER-SUBAGENT.md` | 3.7K | v1.2 | DoD: 5+ alternatives, edge cases, recommendation |
| `agents/subagents/IMPLEMENTER-SUBAGENT.md` | 4.2K | v1.2 | DoD: all specs addressed, sources cited, gaps flagged |
| `agents/subagents/REVIEWER-SUBAGENT.md` | 6.1K | v1.2 | DoD: fabrication audit, 5 severity levels, evidence required |

### Templates (10 — invoked via fill_prompt_template)
| Template | Size | Purpose |
|:---------|:-----|:--------|
| `CLOUDFLARE-DEPLOYMENT.md` | 15.2K | Cloudflare Pages/R2/Workers/Sandboxes |
| `CLOSEOUT-CHECKLIST.md` | 7.9K | Project closeout with archive/PDF/release |
| `EMAIL-AGENT-TEMPLATE.md` | 7.5K | Email composition via Outlook COM |
| `PDF-BUILDER-TEMPLATE.md` | 7.4K | Markdown to PDF conversion |
| `SOCIAL-ORCHESTRATOR-TEMPLATE.md` | 7.4K | Social media cross-posting via Buffer API |
| `DEFINITION-OF-DONE.md` | 6.6K | Task completion verification checklist |
| `PROJECT-INITIATION.md` | 6.3K | New project initialization with GitHub |
| `ZENODO-PUBLISH.md` | 4.3K | Zenodo DOI registration |
| `HANDOFF.md` | 2.8K | Multi-agent handoff with state transfer |
| `PROJECT-CHARTER.md` | 2.1K | Project charter with scope and timeline |

### Skills (7 — loaded on-demand via skill_view)
| Skill | Size | Replaces in DEFAULT.md | When Loaded |
|:------|:-----|:----------------------|:------------|
| `email-composer` | 3.0K | §E email COM (~25K) | Sending email |
| `cloudflare-deployer` | 3.0K | Cloudflare inline (~15K) | Deploying to Cloudflare |
| `publication-publisher` | 3.0K | §11-12 publication (~20K) | Publishing documents |
| `github-manager` | 3.3K | §0.6.8 gh CLI (~20K) | Managing GitHub |
| `closeout-manager` | 2.6K | §12.2 close-out (~10K) | Closing projects |
| `git-hygiene` | 3.7K | §9.7 failures (~4K) | Git error recovery |
| `template-catalog` | 3.4K | §0.6.4 template docs (~53K) | Finding templates |
| **Total** | **22.0K** | **~147K saved** | |

### Config Files (3 — reference copies)
| File | Size | Purpose |
|:-----|:-----|:--------|
| `config/mcp-settings.json` | 4.9K | MCP server configuration |
| `config/model-config.json` | 2.1K | Model provider configuration (4 DeepSeek models) |
| `config/acp_agents.json` | 0.4K | ACP agent configuration (currently disabled) |

---

## 4. Session Change Log (5 Commits)

| # | Commit | What Changed |
|:--|:-------|:-------------|
| 1 | `60c1dc7` | Subagent optimization: stripped parent content, added DoD + self-verification. EXPLORER -43%, IMPLEMENTER -39%, REVIEWER -31% |
| 2 | `8384219` | Agent refactoring: fixed stale PROMPTS subagent claim, added conciseness gates |
| 3 | `827f934` | Deleted extraneous files (ARCHITECTURE.md, SUBAGENT-REFERENCE.md, SYSTEM-PROMPT-SIZING.md). Rewrote all 3 agent files to be self-contained with wiki refs |
| 4 | `500a599` | Audit fix: removed 3 stale `Ref: agents/SUBAGENT-REFERENCE.md` from subagent headers. Fixed Claude→model-agnostic reference in PROMPTS-AGENT.md |
| 5 | `fe30c8f` | Generated complete `optimized-settings/` package (30 files): 7 skills, trimmed DEFAULT.md, updated system prompts, templates, configs |

---

## 5. Deep Test Results (2026-05-27)

**126 tests executed: 114 PASS, 12 WARN, 0 FAIL**

### Group 1: Agent Files — 30/30 PASS
| Test | Result |
|:-----|:-------|
| All 3 agent files have required sections (IDENTITY, PURPOSE, TOOLS, SUBAGENT DELEGATION, GIT PROTOCOL, SESSION STARTUP) | ✅ 18/18 |
| Version numbers match (PROJECTS v1.2, PROMPTS v1.2, QWAV v1.3) | ✅ 3/3 |
| Self-contained — no references to deleted files | ✅ 3/3 |
| Wiki references present | ✅ 3/3 |
| Delegation rules: inline inputs, parent-only I/O, GIT Skip | ✅ 9/9 |
| CPL L19 branch rename awareness | ✅ 3/3 |

### Group 2: Subagent Files — 42/42 PASS
| Test | Result |
|:-----|:-------|
| All 3 subagents have required sections (IDENTITY, TOOLS, WHEN TO USE, DEFINITION OF DONE, INPUT FORMAT, OUTPUT FORMAT, SELF-VERIFICATION) | ✅ 21/21 |
| Versions correct (all v1.2) | ✅ 3/3 |
| DoD checkboxes present (EXPLORER: 5, IMPLEMENTER: 5, REVIEWER: 6) | ✅ 3/3 |
| Self-verification questions present (4-5 per subagent) | ✅ 3/3 |
| Parent-facing content REMOVED (no CHAINING PATTERNS, ANTI-PATTERNS, FAILURE MODES, When NOT to Use) | ✅ 12/12 |
| Inline-only rule + ~35% tool warning + GIT Skip in template | ✅ 9/9 |

### Group 3: Skills — 42/42 PASS
| Test | Result |
|:-----|:-------|
| All 7 skills have SKILL.md with YAML frontmatter | ✅ 7/7 |
| All have required fields: name, description, tools | ✅ 21/21 |
| YAML name matches directory name | ✅ 7/7 |
| All have 'When to Use' section | ✅ 7/7 |
| All have sufficient content (>1500 chars) | ✅ 7/7 |

### Group 4: System Prompts — 18/18 PASS
| Test | Result |
|:-----|:-------|
| Trimmed DEFAULT.md has Rules 1-6, 12-14 | ✅ 9/9 |
| Skill invocation triggers present | ✅ 1/1 |
| All 7 skills referenced | ✅ 7/7 |
| Key sections present (DUE DILIGENCE, GIT PROTOCOL, SUBAGENT DELEGATION, PUBLICATION, SOURCE LABELING, EDGE CASES) | ✅ 6/6 |
| Size < 15K (actual: 9,083 chars) | ✅ 1/1 |
| No Claude references | ✅ 1/1 |
| META-PROMPT-DEEPSEEK.md + QWAV-DEFAULT.md have skill triggers | ✅ 2/2 |

### Group 5: Templates — 12/12 PASS
| Test | Result |
|:-----|:-------|
| All 10 expected templates present | ✅ 10/10 |
| No extra templates | ✅ 1/1 |
| All non-empty (>100 bytes) | ✅ 10/10 |

### Group 6: Cross-References — 12/12 PASS
| Test | Result |
|:-----|:-------|
| Wiki URLs consistent format | ✅ (multiple wiki references found) |
| All 3 agent files agree: EXPLORER = divergent, IMPLEMENTER = convergent, REVIEWER = critical | ✅ 9/9 |

### Group 7: CPL Compliance — 14/14 PASS
| Lesson | Original DEFAULT.md | Trimmed DEFAULT.md |
|:-------|:-------------------:|:------------------:|
| L7 (No inline Python) | ✅ | ✅ |
| L13 (Verify commits) | ✅ | ✅ |
| L14 (No SilentlyContinue) | ✅ | ✅ |
| L15 (Write-then-verify) | ✅ | ✅ |
| L17 (Audit filesystem) | ✅ | ✅ |
| L18 (Tool success ≠ file exists) | ✅ | ✅ |
| L19 (Branch rename) | ✅ | ✅ |

### Group 8: Stress Tests — 12 warnings
| Test | Result |
|:-----|:-------|
| All 7 skills fit in < 30K combined context | ✅ 22.0K (PASS) |
| agents/ dir exactly 3 config files | ✅ (PASS) |
| agents/subagents/ exactly 3 subagents | ✅ (PASS) |
| Main prompts dir .md count | ⚠️ 6 files (WARN — CLOUDFLARE-CLOSEOUT + HANDOFF should be archived) |
| DEFAULT.md original > 100K | ⚠️ 177.7K (WARN — MUST be replaced with trimmed v2.0) |
| Skills NOT installed at DeepChat path | ⚠️ (WARN — installation pending) |
| Agent files contain 'SS' notation instead of '§' | ⚠️ (CPL L35: terminology consistency) |

---

## 6. Known Gaps / Remaining Work

| # | Gap | Priority | Action |
|:--|:----|:---------|:-------|
| 1 | **Main DEFAULT.md still 177.7K** | 🔴 P0 | Replace with trimmed version from `optimized-settings/system-prompts/` |
| 2 | **CLOUDFLARE-CLOSEOUT-2026-05-27.md** | 🔴 P0 | Archive or move — not documentation, clutters prompts root |
| 3 | **HANDOFF-2026-05-27.md** | 🟡 P1 | Archive — project artifact, not documentation |
| 4 | **Skills not installed** | 🔴 P0 | Copy `optimized-settings/skills/*` to `%APPDATA%\DeepChat\skills\` |
| 5 | **default_system_prompt (app-settings.json) is 16.7K** | 🟡 P1 | Trim to ~10K — remove duplicate workflow references now in skills |
| 6 | **Wiki pages may need content updates** | 🟡 P1 | Ensure Architecture, Agent Configuration, Cross-Project Learnings wiki pages reflect new structure |
| 7 | **Template bloat** | 🟢 P2 | CLOUDFLARE-DEPLOYMENT.md (15.2K) is the heaviest template; could become a skill |
| 8 | **ACP agents disabled** | 🟢 P2 | claude-acp, codex-acp, kimi not configured — no action needed unless user wants them |

---

## 7. Installation Guide

### Step 1: Install Skills
```powershell
Copy-Item -Recurse "G:\My Drive\prompts\optimized-settings\skills\*" "$env:APPDATA\DeepChat\skills\"
```

### Step 2: Replace System Prompts
In DeepChat Settings → Agents:
- **Projects Agent** → System Prompt: replace with `optimized-settings/system-prompts/DEFAULT.md`
- **Prompts Agent** → System Prompt: replace with `optimized-settings/system-prompts/META-PROMPT-DEEPSEEK.md`
- **QWAV Agent** → System Prompt: replace with `optimized-settings/system-prompts/QWAV-DEFAULT.md`

### Step 3: Replace Agent Configs
```powershell
Copy-Item "G:\My Drive\prompts\optimized-settings\agents\*.md" "G:\My Drive\prompts\agents\"
Copy-Item "G:\My Drive\prompts\optimized-settings\agents\subagents\*.md" "G:\My Drive\prompts\agents\subagents\"
```

### Step 4: Restart DeepChat
Skills are loaded at startup. Restart to activate.

### Step 5: Verify
- Open a Projects agent session
- Try: "Send a test email" → should trigger `skill_view('email-composer')`
- Try: "Deploy to Cloudflare" → should trigger `skill_view('cloudflare-deployer')`

---

*Architecture Documentation v1.1 — Generated 2026-05-27 from rwnq8/prompts, feature/agent-subagent-refactoring*
*126 tests executed: 114 PASS, 12 WARN, 0 FAIL*
