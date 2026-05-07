# SUBAGENT DESCRIPTIONS — Verbose Dispatch Reference
> Use these descriptions when configuring subagent slots in DeepChat.
> Each description is designed so the LLM can unambiguously route tasks to the correct subagent.

---

## 1. SELF CLONE

**Name:** `FRESH INSTANCE — Clean Slate, Zero Context, Full Tools`

**Description:**
```
An isolated clone of the current agent with NO conversation history, NO priming, and NO access to the parent session's context. Inherits the same working directory and tool access but starts completely fresh.

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

---

## 2. PROJECTS

**Name:** `PROJECTS WORKSPACE — Read/Write Projects & Prompts Only`

**Description:**
```
The ONLY subagent authorized for file writes and edits. All generated content, documents, code, drafts, and outputs MUST be written here. Never write to Archive or Releases — those are read-only resource directories.

TARGET: Configure with write access to project directories

WRITE TARGETS:
  • Project working directories under G:\My Drive\ (user's active project spaces)
  • G:\My Drive\prompts\ — delegate to PROMPTS subagent (this agent reads only)
  • NEVER write to G:\My Drive\Archive\ — archive is historical, read-only
  • NEVER write to G:\My Drive\Obsidian\releases\ — releases are publication source files, read-only

READ ACCESS:
  • Full read access to G:\My Drive\ for sourcing materials
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

---

## 3. RELEASES

**Name:** `PUBLICATION RELEASES READER — Current Publications, YYYY/MM Structure`

**Description:**
```
Read-only access to the CURRENT publication release files at G:\My Drive\Obsidian\releases\. This is the LIVE feed of publications, organized by year and month directories. This is NOT the archive — it contains the authoritative current copies of all publication markdown files.

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

---

## 4. ARCHIVE

**Name:** `ARCHIVE RESEARCHER — 35K+ Historical Documents, Read-Only Deep Search`

**Description:**
```
Read-only deep research agent for the complete historical archive at G:\My Drive\Archive\. This is the system of record for ALL past work — projects, notes, websites, templates, archived releases, and prompts. Contains over 35,000 items spanning years of accumulated research, writing, and development.

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

---

## 5. PROMPTS

**Name:** `PROMPTS AGENT — Tier 1 & Tier 2 Prompt Engineering Workspace`

**Description:**
```
Dedicated agent for the G:\My Drive\prompts\ directory — the prompt engineering workspace. This is where Tier 1 meta-prompts, Tier 2 system prompts, agent configurations, sub-prompt libraries (social/, scholar/), and prompt dispatch reference files live.

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

---

## Quick Dispatch Decision Matrix

| Task Requires... | Use This Subagent |
|:-----------------|:------------------|
| Fresh, unbiased analysis with no context | `SELF CLONE` |
| Parallel processing of independent subtasks | `SELF CLONE` |
| Reader testing / prompt validation | `SELF CLONE` |
| Writing files, generating documents, editing projects | `PROJECTS` |
| Saving data, reports, code, or generated artifacts | `PROJECTS` |
| Creating project directories or scaffolding | `PROJECTS` |
| Reading current publication releases (Obsidian) | `RELEASES` |
| Feeding publication data into SOCIAL-ORCHESTRATOR | `RELEASES` |
| Extracting metadata from publication .md files | `RELEASES` |
| Historical documents, past notes, prior projects | `ARCHIVE` |
| Cross-referencing against past work | `ARCHIVE` |
| Templates from Archive/templates/ | `ARCHIVE` |
| Archived publication copies (Archive/releases/) | `ARCHIVE` |
| Retrieving old prompts or configurations (Archive/prompts/) | `ARCHIVE` |
| Writing or editing prompt files in G:\My Drive\prompts\ | `PROMPTS` |
| Creating Tier 2 system prompts, sub-prompt libraries | `PROMPTS` |
| Auditing/patching existing prompt files | `PROMPTS` |
| Documenting agent workflows and dispatch patterns | `PROMPTS` |
