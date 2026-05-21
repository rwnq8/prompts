# Archive-Discovered Diagnostic Patterns (F22-F24)

**Source:** Cross-project analysis of 15 Archive LEARNINGS.md files (2026-05-21)
**Target:** `G:\My Drive\projects\Hierarchy as Ultrametricity\SYSTEM-PROMPT-DIAGNOSTIC.md`
**Status:** Documented here pending transfer to target (outside prompts write boundary)

---

## F22: Obsidian Note Export Fragility [MODERATE]

### Symptoms
- Exported Obsidian notes may contain only table-of-contents links to external conversation threads, not full content
- Agent reads notes believing they contain substantive material, but the actual content is in unreachable linked conversations
- Creates false sense of data completeness — agent proceeds with analysis based on incomplete inputs

### Root Cause
Obsidian exports concatenated notes where some topic areas have full content (physics/math discussions) while others have only navigation links (TOC entries). The agent cannot distinguish between the two without verifying content depth.

### Source
Tree at the Bottom of Everything, L1

### Recommended System Prompt Change
Add to §0.8 (Due Diligence) or §9 (Git Protocol):
```
After reading imported/external notes, verify content depth:
1. For each note file, check if content is >500 chars (substantive) or <200 chars (likely TOC only)
2. Flag TOC-only notes as [CONTENT-MISSING] — do not treat as having been read
3. Request full content from user before proceeding with analysis
```

---

## F23: Terminology Drift Between Sibling Projects [MODERATE]

### Symptoms
- Multiple projects develop independently, evolving different vocabulary for identical concepts
- Synthesis documents claim convergence using a shared term, but source projects use different words OR use the same word to mean different things
- Reader cannot verify the convergence claim because the terminology mapping is invisible

### Root Cause
Projects that share a mathematical/philosophical domain naturally develop terminology independently. Synthesis authors assume shared vocabulary implies shared semantic structure — but shared name does NOT equal shared structure (extends CPL L22-L23 to cross-project context).

### Source
Ultrametric Geometry as Common Mathematical Structure, L1; Every Point is the Center of its Own Universe, L1; CPL L22-L23

### Recommended System Prompt Change
Add to §11.6 (Multi-Project Synthesis Audit):
```
5. Terminology Drift Documentation: If the synthesis introduces or repurposes terminology,
   include an explicit "Cross-Project Terminology Map" appendix:
   - Table mapping each synthesis term to its source-project equivalents
   - For terms that appear in multiple source projects: verify definitional equivalence
   - If definitions differ, flag as [TERMINOLOGY-DRIFT] — use distinct terms
```

---

## F24: Background Exec Output Buffering on Windows [MINOR]

### Symptoms
- Python stdout may be buffered when running via `exec(background: true)` on Windows
- Output appears delayed, incomplete, or not at all
- Agent assumes execution completed silently when it's still running or buffered

### Root Cause
Windows process I/O buffering differs from Unix. Python's default line-buffering for interactive stdout may not apply to background subprocess pipes. Output is held in a 4KB-8KB buffer and only flushed when full or process exits.

### Source
Symmetric Extension of Ultrametric Error Confinement, ultrametric_v2 (recurring pattern across both projects)

### Recommended System Prompt Change
Add to §0.6 or Python execution instructions:
```
For background Python execution on Windows:
- Use `print(..., flush=True)` for all status/progress output
- Or redirect stdout to a log file and read the file for output
- For long-running scripts, write periodic checkpoint files to confirm progress
- Never assume silent background exec completed — verify with process poll or checkpoint file
```

---

## Cross-Reference Table

| Pattern | Archive Projects | CPL Reference | Diagnostic Reference |
|:--------|:-----------------|:--------------|:---------------------|
| F22: Obsidian export fragility | Tree at Bottom (1) | — | NEW |
| F23: Terminology drift | Ultrametric Geometry (1), Every Point (1) | L22-L23, L35 | Extends |
| F24: Background exec buffering | Symmetric Extension (2), ultrametric_v2 (1) | L39 (subagent truncation) | Related |
