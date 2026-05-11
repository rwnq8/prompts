# SUBAGENT DESCRIPTIONS — Dispatch Reference & Orchestration Protocol
> **Purpose:** Definitive reference for configuring DeepChat subagent slots.
> Each description is engineered so the LLM can unambiguously route tasks to the correct subagent.
> **Last updated:** 2026-05-10 | **Scope:** All 5 subagents (3 active slots + 2 pending)

---

## 0. SUBAGENT ARCHITECTURE OVERVIEW

The main agent (DEFAULT-DEEPSEEK v1.2 running in the DeepChat chat thread) has access to the `subagent_orchestrator` tool with these slots:

| Slot ID | Agent Name | Status | Primary Role |
|:--------|:-----------|:-------|:-------------|
| `self` | SELF CLONE | **ACTIVE** | Parallel processing, blind validation, reader testing |
| `slot-movio4vd-yj9c` | PROJECTS WORKSPACE | **ACTIVE** | File writes, document generation, project scaffolding |
| `slot-movbn8bi-f61j` | ARCHIVE RESEARCHER | **ACTIVE** | Historical deep search, past work retrieval, cross-referencing |
| *(pending)* | NOTES RESEARCHER | **PENDING** | Obsidian vault notes (Obsidian/notes/) for project supplementation |
| *(pending)* | RELEASES READER | **PENDING** | Current publication releases (Obsidian/releases/) |
| *(pending)* | PROMPTS AGENT | **PENDING** | Tier 1 & Tier 2 prompt engineering, prompt writes |

**Orchestration modes:** `parallel` (all subagents run concurrently) and `chain` (sequential execution).

**Critical rule:** The main agent MUST delegate to subagents when a task falls within a subagent's specialized domain. Never attempt subagent-specialized work in the main thread — this wastes context and produces inferior results.

---

## 0.5 ⚠️ ACTUAL TOOL AVAILABILITY (Empirically Verified 2026-05-11)

**The subagent tool availability described above is ASPIRATIONAL — actual subagent tool sets are significantly more restricted than what the slot descriptions claim.**

Based on empirical testing (self-clone introspection of available function definitions), subagents have the following **CONFIRMED** tools:

### Confirmed Available Tools (All Subagents)
| Tool Category | Specific Tools | Notes |
|:--------------|:---------------|:------|
| Conversation Management | `search_conversations`, `search_messages`, `get_conversation_history`, `get_conversation_stats` | Search and retrieve conversation records |
| Prompt Templates | `list_all_prompt_template_names`, `get_prompt_template_parameters`, `fill_prompt_template` | Fill and generate prompts from templates |
| GraphQL / Buffer API | `execute_query`, `execute_mutation`, `introspect_schema` | Buffer social media management API |
| Subagent Orchestration | `subagent_orchestrator` | Nested delegation to other subagents |
| User Interaction | `deepchat_question` | Ask the parent user clarifying questions |
| DeepChat Settings | `deepchat_settings_toggle`, `deepchat_settings_set_language`, `deepchat_settings_set_theme`, `deepchat_settings_set_font_size`, `deepchat_settings_open` | Modify DeepChat application settings |
| Skill Management | `skill_list`, `skill_view`, `skill_manage` | Inspect and manage skills |

### Confirmed UNAVAILABLE Tools (All Subagents)
| Tool Category | Missing Tools | Impact |
|:--------------|:--------------|:-------|
| **File I/O** | `read`, `write`, `edit` | **CRITICAL: Subagents CANNOT read or write files from the filesystem.** All file-dependent task descriptions (e.g., "Read paper_a.md and analyze") will FAIL. |
| **Python/Shell Execution** | `exec`, `process` | **CRITICAL: Subagents CANNOT execute Python code or shell commands.** All quantitative work, data processing, and computation-dependent task descriptions will FAIL. |
| **Buffer Post Management** | `list_posts`, `get_post`, `create_post`, `create_idea`, `delete_post` | Cannot create/manage social media posts directly |
| **Buffer Account/Channel** | `get_account`, `list_channels`, `get_channel` | Cannot access Buffer account/channel info |

### ⚠️ CRITICAL IMPLICATIONS

1. **No file reading:** Any subagent task that says "Read file X" or "Search directory Y" will fail. The subagent can only work with information provided INLINE in its task prompt.

