# Prompts — System Prompt Library v5.1

> **G:\My Drive\prompts\** — git-tracked prompt engineering workspace.
> See ARCHITECTURE.md for full taxonomy and AGENT-CONFIG.md for Settings values.

---

## Architecture (3 Agents)

| Agent | System Prompt | Write Boundary |
|:------|:-------------|:---------------|
| **Projects** | DEFAULT.md v1.10 | `G:\My Drive\projects\<name>\` |
| **QWAV** | DEFAULT.md v1.10 | `G:\My Drive\QWAV\` |
| **Prompts** | META-PROMPT-DEEPSEEK.md v4.1 | `G:\My Drive\prompts\` |

**Design principle:** Agent = filesystem write boundary. Email, social media, image generation are templates consumed within the Projects/QWAV agents — not separate agents.

## Prompt Templates (call via `fill_prompt_template`)

| Template Name | Purpose |
|:--------------|:--------|
| EMAIL-AGENT TEMPLATE v1.2 | Draft emails from project outputs |
| SOCIAL-ORCHESTRATOR TEMPLATE v1.0 | Generate social media posts |
| Research Planning — Step 1 of 4 | Scholar pipeline: planning |
| Research Writing — Step 2 of 4 | Scholar pipeline: drafting |
| Research Review — Step 3 of 4 | Scholar pipeline: review |
| Research Publication — Step 4 of 4 | Scholar pipeline: publication |

## Subagents (3 self-clones)

| Slot | Role | Use |
|:-----|:-----|:----|
| EXPLORER | Divergent thinking | Brainstorming, alternatives, edge cases |
| IMPLEMENTER | Convergent execution | Drafting, structured output |
| REVIEWER | Critical evaluation | Blind validation, gap analysis |

## Directory Structure

```
prompts\
├── DEFAULT.md                    System prompt (Projects + QWAV agents)
├── META-PROMPT-DEEPSEEK.md       System prompt (Prompts agent)
├── ARCHITECTURE.md               Taxonomy + design principles
├── AGENT-CONFIG.md               Settings — exact values to paste
├── README.md                     This file
├── .gitattributes
│
├── agents\                        Agent & subagent description files
│   ├── PROJECTS-AGENT.md          Projects agent (research, writing, email, social)
│   ├── QWAV-AGENT.md              QWAV agent (ultrametric quantum computing)
│   ├── PROMPTS-AGENT.md           Prompts agent (system prompt engineering)
│   └── subagents\                 Subagent execution specifications
│       ├── EXPLORER-SUBAGENT.md   Divergent thinking — brainstorming, alternatives
│       ├── IMPLEMENTER-SUBAGENT.md Convergent execution — drafting, structured output
│       └── REVIEWER-SUBAGENT.md   Critical evaluation — blind validation, gaps
│
├── templates\                    Prompt templates
│   ├── SOCIAL-ORCHESTRATOR-TEMPLATE.md
│   └── image-gen-banner-prompt.md
│
├── email\                        Email system
│   ├── EMAIL-AGENT-v1.2.md       Dedicated email system prompt
│   ├── EMAIL-AGENT-TEMPLATE.md   Email prompt template
│   ├── EMAIL-CAPABILITIES.md     Drop-in email module
│   ├── EMAIL-TEST-SUITE.md       15 validation scenarios
│   ├── README.md                 Email setup guide
│   ├── email_*.py (7 scripts)    COM automation tools
│   ├── _email_utils.py           Shared multi-account utility
│   └── outlook_mcp_server\       MCP server (Graph API)
│
└── scholar\                      Research pipeline stages
    ├── STAGE-1-SETUP.md
    ├── STAGE-2-DRAFT.md
    ├── STAGE-3-REVIEW.md
    └── STAGE-4-PUBLISH.md
```

## DeepChat Settings (see AGENT-CONFIG.md for exact values)

```
Settings → Agents:
  Projects   ← paste DEFAULT.md
  QWAV       ← paste DEFAULT.md
  Prompts    ← paste META-PROMPT-DEEPSEEK.md

Settings → Subagents → paste slot descriptions from AGENT-CONFIG.md
Settings → Templates → auto-registered from file headers
```

## Key Documents

| File | Audience | Purpose |
|:-----|:---------|:--------|
| **AGENT-CONFIG.md** | You (setup) | Exact values to paste into DeepChat Settings |
| **ARCHITECTURE.md** | You + agents | Taxonomy, sandboxing, happy path workflows |
| **DEFAULT.md** v1.10 | Agents | System prompt with due diligence, email, social, sandboxing |
| **agents/*.md** | Agents + you | Detailed agent/subagent execution specs — identity, tools, triggers, anti-patterns |
| **email/README.md** | You + agents | Email system setup and usage |

---

*Prompts Library v5.2 — 3 agents, 6 templates, 3 subagents, 6 description files. All destructive operations gated behind user confirmation.*
