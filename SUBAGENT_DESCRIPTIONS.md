# DEEPCHAT AGENT/SUBAGENT SETUP (v5.0)

> Copy the exact values below into DeepChat Settings → Agents. One prompt per agent.
>
> **Design principle:** An agent exists ONLY when it has a unique filesystem write directory. Everything else (email, social media, image generation) is consumed as a prompt template or sub-prompt within the writing agent — typically the Projects agent.
>
> **For the full architecture taxonomy, see:** `ARCHITECTURE.md` — documents agents, system prompts, prompt templates, subagents, filesystem sandboxing, and happy path workflows.

---

## AGENTS (Minimal Set — 3 Agents)

### Agent: Projects (THE ONE — use for all project work)

| Field | Value |
|:------|:------|
| **Name** | `Projects` |
| **System Prompt** | Paste ENTIRE contents of `DEFAULT.md` |

**Write boundary:** `G:\My Drive\projects\<name>\`
**Can also:** Email (via template), social media (via template), image generation (via skill/template)
**MOVE permissions:** → `Archive\projects\`, → `Obsidian\releases\`

**Tools to enable:** `read write edit exec process deepchat_question skill_list skill_view skill_manage subagent_orchestrator fill_prompt_template search_conversations`

---

### Agent: Prompts (use for prompt engineering)

| Field | Value |
|:------|:------|
| **Name** | `Prompts` |
| **System Prompt** | Paste ENTIRE contents of `META-PROMPT-DEEPSEEK.md` |

**Write boundary:** `G:\My Drive\prompts\`
**Can also:** Audit and version existing prompts, create templates
**MOVE permissions:** → `Archive\prompts\`

**Tools to enable:** `read write edit exec process deepchat_question skill_list skill_view skill_manage`

---

### Agent: QWAV (pending — directory not yet created)

| Field | Value |
|:------|:------|
| **Name** | `QWAV` |
| **System Prompt** | `QWAV-DEFAULT.md` (TBD — create when `G:\My Drive\QWAV\` exists) |

**Write boundary:** `G:\My Drive\QWAV\`
**Can also:** Email (via template), social media (via template)
**MOVE permissions:** → `Archive\QWAV\`, → `Obsidian\releases\`

**Tools to enable:** `read write edit exec process deepchat_question skill_list skill_view skill_manage subagent_orchestrator fill_prompt_template search_conversations`

**Setup when QWAV exists:**
1. Create directory: `G:\My Drive\QWAV\`
2. Create system prompt: `QWAV-DEFAULT.md` (follow the 9-section prompt template from `META-PROMPT-DEEPSEEK.md`)
3. Register agent in DeepChat Settings → Agents with values above

---

## DEPRECATED AGENTS (Do NOT Configure)

These were previously standalone agents. They have been converted to prompt templates or sub-prompts consumed within the Projects agent.

| Agent | Status | Replacement |
|:------|:-------|:------------|
| **Email** | ❌ Removed (v5.0) | Use `EMAIL-AGENT TEMPLATE v1.2` via `fill_prompt_template()` from Projects agent. The system prompt file (`email/EMAIL-AGENT-v1.2.md`) remains available for optional standalone email sessions. |
| **Social** | ❌ Removed (v5.0) | Use `SOCIAL-ORCHESTRATOR TEMPLATE v1.0` via `fill_prompt_template()` from Projects agent. Posts published via Buffer API. |
| **Image Gen** | ❌ Removed (v5.0) | Use `image-gen-banner-prompt.md` as a sub-prompt consumed within the Projects agent. Image generation via the `algorithmic-art` or `frontend-design` skills. |

---

## PROMPT TEMPLATES (Call via `fill_prompt_template()`)

These are NOT agents. They are parameterized sub-prompts called by the Projects agent (or QWAV agent) for specialized tasks.

| Template Name | Parameters | Purpose |
|:--------------|:-----------|:--------|
| `SOCIAL-ORCHESTRATOR TEMPLATE v1.0` | publicationTitle, publicationAuthors, publicationAbstract, publicationDOI, publicationFindings, publicationPath | Generate social media posts from publications |
| `EMAIL-AGENT TEMPLATE v1.2` | recipient, subject, context, bodyDraft, attachmentPath, doiLink | Draft emails from project outputs |
| `Research Planning Agent — Step 1 of 4: Setup` | — | Research project setup |
| `Research Writing Agent — Step 2 of 4: Draft` | — | Research draft generation |
| `Research Review Agent — Step 3 of 4: Quality Check` | — | Research quality review |
| `Research Publication Agent — Step 4 of 4: Final Assembly` | — | Research publication assembly |

**Usage pattern:**
```
Projects agent:
  fill_prompt_template(
    templateName: "EMAIL-AGENT TEMPLATE v1.2",
    templateArgs: {recipient: "...", subject: "...", context: "...", ...}
  )
  → Template returns formatted output (email command, social text, etc.)
  → Projects agent executes or displays the output