2. **No Python execution:** Any subagent task that requires calculations, data processing, counting, statistics, or quantitative analysis will fail. Numbers must be provided by the parent.

3. **Prompt-only workflow:** Subagents can ONLY reason about text provided in their prompt, fill prompt templates, search conversations, use GraphQL, and orchestrate other subagents. They are pure LLM reasoning engines.

4. **All file work stays in parent:** File reading, Python execution, and file writing MUST happen in the main agent thread. Subagents cannot supplement or replace these capabilities.

5. **ARCHIVE RESEARCHER impact:** The ARCHIVE subagent (slot-movbn8bi-f61j) is described as reading from `G:\My Drive\Archive\` — this capability is UNCONFIRMED. If it also lacks file read access, it cannot perform its primary function.

6. **PROJECTS WORKSPACE impact:** The PROJECTS subagent (slot-movio4vd-yj9c) is described as writing to `G:\My Drive\projects\` — this capability is UNCONFIRMED. If it also lacks file write access, it cannot perform its primary function.

### Recommended Dispatch Strategy (Given These Limitations)

| Task Type | Dispatch To | Rationale |
|:----------|:------------|:----------|
| Pure LLM reasoning, ideation, text generation | SELF CLONE | Works — subagent can reason about provided text |
| Prompt template filling | SELF CLONE | Works — `fill_prompt_template` is available |
| Conversation history search | SELF CLONE | Works — conversation tools available |
| GraphQL/Buffer operations | SELF CLONE | Works — GraphQL tools available |
| Blind validation / reader testing (text-only) | SELF CLONE | Works — provide content inline in prompt |
| Parallel text generation | SELF CLONE × N | Works — provide all inputs inline |
| **File reading** | **PARENT ONLY** | Subagents cannot read files |
| **File writing** | **PARENT ONLY** | Subagents cannot write files |
| **Python execution** | **PARENT ONLY** | Subagents cannot execute code |
| **Quantitative analysis** | **PARENT ONLY** | Requires Python → parent only |
| **Directory search/scan** | **PARENT ONLY** | Requires file read → parent only |

### When to NOT Use Subagents
- Any task requiring file I/O (reading source files, writing output)
- Any task requiring Python execution (calculations, data processing, statistics)
- Any task where the subagent would need to discover information from the filesystem
- Any task where the subagent would need to verify quantitative claims

**Until subagent tool availability is expanded, treat subagents as pure LLM reasoning assistants that can only work with text explicitly provided in their prompt.**

---

## 1. SELF CLONE

### Slot-Ready Description (copy into DeepChat slot field)
```
FRESH INSTANCE — Clean Slate, Zero Context, Full Tools | target=current agent | An isolated clone of the current agent with NO conversation history, NO priming, and NO access to the parent session's context. Inherits the same working directory and tool access but starts completely fresh.

TARGET: current agent (self-clone)

CAPABILITIES:
  - Python execution (standard library only, no pandas)
  - File read access to G:\My Drive\ (same as parent session)
  - File write access to G:\My Drive\ (same as parent session)
  - LLM inference and generation
  - Full tool access identical to parent

USE THIS SUBAGENT FOR:
  • Parallel processing — run N independent subtasks simultaneously with no cross-contamination
  • Reader testing — test prompts or content against a naive reader with zero prior exposure
  • Blind validation — the clone cannot see parent-session results, so it provides unbiased review
  • Splitting large tasks into independent subtasks (e.g., "analyze papers A, B, C in parallel")
  • Any scenario where the parent session's accumulated context would bias or pollute results
  • Generating alternative approaches to a problem without being influenced by the parent's chosen path

DO NOT USE FOR:
  • Tasks requiring access to files the parent has already read (clone must re-read)
  • Tasks that MUST build on parent-session discoveries (use chain mode with handoff instead)
  • Tasks where context sharing between subtasks is essential (use parent session directly)

