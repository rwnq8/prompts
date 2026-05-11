# SUBAGENT DESCRIPTIONS — Dispatch Reference & Orchestration Protocol

> **⚠️ ARCHITECTURAL STATUS (2026-05-11):** 20-test empirical study proves ALL subagent slots have non-deterministic tool availability (~35% full tools, ~65% limited to 18 base tools). **The PARENT THREAD is the only guaranteed-capability entity.** Subagents are text-synthesis-only. All file I/O, Python, and git MUST stay in the parent. Read Section 0.5 for the full study, Section 0.6 for the Git Overhead Problem, and the Best Practices checklist at the end of this document.

> **Purpose:** Definitive reference for configuring DeepChat subagent slots.
> **Last updated:** 2026-05-11 | **Scope:** 6 subagents (3 active + 3 pending)
> **⚠️ v2.5:** 20-test study + Git Overhead Problem documented. ALL subagents non-deterministic. PARENT ONLY for file I/O/Python/git. Include git-skip in subagent task prompts.

---

## 0. SUBAGENT ARCHITECTURE OVERVIEW

The main agent has access to the `subagent_orchestrator` tool. **⚠️ ALL subagent slots have non-deterministic tool availability (~35% chance of full tools, ~65% limited to 18 base tools). See Section 0.5 for the 20-test empirical study.**

| Slot ID | Agent Name | Status | Role |
|:--------|:-----------|:-------|:-----|
| `self` | SELF CLONE | **ACTIVE** | Text synthesis, blind validation, parallel generation |
| `slot-movio4vd-yj9c` | PROJECTS WORKSPACE | **ACTIVE** | Text synthesis, prompt templates, conversation search |
| `slot-movbn8bi-f61j` | ARCHIVE RESEARCHER | **ACTIVE** | Text synthesis, prompt templates, conversation search |
| *(pending)* | NOTES RESEARCHER | **PENDING** | Text synthesis (same limited-tool pattern) |
| *(pending)* | RELEASES READER | **PENDING** | Text synthesis (same limited-tool pattern) |
| *(pending)* | PROMPTS AGENT | **PENDING** | Text synthesis (same limited-tool pattern) |

**⚠️ CRITICAL RULE:** File I/O, Python execution, git operations, skill management — ALL belong in the PARENT thread. Subagents are text-synthesis-only. Never delegate tool-dependent work to any subagent slot.

---

## 0.5 ⚠️ DEFINITIVE TOOL AVAILABILITY — 20-Test Empirical Study (2026-05-11)

**20 subagent invocations across 3 slots were tested over 5 orchestration runs. Each was asked to introspect its tool definitions and attempt live tool calls.** Results below are definitive.

### Aggregate Results

| Slot | Total Tests | Full-Tool (32) | Limited (18) | Success Rate |
|:-----|:-----------:|:-------------:|:------------:|:------------:|
| SELF-CLONE (`self`) | 13 | 5 | 8 | **~38%** |
| PROJECTS (`slot-movio4vd-yj9c`) | 5 | 2 | 3 | **~40%** |
| ARCHIVE (`slot-movbn8bi-f61j`) | 2 | 0 | 2 | **~0%** |
| **ALL SLOTS** | **20** | **7** | **13** | **~35%** |

### What "Full-Tool" (32 tools) Includes
`read`, `write`, `edit`, `exec`, `process`, `subagent_orchestrator`, `deepchat_question`, `skill_list`, `skill_view`, `skill_manage`, `deepchat_settings_*` (5), plus the 18 base tools.

### What "Limited" (18 tools) Includes — Always Available
`list_all_prompt_template_names`, `get_prompt_template_parameters`, `fill_prompt_template`, `search_conversations`, `search_messages`, `get_conversation_history`, `get_conversation_stats`, `get_account`, `list_channels`, `get_channel`, `list_posts`, `get_post`, `create_idea`, `create_post`, `delete_post`, `introspect_schema`, `execute_query`, `execute_mutation`

### ⚠️ DEFINITIVE CONCLUSIONS

1. **Tool availability is platform-level non-determinism.** No prompt-engineering technique, keyword trigger, slot selection, or retry strategy can reliably produce the full 32-tool set. Approximately 35% of invocations get full tools; 65% get limited tools.

2. **NO subagent slot is reliably file-capable.** PROJECTS was previously thought to be 100% reliable, but the 5-test battery showed only 40% reliability. SELF-CLONE shows ~38%. ARCHIVE shows ~0% (but sample size is small — it may follow the same distribution).

3. **The parent thread is the ONLY guaranteed-capability entity.** The main agent ALWAYS has full 32-tool access including file I/O, Python, skills, and settings.

4. **Subagents are useful ONLY for text synthesis.** All subagents reliably have LLM reasoning, prompt templates, conversation search, and Buffer API. They can synthesize, analyze, and generate text from inline-provided content. They CANNOT be relied upon for any tool-dependent operation.

5. **Prompt content correlation is weak.** File-requesting prompts had ~50% success (2 of 4), code-requesting prompts had 0% (0 of 1), pure-text prompts had 0% (0 of 1). The correlation exists but is not strong enough to use as a reliable trigger.

### The Only Viable Architecture

```
┌─────────────────────────────────────────────────────────┐
│  PARENT THREAD (100% reliable, 32 tools)                 │
│  • ALL file I/O (read, write, edit)                      │
│  • ALL Python execution (exec, process)                  │
│  • ALL skill management, settings, user interaction      │
│  • ALL git operations                                    │
│  • Subagent orchestration (subagent_orchestrator)        │
├─────────────────────────────────────────────────────────┤
│  ↓ provides content INLINE                              │
├─────────────────────────────────────────────────────────┤
│  SUBAGENTS (65% limited to 18 tools, 35% full tools)     │
│  • Text synthesis, ideation, brainstorming ✅ ALWAYS     │
│  • Prompt template filling ✅ ALWAYS                      │
│  • Conversation search ✅ ALWAYS                          │
│  • Buffer/GraphQL API ✅ ALWAYS                           │
│  • File I/O ❌ UNRELIABLE — never depend on this         │
│  • Python ❌ UNRELIABLE — never depend on this           │
│  • Skills/settings ❌ UNRELIABLE — never depend on this  │
└─────────────────────────────────────────────────────────┘
```

### Corrected Dispatch Strategy (FINAL)

| Task | Dispatch To | Rationale |
|:-----|:------------|:----------|
| File I/O (read/write) | **PARENT ONLY** | No subagent reliably has file access |
| Python execution | **PARENT ONLY** | No subagent reliably has exec |
| Git operations | **PARENT ONLY** | No subagent reliably has exec |
| Skill management | **PARENT ONLY** | No subagent reliably has skill tools |
| Text synthesis from inline content | ANY subagent | All slots always have LLM reasoning |
| Prompt template filling | ANY subagent | Universally available |
| Conversation search | ANY subagent | Universally available |
| Buffer/GraphQL API | ANY subagent | Universally available |
| Parallel text generation | SELF-CLONE × N | Provide all inputs inline |
| Blind validation / reader testing | SELF-CLONE | Provide content inline |

---

## 0.6 ⚠️ THE GIT OVERHEAD PROBLEM (Discovered 2026-05-11)

