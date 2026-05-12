# DEEPCHAT AGENT/SUBAGENT SETUP (v4.1)

> Copy the exact values below into DeepChat Settings → Agents. One prompt per agent.

---

## AGENTS

### Agent: Projects (THE ONE — use for all project work)

| Field | Value |
|:------|:------|
| **Name** | `Projects` |
| **System Prompt** | Paste ENTIRE contents of `DEFAULT.md` |

**Tools — enable:** `read write edit exec process deepchat_question skill_list skill_view skill_manage`

---

### Agent: Prompts (use for prompt engineering)

| Field | Value |
|:------|:------|
| **Name** | `Prompts` |
| **System Prompt** | Paste ENTIRE contents of `META-PROMPT-DEEPSEEK.md` |

**Tools — enable:** `read write edit exec process deepchat_question skill_list skill_view skill_manage`

---

### Agent: Social (use for Buffer/social media)

| Field | Value |
|:------|:------|
| **Name** | `Social` |
| **System Prompt** | Paste ENTIRE contents of `SOCIAL-ORCHESTRATOR-v4.0.md` |

**Tools — enable:** `read write edit exec process deepchat_question skill_list skill_view skill_manage`

---

### Agent: Image Gen (use for banner images)

| Field | Value |
|:------|:------|
| **Name** | `Image Gen` |
| **System Prompt** | Paste ENTIRE contents of `image-gen-banner-prompt.md` |

**Tools — enable:** `read write edit exec process deepchat_question skill_list skill_view skill_manage`

---

## SUBAGENT SLOT: SELF-CLONE

| Field | Value |
|:------|:------|
| **Slot ID** | `self` |
| **Target** | `current agent` |

**Slot description — paste this:**
```
FRESH INSTANCE — Text Synthesis Only | target=current agent | Isolated clone for parallel text generation, blind validation, and reader testing. ALL subagent slots have non-deterministic tool availability (~35% chance of full tools). NEVER rely on this slot for file I/O, Python, git, skills, or settings. Provide ALL content inline.

CONFIRMED (always available):
  - LLM text generation — Parallel text, blind validation, reader testing
  - fill_prompt_template, search_conversations, Buffer API

UNRELIABLE (~35% chance — never depend on):
  - read, write, edit, exec, process, subagent_orchestrator
  - skill_list, skill_view, skill_manage, deepchat_*, deepchat_question

USE: Parallel text generation, blind validation, reader testing — ALL inputs inline.
NEVER USE: File I/O, Python, git, skills, settings.

GIT: Skip all git/branch checks. Read-only task. Proceed directly to assigned work.
```

---

## SUBAGENT TASK TEMPLATE

Every task prompt to SELF-CLONE MUST start with:

```
GIT: Skip all git/branch checks. Read-only task.

[ALL CONTENT INLINE — never reference file paths]

[Clear instructions]
```

---

## DEPRECATED (do not configure)

| File | Reason |
|:-----|:-------|
| PROJECT-ISOLATION-ENFORCER-v1.0.md | Rules absorbed into DEFAULT.md v1.5 |
| PROJECT-ORCHESTRATION-FRAMEWORK-v1.0.md | Rules absorbed into DEFAULT.md v1.5 |
| Project Kaizen agent | Merged into Projects agent via DEFAULT.md v1.5 |
