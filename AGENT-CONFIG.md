# DEEPCHAT AGENT/SETUP CONFIGURATION (v5.2)

> **DeepChat Settings — exact values to paste.** See `ARCHITECTURE.md` for design principles and taxonomy.

---

## SETTINGS → AGENTS (3 to configure)

> **Detailed execution specs:** See `agents/PROJECTS-AGENT.md`, `agents/QWAV-AGENT.md`, `agents/PROMPTS-AGENT.md` for identity, purpose, tools, trigger conditions, anti-patterns, input/output formats, and chaining patterns.

### Agent: Projects

| Field | Value |
|:------|:------|
| **Name** | `Projects` |
| **System Prompt** | Paste ENTIRE contents of `DEFAULT.md` |

**Write boundary:** `G:\My Drive\projects\<name>\`
**MOVE to:** `Archive\projects\`, `Obsidian\releases\`
**Tools:** `read write edit exec process deepchat_question skill_list skill_view skill_manage subagent_orchestrator fill_prompt_template search_conversations`

---

### Agent: QWAV

| Field | Value |
|:------|:------|
| **Name** | `QWAV` |
| **System Prompt** | Paste ENTIRE contents of `DEFAULT.md` |

**Write boundary:** `G:\My Drive\QWAV\` ✅ Active since 2026-05-11
**Scope:** Ultrametric Quantum Computing & AI — passive fault tolerance, glass-based q-computing. Full 7-file documentation + outreach emails + arxiv submission guide.
**MOVE to:** `Archive\QWAV\`, `Obsidian\releases\`
**Tools:** Same as Projects agent

**Note:** QWAV uses the SAME system prompt as Projects (`DEFAULT.md`). This ensures email/social media/due diligence/sandboxing capabilities are identical. Separation is by chat thread, not by prompt content.

---

### Agent: Prompts

| Field | Value |
|:------|:------|
| **Name** | `Prompts` |
| **System Prompt** | Paste ENTIRE contents of `META-PROMPT-DEEPSEEK.md` |

**Write boundary:** `G:\My Drive\prompts\`
**MOVE to:** `Archive\prompts\`
**Tools:** `read write edit exec process deepchat_question skill_list skill_view skill_manage`

---

## SETTINGS → SUBAGENTS (3 already configured)

> **Detailed execution specs:** See `agents/subagents/EXPLORER-SUBAGENT.md`, `agents/subagents/IMPLEMENTER-SUBAGENT.md`, `agents/subagents/REVIEWER-SUBAGENT.md` for slot IDs, confirmed/unreliable tools, trigger conditions, anti-patterns, chaining patterns, failure modes, and `GIT: Skip` directives.

All three slots are self-clones. ~35% chance of file I/O tools — TEXT ONLY.

### EXPLORER (slot: `slot-mp80a5ry-e7hn`)

```
EXPLORER — Divergent Thinking | target=current agent | Isolated clone for
brainstorming, possibility-space mapping, and edge-case discovery.

CONFIRMED: LLM text generation, fill_prompt_template, search_conversations, Buffer API
UNRELIABLE (~35%): read, write, edit, exec, process, subagent_orchestrator, skills

USE: Brainstorming, alternatives, edge cases — ALL inputs inline.
NEVER: File I/O, Python, git, skills, settings.

GIT: Skip all git/branch checks. Read-only task.
```

### IMPLEMENTER (slot: `slot-mp80ay3u-yzqo`)

```
IMPLEMENTER — Convergent Execution | target=current agent | Isolated clone for
drafting, building from specifications, and generating structured output.

CONFIRMED: LLM text generation, fill_prompt_template, search_conversations, Buffer API
UNRELIABLE (~35%): read, write, edit, exec, process, subagent_orchestrator, skills

USE: Drafting, structured output, building from specs — ALL inputs inline.
NEVER: File I/O, Python, git, skills, settings.

GIT: Skip all git/branch checks. Read-only task.
```

### REVIEWER (slot: `slot-mp80b6bl-iix2`)

```
REVIEWER — Critical Evaluation | target=current agent | Isolated clone for
blind validation, reader testing, consistency checking, and gap analysis.

CONFIRMED: LLM text generation, fill_prompt_template, search_conversations, Buffer API
UNRELIABLE (~35%): read, write, edit, exec, process, subagent_orchestrator, skills

USE: Blind validation, reader testing, gap analysis — ALL inputs inline.
NEVER: File I/O, Python, git, skills, settings.

GIT: Skip all git/branch checks. Read-only task.
```

---

## SETTINGS → PROMPT TEMPLATES (call via `fill_prompt_template()`)

| Template Name | Parameters | Purpose |
|:--------------|:-----------|:--------|
| `"EMAIL-AGENT TEMPLATE v1.2"` | recipient, subject, context, bodyDraft, attachmentPath, doiLink | Draft emails from project outputs |
| `"SOCIAL-ORCHESTRATOR TEMPLATE v1.0"` | publicationTitle, publicationAuthors, publicationAbstract, publicationDOI, publicationFindings, publicationPath | Generate social media posts |
| `"Research Planning Agent — Step 1 of 4: Setup"` | — | Research setup |
| `"Research Writing Agent — Step 2 of 4: Draft"` | — | Research drafting |
| `"Research Review Agent — Step 3 of 4: Quality Check"` | — | Quality review |
| `"Research Publication Agent — Step 4 of 4: Final Assembly"` | — | Publication assembly |

---

## FILES NOT IN SETTINGS — Called by Prompt Instructions

| File(s) | How Used |
|:--------|:---------|
| `email/email_*.py` (7 scripts) | `exec("python ...")` — CLI syntax documented IN the prompts |
| `email/outlook_mcp_server/` | MCP server — registered separately |
| `email/EMAIL-CAPABILITIES.md` | Already embedded in DEFAULT.md |
| `email/EMAIL-TEST-SUITE.md` | Test scenarios — not loaded by agents |
| `ARCHITECTURE.md` | Reference — read by agents at startup |
| `AGENT-CONFIG.md` | This file — setup for YOU |

---

*Agent Configuration v5.2 — slot IDs synced to live DEFAULT.md; 3 agents mapped to 3 write boundaries*