**Subagents inherit the full system prompt including mandatory git discipline (pre-flight checks, branch verification, commit requirements). This causes subagents to burn their response budget on git operations that are irrelevant to their delegated task.**

### Observed Failure Pattern
A critical review subagent (self-clone) was deployed to analyze prompt files. Instead of reading and reviewing files, the subagent:
1. Detected it was on an unexpected branch (`feature/fix-social-media-line-breaks`)
2. Attempted to create a new feature branch
3. Spent its **entire response budget** on git operations
4. **Never reached the actual analysis task**

Archive and notes search subagents were similarly paralyzed by git pre-flight checks. Result: **zero task progress — subagents burned their budget on git operations irrelevant to read-only analysis.**

### Root Cause
The system prompt generator's mandatory git protocol (inherited from DEFAULT.md and enforced by META-PROMPT-DEEPSEEK.md) requires EVERY agent to:
1. Verify it's on a feature branch before any file operation
2. Create a feature branch if on main/master
3. Commit after every file change
4. Verify commits exist

Subagents inherit this full protocol but:
- ~65% of the time CANNOT write files (no `write`/`edit` tools)
- Are deployed for read-only tasks (search, review, synthesis)
- Have no use for git operations
- Are confused by unexpected branch states

### Mitigation

**For task prompts to subagents:** Explicitly instruct subagents to SKIP git operations:
```
GIT: Do NOT perform git pre-flight checks. Do NOT check branches. Do NOT commit. 
This is a read-only subagent task. Proceed directly to the assigned work.
```

**For DEFAULT.md delegation section:** Updated to recommend including the git-skip directive in all subagent task prompts.

**For subagent system prompts (long-term):** Consider scoping git requirements — full protocol for write-capable agents, no protocol for read-only subagents. This requires prompt-level changes to DEFAULT.md or META-PROMPT-DEEPSEEK.md.

### Combined Impact
| Problem | Severity | Subagents Affected |
|:--------|:---------|:-------------------|
| Tool non-determinism (~35% full, ~65% limited) | CRITICAL | ALL slots |
| Git overhead (response budget consumed) | HIGH | ALL subagents with inherited git protocol |
| Combined: subagent gets limited tools AND burns budget on git | FATAL | ~65% of invocations — subagent achieves nothing |

**The safe pattern:** PARENT handles ALL file I/O, Python, AND git. Subagents receive clean task prompts with explicit git-skip directives and inline content only.

---

## 1. SELF CLONE

### Slot-Ready Description (copy into DeepChat slot field)
```
FRESH INSTANCE — Clean Slate, Zero Context | target=current agent | Isolated clone. ALL subagent slots have NON-DETERMINISTIC tool availability (~35% chance of full 32-tool set, ~65% chance of limited 18-tool set). NEVER rely on this slot for file I/O or Python.

TARGET: current agent (self-clone)

⚠️ DEFINITIVE TOOL AVAILABILITY (20-test empirical study, 2026-05-11):
  13 tests across this slot: 5 full-tool (38%), 8 limited (62%). File I/O and Python are UNRELIABLE.

ALWAYS AVAILABLE (18 base tools):
  - LLM inference and text generation
  - Prompt templates (fill_prompt_template, etc.)
  - Conversation search (search_conversations, etc.)
  - Buffer/GraphQL API (get_account, create_post, execute_query, etc.)

UNRELIABLE (~35% chance of availability):
  - File I/O (read, write, edit)
  - Python/shell execution (exec, process)
  - Skills (skill_list, skill_view, skill_manage)
  - Settings (deepchat_settings_*)
  - User interaction (deepchat_question)

USE THIS SUBAGENT FOR (ALWAYS WORKS):
  • Pure LLM reasoning, ideation, brainstorming
  • Parallel text generation — ALL inputs inline
  • Reader testing / blind validation — content inline
  • Prompt template filling
  • Conversation history search
  • Buffer/GraphQL API operations

DO NOT USE FOR:
  • ANY file-dependent task — ~62% chance of failure
  • ANY Python-dependent task — ~62% chance of failure
  • ANY task requiring skills or settings

⚠️ CONTEXT: Clone starts with ZERO context. ALL content must be provided INLINE. Never reference file paths.

### Extended Dispatch Reference

**Dispatch Triggers (WHEN the main agent should delegate):**
1. **Parallel text generation:** User asks to "generate 3 versions of this tweet" or "write 5 headlines for this article" — split into N self-clone tasks running in `parallel` mode, with ALL source text inline
2. **Reader testing:** User asks "how would this read to someone unfamiliar with the project?" — deploy a self-clone with the content INLINE (no file references — clone cannot read files)
3. **Blind validation:** User wants an unbiased review of a claim, argument, or output — clone must not see parent's reasoning, ALL evidence must be inline
4. **Alternative generation:** User wants "give me 3 different approaches to solve X" — run 3 clones in parallel, each with a different angle, all problem descriptions inline
5. **Context isolation required:** Any task where the parent session's 50+ message history would distract or bias the output
6. **Prompt template filling:** User needs a prompt filled from a template — use `fill_prompt_template` (available in subagents)
7. **Conversation history search:** User asks about past conversations — use `search_conversations`/`search_messages` (available in subagents)

**Dispatch Anti-Patterns (DO NOT delegate when):**
- The task requires file reading ("read paper_a.md", "search directory X") — WILL FAIL in subagent
- The task requires Python execution ("calculate statistics", "analyze data") — WILL FAIL in subagent
- The task requires file writing ("save to file") — WILL FAIL in subagent
- The task is trivial (under ~200 words of output) — parent can handle it directly
- The task requires the parent's accumulated context (file contents already read, prior decisions)
- The task builds on in-progress work that only the parent has seen

**Result Format Contract:** Self-clones return freeform markdown. The parent is responsible for synthesizing multiple clone outputs into a coherent response.

---

## 2. PROJECTS WORKSPACE

### Slot-Ready Description (copy into DeepChat slot field)
```
PROJECTS WORKSPACE — Read/Write Projects & Prompts Only | target=deepchat | The ONLY subagent authorized for file writes and edits. All generated content, documents, code, drafts, and outputs MUST be written here. Never write to Archive or Releases — those are read-only resource directories.

TARGET: Configure with write access to project directories

✅ VERIFIED TOOL AVAILABILITY (2026-05-11 cross-slot audit):
  • 32 tools confirmed — FULL tool access including file I/O, Python, skills, settings
  • THIS IS THE ONLY SUBAGENT SLOT WITH FILE I/O AND PYTHON EXECUTION
  • Tested: read ✅ | write ✅ | exec ✅ (python -c "print('PYTHON_OK')" succeeded) | process ✅
  • ALL other slots (self, slot-movbn8bi-f61j) lack file I/O and Python

