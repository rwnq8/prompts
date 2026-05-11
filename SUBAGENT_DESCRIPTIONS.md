# DEEPCHAT AGENT/SUBAGENT SETUP (v3.1)

> Copy/paste the exact values below into DeepChat settings. No rationale — just what to type.

---

## 1. AGENTS (create these in DeepChat Settings → Agents)

### Agent 1: Projects

| Setting | Value |
|:--------|:------|
| **Name** | `Projects` |
| **Description** | General-purpose research, writing, and brainstorming agent. Handles all file I/O, Python execution, git operations, and subagent orchestration. |
| **Built-in** | ✅ Enabled |
| **System Prompt** | Paste full contents of `DEFAULT.md` |

**Tools — enable ALL:**

```
edit exec process read write
deepchat_question
skill_list skill_manage skill_view
```

---

### Agent 2: Prompts

| Setting | Value |
|:--------|:------|
| **Name** | `Prompts` |
| **Description** | Tier 1 system prompt compiler and auditor. Creates, reviews, and improves system prompts using META-PROMPT-DEEPSEEK methodology. Handles all file I/O, Python execution, and git operations for prompt engineering tasks. |
| **Built-in** | ☐ (optional) |
| **System Prompt** | Paste full contents of `META-PROMPT-DEEPSEEK.md` |

**Tools — enable ALL:**

```
edit exec process read write
deepchat_question
skill_list skill_manage skill_view
```

---

### Agents NOT to create

| Agent | Reason |
|:------|:-------|
| Archive | `Projects` already reads `G:\My Drive\Archive\` |
| Notes | `Projects` already reads `G:\My Drive\Obsidian\notes\` |
| Releases | `Projects` already reads `G:\My Drive\Obsidian\releases\` |

---

## 2. SUBAGENT SLOT (copy into DeepChat subagent slot field)

### Slot: SELF-CLONE (`self`)

| Setting | Value |
|:--------|:------|
| **Slot ID** | `self` |
| **Target** | `current agent` |

**Copy this exact text into the subagent slot description:**

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

## 3. SUBAGENT TASK PROMPT TEMPLATE

Every task prompt sent to SELF-CLONE must include:

```
GIT: Skip all git/branch checks. Read-only task.

[ALL CONTENT INLINE — never reference file paths]

[Clear instructions for the text task]
```

**Example:**

```
GIT: Skip all git/branch checks. Read-only task.

Generate 3 headline variants for this article. Make one bold, one academic, one question-format.

ARTICLE TEXT:
[full article text pasted here]
```

---

## 4. CORE RULE

```
PARENT → all file I/O, Python, git → inline content → SELF-CLONE text synthesis → PARENT saves
```

- File reading: `Projects` or `Prompts` agent handles it
- File writing: `Projects` or `Prompts` agent handles it
- Python: `Projects` or `Prompts` agent handles it
- Git: `Projects` or `Prompts` agent handles it
- Text synthesis: SELF-CLONE (with all content inline, git-skip directive)

---

## 5. REMOVED (do not configure)

| Removed | Target | Why |
|:--------|:-------|:----|
| Archive agent | — | Projects already reads Archive |
| Notes agent | — | Projects already reads vault |
| Releases agent | — | Projects already reads releases |
| PROJECTS subagent slot (`slot-movio4vd-yj9c`) | target: `deepchat` | ~40% file I/O — unreliable |
| ARCHIVE subagent slot (`slot-movbn8bi-f61j`) | target: `deepchat-INfqIWc0` | 0% file I/O — cannot read Archive |
| AGENT_DEFAULTS.conf | — | Deleted — DeepChat doesn't read `.conf` files |
