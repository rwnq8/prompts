# DeepChat Agent System Architecture v1.4

> **High-level taxonomy of the DeepChat agent system.** Documents what DeepChat/DeepSeek operates on: agents, system prompts, prompt templates, subagents, and their interactions. Defines the filesystem sandboxing model and the Program Agent ↔ Project Agent separation.

---

## 1. TAXONOMY — What DeepChat Operates On

### Layer 1: DeepChat (Application)
The platform that hosts agents, manages chat sessions, and provides tool infrastructure (file I/O, Python execution, git). Configured via Settings → Agents.

### Layer 2: DeepSeek (Model)
The LLM provider powering the agents. DeepSeek V3, V4, and R1 models. The model receives the system prompt + conversation history and produces text output.

### Layer 3: Agents (Named Instances)
Configured in DeepChat Settings → Agents. Each agent loads ONE system prompt and has a defined set of enabled tools. **Agents are mapped 1:1 to filesystem write directories.**

| Agent | System Prompt | Write Sandbox | Read Scope | Purpose |
|:------|:-------------|:--------------|:-----------|:--------|
| **Projects** | `DEFAULT.md` | `G:\My Drive\projects\<name>\` | ALL directories | Project Executor — autonomous research, writing, coding. Receives handoff from Program Agent, executes Phases 0-5, returns deliverables. §0.9: Independent Project Executor role. Uses `gh` CLI for Issues/Projects (§0.6.8). |
| **Prompts** | `META-PROMPT-DEEPSEEK.md` | `G:\My Drive\prompts\` | ALL directories | System prompt engineering — create, edit, audit prompts |
| **QWAV** | `QWAV-DEFAULT.md` + `DEFAULT.md` | `G:\My Drive\projects\` | ALL directories | **Program/Portfolio Manager** — initiates projects via templates, coordinates across projects, manages GitHub Issues/Projects, quality-gates deliverables, manages social media (Buffer API). Inherits DEFAULT.md (Rules 1-6,12-14, Git, Email). QWAV-DEFAULT.md is program-specific delta (16K, not duplicate of DEFAULT.md). |

**Design principle:** An agent exists ONLY when it has a unique filesystem write boundary. Everything else (email, image generation, social media) is consumed as a template or sub-prompt WITHIN the writing agent — typically the Projects agent.

### Layer 4: System Prompts (Instruction Files)
Markdown files loaded as the system prompt when an agent starts. They define the agent's behavior, tool access, operating rules, and workflow patterns.

| System Prompt | Version | Loaded By | Scope |
|:--------------|:--------|:----------|:------|
| `DEFAULT.md` | — | Projects agent | Project Executor — full research/writing/coding/email/social workflow. §0.9: Independent Project Executor role. §0.6.8: GitHub CLI integration. Rules 1-6, 12-14 (ANTI-PHANTOM). 142K chars. |
| `QWAV-DEFAULT.md` | v2.0 | QWAV agent (appended to DEFAULT.md) | Program/Portfolio Manager — inherits all rules, protocols, and standards from DEFAULT.md. Adds ONLY program-specific delta (16K): Portfolio Manager role, email outreach framework, GitHub-native program management, Buffer social media, program↔project handoff protocol, project initiation via templates. NO duplication with DEFAULT.md. |
| `META-PROMPT-DEEPSEEK.md` | v4.5 | Prompts agent | System prompt generation and auditing. Template includes all 9 core rules (1-6, 12-14) + 7 structural gates. |
| `EMAIL-AGENT-v1.3.md` | v1.2 | *(Optional standalone email sessions)* | Dedicated email operations |
| `image-gen-banner-prompt.md` | — | *(Consumed within Projects)* | Banner image generation |

### Layer 5: Prompt Templates (Parameterized Sub-Prompts)
Filled via `fill_prompt_template(templateName, templateArgs, additionalContent)`. Templates are called BY agents (Projects and QWAV) to handle specialized tasks without needing a separate agent instance.

**Functional Templates (Task-Specific):**

| Template | Parameters | Called From | Produces |
|:---------|:-----------|:------------|:---------|
| `SOCIAL-ORCHESTRATOR TEMPLATE v1.0` | publicationTitle, publicationAuthors, publicationAbstract, publicationDOI, publicationFindings, publicationPath | Projects agent | Social media post text → published via Buffer API |
| `EMAIL-AGENT TEMPLATE v1.2` | recipient, subject, context, bodyDraft, attachmentPath, doiLink | Projects agent | `email_draft.py` / `email_send.py` command → executed by calling agent |
| `PDF-BUILDER-TEMPLATE v1.0` | markdownPath, outputPdfPath, cssPath, title, noMath, htmlOnly | Projects agent | `pdf/build_pdf.py` command → executed by calling agent |
| `Research Planning Agent — Step 1 of 4: Setup` | — | Research pipeline | Project setup plan |
| `Research Writing Agent — Step 2 of 4: Draft` | — | Research pipeline | Research draft |
| `Research Review Agent — Step 3 of 4: Quality Check` | — | Research pipeline | Quality review |
| `Research Publication Agent — Step 4 of 4: Final Assembly` | — | Research pipeline | Final publication |

**Project Management Templates (Project Lifecycle):**

| Template | Parameters | Called From | Produces |
|:---------|:-----------|:------------|:---------|
| `PROJECT-CHARTER-TEMPLATE` | — | Program agent (Â§0.9 Initiation) | `CHARTER.md` — scope, success criteria, constraints, deliverables |
| `DEFINITION-OF-DONE-TEMPLATE` | — | Program agent (Â§0.9 Initiation) | `DEFINITION-OF-DONE.md` — CODE/DOC/PUBLICATION/ANALYSIS gates |
| `RISK-REGISTER-TEMPLATE` | — | Program agent (Â§0.9 Initiation) | `RISK-REGISTER.md` — CPL + project-specific risks |
| `README-TEMPLATE` | — | Program agent (Â§0.9), Projects agent (Â§0.7) | `README.md` — dependencies, architecture, usage |
| `SPRINT-BACKLOG-TEMPLATE` | — | Program agent (Â§0.9), Projects agent (Â§0.7) | `SPRINT.md` — **DEPRECATED → GitHub Projects (§0.6.8)** |
| `PRODUCT-BACKLOG-TEMPLATE` | — | Program agent (Â§0.9), Projects agent (Â§0.7) | `BACKLOG.md` — **DEPRECATED → GitHub Issues (§0.6.8)** |
| `CHANGELOG-TEMPLATE` | — | Program agent (Â§0.9), Projects agent (Â§0.7) | `CHANGELOG.md` — **DEPRECATED → GitHub Releases (§0.6.8)** |
| `CONTRIBUTING-TEMPLATE` | — | Program agent (Â§0.9 Initiation) | `CONTRIBUTING.md` — project rules, domain rules, escalation |
| `HANDOFF-TEMPLATE` | — | Program agent (Â§0.9 Initiation) | Handoff document — scope, criteria, acceptance gate |
| `ADR-TEMPLATE` | — | Program agent (Â§0.9), Projects agent (Â§0.7) | Individual ADR appended to `DECISIONS.md` — **DEPRECATED → GitHub Discussions (§0.6.8)** |
| `RETROSPECTIVE-TEMPLATE` | — | Program agent, Projects agent (Â§12 close-out) | Sprint retrospective — start/stop/continue + CPL candidates |
| \TEST-EVIDENCE-TEMPLATE\ | — | Projects agent (§5 Phase workflow, DoD) | Standardized test execution evidence document |
| \QA-QC-TESTING-PROTOCOL\ | — | All agents (reference) | Universal QA/QC framework — deliverable type testing matrix, phase gate integration |
| `PROJECT-STATE-TEMPLATE` | — | Program agent (§0.9), Projects agent (§0.7) | `PROJECT STATE.md` — status, branch, phase, constraints |
| `LEARNINGS-TEMPLATE` | — | Program agent (§0.9), Projects agent (§0.7) | `LEARNINGS.md` — **DEPRECATED → GitHub Wiki (§0.6.8)** |
| `CLOSEOUT-CHECKLIST-TEMPLATE` | — | Projects agent (§12 close-out) | `CLOSEOUT-CHECKLIST.md` — 7-item close-out checklist with human sign-off |
| `WEB-APP-RELEASE-CHECKLIST` | — | Projects agent (§12 close-out, web app releases) | Pre-deployment gate — 9-section checklist for web app releases to GitHub Pages |

### Layer 6: Subagents (Isolated Clones)
Called via `subagent_orchestrator`. Self-clones of the current agent with ~35% chance of file I/O tools. Used for parallel or pipelined work.

| Slot ID | Role | Input | Output | Tool Reliability |
|:--------|:-----|:------|:-------|:-----------------|
| `slot-mp80a5ry-e7hn` | **EXPLORER** — Divergent Thinking | Inline text only | Brainstorming, alternatives, edge-case discovery | LLM only (~35% file I/O) |
| `slot-mp80ay3u-yzqo` | **IMPLEMENTER** — Convergent Execution | Inline text only | Drafting, structured output, content generation | LLM only (~35% file I/O) |
| `slot-mp80b6bl-iix2` | **REVIEWER** — Critical Evaluation | Inline text only | Blind validation, reader testing, gap analysis | LLM only (~35% file I/O) |

**CRITICAL:** Never rely on subagents for file I/O, Python, git, skills, or settings. Provide ALL content inline. Subagents are for TEXT PROCESSING only — generate alternatives, draft from specs, validate output.

### Layer 7: Agent Description Files (`agents/` and `agents/subagents/`)

Detailed execution specs stored in `G:\My Drive\prompts\agents\`. These files tell the LLM EXACTLY how and when to execute each agent or subagent — identity, purpose, tools (confirmed vs unreliable), trigger conditions, input/output formats, anti-patterns, chaining patterns, failure modes, and the `GIT: Skip` directive for subagents.

| File | Audience | Purpose |
|:-----|:---------|:--------|
| `agents/PROJECTS-AGENT.md` | Projects agent | Full research/writing/email/social lifecycle, subagent delegation patterns |
| `agents/QWAV-AGENT.md` | QWAV agent | Program/Portfolio Manager — uses QWAV-DEFAULT.md (appended to DEFAULT.md), §0.9 role boundary, coordinates across projects, manages GitHub Issues/Projects, initiates projects via templates |
| `agents/PROMPTS-AGENT.md` | Prompts agent | System prompt engineering, 11-section template with embedded structural gates, no subagent delegation |
| `agents/subagents/EXPLORER-SUBAGENT.md` | All agents | Divergent thinking — brainstorming, alternatives, edge cases |
| `agents/subagents/IMPLEMENTER-SUBAGENT.md` | All agents | Convergent execution — drafting, structured output from specs |
| `agents/subagents/REVIEWER-SUBAGENT.md` | All agents | Critical evaluation — blind validation, reader testing, gap analysis |

**Design principle:** Agent description files are reference documentation read by agents during due diligence (§0.8). They complement the 7-file project documentation standard (§0.7) by providing static execution specifications that don't change per session.

---

## 2. FILESYSTEM SANDBOXING MODEL

### 2.1 Write Isolation

```
┌─────────────────────────────────────────────────────────┐
│  G:\My Drive\                                           │
│  ├── projects\          ← WRITE: Projects agent         │
│  │   ├── <project>\     ← active project work           │
│  │   └── _shared\       ← READ-ONLY: CROSS-PROJECT      │
│  ├── prompts\           ← WRITE: Prompts agent          │
│  ├── QWAV\              ← WRITE: QWAV agent (pending)   │
│  ├── Obsidian\releases\ ← READ-ONLY: all agents         │
│  └── Archive\           ← READ-ONLY: all agents         │
│      ├── projects\YYYY\MM\ ← MOVE target (completed)    │
│      ├── prompts\       ← MOVE target (archived prompts)│
│      └── backup\        ← MOVE target                   │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Cross-Directory MOVE Permissions

