# SUBAGENT ARCHITECTURE — Simplified (v3.0)

> **⚠️ ARCHITECTURAL STATUS (2026-05-11):** 20-test empirical study proved ALL subagent slots have non-deterministic tool availability (~35% full 32-tool set, ~65% limited to 18 base tools). The PARENT THREAD is the only guaranteed-capability entity. Subagents are text-synthesis-only. All file I/O, Python, git, skills, and settings MUST stay in the parent. See verification data at end of this document.

> **Last updated:** 2026-05-11 | **Version:** v3.0 (simplified — removes aspirational architecture, keeps only verified capabilities)

---

## QUICK SETUP DICTIONARY

### Standalone DeepChat Agents

| Agent | Create? | Tools to Enable | System Prompt |
|:------|:-------:|:----------------|:--------------|
| **Projects** | ✅ YES | **ALL**: `edit` `exec` `process` `read` `write` + `deepchat_question` + `skill_list` `skill_manage` `skill_view` | `DEFAULT.md` |
| Archive | ❌ NO | — | Projects reads `G:\My Drive\Archive\` directly |
| Notes | ❌ NO | — | Projects reads `G:\My Drive\Obsidian\notes\` directly |
| Prompts | ❌ NO | — | Prompt engineering done via META-PROMPT-DEEPSEEK in Projects |
| Releases | ❌ NO | — | Projects reads `G:\My Drive\Obsidian\releases\` directly |

### Subagent Slots (for subagent_orchestrator)

| Slot | Keep? | Slot ID | Copy-Paste Description |
|:-----|:-----:|:--------|:-----------------------|
| **SELF-CLONE** | ✅ KEEP | `self` | See Section 2 below |
| PROJECTS WORKSPACE | ❌ REMOVE | `slot-movio4vd-yj9c` | ~40% file I/O — unreliable |
| ARCHIVE RESEARCHER | ❌ REMOVE | `slot-movbn8bi-f61j` | 0% file I/O — cannot read Archive |
| NOTES RESEARCHER | ❌ DON'T CREATE | — | Never configured; don't start |
| RELEASES READER | ❌ DON'T CREATE | — | Never configured; don't start |
| PROMPTS AGENT | ❌ DON'T CREATE | — | Never configured; don't start |

---

## 1. STANDALONE AGENT CONFIGURATION

### 1.1 Projects (Primary Agent) — THE ONLY AGENT NEEDED

**DeepChat Agent Settings:**
```
Name: Projects
Built-in: ✅ Enabled
Tools:
  ☑ edit      ☑ exec      ☑ process      ☑ read      ☑ write
  ☑ deepchat_question
  ☑ skill_list    ☑ skill_manage    ☑ skill_view
System Prompt: DEFAULT.md (loaded via system_prompts.json or pasted into agent settings)
```

**What This Agent Does:**
- ALL file I/O — reads and writes every directory (`G:\My Drive\Archive\`, `projects\`, `Obsidian\notes\`, `Obsidian\releases\`, `prompts\`)
- ALL Python execution — calculations, data processing, quantitative analysis
- ALL git operations — branch management, commits, push/pull
- ALL skill management — inspecting and modifying skills
- ALL DeepChat settings modification
- Subagent orchestration — deploys SELF-CLONE for text synthesis tasks
- Buffer/GraphQL API operations

**Why Only One Agent Is Needed:**
The Projects agent already reads ALL directories. Separate Archive, Notes, Prompts, and Releases agents are just scoped entry points to the same filesystem — they provide context isolation but no unique capability. A single well-tooled agent eliminates duplicate configuration and simplifies the mental model.

**If You Want Context Isolation:**
Start a fresh Projects session and ask it to focus on one directory. The system prompt is the same — the session context provides the scoping.

---

## 2. SUBAGENT SLOT CONFIGURATION

### 2.1 SELF-CLONE — THE ONLY SUBAGENT SLOT NEEDED

**Slot ID:** `self` (always available — no configuration needed)

**Copy this description into the DeepChat subagent slot field:**

```
FRESH INSTANCE — Text Synthesis Only | target=current agent | Isolated clone for parallel text generation, blind validation, and reader testing. ALL subagent slots have non-deterministic tool availability (~35% chance of full 32-tool set, ~65% chance of limited 18-tool set). NEVER rely on this slot for file I/O, Python, git, skills, or settings. Provide ALL content inline.

CONFIRMED CAPABILITIES (always available):
  - LLM reasoning and text generation
  - Prompt template filling (fill_prompt_template, etc.)
  - Conversation history search (search_conversations, etc.)
  - Buffer/GraphQL API (get_account, create_post, execute_query, etc.)

UNRELIABLE CAPABILITIES (~35% chance, never depend on):
  - File I/O (read, write, edit)
  - Python/shell execution (exec, process)
  - Skills (skill_list, skill_view, skill_manage)
  - DeepChat settings (deepchat_settings_*)
  - User interaction (deepchat_question)
  - Subagent orchestration (subagent_orchestrator)

