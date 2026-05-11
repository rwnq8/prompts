# DEEPCHAT AGENT/SUBAGENT SETUP (v4.0)

> **WHAT THIS IS:** The master configuration reference. Copy the exact values below into DeepChat Settings.
> **WHAT THIS IS NOT:** A system prompt. This file stays in `G:\My Drive\prompts\`.
> **Companion file:** `SETUP-GUIDE.md` — decision tree and file inventory. Read that if you're unsure which prompt to use.

---

## WHERE TO FIND THESE SETTINGS IN DEEPCHAT

```
DeepChat → Settings (gear icon, bottom-left)
├── Agents tab       → Create/edit agents, paste System Prompts, enable tools
├── Subagents tab    → Configure subagent slots
├── Prompts tab      → Prompt templates
└── General tab      → Theme, language, font size
```

---

## 1. AGENTS — Create/Update These

### Navigation: Settings → Agents → [+ Add] or click existing agent

---

### Agent: Projects

| Field | Value |
|:------|:------|
| **Name** | `Projects` |
| **Description** | General-purpose research, writing, coding, and project work. Handles all file I/O, Python, git, and subagent orchestration. |
| **Built-in** | ✅ Enabled |
| **System Prompt** | Paste the ENTIRE contents of `DEFAULT.md` |

**Tools — enable checkboxes for:**

```
read
write
edit
exec
process
deepchat_question
skill_list
skill_view
skill_manage
```

---

### Agent: Prompts

| Field | Value |
|:------|:------|
| **Name** | `Prompts` |
| **Description** | System prompt compiler and auditor. Creates, reviews, and improves system prompts. Handles all file I/O, Python, and git for prompt engineering tasks. |
| **Built-in** | ☐ (optional) |
| **System Prompt** | Paste the ENTIRE contents of `META-PROMPT-DEEPSEEK.md` |

**Tools — enable checkboxes for:**

```
read
write
edit
exec
process
deepchat_question
skill_list
skill_view
skill_manage
```

---

### Agent: Social (CREATE NEW if doesn't exist)

| Field | Value |
|:------|:------|
| **Name** | `Social` |
| **Description** | Social media orchestrator. Manages Buffer posts, campaigns, and content calendars across all platforms. |
| **Built-in** | ☐ |
| **System Prompt** | Paste the ENTIRE contents of `SOCIAL-ORCHESTRATOR-v4.0.md` |

**Tools — enable checkboxes for:**

```
read
write
edit
exec
process
deepchat_question
skill_list
skill_view
skill_manage
```

---

### Agent: Image Gen (CREATE NEW if doesn't exist)

| Field | Value |
|:------|:------|
| **Name** | `Image Gen` |
| **Description** | Banner and social media image generator. |
| **Built-in** | ☐ |
| **System Prompt** | Paste the ENTIRE contents of `image-gen-banner-prompt.md` |

**Tools — enable checkboxes for:**

```
read
write
edit
exec
process
deepchat_question
skill_list
skill_view
skill_manage
```

---

### Agent: Project Kaizen (CREATE NEW — optional, for projects using full kaizen)

| Field | Value |
|:------|:------|
| **Name** | `Project Kaizen` |
| **Description** | Full kaizen project management — sprint lifecycle, cross-project learning, 7-file documentation, workspace isolation. |
| **Built-in** | ☐ |
| **System Prompt** | Prepend your project header, then paste `PROJECT-ORCHESTRATION-FRAMEWORK-v1.0.md`, then paste `DEFAULT.md`. See setup below. |

**System Prompt assembly for Project Kaizen:**
```
PROJECT: <your-project-name>
WORKSPACE: G:\My Drive\projects\<your-project-name>\
SHARED: G:\My Drive\projects\_shared\

[paste PROJECT-ORCHESTRATION-FRAMEWORK-v1.0.md here]

---

[paste DEFAULT.md here]
```

**Tools — enable checkboxes for:**
```
read
write
edit
exec
process
deepchat_question
skill_list
skill_view
skill_manage
```

---

## 2. AGENTS NOT TO CREATE

| Agent | Reason |
|:------|:-------|
| Archive | Projects agent already reads `G:\My Drive\Archive\` |
| Notes | Projects agent already reads `G:\My Drive\Obsidian\notes\` |
| Releases | Projects agent already reads `G:\My Drive\Obsidian\releases\` |
| Any agent with fewer tools | The 8-tool set (read/write/edit/exec/process/deepchat_question/skill_list/skill_view/skill_manage) is the minimum for productive work |

---

## 3. SUBAGENT SLOT — SELF-CLONE

### Navigation: Settings → Subagents → SELF-CLONE slot

| Field | Value |
|:------|:------|
| **Slot ID** | `self` |
| **Target** | `current agent` |

**Slot Description — paste this EXACT text:**

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

## 4. SUBAGENT TASK PROMPT TEMPLATE

Every task prompt sent to the SELF-CLONE subagent MUST start with:

```
GIT: Skip all git/branch checks. Read-only task.

[ALL CONTENT INLINE — never reference file paths]

[Clear instructions for the text task]
```

**Example:**
```
GIT: Skip all git/branch checks. Read-only task.

Generate 3 headline variants for this article. One bold, one academic, one question-format.

ARTICLE TEXT:
[full article text pasted here — no file references]
```

---

## 5. CORE RULE — Parent Does File I/O, Subagents Do Text Only

```
PARENT → all file I/O, Python, git, skills, settings
       → extracts content from files
       → pastes content INLINE into subagent prompts
       → subagents synthesize text
       → PARENT saves output to files
```

- File reading: **Projects** or **Prompts** agent handles it
- File writing: **Projects** or **Prompts** agent handles it
- Python: **Projects** or **Prompts** agent handles it
- Git: **Projects** or **Prompts** agent handles it
- Text synthesis: SELF-CLONE subagent (all content inline, git-skip directive)

---

## 6. COMPLETE AGENT INVENTORY

| Agent | Prompt File | When Used | Priority |
|:------|:------------|:----------|:---------|
| **Projects** | `DEFAULT.md` | General research, writing, coding, project work | PRIMARY |
| **Prompts** | `META-PROMPT-DEEPSEEK.md` | Create/improve system prompts | SECONDARY |
| **Social** | `SOCIAL-ORCHESTRATOR-v4.0.md` | Manage Buffer social media | WHEN NEEDED |
| **Image Gen** | `image-gen-banner-prompt.md` | Generate banner images | WHEN NEEDED |
| **Project Kaizen** | `PROJECT-ORCHESTRATION-FRAMEWORK-v1.0.md` + `DEFAULT.md` | Full kaizen project management | NEW PROJECTS |

---

## 7. WHAT THE SETTINGS TOOLS CAN AND CANNOT DO

| I CAN do this via tools | I CANNOT do this — YOU must do it manually |
|:------------------------|:------------------------------------------|
| Toggle sound on/off | Create agents |
| Toggle copy-with-COT on/off | Paste system prompts into agents |
| Set language (en-US, zh-CN, etc.) | Configure subagent slots |
| Set theme (dark/light/system) | Enable/disable agent tools |
| Set font size (0-4) | Change model/provider settings |
| | Edit MCP/server configurations |
| | Edit knowledge bases |
| | Change API keys or paths |

**Bottom line:** All agent creation, prompt pasting, and tool configuration MUST be done manually in Settings → Agents. The SETUP-GUIDE.md and this file tell you exactly what to paste where.
