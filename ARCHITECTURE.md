# ARCHITECTURE.md — System Taxonomy & Agent Configuration (v1.4)

> **Source of truth for system structure, slot IDs, sandboxing model, and agent roles.**
> Referenced by META-PROMPT-DEEPSEEK.md §0, DEFAULT.md §0.6.5, and all agent execution specs.

---

## 1. Taxonomy — 3-Agent System

The system comprises three specialized agents, each with a dedicated system prompt, write sandbox, and role:

| # | Agent Name | System Prompt | Write Sandbox | Role |
|:--|:-----------|:-------------|:---------------|:-----|
| 1 | **Projects** | `DEFAULT.md` | `G:\My Drive\projects\<name>\` | Primary workhorse — research, code, document creation, project execution |
| 2 | **QWAV** | `QWAV-DEFAULT.md` | `G:\My Drive\QWAV\` | Portfolio/Program Manager — cross-project coordination, initiation, quality gates |
| 3 | **Prompts** | `META-PROMPT-DEEPSEEK.md` | `G:\My Drive\prompts\` | System Prompt Generator — creates and maintains prompts, templates, architecture |

### Agent Relationship Model

```
┌─────────────────────────────────────────────────────────────┐
│                       QWAV (Program)                         │
│  Portfolio management, project initiation, quality gates     │
│  Coordinates: Issues (program label), QWAV Program Board      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌──────────────────────────────────┐ │
│  │  Projects Agent   │  │        Prompts Agent              │ │
│  │  (Project-level)  │  │     (System Factory)              │ │
│  │  DEFAULT.md       │  │  META-PROMPT-DEEPSEEK.md         │ │
│  └──────────────────┘  └──────────────────────────────────┘ │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

- **QWAV → Projects:** Initiates projects via §0.9.1 Protocol, hands off via §0.9.2 Handoff
- **QWAV → Prompts:** Creates `meta`-labeled Issues for systemic prompt improvements
- **Prompts → All:** Generates and maintains the system prompts all agents use
- **Projects → Prompts:** Reports systemic gaps via CROSS-PROJECT-LEARNINGS

---

## 2. Subagent Architecture — Self-Clone Slots

Each agent has 3 self-clone subagent slots (EXPLORER, IMPLEMENTER, REVIEWER) with ~35% tool reliability. The actual slot IDs are agent-dependent — see AGENT-CONFIG.md for per-agent values.

| Role | Purpose | Tool Reliability |
|:-----|:--------|:-----------------|
| **EXPLORER** (`self`) | Divergent thinking — brainstorming, alternatives, edge cases | ~35% file I/O |
| **IMPLEMENTER** | Convergent execution — drafting, structured output | ~35% file I/O |
| **REVIEWER** | Critical evaluation — blind validation, gap analysis, fabrication audit | ~35% file I/O |

### Subagent Protocol

- **ALL inputs must be provided inline.** Subagents cannot reliably read files.
- **Parent handles ALL file I/O, Python, and git.** Subagents return text only.
- **GIT: Skip directive** required in every subagent task prompt.
- **Subagent output truncation at ~32K tokens** (CPL L39) — break long tasks into sections.

### Recommended Workflow

```
EXPLORER (alternatives) → IMPLEMENTER (draft) → REVIEWER (validate)
    ↓                         ↓                      ↓
PARENT reads                PARENT reads           PARENT reads
subagent output             subagent output        subagent output
    ↓                         ↓                      ↓
PARENT selects              PARENT writes           PARENT addresses
best alternative            draft to disk           review findings
```

---

## 3. Sandboxing Model

### Principle: Agent = Filesystem Write Boundary

Each agent writes ONLY to its assigned sandbox. Cross-sandbox writes are forbidden.