USE FOR (always works):
  • Parallel text generation — provide ALL inputs inline
  • Blind validation — provide content inline (clone cannot read files)
  • Reader testing — "how does this read to a new audience?"
  • Prompt template filling
  • Conversation history search
  • Buffer/GraphQL API operations

DO NOT USE FOR:
  • File reading — "read paper.md" WILL FAIL ~65% of invocations
  • File writing — "save output" WILL FAIL ~65% of invocations
  • Python execution — "calculate statistics" WILL FAIL ~65% of invocations
  • Git operations — WILL FAIL or burn response budget
  • Skill/settings modification

GIT: Skip all git/branch checks. Read-only task. Proceed directly to assigned work.
```

### 2.2 Removed Subagent Slots — Why and What to Use Instead

| Removed Slot | Reason for Removal | What to Use Instead |
|:-------------|:-------------------|:--------------------|
| **PROJECTS WORKSPACE** (`slot-movio4vd-yj9c`) | ~40% chance of file write access. Unreliable for its designed primary function (file I/O). | **PARENT THREAD** — 100% reliable file I/O. Parent writes all files; subagents return text for parent to save. |
| **ARCHIVE RESEARCHER** (`slot-movbn8bi-f61j`) | 0% observed file read access (0 for 2 tests). Cannot read `G:\My Drive\Archive\` — its entire reason for existing is impossible. | **PARENT THREAD** — reads archive files, provides content inline to SELF-CLONE for synthesis, saves any output. |
| **NOTES RESEARCHER** | Never configured. Would have same ~65% failure rate. Cannot read vault. | **PARENT THREAD** — searches `G:\My Drive\Obsidian\notes\` directly. |
| **RELEASES READER** | Never configured. Would have same ~65% failure rate. Cannot read releases. | **PARENT THREAD** — reads `G:\My Drive\Obsidian\releases\` directly. |
| **PROMPTS AGENT** | Never configured. Prompt engineering already handled by META-PROMPT-DEEPSEEK in parent thread. | **PARENT THREAD** — runs META-PROMPT-DEEPSEEK methodology directly. |

---

## 3. VERIFIED WORKFLOW PATTERNS

These patterns are proven to work based on the 20-test empirical study. All aspirational multi-agent pipeline patterns (Research → Write, Triple Knowledge Coverage, Full Historical Coverage, Notes-Informed Research, Social Publication Pipeline) have been removed — they depended on subagent capabilities that don't exist.

### Pattern A: Parallel Text Generation

**When:** You need multiple text variants (headlines, angles, summaries) generated simultaneously.

**How:**
```
PARENT → deploys 3-5 SELF-CLONEs in parallel mode
       → each clone receives the SAME source text INLINE in its prompt
       → each clone generates a different variant/angle
       → PARENT aggregates, removes redundancy, synthesizes
```

**Example orchestrator call:**
```
subagent_orchestrator(mode="parallel", tasks=[
  {slotId: "self", title: "Variant A: Bold", prompt: "GIT: Skip all git checks. Read-only task. Generate a bold, attention-grabbing headline for this article: [ARTICLE TEXT INLINE]"},
  {slotId: "self", title: "Variant B: Academic", prompt: "GIT: Skip all git checks. Read-only task. Generate an academic-style headline for this article: [ARTICLE TEXT INLINE]"},
  {slotId: "self", title: "Variant C: Question", prompt: "GIT: Skip all git checks. Read-only task. Generate a question-format headline for this article: [ARTICLE TEXT INLINE]"},
])
```

**⚠️ REQUIRED in every task prompt:**
- `GIT: Skip all git/branch checks. Read-only task.` — prevents git overhead
- ALL source content provided INLINE — never reference file paths
- Self-contained prompt — clone starts with ZERO context

### Pattern B: Blind Validation

**When:** You need an unbiased review of a claim, argument, or generated content.

**How:**
```
PARENT → deploys 1 SELF-CLONE
       → clone receives the content to validate INLINE
       → clone does NOT see the parent's reasoning or context
       → clone evaluates and returns findings
       → PARENT reviews the blind audit
```

**Example task prompt:**
```
GIT: Skip all git checks. Read-only task.

Review the following claim for accuracy, completeness, and bias:

[CLAIM TEXT INLINE]

Evaluate:
1. Is every factual claim traceable to a verifiable source?
2. Are there any unsupported assertions?
3. Is the reasoning logically sound?
4. What's missing?

Return a structured audit with specific citations to the inline text.
```

### Pattern C: Reader Testing

**When:** You need to know how content reads to someone unfamiliar with the project.

**How:** Same as Pattern B, but the clone evaluates clarity, accessibility, and assumed knowledge.

**Example task prompt:**
```
GIT: Skip all git checks. Read-only task.

You are a naive reader with NO prior knowledge of this project. Read the following content and answer:

[CONTENT INLINE]

1. What concepts are unclear or unexplained?
2. Where do you feel lost?
3. What jargon needs definition?
4. What questions do you have that the text doesn't answer?