Agents may MOVE completed/archived work OUT of their write sandbox and INTO read-only directories. This is NOT a write violation — it's a handoff.

| Agent | Can MOVE from | Can MOVE to | Use Case |
|:------|:-------------|:------------|:---------|
| Projects | `projects\<name>\` | `Archive\projects\YYYY\MM\project-name\` | Archive completed project |
| Projects | `projects\<name>\` | `Obsidian\releases\` | Publish finalized research |
| Prompts | `prompts\` | `Archive\prompts\` | Archive deprecated prompts |
| QWAV | `projects\` | `Archive\projects\YYYY\MM\` | Archive completed project work |
| QWAV | `projects\` | `Obsidian\releases\` | Publish program deliverables |

**Rule:** MOVE is allowed. COPY+DELETE is equivalent. Never WRITE directly to Archive or releases — only MOVE into them.

### 2.3 Read-Only Access (All Agents)

All agents have read access to all directories for due diligence (§0.8), cross-project learning, and context retrieval. This includes:
- `G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md`
- `G:\My Drive\Obsidian\releases\`
- `G:\My Drive\Archive\` (all subdirectories)
- `G:\My Drive\prompts\` (system prompts and templates)
- Any project directory (read-only; write only to assigned project)

---

## 3. HAPPY PATH WORKFLOWS

### 3.1 Email Drafted from Project Output

```
PROJECTS AGENT (DEFAULT.md):
  User: "Richard emailed about my fractal paper. Respond with the DOI."
  ↓
  §0.8 Due Diligence: search projects → find Fractal Harmonic Trees
  ↓
  Call: fill_prompt_template(
    templateName: "EMAIL-AGENT TEMPLATE v1.2",
    templateArgs: {
      recipient: "Richard Goodman <rgoodman@apoth3osis.io>",
      subject: "Re: Reply - New Inquiry Submission",
      context: "Fractal Harmonic Trees paper — number theory, complex analysis",
      bodyDraft: "",              ← EMPTY → triggers ASK protocol
      doiLink: "https://doi.org/..."
    }
  )
  ↓
  EMAIL-AGENT TEMPLATE:
    → Extracts facts from context
    → Identifies gap: bodyDraft empty
    → ASKS user: "What would you like to say?"
  ↓
  User: "Richard, here's my paper: [DOI]. Let me know your thoughts. -Rowan"
  ↓
  EMAIL-AGENT TEMPLATE:
    → Produces: python email_draft.py --to ... --subject ... --body "..."
    → Pre-send checklist: 6/6 ✓
  ↓
  PROJECTS AGENT:
    → Executes: python "G:\My Drive\prompts\email\email_draft.py" ...
    → Reports: "Draft saved. Review in Outlook Drafts."