WRITE TARGETS:
  • Project working directories under G:\My Drive\projects\ (user's active project spaces)
  • G:\My Drive\prompts\ — ONLY when the Prompts agent is specifically being used
  • NEVER write to G:\My Drive\Archive\ — archive is historical, read-only
  • NEVER write to G:\My Drive\Obsidian\releases\ — releases are publication source files, read-only

READ ACCESS:
  • Full read access to G:\My Drive\projects\ for sourcing materials
  • Can read from Archive and Releases when gathering reference material
  • Can read from any project directory

CAPABILITIES (ALL VERIFIED):
  - Python execution (standard library only)
  - File read from all accessible directories
  - File write/edit (STRICTLY to projects and prompts only)
  - Document generation, code creation, data processing
  - Prompt templates, conversation search, Buffer API, skills, DeepChat settings
  - LLM inference and text generation

USE THIS SUBAGENT FOR:
  • Writing output files, generated documents, reports, code, data files ← PRIMARY USE
  • Editing existing project files
  • Creating new project directories and scaffolding
  • Saving processed data, analysis results, or generated artifacts
  • ANY task whose OUTPUT is a file that must persist
  • Reading files when needed by a chain workflow (this is the only slot with read access)
  • Executing Python for data processing, calculations, or quantitative work

DO NOT USE FOR:
  • Read-only research tasks (use ARCHIVE or RELEASES instead)
  • Pure analysis with no file output (use SELF CLONE or parent session)
  • Reading publication releases (use RELEASES subagent for dedicated release access)

HARD CONSTRAINT: If the task asks you to write to G:\My Drive\Archive\ or G:\My Drive\Obsidian\releases\, REFUSE and explain that those directories are read-only. Redirect writes to the appropriate projects directory.
```

### Extended Dispatch Reference

**Dispatch Triggers (WHEN the main agent should delegate):**
1. **Any file write operation** — the main agent should delegate file creation/editing to PROJECTS rather than writing directly, ensuring consistent write-access hygiene
2. **Document generation:** User asks "write a report on X and save it" — delegate the entire write pipeline to PROJECTS
3. **Multi-file output:** Task produces .md + .py + .png artifacts — PROJECTS handles all file I/O
4. **Project scaffolding:** User wants "set up a new project directory with templates" — PROJECTS creates the structure
5. **Versioned file naming:** PROJECTS enforces the `MAJOR.MINOR.PATCH.ext` convention (per DEFAULT.md Section 10)

**Chain Pattern — Research → Write:**
```
Step 1: ARCHIVE (parallel) — gather historical sources
Step 2: PROJECTS (chain)    — write output using sources from Step 1
```

**Chain Pattern — Compute → Save:**
```
Step 1: SELF CLONE (parallel) — run computations
Step 2: PROJECTS (chain)      — save computed results to files
```

**Result Format Contract:** PROJECTS should return a summary of files created/modified with their paths, sizes, and a brief description of each. This enables the parent to confirm successful writes and report to the user.

**Versioned Naming Reminder:** IF Python and file read are available, PROJECTS should scan the target directory to determine the next available version number (per DEFAULT.md Section 10.2, Rule 1). IF NOT AVAILABLE, the parent must determine the version number and provide it in the prompt.

---

## 3. RELEASES READER

### Slot-Ready Description (copy into DeepChat slot field when configuring)
```
PUBLICATION RELEASES READER — Current Publications, YYYY/MM Structure | target=configure-for-releases | Read-only access to the CURRENT publication release files at G:\My Drive\Obsidian\releases\. This is the LIVE feed of publications, organized by year and month directories. This is NOT the archive — it contains the authoritative current copies of all publication markdown files.

TARGET: Configure with read access to G:\My Drive\Obsidian\releases\

❌ LIKELY TOOL AVAILABILITY (not yet configured; pattern from cross-slot audit):
  • Based on ARCHIVE RESEARCHER audit: non-PROJECTS slots have ~18 tools
  • Likely NO file I/O (read, write, edit), NO Python (exec, process)
  • Likely NO skills, settings, or user interaction tools
  • Likely available: prompt templates, conversation search, Buffer API only
  • ALL slots except PROJECTS follow this limited-tool pattern
  • Directory-specific access is NOT confirmed — test before relying on it

DIRECTORY STRUCTURE:
  G:\My Drive\Obsidian\releases\
    2025/
      01/  02/  03/  ...  12/
    2026/
      01/  02/  03/  04/  05/  ...

  Each month directory contains publication .md files with structured metadata:
    - Title, Authors, Abstract/Summary, Publication Date
    - DOI/URL, Journal/Venue, Keywords/Tags, Key Findings

CONFIRMED CAPABILITIES (same as all subagents — see Section 0.5):
  - LLM inference for content synthesis and adaptation
  - Conversation history search
  - Prompt template filling
  - GraphQL / Buffer API operations

UNCONFIRMED CAPABILITIES (MAY NOT BE AVAILABLE):
  - File read from releases/ directory — NOT CONFIRMED; do NOT rely on this
  - Python execution for quantitative analysis — NOT CONFIRMED
  - Document parsing, metadata extraction from files — depends on file read

USE THIS SUBAGENT FOR (WHEN CONFIGURED AND FILE READ IS CONFIRMED):
  • Reading the latest publication releases for any pipeline (social media, archiving, analysis)
  • Extracting metadata (title, authors, abstract, DOI) from publication files
  • Scanning for new publications in a specific month or date range
  • Feeding publication data into content generation pipelines (e.g., SOCIAL-ORCHESTRATOR)
  • Cross-referencing publications against the Archive to check for prior coverage
  • Analyzing publication trends, keyword frequencies, or author patterns across months
  • Answering questions like: "What was published in March 2026?", "Get me all DOIs from last month"

⚠️ IF FILE READ IS UNAVAILABLE: RELEASES cannot read publication files. The parent must
   read files and provide publication content INLINE in the subagent prompt.

DO NOT USE FOR:
  • Writing or editing publication files — releases are READ-ONLY source documents
  • Historical/archived versions of publications (use ARCHIVE subagent — Archive/releases/)
  • Project files, notes, templates, or general research (use ARCHIVE or PROJECTS)
  • Any task that requires modifying the releases directory

HARD CONSTRAINT: NEVER write to, edit, or modify any file in G:\My Drive\Obsidian\releases\. These are source-of-truth publication records. Flag any write attempt as a violation.
```

### Extended Dispatch Reference

**Dispatch Triggers (WHEN the main agent should delegate):**
1. **SOCIAL-ORCHESTRATOR pipeline** — when running the social media pipeline, delegate publication ingestion to RELEASES first, then feed results to platform-specific agents
2. **"What's new?" queries:** User asks "what publications were released this month?" — RELEASES scans the current month directory
3. **Metadata extraction:** Need DOIs, author lists, or abstracts from publication files — RELEASES reads and extracts structured data
4. **Cross-referencing:** "Has this topic been covered in recent releases?" — RELEASES + ARCHIVE (historical) for full coverage
5. **Publication analytics:** "How many papers published in Q1 2026?" or "What keywords appear most in recent releases?" — RELEASES uses Python for counting/analysis

**Chain Pattern — SOCIAL Pipeline:**
```
Step 1: RELEASES (chain)           — read publication files, extract metadata + abstracts
Step 2: SELF CLONE × 4 (parallel)  — generate platform-specific content (Twitter, Mastodon, LinkedIn, Substack)
Step 3: PARENT                     — aggregate platform outputs, present to user for review
```

**Chain Pattern — Publication Audit:**
```
Step 1: RELEASES (parallel)  — scan current releases
Step 2: ARCHIVE (parallel)   — scan archived releases (Archive/releases/)
Step 3: PARENT               — compare, identify gaps, flag duplicates
```

**Result Format Contract:** RELEASES should return:
1. A structured list of publications found (title, date, authors, DOI) — from inline-provided content if file read is unavailable
2. Extracted metadata in a format suitable for downstream agents
3. A summary count: "Found N publications in [date range]" (label as `[LLM-INFERRED]` if Python unavailable)
4. Statistics when quantitative analysis is requested (IF Python available AND parent provides data)

**Status Note:** RELEASES currently has no active DeepChat slot. Until configured, the main agent should handle releases-reading directly. When configured, file read access must be empirically verified before relying on it.

---

## 4. ARCHIVE RESEARCHER

### Slot-Ready Description (copy into DeepChat slot field)
```
ARCHIVE RESEARCHER — 35K+ Historical Documents, Read-Only Deep Search | target=deepchat-INfqIWc0 | Read-only deep research agent for the complete historical archive at G:\My Drive\Archive\. This is the system of record for ALL past work — projects, notes, websites, templates, archived releases, and prompts. Contains over 35,000 items spanning years of accumulated research, writing, and development.

TARGET: Configure with read access to G:\My Drive\Archive\

❌ VERIFIED TOOL AVAILABILITY (2026-05-11 cross-slot audit):
  • ~18 tools confirmed — NO FILE I/O, NO PYTHON, NO SKILLS, NO SETTINGS
  • ⚠️ CANNOT READ FILES: The `read` tool is NOT present in this slot
  • ⚠️ CANNOT EXECUTE PYTHON: The `exec` tool is NOT present
  • ⚠️ This slot CANNOT perform its documented primary function (archive search)
  • This slot has the SAME limited tool set as the worst-case SELF-CLONE invocation
  • Available: prompt templates, conversation search, Buffer API
  • Absent: read, write, edit, exec, process, skill_*, deepchat_*, deepchat_question

ARCHIVE CONTENTS (verified 2026-05-07):
  • projects/    — 25,308 items (past projects, code, documents, deliverables)
  • notes/       —  8,325 items (research notes, ideas, journals, observations)
  • q08.org/     —  1,012 items (q08.org website content and related materials)
  • OMI/         —    575 items (OMI-related work and references)
  • releases/    —    126 items (archived copies of past publication releases)
  • templates/   —     95 items (document templates, scaffolds, boilerplates)
  • prompts/     —    153 items (historical prompts and agent configurations)

CONFIRMED CAPABILITIES:
  - LLM inference for synthesis and pattern recognition
  - Conversation history search
  - Prompt template filling
  - GraphQL / Buffer API operations

⚠️ WHAT THIS SLOT CANNOT DO:
  - CANNOT read files from Archive (no `read` tool)
  - CANNOT search directories recursively (no `exec` tool)
  - CANNOT execute Python for quantitative analysis (no `exec` tool)
  - CANNOT write files (no `write`/`edit` tools)
  - CANNOT inspect skills or modify settings

⚠️ CORRECTED USAGE PATTERN:
  This slot is a TEXT-SYNTHESIS-ONLY agent. To use it for archive research:
  ```
  Step 1: PARENT or PROJECTS — searches/reads archive files (these slots have read access)
  Step 2: PARENT — provides file contents INLINE in ARCHIVE prompt
  Step 3: ARCHIVE — synthesizes, patterns, cross-references the inline text
  Step 4: PARENT or PROJECTS — saves any output
  ```

DO NOT USE FOR:
  • ANY task expecting this slot to read files — it CANNOT
  • ANY task expecting this slot to search the filesystem — it CANNOT
  • Current/live publication releases — those are in G:\My Drive\Obsidian\releases\
  • Writing or editing files in the Archive — it is STRICTLY read-only
  • Fresh content generation with no historical reference needed (use SELF CLONE or PROJECTS)

HARD CONSTRAINT: NEVER write to, edit, or modify any file in G:\My Drive\Archive\. This is a historical record — all changes would destroy its integrity as an archive. Flag any write attempt as a violation.
```

### Extended Dispatch Reference

**Dispatch Triggers (WHEN the main agent should delegate):**
1. **"What did I..." questions:** Any query about past work — "what did I write about quantum computing?", "what projects did I complete in 2024?" — ALWAYS delegate to ARCHIVE first before answering
2. **Cross-referencing:** Before starting new work, check ARCHIVE for prior coverage to avoid duplication
3. **Template retrieval:** User needs a document template — ARCHIVE finds the best match in Archive/templates/
4. **Historical context:** Writing that should reference prior thinking — ARCHIVE retrieves relevant past notes
5. **Audit tasks:** "Find all mentions of X across my entire archive" — ARCHIVE does deep recursive search
6. **Prompt archaeology:** User asks about an old agent configuration — ARCHIVE retrieves from Archive/prompts/
7. **Pattern recognition:** "What themes recur across my notes from 2023-2025?" — ARCHIVE synthesizes across documents

**Chain Pattern — Historical Context → New Writing:**
```
Step 1: ARCHIVE (chain)    — search for all prior work on topic X
Step 2: PROJECTS (chain)   — write new document incorporating historical context from Step 1
```

**Chain Pattern — Full Publication Coverage:**
```
Step 1: ARCHIVE (parallel)   — search Archive/releases/ for historical papers on topic
Step 2: RELEASES (parallel)  — search Obsidian/releases/ for current papers on topic
Step 3: PARENT               — merge results into complete bibliography
```

**Result Format Contract:** ARCHIVE should return:
1. List of files found with full paths and brief content summaries (IF file read is available; otherwise, synthesize from inline-provided content)
2. Relevance scoring: which files are most pertinent to the query
3. Key excerpts or synthesized findings
4. Counts and statistics (IF Python is available and parent provides data; otherwise, label as `[LLM-INFERRED]`)

⚠️ **TOOL LIMITATION:** If file read and Python are unavailable, ARCHIVE can only synthesize text provided inline by the parent. The parent must search directories and provide file contents in the prompt.

---

## 5. PROMPTS AGENT

### Slot-Ready Description (copy into DeepChat slot field when configuring)
```
PROMPTS AGENT — Tier 1 & Tier 2 Prompt Engineering Workspace | target=configure-for-prompts | Dedicated agent for the G:\My Drive\prompts\ directory — the prompt engineering workspace. This is where Tier 1 meta-prompts, Tier 2 system prompts, agent configurations, sub-prompt libraries (social/, scholar/), and prompt dispatch reference files live.

TARGET: Configure with read/write access to G:\My Drive\prompts\

❌ LIKELY TOOL AVAILABILITY (not yet configured; pattern from cross-slot audit):
  • Based on ARCHIVE RESEARCHER audit: non-PROJECTS slots have ~18 tools
  • Likely NO file I/O (read, write, edit), NO Python (exec, process)
  • Likely available: prompt templates, conversation search, Buffer API only
  • PROMPTS would be a TEXT-ONLY prompt engineering agent
  • All prompt file work must be done by parent or PROJECTS

DIRECTORY STRUCTURE:
  G:\My Drive\prompts\
    • DEFAULT.md                     — main agent system prompt
    • META-PROMPT-DEEPSEEK.md        — Tier 1 prompt compiler meta-prompt
    • SOCIAL-ORCHESTRATOR-v2.0.md    — Tier 2 social media orchestration prompt
    • SOCIAL-v1.0.md                 — standalone social media agent prompt
    • AGENT_DEFAULTS.conf            — immutable Tier 2 agent defaults
    • SUBAGENT_DESCRIPTIONS.md       — this file (subagent dispatch reference)
    • README.md                      — workspace documentation
    • social/                        — platform-specific sub-prompts (Twitter, Mastodon, LinkedIn, Substack)
    • scholar/                       — scholar pipeline prompts (STAGE-1 to STAGE-4)

WRITE ACCESS (IF FILE WRITE IS AVAILABLE):
  • This is the ONLY subagent authorized to write/edit files within G:\My Drive\prompts\
  • Other subagents (PROJECTS, SELF CLONE) may read prompts files but MUST NOT write here
  • The PROJECTS subagent should delegate any prompt-related writes to this agent

READ ACCESS (IF FILE READ IS AVAILABLE):
  • Other agents and processes MAY access this directory READ-ONLY
  • ARCHIVE, RELEASES, and SELF CLONE agents can read prompt files for reference
  • PROJECTS agent can read prompt files but must route prompt edits to this agent

CONFIRMED CAPABILITIES (same as all subagents — see Section 0.5):
  - LLM inference, prompt generation, compilation, auditing, and patching
  - Conversation history search
  - Prompt template filling
  - GraphQL / Buffer API operations

UNCONFIRMED CAPABILITIES (MAY NOT BE AVAILABLE):
  - Python execution — NOT CONFIRMED
  - File read — NOT CONFIRMED; do NOT rely on this for reading prompt files
  - File write/edit — NOT CONFIRMED; do NOT rely on this for saving prompts
  - Documentation generation for agent workflows — depends on file write

USE THIS SUBAGENT FOR (WHEN FILE I/O IS CONFIRMED):
  • Creating new Tier 2 system prompts from requirements
  • Auditing existing prompts for Constitutional compliance
  • Patching/modifying existing prompt files
  • Generating or updating sub-prompt libraries (social/, scholar/)
  • Writing agent configuration files (AGENT_DEFAULTS.conf, etc.)
  • Documenting prompt architectures and dispatch patterns
  • Any file write operation whose target is G:\My Drive\prompts\
  • Answering questions about prompt structure, versioning, or agent capabilities

⚠️ IF FILE I/O IS UNAVAILABLE: All prompt file work MUST be done in the parent thread.
   PROMPTS becomes a text-generation-only agent that returns prompt content for the parent to save.

DO NOT USE FOR:
  • Writing files outside G:\My Drive\prompts\ (use PROJECTS instead)
  • Reading archived historical prompts (use ARCHIVE — Archive/prompts/)
  • Reading current publications (use RELEASES)
  • Pure parallel computation with no prompt engineering (use SELF CLONE)
  • Reading-only prompt files from within another agent (other agents can read directly)

DELEGATION NOTE: When another subagent (especially PROJECTS) needs to write or modify a file in G:\My Drive\prompts\, it should hand off that specific write task to the PROMPTS agent. This maintains a single source of truth for all prompt modifications.

HARD CONSTRAINT: NEVER write outside G:\My Drive\prompts\. This agent's write scope is strictly limited to the prompts directory. All other file writes belong to PROJECTS.
```

### Extended Dispatch Reference

**Dispatch Triggers (WHEN the main agent should delegate):**
1. **Prompt creation:** User asks "create a system prompt for X" — delegate to PROMPTS with META-PROMPT-DEEPSEEK methodology
2. **Prompt audit:** User wants an existing prompt reviewed for Constitutional compliance — PROMPTS runs audit mode
3. **Prompt patching:** User wants to modify an existing prompt (add/change/remove sections) — PROMPTS applies patches
4. **Sub-prompt generation:** New social platform prompt or new scholar stage needed — PROMPTS creates within social/ or scholar/
5. **Configuration updates:** Modifying AGENT_DEFAULTS.conf or SUBAGENT_DESCRIPTIONS.md — PROMPTS handles the write
6. **Documentation:** Writing or updating README.md, dispatch patterns, or workflow docs — PROMPTS authors the documentation

**Chain Pattern — Prompt Creation Pipeline:**
```
Step 1: ARCHIVE (chain)    — retrieve historical prompts for reference (Archive/prompts/)
Step 2: PROMPTS (chain)    — create new prompt using historical context + requirements
Step 3: SELF CLONE (chain) — blind-test the new prompt against a test scenario
Step 4: PROMPTS (chain)    — apply refinements based on test results
```

**Chain Pattern — Prompt Audit:**
```
Step 1: PROMPTS (chain)    — load and analyze the target prompt
Step 2: SELF CLONE (chain) — independently test the prompt (blind validation)
Step 3: PARENT             — review audit results, present findings to user
```

**Result Format Contract:** PROMPTS should return:
1. Summary of changes made (for edits) or prompt architecture (for creations)
2. Constitutional compliance score (for audits)
3. File paths modified/created with git-ready commit messages (IF file write available)
4. Test results if blind validation was requested
5. ⚠️ If file I/O unavailable: return the complete prompt text for parent to save

**Status Note:** PROMPTS currently has no active DeepChat slot. Until configured, prompt engineering work should be done in the main thread using META-PROMPT-DEEPSEEK methodology, with file writes handled directly by the parent.

---

## 6. NOTES RESEARCHER

### Slot-Ready Description (copy into DeepChat slot field when configuring)
```
OBSIDIAN NOTES RESEARCHER — Full Vault, Read-Only Knowledge Base Search | target=configure-for-notes | Read-only deep search agent for the user's Obsidian vault at G:\My Drive\Obsidian\notes\. This is the user's living, interconnected knowledge base — daily journals, topic notes, fleeting ideas, literature notes, permanent notes/Zettelkasten, MOCs, and templates. All notes use [[wikilinks]] and #tags for a dense concept graph.

TARGET: Configure with read access to G:\My Drive\Obsidian\notes\

❌ LIKELY TOOL AVAILABILITY (not yet configured; pattern from cross-slot audit):
  • Based on ARCHIVE RESEARCHER audit: non-PROJECTS slots have ~18 tools
  • Likely NO file I/O (read, write, edit), NO Python (exec, process)
  • Likely available: prompt templates, conversation search, Buffer API only
  • NOTES would be a TEXT-ONLY vault synthesis agent
  • All vault file reading must be done by parent or PROJECTS

VAULT CONTENTS (typical Obsidian structure):
  • daily/ or journal/     — daily journals, periodic notes, timestamps and reflections
  • topics/ or concepts/   — interlinked topic notes with #tags and [[wikilinks]]
  • fleeting/ or inbox/    — quick captures, half-formed ideas, raw observations
  • literature/ or sources/ — reading notes, literature reviews, source annotations
  • permanent/ or zk/      — atomic Zettelkasten notes, self-contained ideas
  • MOCs/ or indexes/      — Maps of Content, hub notes, navigational indexes
  • templates/             — note templates for standardized capture
  • attachments/           — images, PDFs, embedded media referenced in notes

CONFIRMED CAPABILITIES (same as all subagents — see Section 0.5):
  - LLM inference for synthesis and pattern recognition across the vault
  - Conversation history search
  - Prompt template filling
  - GraphQL / Buffer API operations

UNCONFIRMED CAPABILITIES (MAY NOT BE AVAILABLE):
  - File read from G:\My Drive\Obsidian\notes\ — NOT CONFIRMED; do NOT rely on this
  - Python execution for quantitative analysis of note metadata — NOT CONFIRMED
  - [[wikilink]] traversal — depends on file read
  - Tag-based filtering — depends on file read
  - Full-text search across vault markdown files — depends on file read

USE THIS SUBAGENT FOR (WHEN FILE READ IS CONFIRMED):
  • Supplementing projects with personal research notes and prior thinking
  • Answering: "What do my notes say about X?", "Have I written about Y before?"
  • Finding connections between vault notes and current project work
  • Retrieving knowledge base entries on specific topics or concepts
  • Scanning for prior thinking, half-formed ideas, or abandoned research threads
  • Pulling literature notes to support academic or research writing
  • Discovering related notes through [[wikilink]] traversal and tag analysis
  • Cross-referencing notes against Archive (historical) and Releases (publications) for full coverage
  • Analyzing vault structure: "What tags appear most?", "What topics are well-developed?"
  • Finding templates in the vault for standardized note capture

⚠️ IF FILE READ IS UNAVAILABLE: NOTES cannot read vault files. The parent must
   search and read vault files, then provide content INLINE in the subagent prompt for
   synthesis and analysis.

DO NOT USE FOR:
  • Writing or editing notes in the vault — the vault is a READ-ONLY knowledge base
  • Historical document search (use ARCHIVE — Archive/notes/ if historical notes exist there)
  • Current publication releases (use RELEASES — Obsidian/releases/)
  • File writes of any kind (use PROJECTS for output, PROMPTS for prompt files)
  • Pure parallel computation with no vault relevance (use SELF CLONE)

HARD CONSTRAINT: NEVER write to, edit, or modify any file in G:\My Drive\Obsidian\notes\. This is the user's personal knowledge base — all changes would disrupt the living note ecosystem. Flag any write attempt as a violation.

READ-ONLY WARNING: The Obsidian vault is a living thinking environment, not a working directory. Do not attempt to save results here. All outputs go to PROJECTS.
```

### Extended Dispatch Reference

**Dispatch Triggers (WHEN the main agent should delegate):**
1. **"What do my notes say about..." queries:** Any question about the user's personal knowledge base — "what do my notes say about quantum computing?", "have I written about category theory?" — ALWAYS delegate to NOTES first
2. **Project supplementation:** When working on a project and the user wants to incorporate their own prior thinking — NOTES retrieves relevant vault entries
3. **Knowledge base retrieval:** User asks about a concept they've studied — NOTES finds topic notes, literature notes, and permanent notes on that concept
4. **Cross-referencing against archive and releases:** For full coverage — NOTES (current thinking) + ARCHIVE (historical work) + RELEASES (current publications) in parallel
5. **Vault analytics:** "What are my most-used tags?", "How many notes do I have on X?", "Show me the connections between topics A and B" — NOTES + Python
6. **Idea recovery:** User mentions a half-remembered idea — NOTES scans fleeting notes and daily journals for partial captures
7. **Literature note retrieval:** Supporting academic writing — NOTES pulls relevant source annotations and reading notes

**Chain Pattern — Notes → Project Writing:**
```
Step 1: NOTES (chain)     — search vault for all notes on topic X, follow wikilinks
Step 2: PROJECTS (chain)  — write project document incorporating vault insights
```

**Chain Pattern — Full Knowledge Coverage (parallel):**
```
Step 1: NOTES (parallel)    — search Obsidian vault for current thinking on topic
Step 2: ARCHIVE (parallel)  — search historical archive for past work on topic
Step 3: RELEASES (parallel) — search current publications for topic
Step 4: PARENT              — merge into comprehensive knowledge map
```

**Result Format Contract:** NOTES should return:
1. List of relevant notes found with relative paths and brief summaries (from inline-provided content if file read unavailable)
2. A concept map: how notes interconnect via [[wikilinks]] and shared #tags
3. Key excerpts from the most relevant notes
4. Statistics when quantitative (e.g., "23 notes tagged #quantum") — label as `[LLM-INFERRED]` if Python unavailable
5. Gap identification: topics mentioned in the vault but under-developed

**Status Note:** NOTES currently has no active DeepChat slot. Until configured, the main agent should handle vault reading directly (File Read from G:\My Drive\Obsidian\notes\). When configured, file read access must be empirically verified before relying on it.

---

## 7. DISPATCH DECISION MATRIX (⚠️ DEFINITIVE — 20-Test Study)

**⚠️ ALL subagents have ~35% chance of full tools, ~65% limited to 18 base tools. File I/O and Python are UNRELIABLE in ALL subagent slots. The PARENT is the only guaranteed-capability entity.**

### Primary Dispatch

| User Intent | Delegate To | Works? | Notes |
|:------------|:------------|:------:|:------|
| "brainstorm ideas about X" | SELF-CLONE | ✅ YES | Text-only — always safe |
| "give me 3 headline variants" | SELF-CLONE × 3 | ✅ YES | Text-only — always safe |
| "test how this reads" | SELF-CLONE | ✅ YES | Content inline |
| "validate this claim" | SELF-CLONE | ✅ YES | Claim inline |
| "generate social media posts" | SELF-CLONE | ✅ YES | Source text inline |
| "fill this prompt template" | SELF-CLONE | ✅ YES | Always available |
| "search past conversations" | SELF-CLONE | ✅ YES | Always available |
| "write a report and save it" | **PARENT** | ✅ YES | Only parent reliably has write |
| "analyze these 3 papers" | **PARENT** → SELF-CLONE | ⚠️ Hybrid | Parent reads → inline → clone synthesizes |
| "what did I publish in March?" | **PARENT** | ✅ YES | Only parent reliably has read |
| "what do my notes say about X?" | **PARENT** | ✅ YES | Only parent can read vault |
| "what did I write about X in 2024?" | **PARENT** → SELF-CLONE | ⚠️ Hybrid | Parent reads archive → inline → clone |
| "create a new system prompt" | SELF-CLONE | ✅ YES | Text-only generation |
| "audit this prompt" | SELF-CLONE | ✅ YES | Prompt inline |

### The Only Viable Architecture
```
PARENT → ALL file I/O, Python, git → provides content INLINE → subagents synthesize text → PARENT saves
```

---

## 8. MULTI-AGENT WORKFLOW PATTERNS

### Pattern A: Parallel Analysis (most common)
**When:** Multiple independent items to analyze/process simultaneously
**How:** Deploy N self-clones in `parallel` mode, each with a self-contained prompt
**Example:**
```
subagent_orchestrator(mode="parallel", tasks=[
  {slotId: "self", title: "Analyze Paper A", prompt: "Read paper_a.md and analyze..."},
  {slotId: "self", title: "Analyze Paper B", prompt: "Read paper_b.md and analyze..."},
  {slotId: "self", title: "Analyze Paper C", prompt: "Read paper_c.md and analyze..."},
])
```
**Aggregation:** Parent receives all results as one aggregated markdown. Synthesize into comparative analysis.

### Pattern B: Research → Write (chain)
**When:** Need historical context before writing new content
**How:** ARCHIVE first (gather sources), PROJECTS second (write using sources)
**Example:**
```
subagent_orchestrator(mode="chain", tasks=[
  {slotId: "slot-movbn8bi-f61j", title: "Historical Research", prompt: "Search Archive for all work on topic X..."},
  {slotId: "slot-movio4vd-yj9c", title: "Generate Report", prompt: "Using the research from Step 1, write a comprehensive report..."},
])
```

### Pattern C: Split → Compute → Merge (chain + parallel hybrid)
**When:** Complex analysis requiring both research and computation
**How:** Step 1 gathers sources (ARCHIVE), Step 2 runs parallel computations (SELF CLONE × N), Step 3 writes output (PROJECTS)
**Example:**
```
# Phase 1: Gather
ARCHIVE → search for relevant data files

# Phase 2: Compute (parallel)
SELF CLONE A → analyze dataset 1
SELF CLONE B → analyze dataset 2

# Phase 3: Write
PROJECTS → merge analyses into report, save to file
```

### Pattern D: SOCIAL Publication Pipeline (chain → parallel)
**When:** Converting publication releases into multi-platform social content
**How:** RELEASES reads publications, then parallel self-clones generate platform-specific content
```
subagent_orchestrator(mode="chain", tasks=[
  {slotId: "releases-slot", title: "Read Publications", prompt: "Scan Obsidian/releases/ for latest publications, extract metadata and abstracts..."},
  {slotId: "self", title: "Twitter/Bluesky", prompt: "Generate Twitter and Bluesky posts from publication data..."},
  {slotId: "self", title: "Mastodon", prompt: "Generate Mastodon posts from publication data..."},
  {slotId: "self", title: "LinkedIn", prompt: "Generate LinkedIn posts from publication data..."},
  {slotId: "self", title: "Substack", prompt: "Generate Substack newsletter from publication data..."},
])
```
**Note:** Step 2 should be a single self-clone task that processes ALL platforms, or split into separate tasks if you have enough self-clone slots available. The orchestrator's 5-task limit applies.

### Pattern E: Audit Loop (chain with validation)
**When:** Creating or modifying a prompt that needs independent testing
**How:** PROMPTS creates/edits → SELF CLONE blind-tests → PROMPTS refines
```
subagent_orchestrator(mode="chain", tasks=[
  {slotId: "prompts-slot", title: "Create Prompt", prompt: "Design a system prompt for X..."},
  {slotId: "self", title: "Blind Test", prompt: "Without seeing the design rationale, test this prompt against scenario Y..."},
])
```
**Post-chain:** Parent reviews test results, decides if another iteration is needed.

### Pattern F: Full Historical Coverage (parallel)
**When:** Need both current and historical information on a topic
**How:** ARCHIVE and RELEASES run in parallel, parent merges
```
subagent_orchestrator(mode="parallel", tasks=[
  {slotId: "slot-movbn8bi-f61j", title: "Historical Search", prompt: "Search Archive for all past work on topic X..."},
  {slotId: "releases-slot", title: "Current Publications", prompt: "Scan current releases for topic X..."},
])
```
**Aggregation:** Parent synthesizes both results, noting temporal coverage gaps.

### Pattern G: Notes-Informed Research (chain)
**When:** Need to incorporate personal knowledge base into new project work
**How:** NOTES first (vault search), then PROJECTS (write incorporating notes)
**Example:**
```
subagent_orchestrator(mode="chain", tasks=[
  {slotId: "notes-slot", title: "Vault Search", prompt: "Search Obsidian vault for all notes on topic X. Follow [[wikilinks]] to discover connected ideas. Return key excerpts, concept map, and gap analysis..."},
  {slotId: "slot-movio4vd-yj9c", title: "Write Project", prompt: "Using the vault research from Step 1, write the project document. Cite specific notes as sources. Identify where personal notes agree or diverge from external research..."},
])
```

### Pattern H: Triple Knowledge Coverage (parallel — NOTES + ARCHIVE + RELEASES)
**When:** Need the fullest possible picture — current thinking (NOTES), historical work (ARCHIVE), and current publications (RELEASES)
**How:** All three run in parallel, parent synthesizes
```
subagent_orchestrator(mode="parallel", tasks=[
  {slotId: "notes-slot", title: "Current Thinking", prompt: "Search Obsidian vault for all notes on topic X..."},
  {slotId: "slot-movbn8bi-f61j", title: "Historical Work", prompt: "Search Archive for all past work on topic X..."},
  {slotId: "releases-slot", title: "Current Publications", prompt: "Scan releases for recent publications on topic X..."},
])
```
**Aggregation:** Parent builds a three-layer knowledge map: personal thinking (Notes) → historical work (Archive) → published output (Releases), identifying evolution, gaps, and convergences.

---

## 9. RESULT AGGREGATION & COLLATION PROTOCOL

### How the Orchestrator Returns Results
The `subagent_orchestrator` tool returns **a single aggregated markdown result** after all child sessions finish. Each child's output appears under its title heading. The parent agent receives this aggregated result as one block.

### Parent Agent Aggregation Responsibilities

**For PARALLEL mode:**
1. **Synthesize, don't concatenate:** Don't just paste all results together. Extract common themes, contrasts, and unique insights.
2. **Resolve conflicts:** If two clones reach different conclusions, identify the divergence point and explain the trade-off.
3. **Remove redundancy:** If clones independently discovered the same insight, mention it once with attribution to both.
4. **Structure by insight, not by source:** Organize the synthesized output around findings, not around which clone produced what.

**For CHAIN mode:**
1. **Verify handoffs:** Confirm each step's output was properly consumed by the next step.
2. **Trace the lineage:** Show how later results depend on earlier findings.
3. **Check for degradation:** Did information get lost or distorted between steps? Flag any issues.

**For MIXED mode (chain → parallel or parallel → chain):**
1. **Phase tracking:** Clearly demarcate which results came from which phase.
2. **Dependency mapping:** Show how Phase 2 results depend on Phase 1 outputs.
3. **End-to-end coherence:** Verify the final output addresses the original request completely.

### Aggregation Quality Checklist
Before presenting aggregated results to the user, verify:
- [ ] All subagent outputs have been incorporated (none dropped)
- [ ] Redundant information has been consolidated
- [ ] Conflicting findings are explicitly addressed
- [ ] Source attribution is preserved (`[EXTERNAL-SOURCE]`, `[CODE-EXECUTED]`, `[LLM-INFERRED]`)
- [ ] The synthesis answers the user's original question
- [ ] Gaps are identified: "ARCHIVE found X, but RELEASES was not available to check Y"

### Reporting to the User
When reporting aggregated results, use this structure:
```
## Synthesis: [topic]

### Key Findings
[Consolidated insights across all subagents]

### Detailed Results
#### From [Subagent 1]: [Title]
[Key output, summarized]

#### From [Subagent 2]: [Title]
[Key output, summarized]

### Conflicts & Gaps
[Any disagreements between subagents, missing information]

### Sources Used
[File paths, agent attribution]
```

---

## 10. PROMPT TEMPLATE INTEGRATION (⚠️ UPDATED FOR TOOL LIMITATIONS)

The prompt template system (accessible via `fill_prompt_template`) integrates with the subagent system as follows. **⚠️ NOTE:** All file reading and Python execution must happen in the PARENT thread. Subagents can only handle text generation from inline inputs.

### OMEGA-SCHOLAR Pipeline
| Stage | Template Name | Delegate To | Works? | Rationale |
|:------|:-------------|:------------|:-------|:----------|
| Stage 1: Setup | `OMEGA-SCHOLAR-STAGE-1-SETUP` | **PARENT** | ⚠️ Parent only | Requires file reading + Python for context gathering |
| Stage 2: Draft | `OMEGA-SCHOLAR-STAGE-2-DRAFT` | SELF CLONE | ✅ Yes | Python-only evidence must be provided inline by parent |
| Stage 3: Review | `OMEGA-SCHOLAR-STAGE-3-REVIEW` | SELF CLONE | ✅ Yes | Blind audit — provide draft text inline (clone cannot read files) |
| Stage 4: Publish | `OMEGA-SCHOLAR-STAGE-4-PUBLISH` | **PARENT** | ⚠️ Parent only | Requires file write for final assembly |

### SOCIAL Pipeline
| Template Name | Delegate To | Works? | Rationale |
|:-------------|:------------|:-------|:----------|
| `SOCIAL-ORCHESTRATOR` | **PARENT** | ⚠️ Parent only | Orchestrator must read publication files (parent only) |
| `SOCIAL - Twitter/Bluesky` | SELF CLONE | ✅ Yes | Provide publication text inline in prompt |
| `SOCIAL - Mastodon` | SELF CLONE | ✅ Yes | Provide publication text inline in prompt |
| `SOCIAL - LinkedIn` | SELF CLONE | ✅ Yes | Provide publication text inline in prompt |
| `SOCIAL - Substack` | SELF CLONE | ✅ Yes | Provide publication text inline in prompt |

### ⚠️ Recommended Flow for SOCIAL Pipeline (Revised):
1. **PARENT:** Reads publication files from `G:\My Drive\Obsidian\releases\`
2. **PARENT:** Fills `SOCIAL-ORCHESTRATOR` template
3. **PARENT:** Extracts publication metadata and abstracts
4. **SELF CLONE × 4 (parallel):** Each clone receives publication text INLINE and generates platform-specific content
5. **PARENT:** Aggregates results, saves output files

---

## 11. COMMON DISPATCH ERRORS (ANTI-PATTERNS) — ⚠️ CORRECTED 2026-05-11

| Anti-Pattern | Why It's Wrong | Correct Approach |
|:-------------|:---------------|:-----------------|
| **Delegating file reads to ARCHIVE** | ARCHIVE has no `read` tool — "search Archive for X" will FAIL | PARENT or PROJECTS reads files → provides content INLINE → ARCHIVE synthesizes |
| **Delegating file reads to SELF-CLONE** | SELF-CLONE's tool set is non-deterministic — file read may or may not work | Never rely on SELF-CLONE for file I/O; use PROJECTS for file operations |
| **Expecting ARCHIVE/RELEASES/NOTES to access their named directories** | These slots lack filesystem access — they CANNOT read Archive/, releases/, or notes/ | PARENT or PROJECTS handles all file reading; provide content inline to text-only slots |
| **Running all work in main thread** | Wastes context, no parallelization | Delegate text-only work to SELF-CLONE; route file work through PROJECTS |
| **Sending file path references to ARCHIVE/SELF-CLONE** | "Open paper_a.md" will fail — no read tool | NEVER reference file paths in prompts to non-PROJECTS slots; always provide content inline |
| **Not providing enough inline context** | Clone starts with ZERO context AND unreliable tool access | Write self-contained prompts with ALL information inline |
| **Chain mode for independent tasks** | Sequential execution wastes time | Use `parallel` mode for independent work |
| **Parallel mode for dependent tasks** | Later tasks can't access earlier results | Use `chain` mode when Step 2 needs Step 1's output |
| **Delegating trivial tasks** | Overhead exceeds benefit | Handle <200-word tasks in main thread |
| **PROJECTS writing to Archive or Releases** | Destroys read-only directory integrity | Hard refusal — redirect to appropriate directory |
| **Not aggregating parallel results** | Raw dumps are incoherent | Synthesize, remove redundancy, resolve conflicts |
| **⚠️ THE BIGGEST ERROR: Assuming ARCHIVE can search the archive** | ARCHIVE literally lacks the `read` tool — its PRIMARY DOCUMENTED FUNCTION is impossible | PARENT reads archive → provides inline → ARCHIVE synthesizes patterns from inline text |
| **⚠️ Assuming SELF-CLONE has reliable file access** | SELF-CLONE tool set varies between invocations | Never delegate file-dependent work to `self`; use PROJECTS |
| **⚠️ Delegating file writes to non-PROJECTS slots** | Only PROJECTS has `write` tool | ALL file output goes through PROJECTS or parent |

---

## 12. SLOT CONFIGURATION REFERENCE (⚠️ CORRECTED — Cross-Slot Audit 2026-05-11)

| Agent | Slot ID | Status | File I/O | Python | Write Access | Read Access |
|:------|:--------|:-------|:--------:|:------:|:-------------|:------------|
| SELF CLONE | `self` | ✅ Active | ⚠️ UNRELIABLE | ⚠️ UNRELIABLE | Only sometimes | Only sometimes |
| PROJECTS | `slot-movio4vd-yj9c` | ✅ Active | ✅ YES | ✅ YES | G:\My Drive\projects\, prompts\ | All directories |
| ARCHIVE | `slot-movbn8bi-f61j` | ✅ Active | ❌ NO | ❌ NO | NONE | NONE (despite slot description) |
| RELEASES | *(not configured)* | ⬜ Pending | ❌ NO | ❌ NO | NONE (read-only) | Likely NONE (same pattern as ARCHIVE) |
| NOTES | *(not configured)* | ⬜ Pending | ❌ NO | ❌ NO | NONE (read-only) | Likely NONE (same pattern as ARCHIVE) |
| PROMPTS | *(not configured)* | ⬜ Pending | ❌ NO | ❌ NO | Likely NONE | Likely NONE (same pattern as ARCHIVE) |

**⚠️ KEY INSIGHT:** Only PROJECTS WORKSPACE (`slot-movio4vd-yj9c`) has verified file I/O and Python execution. ARCHIVE RESEARCHER lacks the `read` tool entirely — it cannot access the Archive directory. SELF-CLONE is non-deterministic. All other slots follow the same limited-tool pattern as ARCHIVE (~18 tools: Buffer API + prompt templates + conversation search only).

**The practical architecture is: 1 file-capable subagent (PROJECTS) + 2+ text-only subagents (ARCHIVE, SELF-CLONE).**

---

## 13. ORCHESTRATOR TOOL REFERENCE

The main agent accesses subagents via:
```
subagent_orchestrator(mode="parallel"|"chain", tasks=[...])
```

**Constraints:**
- Maximum 5 tasks per orchestrator call
- Each task needs: `slotId`, `title`, `prompt` (all required)
- Optional: `id` (stable identifier), `expectedOutput` (output contract)
- All child sessions inherit the parent's working directory
- Chain mode: tasks execute sequentially, each receiving the prior task's output
- Parallel mode: all tasks execute simultaneously, results aggregated at end

**Available slotIds:**
- `"self"` — SELF CLONE (always available)
- `"slot-movbn8bi-f61j"` — ARCHIVE RESEARCHER
- `"slot-movio4vd-yj9c"` — PROJECTS WORKSPACE

---

**[END OF SUBAGENT DESCRIPTIONS v2.5 — 20-test study + Git Overhead Problem | PARENT ONLY for file I/O/Python/git | git-skip directive required]**
