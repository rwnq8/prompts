# DeepChat Agent System Architecture v1.2

> **High-level taxonomy of the DeepChat agent system.** Documents what DeepChat/DeepSeek operates on: agents, system prompts, prompt templates, subagents, and their interactions. Defines the filesystem sandboxing model.

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
| **Projects** | `DEFAULT.md` | `G:\My Drive\projects\<name>\` | ALL directories | All project work — research, writing, coding, email, social media |
| **Prompts** | `META-PROMPT-DEEPSEEK.md` | `G:\My Drive\prompts\` | ALL directories | System prompt engineering — create, edit, audit prompts |
| **QWAV** | `QWAV-DEFAULT.md` (TBD) | `G:\My Drive\QWAV\` | ALL directories | Ultrametric Quantum Computing & AI — passive fault tolerance, glass-based q-computing |

**Design principle:** An agent exists ONLY when it has a unique filesystem write boundary. Everything else (email, image generation, social media) is consumed as a template or sub-prompt WITHIN the writing agent — typically the Projects agent.

### Layer 4: System Prompts (Instruction Files)
Markdown files loaded as the system prompt when an agent starts. They define the agent's behavior, tool access, operating rules, and workflow patterns.

| System Prompt | Version | Loaded By | Scope |
|:--------------|:--------|:----------|:------|
| `DEFAULT.md` | v1.11 | Projects agent | Full research/writing/coding/email/social workflow |
| `META-PROMPT-DEEPSEEK.md` | v4.2 | Prompts agent | System prompt generation and auditing |
| `EMAIL-AGENT-v1.3.md` | v1.2 | *(Optional standalone email sessions)* | Dedicated email operations |
| `image-gen-banner-prompt.md` | — | *(Consumed within Projects)* | Banner image generation |

### Layer 5: Prompt Templates (Parameterized Sub-Prompts)
Filled via `fill_prompt_template(templateName, templateArgs, additionalContent)`. Templates are called BY agents (usually Projects) to handle specialized tasks without needing a separate agent instance.

| Template | Parameters | Called From | Produces |
|:---------|:-----------|:------------|:---------|
| `SOCIAL-ORCHESTRATOR TEMPLATE v1.0` | publicationTitle, publicationAuthors, publicationAbstract, publicationDOI, publicationFindings, publicationPath | Projects agent | Social media post text → published via Buffer API |
| `EMAIL-AGENT TEMPLATE v1.2` | recipient, subject, context, bodyDraft, attachmentPath, doiLink | Projects agent | `email_draft.py` / `email_send.py` command → executed by calling agent |
| `Research Planning Agent — Step 1 of 4: Setup` | — | Research pipeline | Project setup plan |
| `Research Writing Agent — Step 2 of 4: Draft` | — | Research pipeline | Research draft |
| `Research Review Agent — Step 3 of 4: Quality Check` | — | Research pipeline | Quality review |
| `Research Publication Agent — Step 4 of 4: Final Assembly` | — | Research pipeline | Final publication |

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
| `agents/QWAV-AGENT.md` | QWAV agent | Ultrametric quantum computing & AI, same DEFAULT.md, separate sandbox |
| `agents/PROMPTS-AGENT.md` | Prompts agent | System prompt engineering, 9-section template, no subagent delegation |
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
│      ├── projects\      ← MOVE target (completed)       │
│      ├── prompts\       ← MOVE target (archived prompts)│
│      └── backup\        ← MOVE target                   │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Cross-Directory MOVE Permissions

Agents may MOVE completed/archived work OUT of their write sandbox and INTO read-only directories. This is NOT a write violation — it's a handoff.

| Agent | Can MOVE from | Can MOVE to | Use Case |
|:------|:-------------|:------------|:---------|
| Projects | `projects\<name>\` | `Archive\projects\` | Archive completed project |
| Projects | `projects\<name>\` | `Obsidian\releases\` | Publish finalized research |
| Prompts | `prompts\` | `Archive\prompts\` | Archive deprecated prompts |
| QWAV | `QWAV\` | `Archive\QWAV\` | Archive completed QWAV work |
| QWAV | `QWAV\` | `Obsidian\releases\` | Publish QWAV research |

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

---

## 5. FILE REFERENCE

| File | Purpose | Version |
|:-----|:--------|:--------|
| `ARCHITECTURE.md` | This document — high-level taxonomy | v1.2 |
| `DEFAULT.md` | System prompt for the Projects agent | v1.11 |
| `META-PROMPT-DEEPSEEK.md` | System prompt for the Prompts agent | v4.2 |
| `AGENT-CONFIG.md` | Agent configuration values for DeepChat Settings | v5.2 |
| `agents/*.md` (6 files) | Agent and subagent execution specs — identity, tools, triggers, anti-patterns | v1.0 |
| `email/EMAIL-AGENT-v1.3.md` | System prompt for optional dedicated email sessions | v1.2 |
| `email/EMAIL-AGENT-TEMPLATE.md` | Prompt template for in-line email drafting | v1.2 |
| `email/EMAIL-CAPABILITIES.md` | Drop-in prompt module for email capabilities | v1.2 |
| `email/README.md` | Setup and usage guide for email system | — |
| `SOCIAL-ORCHESTRATOR-TEMPLATE.md` | Prompt template for social media generation | v1.0 |

---

*Architecture v1.2 — slot IDs synced to live DEFAULT.md; documents the DeepChat agent system taxonomy*