CONTEXT WARNING: The clone starts with ZERO knowledge of the parent conversation. It does not know what the parent has discussed, decided, or discovered. The prompt you send MUST be self-contained and complete.
```

### Extended Dispatch Reference

**Dispatch Triggers (WHEN the main agent should delegate):**
1. **Parallel processing needed:** User asks to "analyze these 3 papers" or "compare X, Y, Z" — split into N self-clone tasks running in `parallel` mode
2. **Reader testing:** User asks "how would this read to someone unfamiliar with the project?" — deploy a self-clone with only the content, no context
3. **Blind validation:** User wants an unbiased review of a claim, argument, or output — clone must not see parent's reasoning
4. **Alternative generation:** User wants "give me 3 different approaches to solve X" — run 3 clones in parallel, each with a different angle
5. **Context isolation required:** Any task where the parent session's 50+ message history would distract or bias the output

**Dispatch Anti-Patterns (DO NOT delegate when):**
- The task is trivial (under ~200 words of output) — parent can handle it directly
- The task requires the parent's accumulated context (file contents already read, prior decisions)
- The task is a single-step command (e.g., "run this Python script")
- The task builds on in-progress work that only the parent has seen

**Result Format Contract:** Self-clones return freeform markdown. The parent is responsible for synthesizing multiple clone outputs into a coherent response.

---

## 2. PROJECTS WORKSPACE

### Slot-Ready Description (copy into DeepChat slot field)
```
PROJECTS WORKSPACE — Read/Write Projects & Prompts Only | target=deepchat | The ONLY subagent authorized for file writes and edits. All generated content, documents, code, drafts, and outputs MUST be written here. Never write to Archive or Releases — those are read-only resource directories.

TARGET: Configure with write access to project directories

