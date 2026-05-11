# DEEPCHAT SETUP GUIDE — Everything In `G:\My Drive\prompts\`

**Purpose:** This is the MASTER reference. One document to answer: what every file IS, where it GOES in DeepChat, and WHEN to use it.

**Last updated:** 2026-05-11

---

## THE BIG PICTURE — Two Kinds of Files

```
G:\My Drive\prompts\
│
├── SYSTEM PROMPTS (6 files)           ← PASTE THESE INTO DEEPCHAT AGENTS
│   They ARE the agent's brain.        ← Go in: Settings → Agents → [Agent] → System Prompt
│
├── PROJECT RECORDS (7 files)          ← STAY HERE. Agents READ these.
│   Track the prompts project itself.  ← Never pasted anywhere.
│
├── CONFIG REFERENCE (1 file)          ← COPY VALUES from here into settings.
│   Setup checklist.                   ← Read when configuring agents/subagents.
│
└── GIT CONFIG (1 file)               ← Leave alone. Git needs it.
```

---

## A. SYSTEM PROMPTS — Paste Into DeepChat Agents

### Agent Setup Table (Copy/Paste This)

| Agent Name | System Prompt File | Paste This File Content | Tools to Enable |
|:-----------|:-------------------|:------------------------|:----------------|
| **Projects** | `DEFAULT.md` | Paste the ENTIRE file | `read write edit exec process deepchat_question skill_list skill_view skill_manage` |
| **Prompts** | `META-PROMPT-DEEPSEEK.md` | Paste the ENTIRE file | (same as Projects) |
| **Social** | `SOCIAL-ORCHESTRATOR-v4.0.md` | Paste the ENTIRE file | (same as Projects) |
| **Image Gen** | `image-gen-banner-prompt.md` | Paste the ENTIRE file | (same as Projects) |

### When To Use Each Agent

| You want to... | Use this agent | Because... |
|:---------------|:---------------|:-----------|
| Research, write, code, brainstorm, do project work | **Projects** | General-purpose. Handles everything. |
| Create or improve a system prompt | **Prompts** | Specialized prompt compiler/auditor. |
| Schedule social media posts, manage Buffer | **Social** | Has Buffer API integration. |
| Generate banner images for blog/social | **Image Gen** | Specialized image generation. |

### Advanced: Adding Project Isolation

When working on a SPECIFIC project under `G:\My Drive\projects\` (e.g., QWAV, Undecidability):

**Option A: Full Kaizen Framework (Recommended for new projects)**
```
Prepend this BEFORE DEFAULT.md in the Projects agent's System Prompt:

PROJECT: <your-project-name>
WORKSPACE: G:\My Drive\projects\<your-project-name>\
SHARED: G:\My Drive\projects\_shared\

[paste PROJECT-ORCHESTRATION-FRAMEWORK-v1.0.md here]

---

[paste DEFAULT.md here]
```

**Option B: Lightweight Isolation Only**
```
PROJECT: <your-project-name>
WORKSPACE: G:\My Drive\projects\<your-project-name>\

[paste PROJECT-ISOLATION-ENFORCER-v1.0.md here]

---

[paste DEFAULT.md here]
```

---

## B. PROJECT RECORDS — These Stay Here. Never Pasted.

These 7 files are the **kaizen documentation** for the `prompts/` project itself. Agents read them to know the state of prompt engineering work. They are NOT system prompts.

| File | What It Tells An Agent | When An Agent Reads It |
|:-----|:-----------------------|:-----------------------|
| `PROJECT STATE.md` | "Here's everything about the prompts project — what we've done, what's next, what's broken" | **First** — every session start |
| `SPRINT.md` | "Here are the current tasks. Work on the highest-priority incomplete one." | After PROJECT STATE |
| `LEARNINGS.md` | "Don't repeat these 7 mistakes. Here's what we learned." | Before starting work |
| `CHANGELOG.md` | "Here's what changed in the last session." | After LEARNINGS (last entry only) |
| `BACKLOG.md` | "Here's everything we want to do eventually (15 items, prioritized)" | During sprint planning |
| `DECISIONS.md` | "Here's WHY we chose this architecture (6 key decisions)" | When questioning "why did we do it this way?" |
| `README.md` | "This is the prompts project — it produces system prompts for other agents" | Rarely — project identity |

---

## C. CONFIG REFERENCE — Copy Values From Here

| File | What It Contains | Where Values Go |
|:-----|:-----------------|:----------------|
| `SUBAGENT_DESCRIPTIONS.md` | Agent names, tool lists, subagent slot configuration, task prompt templates | Settings → Agents (agent fields) + Settings → Subagent (slot fields) |

---

## QUICK-START: Configure Everything (Step by Step)

### Step 1: Create/Update Agents

```
DeepChat Settings → Agents → [agent name]