```

### 3.2 Social Media from Publication

```
PROJECTS AGENT (DEFAULT.md):
  User: "Generate social posts from my latest release"
  ↓
  Call: fill_prompt_template(
    templateName: "SOCIAL-ORCHESTRATOR TEMPLATE v1.0",
    templateArgs: {
      publicationTitle: "...",
      publicationAuthors: "...",
      publicationAbstract: "...",
      publicationDOI: "...",
      publicationFindings: "...",
      publicationPath: "G:\My Drive\Obsidian\releases\..."
    }
  )
  ↓
  SOCIAL-ORCHESTRATOR TEMPLATE:
    → Reads publication file
    → Generates platform-specific post text (Bluesky, Twitter, Mastodon, LinkedIn)
    → Outputs inline text — no files created
  ↓
  PROJECTS AGENT:
    → Publishes via Buffer API
```

### 3.3 Prompt Engineering (Prompts Agent)

```
PROMPTS AGENT (META-PROMPT-DEEPSEEK.md):
  User: "Create a new prompt template for X"
  
  Prompts agent designs prompt following 9-section template
  
  Writes to: G:\My Drive\prompts\<new-prompt>.md
  
  If replacing old prompt: MOVE old to Archive\prompts\
  
  Commit with: ACTION:CREATE FILE: ...