```

---

## SUBAGENT SLOTS: SELF-CLONES (explorer / implementer / reviewer)

All three slots are SELF-CLONES — isolated instances of the current agent. They share the same tool availability profile.

**⚠️ DEFINITIVE TOOL LIMITATION (20-test empirical study, 2026-05-11):** ALL subagent slots have NON-DETERMINISTIC tool availability. ~35% chance of having file I/O tools (read, write, edit, exec, process, subagent_orchestrator, skill_*, deepchat_*). NEVER rely on subagents for any file operation, Python execution, git, skills, or settings.

- CONFIRMED (always available): LLM text generation, fill_prompt_template, search_conversations, Buffer API
- UNRELIABLE (~35% chance — never depend on): read, write, edit, exec, process, subagent_orchestrator, skill_list, skill_view, skill_manage, deepchat_*

### Subagent Task Template

Every task prompt to a self-clone subagent (explorer, implementer, or reviewer) MUST start with:

```
GIT: Skip all git/branch checks. Read-only task. Proceed directly to assigned work.
```

**Rationale:** Subagents inherit the full system prompt including git discipline. Without this directive, subagents burn their response budget on irrelevant git pre-flight checks (branch verification, feature branch creation, commit execution) instead of completing their delegated task. Subagents have ~65% chance of lacking write/exec tools, making git impossible.

---

### EXPLORER — Divergent Thinking | slot: `self`

| Field | Value |
|:------|:------|
| **Name** | `EXPLORER` |
| **Slot ID** | `self` |
| **Target** | Current agent (self-clone) |
| **System Prompt** | Inherits from parent agent |

**CONFIRMED (always available):**
- LLM text generation — brainstorming, alternative generation, edge-case discovery
- fill_prompt_template, search_conversations, Buffer API

**UNRELIABLE (~35% chance — never depend on):**
- read, write, edit, exec, process, subagent_orchestrator
- skill_list, skill_view, skill_manage, deepchat_*, deepchat_question

**USE:** Brainstorming alternatives, mapping possibility spaces, finding edge cases — ALL inputs inline.
**NEVER USE:** File I/O, Python, git, skills, settings.

---

### IMPLEMENTER — Convergent Execution | slot: `slot-mp80dr5g-oh9g`

| Field | Value |
|:------|:------|
| **Name** | `IMPLEMENTER` |
| **Slot ID** | `slot-mp80dr5g-oh9g` |
| **Target** | Current agent (self-clone) |
| **System Prompt** | Inherits from parent agent |

**CONFIRMED (always available):**
- LLM text generation — drafting, structured output, content generation
- fill_prompt_template, search_conversations, Buffer API

**UNRELIABLE (~35% chance — never depend on):**
- read, write, edit, exec, process, subagent_orchestrator
- skill_list, skill_view, skill_manage, deepchat_*, deepchat_question

**USE:** Drafting content, building from specs, generating structured output — ALL inputs inline.
**NEVER USE:** File I/O, Python, git, skills, settings.

---

### REVIEWER — Critical Evaluation | slot: `slot-mp80e4mj-5s1l`

| Field | Value |
|:------|:------|
| **Name** | `REVIEWER` |
| **Slot ID** | `slot-mp80e4mj-5s1l` |
| **Target** | Current agent (self-clone) |
| **System Prompt** | Inherits from parent agent |

**CONFIRMED (always available):**
- LLM text generation — blind validation, reader testing, consistency checking
- fill_prompt_template, search_conversations, Buffer API

**UNRELIABLE (~35% chance — never depend on):**
- read, write, edit, exec, process, subagent_orchestrator
- skill_list, skill_view, skill_manage, deepchat_*, deepchat_question

**USE:** Blind validation, reader testing, consistency checking, gap analysis — ALL inputs inline.
**NEVER USE:** File I/O, Python, git, skills, settings.

---

## FILESYSTEM SANDBOXING — Cross-Directory Access

See `ARCHITECTURE.md` §2 for the complete sandboxing model. Summary:

| Agent | Write | Can MOVE to | Read |
|:------|:------|:------------|:-----|
| Projects | `projects\<name>\` | `Archive\projects\`, `Obsidian\releases\` | ALL |
| Prompts | `prompts\` | `Archive\prompts\` | ALL |
| QWAV | `QWAV\` | `Archive\QWAV\`, `Obsidian\releases\` | ALL |

**Rule:** MOVE is allowed (handoff, not write). READ is allowed everywhere. WRITE is ONLY allowed in the agent's sandbox.

---

*DeepChat Agent/Subagent Setup v5.0 — minimal 3-agent architecture. Design principle: agent = filesystem write boundary. Templates for everything else.*