Be brutally honest. You are encountering this material for the first time.
```

### Pattern D: Parent-Reads → Clone-Synthesizes → Parent-Saves

**When:** You need to process files (archive, vault, releases) and generate synthesized output.

**How:**
```
Step 1: PARENT — reads files, executes Python, extracts data
Step 2: PARENT — provides extracted content INLINE in SELF-CLONE prompt
Step 3: SELF-CLONE — synthesizes, finds patterns, generates text
Step 4: PARENT — saves output to files
```

**This is the only viable multi-step file-dependent workflow.** Subagents cannot read or write files reliably. The parent does all file I/O.

**Example:**
```
# Step 1: Parent reads archive files
PARENT reads 3 papers from G:\My Drive\Archive\ and extracts key findings

# Step 2: Parent deploys clone with inline content
subagent_orchestrator(mode="chain", tasks=[
  {slotId: "self", title: "Synthesize Findings", prompt: "GIT: Skip all git checks. Read-only task. Synthesize these three papers into a unified analysis: [PAPER 1 TEXT] [PAPER 2 TEXT] [PAPER 3 TEXT]. Identify common themes, contradictions, and gaps."},
])

# Step 3: Clone returns synthesized analysis

# Step 4: Parent saves
PARENT writes the analysis to G:\My Drive\projects\analysis.md
```

---

## 4. FAILSAFE CHECKLIST

Before every subagent orchestration call, verify:

```
□ Task is TEXT-ONLY (synthesis, generation, validation, search)
  → If NO: handle in PARENT

□ NO file I/O required from subagent
  → If YES: handle in PARENT, provide content inline

□ NO Python execution required from subagent
  → If YES: handle in PARENT, provide results inline

□ NO git operations required from subagent
  → If YES: handle in PARENT

□ ALL content provided INLINE in task prompt
  → If NO: parent must read files and inline the content

□ Git-skip directive present: "GIT: Skip all git/branch checks. Read-only task."
  → If NO: add it — prevents git overhead from consuming response budget

□ Task prompt is self-contained (clone has ZERO context)
  → If NO: add all necessary context inline

□ Under 5 subagents per orchestrator call
  → If over: split into multiple calls

□ Expected output format is specified in task prompt
  → If NO: add expectedOutput contract
```

---

## 5. GIT PROTOCOL FOR SUBAGENTS

**Why git is disabled for subagents:**
- ~65% of subagent invocations lack `exec` tool — cannot run git commands
- ~65% lack `write`/`edit` tools — cannot create commits
- Subagents inherit the full git protocol from DEFAULT.md, causing them to burn response budget on irrelevant branch checks
- Read-only text synthesis tasks have zero need for git operations
- Observed failure: a critical review subagent spent its entire response on git branch management and never reached the analysis task

**Required directive in every subagent task prompt:**
```
GIT: Skip all git/branch checks. Read-only task. Proceed directly to assigned work.
```

**This is Heuristic #8 in DEFAULT.md's delegation section.**

---

## 6. EMPIRICAL VERIFICATION DATA

### 20-Test Aggregate Results (2026-05-11)

| Slot | Tests | Full-Tool (32) | Limited (18) | Rate |
|:-----|:-----:|:-------------:|:------------:|:----:|
| SELF-CLONE (`self`) | 13 | 5 | 8 | 38% |
| PROJECTS (`slot-movio4vd-yj9c`) | 5 | 2 | 3 | 40% |
| ARCHIVE (`slot-movbn8bi-f61j`) | 2 | 0 | 2 | 0% |
| **ALL SLOTS** | **20** | **7** | **13** | **35%** |

### What "Full-Tool" (32) Includes
`read`, `write`, `edit`, `exec`, `process`, `subagent_orchestrator`, `deepchat_question`, `skill_list`, `skill_view`, `skill_manage`, `deepchat_settings_*` (5), plus the 18 base tools.

### What "Limited" (18) Includes — ALWAYS AVAILABLE
`list_all_prompt_template_names`, `get_prompt_template_parameters`, `fill_prompt_template`, `search_conversations`, `search_messages`, `get_conversation_history`, `get_conversation_stats`, `get_account`, `list_channels`, `get_channel`, `list_posts`, `get_post`, `create_idea`, `create_post`, `delete_post`, `introspect_schema`, `execute_query`, `execute_mutation`

### Key Findings
1. Tool availability is platform-level non-determinism — no prompt-engineering fix
2. No slot is reliably file-capable (~35% overall success rate)
3. Subagents are useful ONLY for text synthesis from inline content
4. The parent thread is the only 100% reliable entity
5. Git overhead (inherited from DEFAULT.md) paralyzes subagents

---

## 7. ORCHESTRATOR TOOL REFERENCE

```
subagent_orchestrator(mode="parallel"|"chain", tasks=[...])
```

**Available slotId (only one needed):**
- `"self"` — SELF-CLONE

**Constraints:**
- Maximum 5 tasks per call
- Each task needs: `slotId`, `title`, `prompt`
- Optional: `id`, `expectedOutput`
- Chain mode: tasks execute sequentially
- Parallel mode: all tasks execute simultaneously

---

**[END OF SUBAGENT DESCRIPTIONS v3.0 — Simplified | 1 agent + 1 subagent slot | PARENT ONLY for file I/O/Python/git]**
