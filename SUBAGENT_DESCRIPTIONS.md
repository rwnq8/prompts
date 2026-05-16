# DEEPCHAT AGENT/SUBAGENT SETUP (v4.2)

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

### Agent: Social (DEPRECATED — use template instead)

| Field | Value |
|:------|:------|
| **Name** | `Social` |
| **System Prompt** | Paste ENTIRE contents of `SOCIAL-ORCHESTRATOR-v4.0.md` (DEPRECATED) |

> **NOTE:** The SOCIAL-ORCHESTRATOR has been converted to a prompt template (`SOCIAL-ORCHESTRATOR TEMPLATE v1.0`), auto-registered and callable via `fill_prompt_template`. The dedicated Social agent is retained only for manual Buffer operations. For publication promotion, the template is invoked automatically during project close-out (DEFAULT.md Section 12.4).

**Tools — enable:** `read write edit exec process deepchat_question skill_list skill_view skill_manage`

---

### Agent: Email (use for inbox sessions)

| Field | Value |
|:------|:------|
| **Name** | `Email` |
| **System Prompt** | Paste ENTIRE contents of `email/EMAIL-AGENT-v1.0.md` |

**Tools — enable:** `read write edit exec process deepchat_question skill_list skill_view skill_manage`

---

### Agent: Image Gen (use for banner images)

| Field | Value |
|:------|:------|
| **Name** | `Image Gen` |
| **System Prompt** | Paste ENTIRE contents of `image-gen-banner-prompt.md` |

**Tools — enable:** `read write edit exec process deepchat_question skill_list skill_view skill_manage`

---

## SUBAGENT SLOTS: SELF-CLONES (explorer / implementer / reviewer)

All three slots are SELF-CLONES — isolated instances of the current agent. They share the same tool availability profile.

**Tool Availability (ALL self-clone slots):**
- CONFIRMED (always available): LLM text generation, fill_prompt_template, search_conversations, Buffer API
- UNRELIABLE (~35% chance — never depend on): read, write, edit, exec, process, subagent_orchestrator, skill_list, skill_view, skill_manage, deepchat_*, deepchat_question

---

### Slot 1: EXPLORER

| Field | Value |
|:------|:------|
| **Slot ID** | `explorer` |
| **Target** | `current agent` |

**Slot description — paste this:**
```
EXPLORER — Divergent Thinking | target=current agent | Isolated clone for brainstorming, possibility-space mapping, and edge-case discovery. ALL subagent slots have non-deterministic tool availability (~35% chance of full tools). NEVER rely on this slot for file I/O, Python, git, skills, or settings. Provide ALL content inline.

CONFIRMED (always available):
  - LLM text generation — Brainstorming, alternative generation, edge-case discovery
  - fill_prompt_template, search_conversations, Buffer API

UNRELIABLE (~35% chance — never depend on):
  - read, write, edit, exec, process, subagent_orchestrator
  - skill_list, skill_view, skill_manage, deepchat_*, deepchat_question

USE: Brainstorming alternatives, mapping possibility spaces, finding edge cases — ALL inputs inline.
NEVER USE: File I/O, Python, git, skills, settings.

GIT: Skip all git/branch checks. Read-only task. Proceed directly to assigned work.
```

---

### Slot 2: IMPLEMENTER

| Field | Value |
|:------|:------|
| **Slot ID** | `implementer` |
| **Target** | `current agent` |

**Slot description — paste this:**
```
IMPLEMENTER — Convergent Execution | target=current agent | Isolated clone for drafting, building from specifications, and generating structured output. ALL subagent slots have non-deterministic tool availability (~35% chance of full tools). NEVER rely on this slot for file I/O, Python, git, skills, or settings. Provide ALL content inline.

CONFIRMED (always available):
  - LLM text generation — Drafting, structured output, content generation
  - fill_prompt_template, search_conversations, Buffer API

UNRELIABLE (~35% chance — never depend on):
  - read, write, edit, exec, process, subagent_orchestrator
  - skill_list, skill_view, skill_manage, deepchat_*, deepchat_question

USE: Drafting content, building from specs, generating structured output — ALL inputs inline.
NEVER USE: File I/O, Python, git, skills, settings.

GIT: Skip all git/branch checks. Read-only task. Proceed directly to assigned work.
```

---

### Slot 3: REVIEWER

| Field | Value |
|:------|:------|
| **Slot ID** | `reviewer` |
| **Target** | `current agent` |

**Slot description — paste this:**
```
REVIEWER — Critical Evaluation | target=current agent | Isolated clone for blind validation, reader testing, consistency checking, and gap analysis. ALL subagent slots have non-deterministic tool availability (~35% chance of full tools). NEVER rely on this slot for file I/O, Python, git, skills, or settings. Provide ALL content inline.

CONFIRMED (always available):
  - LLM text generation — Blind validation, reader testing, consistency checking
  - fill_prompt_template, search_conversations, Buffer API

UNRELIABLE (~35% chance — never depend on):
  - read, write, edit, exec, process, subagent_orchestrator
  - skill_list, skill_view, skill_manage, deepchat_*, deepchat_question

USE: Blind validation, reader testing, consistency checking, gap analysis — ALL inputs inline.
NEVER USE: File I/O, Python, git, skills, settings.

GIT: Skip all git/branch checks. Read-only task. Proceed directly to assigned work.
```

---

## SUBAGENT TASK TEMPLATE

Every task prompt to a self-clone subagent (explorer, implementer, or reviewer) MUST start with:

```
GIT: Skip all git/branch checks. Read-only task.

[ALL CONTENT INLINE — never reference file paths]

[Clear instructions matching the slot's role: explorer → brainstorm, implementer → draft, reviewer → validate]
```

### Recommended Workflow Pattern

```
EXPLORER (brainstorm alternatives) → IMPLEMENTER (draft from best ideas) → REVIEWER (validate output)
```

PARENT handles ALL file I/O, Python, and git between stages.