For each agent below, paste the FULL file content into System Prompt,
and enable the listed tools.
```

| Agent | System Prompt (paste file) | Tools (enable checkboxes) |
|:------|:---------------------------|:--------------------------|
| Projects | DEFAULT.md | read, write, edit, exec, process, deepchat_question, skill_list, skill_view, skill_manage |
| Prompts | META-PROMPT-DEEPSEEK.md | (same) |
| Social | SOCIAL-ORCHESTRATOR-v4.0.md | (same) |
| Image Gen | image-gen-banner-prompt.md | (same) |

### Step 2: Configure Subagent Slot

```
DeepChat Settings → Subagent Slots → SELF-CLONE (slot ID: self)
```

Paste this as the slot description (from SUBAGENT_DESCRIPTIONS.md Section 2):
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

### Step 3: Use The Right Agent

- Starting research or writing? → Switch to **Projects** agent
- Creating a new system prompt? → Switch to **Prompts** agent
- Scheduling social posts? → Switch to **Social** agent
- Need a banner image? → Switch to **Image Gen** agent

---

## FILE INVENTORY (Complete, 15 Files)

| # | File | Category | Goes Where? | Size |
|:--|:-----|:---------|:------------|:-----|
| 1 | `DEFAULT.md` | System Prompt | Projects agent → System Prompt | 43 KB |
| 2 | `META-PROMPT-DEEPSEEK.md` | System Prompt | Prompts agent → System Prompt | 15 KB |
| 3 | `SOCIAL-ORCHESTRATOR-v4.0.md` | System Prompt | Social agent → System Prompt | 11 KB |
| 4 | `PROJECT-ORCHESTRATION-FRAMEWORK-v1.0.md` | System Prompt | Prepended to Projects agent (for kaizen projects) | 32 KB |
| 5 | `PROJECT-ISOLATION-ENFORCER-v1.0.md` | System Prompt | Prepended to Projects agent (lighter alternative to #4) | 22 KB |
| 6 | `image-gen-banner-prompt.md` | System Prompt | Image Gen agent → System Prompt | 2 KB |
| 7 | `SUBAGENT_DESCRIPTIONS.md` | Config Reference | Copy values into Agent/Subagent settings | 4 KB |
| 8 | `PROJECT STATE.md` | Project Record | Stays in `G:\My Drive\prompts\` — read by agents | 5 KB |
| 9 | `SPRINT.md` | Project Record | Stays in `G:\My Drive\prompts\` — read by agents | 3 KB |
| 10 | `CHANGELOG.md` | Project Record | Stays in `G:\My Drive\prompts\` — read by agents | 4 KB |
| 11 | `BACKLOG.md` | Project Record | Stays in `G:\My Drive\prompts\` — read by agents | 3 KB |
| 12 | `LEARNINGS.md` | Project Record | Stays in `G:\My Drive\prompts\` — read by agents | 10 KB |
| 13 | `DECISIONS.md` | Project Record | Stays in `G:\My Drive\prompts\` — read by agents | 9 KB |
| 14 | `README.md` | Project Record | Stays in `G:\My Drive\prompts\` — read by agents | 4 KB |
| 15 | `.gitattributes` | Git Config | Leave alone | 0.1 KB |

---

## DECISION TREE: Which File Do I Need?

```
Q: What do you want to do?

├─ "Do general research, writing, or coding"
│  └─ Use: DEFAULT.md → Projects agent
│
├─ "Create or improve a system prompt"
│  └─ Use: META-PROMPT-DEEPSEEK.md → Prompts agent
│
├─ "Schedule or manage social media posts"
│  └─ Use: SOCIAL-ORCHESTRATOR-v4.0.md → Social agent
│
├─ "Generate a banner image"
│  └─ Use: image-gen-banner-prompt.md → Image Gen agent
│
├─ "Start a NEW project under G:\My Drive\projects\"
│  └─ Use: PROJECT-ORCHESTRATION-FRAMEWORK-v1.0.md (prepend to Projects agent)
│
├─ "Just prevent agents from mixing up projects"
│  └─ Use: PROJECT-ISOLATION-ENFORCER-v1.0.md (prepend to Projects agent)
│
├─ "Configure subagent slots"
│  └─ Read: SUBAGENT_DESCRIPTIONS.md → copy values into Settings
│
├─ "Know what the prompts project is working on"
│  └─ Read: PROJECT STATE.md, SPRINT.md
│
├─ "Know what mistakes to avoid"
│  └─ Read: LEARNINGS.md
│
└─ "Know why we made certain architecture choices"
   └─ Read: DECISIONS.md
```