| Agent | Write Sandbox | Read Scope |
|:------|:-------------|:-----------|
| Projects | `G:\My Drive\projects\<name>\` | ALL directories + GitHub Releases |
| QWAV | `G:\My Drive\QWAV\` | ALL directories + GitHub Releases |
| Prompts | `G:\My Drive\prompts\` | `G:\My Drive\prompts\` + `G:\My Drive\projects\_shared\` |

### MOVE Permissions

Agents may MOVE completed work OUT of their sandbox INTO read-only destinations:

| From | To | Purpose |
|:-----|:---|:--------|
| `projects\<name>\` | `Archive\projects\YYYY\MM\project-name\` | Archive completed project |
| `projects\<name>\` | GitHub Releases | Publish finalized research |
| `prompts\` | `Archive\prompts\` | Archive deprecated prompts |
| `QWAV\` | `Archive\QWAV\` | Archive completed QWAV work |

**HARD RULE:** NEVER write directly to `Archive\` or GitHub Releases. ONLY move into them.
**BLOCKING:** ANY move to GitHub Releases requires EXPLICIT USER APPROVAL.

---

## 4. GitHub-Native Project Management

### Organization: `qnfo` (MANDATORY)

ALL project repos must be created under the `qnfo` GitHub organization. NEVER create repos under personal accounts.

```
gh repo create qnfo/<repo-name> --public
```

### GitHub Features Used

| Feature | Replaces | Purpose |
|:--------|:---------|:--------|
| **Issues** | BACKLOG.md, PROJECT STATE.md | Task tracking, state management |
| **Projects** | SPRINT.md | Kanban sprint boards |
| **Releases** | CHANGELOG.md | Version-tagged releases |
| **Discussions** | DECISIONS.md | Architecture decisions, Q&A |
| **Wiki** | LEARNINGS.md, docs | Program documentation |

### Deprecated Files (NEVER CREATE)

Per DEFAULT.md §0.6.8 File Deprecation Map:
- `PROJECT STATE.md`, `SPRINT.md`, `BACKLOG.md`, `CHANGELOG.md`, `LEARNINGS.md`, `DECISIONS.md`
- `PROJECT-INITIATION.md`, `CHARTER.md`, `DEFINITION-OF-DONE.md`, `RISK-REGISTER.md`

---

## 5. Directory Structure

```
prompts\                          ← System prompt engineering workspace
├── README.md                     ← Human reference (repo landing page)
├── ARCHITECTURE.md               ← THIS FILE — system taxonomy
├── AGENT-CONFIG.md               ← Agent configuration details
├── DEFAULT.md                    ← System prompt for Projects agent
├── QWAV-DEFAULT.md               ← System prompt for QWAV (Program) agent
├── META-PROMPT-DEEPSEEK.md       ← System Prompt Generator (the factory)
├── prompts.json                  ← Auto-generated prompt template cache
│
├── agents\                       ← Agent execution specs (LLM reference)
│   ├── PROJECTS-AGENT.md
│   ├── QWAV-AGENT.md
│   ├── PROMPTS-AGENT.md
│   └── subagents\
│       ├── EXPLORER-SUBAGENT.md
│       ├── IMPLEMENTER-SUBAGENT.md
│       └── REVIEWER-SUBAGENT.md
│
├── templates\                    ← Prompt templates (consumed via fill_prompt_template)
│   ├── DEFINITION-OF-DONE.md
│   ├── HANDOFF.md
│   ├── PROJECT-CHARTER.md
│   ├── PROJECT-INITIATION.md
│   ├── CLOSEOUT-CHECKLIST.md
│   ├── SOCIAL-ORCHESTRATOR-TEMPLATE.md
│   ├── EMAIL-AGENT-TEMPLATE.md
│   ├── PDF-BUILDER-TEMPLATE.md
│   └── ZENODO-PUBLISH.md
│
├── email\                        ← Email agent templates + workflow
├── scholar\                      ← Scholar pipeline (4-stage research)
├── pdf\                          ← PDF builder workflow
├── tools\                        ← Utility scripts
├── audit-reports\                ← DEPRECATED — use GitHub Issues (label: audit)
├── .github\
│   ├── workflows\               ← CI/CD (GitHub Actions)
│   └── ISSUE_TEMPLATE\           ← GitHub Issue templates
└── LICENSE
```

---

## 6. Tool Availability Matrix

### All Agents (Always Available)

| Tool | Purpose |
|:-----|:--------|
| `read`, `write`, `edit` | File I/O (within sandbox) |
| `exec`, `process` | Shell commands, Python, git |
| `gh` CLI (via exec) | GitHub Issues, Projects, Releases, PRs |
| `deepchat_question` | User interaction |
| `brave_web_search`, `brave_local_search` | Web search |
| `get_browser_status`, `load_url`, `cdp_send` | YoBrowser autonomous research |
| `fill_prompt_template` | Template invocation |
| `subagent_orchestrator` | Delegate to EXPLORER/IMPLEMENTER/REVIEWER |
| `skill_list`, `skill_view`, `skill_manage` | Skill management |
| `search_conversations` | Search historical conversations |

### Additional per-agent tools listed in AGENT-CONFIG.md §2.

---

## 7. Version History

| Version | Date | Changes |
|:--------|:-----|:--------|
| v1.4 | 2026-05-27 | Initial creation — synthesized from DEFAULT.md, QWAV-DEFAULT.md, META-PROMPT, and agents/ |
