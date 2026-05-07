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
  • G:\My Drive\prompts\ — ONLY when the Prompts agent is specifically being used
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
| Retrieving old prompts or agent configurations | `ARCHIVE` |