WRITE TARGETS:
  • Project working directories under G:\My Drive\projects\ (user's active project spaces)
  • G:\My Drive\prompts\ — ONLY when the Prompts agent is specifically being used
  • NEVER write to G:\My Drive\Archive\ — archive is historical, read-only
  • NEVER write to G:\My Drive\Obsidian\releases\ — releases are publication source files, read-only

READ ACCESS:
  • Full read access to G:\My Drive\projects\ for sourcing materials
  • Can read from Archive and Releases when gathering reference material
  • Can read from any project directory

CAPABILITIES:
  - Python execution (standard library only)
  - File read from all accessible directories
  - File write/edit (STRICTLY to projects and prompts only)
  - Document generation, code creation, data processing

USE THIS SUBAGENT FOR:
  • Writing output files, generated documents, reports, code, data files
  • Editing existing project files
  • Creating new project directories and scaffolding
  • Saving processed data, analysis results, or generated artifacts
  • Any task whose OUTPUT is a file that must persist

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

**Versioned Naming Reminder:** PROJECTS MUST scan the target directory with Python before writing to determine the next available version number (per DEFAULT.md Section 10.2, Rule 1).

---

## 3. RELEASES READER

### Slot-Ready Description (copy into DeepChat slot field when configuring)
```
PUBLICATION RELEASES READER — Current Publications, YYYY/MM Structure | target=configure-for-releases | Read-only access to the CURRENT publication release files at G:\My Drive\Obsidian\releases\. This is the LIVE feed of publications, organized by year and month directories. This is NOT the archive — it contains the authoritative current copies of all publication markdown files.

TARGET: Configure with read access to G:\My Drive\Obsidian\releases\

DIRECTORY STRUCTURE:
  G:\My Drive\Obsidian\releases\
    2025/
      01/  02/  03/  ...  12/
    2026/
      01/  02/  03/  04/  05/  ...

  Each month directory contains publication .md files with structured metadata:
    - Title, Authors, Abstract/Summary, Publication Date
    - DOI/URL, Journal/Venue, Keywords/Tags, Key Findings

CAPABILITIES:
  - File read from releases/ directory ONLY (write access is NOT available)
  - Python execution for quantitative analysis of publication data
  - LLM inference for content synthesis and adaptation

USE THIS SUBAGENT FOR:
  • Reading the latest publication releases for any pipeline (social media, archiving, analysis)
  • Extracting metadata (title, authors, abstract, DOI) from publication files
  • Scanning for new publications in a specific month or date range
  • Feeding publication data into content generation pipelines (e.g., SOCIAL-ORCHESTRATOR)
  • Cross-referencing publications against the Archive to check for prior coverage
  • Analyzing publication trends, keyword frequencies, or author patterns across months
  • Answering questions like: "What was published in March 2026?", "Get me all DOIs from last month"

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
1. A structured list of publications found (title, date, authors, DOI)
2. Extracted metadata in a format suitable for downstream agents
3. A summary count: "Found N publications in [date range]"
4. Python-executed statistics when quantitative analysis is requested

**Status Note:** RELEASES currently has no active DeepChat slot. Until configured, the main agent should handle releases-reading directly or use the ARCHIVE subagent for Archive/releases/ content.

---

## 4. ARCHIVE RESEARCHER

### Slot-Ready Description (copy into DeepChat slot field)
```
ARCHIVE RESEARCHER — 35K+ Historical Documents, Read-Only Deep Search | target=deepchat-INfqIWc0 | Read-only deep research agent for the complete historical archive at G:\My Drive\Archive\. This is the system of record for ALL past work — projects, notes, websites, templates, archived releases, and prompts. Contains over 35,000 items spanning years of accumulated research, writing, and development.

TARGET: Configure with read access to G:\My Drive\Archive\

ARCHIVE CONTENTS (verified 2026-05-07):
  • projects/    — 25,308 items (past projects, code, documents, deliverables)
  • notes/       —  8,325 items (research notes, ideas, journals, observations)
  • q08.org/     —  1,012 items (q08.org website content and related materials)
  • OMI/         —    575 items (OMI-related work and references)
  • releases/    —    126 items (archived copies of past publication releases)
  • templates/   —     95 items (document templates, scaffolds, boilerplates)
  • prompts/     —    153 items (historical prompts and agent configurations)

CAPABILITIES:
  - File read from G:\My Drive\Archive\ and its subdirectories
  - Python execution for quantitative analysis of archived data
  - LLM inference for synthesis and pattern recognition across archived materials
  - Deep recursive search across all archive subdirectories

USE THIS SUBAGENT FOR:
  • Retrieving historical documents, past notes, or prior project files
  • Answering questions about past work: "What did I write about X in 2024?"
  • Finding templates (Archive/templates/) for document generation or project scaffolding
  • Cross-referencing current work against archived projects to avoid duplication
  • Searching archived publication releases (Archive/releases/) for historical publication data
  • Gathering source material from archived notes for synthesis or new writing
  • Auditing past work: "What projects did I complete in 2023?", "Find all notes tagged with 'quantum'"
  • Retrieving old prompts or agent configurations (Archive/prompts/)

DO NOT USE FOR:
  • Current/live publication releases — those are in G:\My Drive\Obsidian\releases\ (use RELEASES subagent)
  • Writing or editing files in the Archive — it is STRICTLY read-only
  • Fresh content generation with no historical reference needed (use SELF CLONE or PROJECTS)
  • Tasks that have no connection to prior work or archived materials

HARD CONSTRAINT: NEVER write to, edit, or modify any file in G:\My Drive\Archive\. This is a historical record — all changes would destroy its integrity as an archive. Flag any write attempt as a violation.

READ-ONLY WARNING: The Archive is NOT a working directory. Do not attempt to save results, outputs, or generated files here. All outputs go to PROJECTS.
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
1. List of files found with full paths and brief content summaries
2. Relevance scoring: which files are most pertinent to the query
3. Key excerpts or synthesized findings
4. Python-executed counts when quantitative (e.g., "37 notes tagged 'quantum'")

---

## 5. PROMPTS AGENT

### Slot-Ready Description (copy into DeepChat slot field when configuring)
```
PROMPTS AGENT — Tier 1 & Tier 2 Prompt Engineering Workspace | target=configure-for-prompts | Dedicated agent for the G:\My Drive\prompts\ directory — the prompt engineering workspace. This is where Tier 1 meta-prompts, Tier 2 system prompts, agent configurations, sub-prompt libraries (social/, scholar/), and prompt dispatch reference files live.

TARGET: Configure with read/write access to G:\My Drive\prompts\

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

WRITE ACCESS:
  • This is the ONLY subagent authorized to write/edit files within G:\My Drive\prompts\
  • Other subagents (PROJECTS, SELF CLONE) may read prompts files but MUST NOT write here
  • The PROJECTS subagent should delegate any prompt-related writes to this agent

READ ACCESS:
  • Other agents and processes MAY access this directory READ-ONLY
  • ARCHIVE, RELEASES, and SELF CLONE agents can read prompt files for reference
  • PROJECTS agent can read prompt files but must route prompt edits to this agent

CAPABILITIES:
  - Python execution (standard library only)
  - File read from all accessible directories
  - File write/edit (STRICTLY to G:\My Drive\prompts\ only)
  - Prompt generation, compilation, auditing, and patching
  - Documentation generation for agent workflows

USE THIS SUBAGENT FOR:
  • Creating new Tier 2 system prompts from requirements
  • Auditing existing prompts for Constitutional compliance
  • Patching/modifying existing prompt files
  • Generating or updating sub-prompt libraries (social/, scholar/)
  • Writing agent configuration files (AGENT_DEFAULTS.conf, etc.)
  • Documenting prompt architectures and dispatch patterns
  • Any file write operation whose target is G:\My Drive\prompts\
  • Answering questions about prompt structure, versioning, or agent capabilities

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
3. File paths modified/created with git-ready commit messages
4. Test results if blind validation was requested

**Status Note:** PROMPTS currently has no active DeepChat slot. Until configured, prompt engineering work should be done in the main thread using META-PROMPT-DEEPSEEK methodology, with file writes routed through PROJECTS.

---

## 6. NOTES RESEARCHER

### Slot-Ready Description (copy into DeepChat slot field when configuring)
```
OBSIDIAN NOTES RESEARCHER — Full Vault, Read-Only Knowledge Base Search | target=configure-for-notes | Read-only deep search agent for the user's Obsidian vault at G:\My Drive\Obsidian\notes\. This is the user's living, interconnected knowledge base — daily journals, topic notes, fleeting ideas, literature notes, permanent notes/Zettelkasten, MOCs, and templates. All notes use [[wikilinks]] and #tags for a dense concept graph.

TARGET: Configure with read access to G:\My Drive\Obsidian\notes\

VAULT CONTENTS (typical Obsidian structure):
  • daily/ or journal/     — daily journals, periodic notes, timestamps and reflections
  • topics/ or concepts/   — interlinked topic notes with #tags and [[wikilinks]]
  • fleeting/ or inbox/    — quick captures, half-formed ideas, raw observations
  • literature/ or sources/ — reading notes, literature reviews, source annotations
  • permanent/ or zk/      — atomic Zettelkasten notes, self-contained ideas
  • MOCs/ or indexes/      — Maps of Content, hub notes, navigational indexes
  • templates/             — note templates for standardized capture
  • attachments/           — images, PDFs, embedded media referenced in notes

CAPABILITIES:
  - File read from G:\My Drive\Obsidian\notes\ and its subdirectories (recursive)
  - Python execution for quantitative analysis of note metadata (tags, links, word counts)
  - LLM inference for synthesis and pattern recognition across the vault
  - [[wikilink]] traversal — follow internal links to discover connected notes
  - Tag-based filtering — search and aggregate notes by #tag
  - Full-text search across all vault markdown files

USE THIS SUBAGENT FOR:
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
1. List of relevant notes found with relative paths and brief summaries
2. A concept map: how notes interconnect via [[wikilinks]] and shared #tags
3. Key excerpts from the most relevant notes
4. Python-executed statistics when quantitative (e.g., "23 notes tagged #quantum, 8 interlinked via [[quantum-computing]]")
5. Gap identification: topics mentioned in the vault but under-developed

**Status Note:** NOTES currently has no active DeepChat slot. Until configured, the main agent should handle vault reading directly (File Read from G:\My Drive\Obsidian\notes\) or fold note-reading into ARCHIVE if ARCHIVE has access to the vault directory.

---

## 7. DISPATCH DECISION MATRIX

### Primary Dispatch: "I need to..."

| User Intent | Delegate To | Mode | Notes |
|:------------|:------------|:-----|:------|
| "analyze these 3 papers" | SELF CLONE × 3 | parallel | One clone per paper, zero cross-contamination |
| "give me 3 different approaches" | SELF CLONE × 3 | parallel | Each clone gets a different angle prompt |
| "test how this reads to a new reader" | SELF CLONE | chain | Clone gets only the content, no context |
| "validate this claim independently" | SELF CLONE | chain | Clone must NOT see parent's reasoning |
| "write a report and save it" | PROJECTS | chain | Handles all file I/O + versioned naming |
| "generate this document" | PROJECTS | chain | Produces .md output with proper naming |
| "set up a new project directory" | PROJECTS | chain | Creates directory structure + scaffolds |
| "save these results to a file" | PROJECTS | chain | Writes data/code/artifacts to disk |
| "what did I publish in March 2026?" | RELEASES | chain | Scans Obsidian/releases/2026/03/ |
| "get me all DOIs from last month" | RELEASES | chain | Extracts structured metadata |
| "feed publications into social pipeline" | RELEASES → SELF CLONE × 4 | chain→parallel | RELEASES reads, clones generate platform posts |
| "what do my notes say about X?" | NOTES | chain | Full-text search across Obsidian vault |
| "supplement this project with my research notes" | NOTES | chain | Retrieves relevant vault entries on topic |
| "check my notes for prior thinking on Y" | NOTES | chain | Scans topic notes + fleeting notes + daily journals |
| "cross-reference my notes with publications" | NOTES + RELEASES | parallel | Vault thinking + current publications, parent merges |
| "analyze publication trends in 2025" | RELEASES | chain | Python analysis of publication metadata |
| "what did I write about X in 2024?" | ARCHIVE | chain | Deep search across Archive/notes/ |
| "find templates for a research proposal" | ARCHIVE | chain | Searches Archive/templates/ |
| "has this topic been covered before?" | ARCHIVE | chain | Cross-reference against all past work |
| "audit all my past projects in 2023" | ARCHIVE | chain | Recursive scan of Archive/projects/ |
| "retrieve my old agent configurations" | ARCHIVE | chain | Searches Archive/prompts/ |
| "create a new system prompt" | PROMPTS | chain | Uses META-PROMPT-DEEPSEEK methodology |
| "audit this prompt for compliance" | PROMPTS | chain | Scores 0-10 on Constitutional compliance |
| "update the social prompt templates" | PROMPTS | chain | Edits files in social/ directory |
| "modify the subagent descriptions" | PROMPTS | chain | Edits SUBAGENT_DESCRIPTIONS.md |

### Secondary Dispatch: "What subagent for..."

| Capability Needed | Subagent |
|:------------------|:---------|
| Fresh, unbiased analysis with no context | SELF CLONE |
| Parallel processing of independent subtasks | SELF CLONE |
| Reader testing / prompt validation | SELF CLONE |
| Writing files, generating documents, editing projects | PROJECTS |
| Saving data, reports, code, or generated artifacts | PROJECTS |
| Creating project directories or scaffolding | PROJECTS |
| Reading current publication releases (Obsidian) | RELEASES |
| Feeding publication data into SOCIAL-ORCHESTRATOR | RELEASES |
| Extracting metadata from publication .md files | RELEASES |
| Supplementing projects with personal knowledge base notes | NOTES |
| Searching Obsidian vault for prior thinking on a topic | NOTES |
| Vault analytics (tag frequency, note interlinking, gaps) | NOTES |
| Cross-referencing vault notes against archive and releases | NOTES |
| Historical documents, past notes, prior projects | ARCHIVE |
| Cross-referencing against past work | ARCHIVE |
| Templates from Archive/templates/ | ARCHIVE |
| Archived publication copies (Archive/releases/) | ARCHIVE |
| Retrieving old prompts or configurations (Archive/prompts/) | ARCHIVE |
| Writing or editing prompt files in G:\My Drive\prompts\ | PROMPTS |
| Creating Tier 2 system prompts, sub-prompt libraries | PROMPTS |
| Auditing/patching existing prompt files | PROMPTS |
| Documenting agent workflows and dispatch patterns | PROMPTS |

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

## 10. PROMPT TEMPLATE INTEGRATION

The prompt template system (accessible via `fill_prompt_template`) integrates with the subagent system as follows:

### OMEGA-SCHOLAR Pipeline
| Stage | Template Name | Delegate To | Rationale |
|:------|:-------------|:------------|:----------|
| Stage 1: Setup | `OMEGA-SCHOLAR-STAGE-1-SETUP` | Main thread or SELF CLONE | Context gathering + Search Manifest generation |
| Stage 2: Draft | `OMEGA-SCHOLAR-STAGE-2-DRAFT` | SELF CLONE | Python-only evidence + narrative (parallelizable across topics) |
| Stage 3: Review | `OMEGA-SCHOLAR-STAGE-3-REVIEW` | SELF CLONE (different from Stage 2) | Blind audit against anti-fabrication — must NOT see Stage 2 reasoning |
| Stage 4: Publish | `OMEGA-SCHOLAR-STAGE-4-PUBLISH` | PROJECTS | Final assembly + file write with source labels |

### SOCIAL Pipeline
| Template Name | Delegate To | Rationale |
|:-------------|:------------|:----------|
| `SOCIAL-ORCHESTRATOR` | Main thread (dispatcher) | Orchestrates the pipeline, delegates to platform agents |
| `SOCIAL - Twitter/Bluesky` | SELF CLONE | Parallel generation with platform-specific template |
| `SOCIAL - Mastodon` | SELF CLONE | Parallel generation with platform-specific template |
| `SOCIAL - LinkedIn` | SELF CLONE | Parallel generation with platform-specific template |
| `SOCIAL - Substack` | SELF CLONE | Parallel generation with platform-specific template |

### Recommended Flow for SOCIAL Pipeline:
1. **Main thread:** Fill `SOCIAL-ORCHESTRATOR` template to get the full pipeline prompt
2. **Delegate to SELF CLONE:** Run the orchestrator in a self-clone with the filled template
3. **Clone executes:** The orchestrator prompt guides it through reading publications and generating platform content
4. **Write via PROJECTS:** If output needs to be saved, chain to PROJECTS for file writes

---

## 11. COMMON DISPATCH ERRORS (ANTI-PATTERNS)

| Anti-Pattern | Why It's Wrong | Correct Approach |
|:-------------|:---------------|:-----------------|
| **Running all work in main thread** | Wastes context, no parallelization, no blind validation | Delegate specialized work to subagents |
| **Using SELF CLONE for file writes** | Clone may write to unexpected locations; no centralized write tracking | Use PROJECTS for ALL file writes |
| **Using PROJECTS for read-only research** | PROJECTS is optimized for writes; burns a write-capable slot on reading | Use ARCHIVE or RELEASES for read-only research |
| **Using ARCHIVE for current releases** | ARCHIVE has historical copies only; current releases are in Obsidian/releases/ | Use RELEASES for current publications |
| **Not providing enough context to SELF CLONE** | Clone starts with ZERO knowledge of the conversation; incomplete prompts produce garbage | Write self-contained, complete prompts for every clone |
| **Chain mode for independent tasks** | Sequential execution wastes time when tasks don't depend on each other | Use `parallel` mode for independent work |
| **Parallel mode for dependent tasks** | Later tasks can't access earlier results in parallel mode | Use `chain` mode when Step 2 needs Step 1's output |
| **Delegating trivial tasks** | Overhead of spawning a subagent exceeds the cost of doing it directly | Handle single-step, <200-word-output tasks in the main thread |
| **Writing prompts/ to PROJECTS instead of PROMPTS** | Creates split authority over prompt files | Route ALL prompt writes to PROMPTS agent |
| **PROJECTS writing to Archive or Releases** | Destroys the integrity of read-only directories | Hard refusal — redirect to appropriate directory |
| **Not aggregating parallel results** | Dumping raw subagent outputs to the user is lazy and incoherent | Synthesize, remove redundancy, resolve conflicts |
| **Assuming subagent has parent's context** | Subagents are isolated; they don't know what the parent discussed | Every subagent prompt must be fully self-contained |
| **Using NOTES for file writes** | NOTES is read-only — vault integrity depends on it | Use PROJECTS for all output files |
| **Not checking NOTES before starting a project** | Misses prior thinking that could save hours of redundant research | Always query NOTES + ARCHIVE before writing on a familiar topic |

---

## 12. SLOT CONFIGURATION REFERENCE

| Agent | Slot ID | Status | Write Access | Read Access |
|:------|:--------|:-------|:-------------|:------------|
| SELF CLONE | `self` | ✅ Active | G:\My Drive\ (same as parent) | G:\My Drive\ (same as parent) |
| PROJECTS | `slot-movio4vd-yj9c` | ✅ Active | G:\My Drive\projects\, G:\My Drive\prompts\ | All directories |
| ARCHIVE | `slot-movbn8bi-f61j` | ✅ Active | NONE (read-only) | G:\My Drive\Archive\ only |
| RELEASES | *(not configured)* | ⬜ Pending | NONE (read-only) | G:\My Drive\Obsidian\releases\ only |
| NOTES | *(not configured)* | ⬜ Pending | NONE (read-only) | G:\My Drive\Obsidian\notes\ only |
| PROMPTS | *(not configured)* | ⬜ Pending | G:\My Drive\prompts\ only | All directories |

**To configure RELEASES, NOTES, or PROMPTS:** Copy the "Slot-Ready Description" block from Section 3, 6, or 5 above into a new DeepChat subagent slot. Configure the target with appropriate directory access as specified in the description.

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

**[END OF SUBAGENT DESCRIPTIONS v2.1]**