```

### 3.4 Program-Project Handoff (Program Agent -> Project Agent)

```
PROGRAM AGENT (QWAV-DEFAULT.md + DEFAULT.md):
  User: "Start a new project for X"
  
  Complete Project Initiation Protocol (QWAV-DEFAULT.md S0.9.1)
  Create project directory + scaffolding docs via fill_prompt_template
  
  Create handoff via fill_prompt_template("HANDOFF", {type: "Program->Project", ...})
  Create GitHub Issue(s) for project tasks via gh issue create
  
  Update PROJECT STATE.md: STATUS: DELEGATED TO PROJECTS | HANDOFF: path
  
  PAUSE - wait for Projects agent
  
  PROJECTS AGENT (DEFAULT.md):
  Read handoff document
  Follow research trail (Archive, releases, active projects)
  Execute Phases 0-5 (DEFAULT.md S5)
  Place deliverables in Obsidian\releases\YYYY\MM\
  Update PROJECT STATE.md: STATUS: COMPLETE | DELIVERABLE: path
  Close GitHub Issue: gh issue close <num> --reason completed
  
  BACK TO PROGRAM AGENT:
  Read PROJECT STATE.md - confirm STATUS: COMPLETE
  Review deliverable in Obsidian\releases\
  Quality check against DEFINITION-OF-DONE.md gates
  If PASS: update program docs, plan next steps
  If FAIL: re-open GitHub Issue, create new handoff
