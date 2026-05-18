# Prompts — System Prompt Library v5.3

> **G:\My Drive\prompts\** — git-tracked prompt engineering workspace.
> See ARCHITECTURE.md (v1.2) for full taxonomy and slot ID ground truth. See AGENT-CONFIG.md (v5.2) for Settings values.

---

## Architecture (3 Agents)

| Agent | System Prompt | Write Boundary |
|:------|:-------------|:---------------|
| **Projects** | DEFAULT.md v1.11 | `G:\My Drive\projects\<name>\` |
| **QWAV** | DEFAULT.md v1.11 | `G:\My Drive\QWAV\` |
| **Prompts** | META-PROMPT-DEEPSEEK.md v4.2 | `G:\My Drive\prompts\` |

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

| Slot ID | Role | Use |
|:--------|:-----|:----|
| `slot-mp80a5ry-e7hn` | EXPLORER — Divergent thinking | Brainstorming, alternatives, edge cases |
| `slot-mp80ay3u-yzqo` | IMPLEMENTER — Convergent execution | Drafting, structured output |
| `slot-mp80b6bl-iix2` | REVIEWER — Critical evaluation | Blind validation, gap analysis |

## Directory Structure

```
prompts\
├── DEFAULT.md                    System prompt (Projects + QWAV agents)
├── META-PROMPT-DEEPSEEK.md       System prompt (Prompts agent)
├── ARCHITECTURE.md               Taxonomy + design principles
├── AGENT-CONFIG.md               Settings — exact values to paste
├── README.md                     This file
├── system_audit.py               Self-learning system health check
├── .gitattributes
├── audit-reports\                Periodic system health reports
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
│   ├── EMAIL-AGENT-v1.3.md       Dedicated email system prompt
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
| **AGENT-CONFIG.md** (v5.2) | You (setup) | Exact values to paste into DeepChat Settings |
| **ARCHITECTURE.md** (v1.2) | You + agents | Taxonomy, sandboxing, slot IDs, happy path workflows |
| **DEFAULT.md** (v1.11) | Agents | System prompt with due diligence, email, social, sandboxing, reader testing, synthesis audit |
| **META-PROMPT-DEEPSEEK.md** (v4.2) | Prompts agent | Generates and reviews system prompts; self-audit aware |
| **agents/*.md** | Agents + you | Detailed agent/subagent execution specs |
| **CROSS-PROJECT-LEARNINGS.md** | All agents | 35 cross-project lessons (L1-L40) at `G:\My Drive\projects\_shared\` |
| **email/README.md** | You + agents | Email system setup and usage |

**Cross-Project Lessons:** `G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md` contains 35 lessons (L1-L40) catalogued from 11 archived projects. Categories: git, methodology, writing, python, tool-use. All agents should read this at session start.

---

*Prompts Library v5.3 — 3 agents, 7 templates, 3 subagents, 7 description files. All destructive operations gated behind user confirmation.*