```

```
PROMPTS AGENT (META-PROMPT-DEEPSEEK.md):
  User: "Create a new prompt template for X"
  ↓
  Prompts agent designs prompt following 9-section template
  ↓
  Writes to: G:\My Drive\prompts\<new-prompt>.md
  ↓
  If replacing old prompt: MOVE old to Archive\prompts\
  ↓
  Commit with: ACTION:CREATE FILE: ...
```

---

## 4. DESIGN PRINCIPLES

| # | Principle | Rationale |
|:--|:----------|:----------|
| 1 | **Agent = write boundary** | An agent exists ONLY when it has a unique filesystem write directory. No write directory? No agent — use a template instead. |
| 2 | **Templates over agents** | If an operation doesn't need its own write sandbox, it's a template consumed within the writing agent. |
| 3 | **Read-all, write-one** | Every agent can READ from any directory (for due diligence, context). Each agent WRITES to exactly one directory. |
| 4 | **MOVE is not write** | Archiving or publishing work via MOVE is a handoff, not a write violation. |
| 5 | **Subagents are text-only** | Subagents have unreliable file I/O. Use them for brainstorming, drafting, and validation — never for read/write/exec. |
| 6 | **Program coordinates, Project executes** | The Program Agent initiates, monitors, and quality-gates. The Project Agent executes autonomously. Handoff uses `fill_prompt_template("HANDOFF")` with a 5-state machine. See QWAV-DEFAULT.md §0.9.2. |

---

## 5. FILE REFERENCE

| File | Purpose | Version |
|:-----|:--------|:--------|
| `ARCHITECTURE.md` | This document — high-level taxonomy | v1.3 |
| `DEFAULT.md` | System prompt for the Projects agent | — |
| `META-PROMPT-DEEPSEEK.md` | System prompt for the Prompts agent | v4.5 |
| `AGENT-CONFIG.md` | Agent configuration values for DeepChat Settings | v5.2 |
| `agents/*.md` (6 files) | Agent and subagent execution specs — identity, tools, triggers, anti-patterns | v1.1 |
| `email/EMAIL-AGENT-v1.3.md` | System prompt for optional dedicated email sessions | v1.2 |
| `email/EMAIL-AGENT-TEMPLATE.md` | Prompt template for in-line email drafting | v1.2 |
| `email/EMAIL-CAPABILITIES.md` | Drop-in prompt module for email capabilities | v1.2 |
| `email/README.md` | Setup and usage guide for email system | — |
| `pdf/build_pdf.py` | Reusable Markdown → HTML → PDF CLI pipeline (v3.0) | v3.0 |
| `pdf/README.md` | Setup and usage guide for pdf builder | — |
| `SOCIAL-ORCHESTRATOR-TEMPLATE.md` | Prompt template for social media generation | v1.0 |

---

*Architecture v1.4 — QWAV-DEFAULT.md (v2.0, 16K) inherits from DEFAULT.md (142K) adding Program/Portfolio Manager role; Projects uses DEFAULT.md with §0.9 Project Executor role; §0.6.8 GitHub CLI integration; Rules 1-6, 12-14; program-project handoff via HANDOFF template with 5-state machine*
