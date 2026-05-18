# SYSTEM-WIDE AUDIT — IMPLEMENTATION SPECIFICATION v1.0

> **Generated:** 2026-05-18 | **Audit Branch:** `feature/projects-cleanup-audit`
> **Purpose:** Self-contained implementation prompt for executing ALL recommendations from the comprehensive projects-directory audit. Feed this specification to a Prompts-agent session for execution.
> **Design principle:** Every action has explicit commands, expected output, and verification step. No ambiguity.

---

## PRE-EXECUTION: Session Identity & Git Hygiene

```
□ Verify you are on a feature/ branch, not main/master
□ Working tree is clean: git status --short returns empty
□ Read this entire specification before executing any changes
□ Execute in order: PART I → PART II → PART III → PART IV → PART V
□ After EACH file modification: git add <file> + git commit
□ After EACH commit: git log -1 --oneline to verify
```

---

# PART I: CLEANUP — ROOT-LEVEL .GIT REMEDIATION

## I.1 Diagnostic Confirmation

```powershell
# Confirm the parent .git exists
Test-Path "G:\My Drive\projects\.git"
# Expected: True

# Confirm current dirty state (staged deletions)
git -C "G:\My Drive\projects" status --short | Measure-Object | Select-Object -ExpandProperty Count
# Expected: >100 (staged deletions from archived projects)
```

## I.2 Action: Unstage All Deletions + Remove Parent .git

```
STEP 1: Unstage everything (preserves files in archive)
  git -C "G:\My Drive\projects" reset HEAD
  VERIFY: git -C "G:\My Drive\projects" status --short → should show untracked deletions, NOT staged

STEP 2: Checkout to a clean state (discard working tree changes)
  git -C "G:\My Drive\projects" checkout -- .
  VERIFY: git -C "G:\My Drive\projects" status --short → should be EMPTY

STEP 3: Remove the parent .git directory
  Remove-Item "G:\My Drive\projects\.git" -Recurse -Force
  VERIFY: Test-Path "G:\My Drive\projects\.git" → False

STEP 4: Confirm no other .git contamination in projects tree
  Get-ChildItem "G:\My Drive\projects" -Recurse -Directory -Filter ".git" -Depth 3
  VERIFY: Should return NOTHING (no .git directories anywhere in projects/)
```

## I.3 Verification That Archived Projects Are Intact

```powershell
# Each archived month should still have its full file count
Get-ChildItem "G:\My Drive\Archive\projects\2026\05" -Directory | ForEach-Object {
    $count = (Get-ChildItem $_.FullName -File -Recurse | Measure-Object).Count
    "$($_.Name): $count files"
}
# Compare against pre-removal counts from audit:
# Language-Info-Architecture: 845 files (month 03 total — verify project-specific)
# Every Point is the Center: part of month 05 (1307 total across 11 projects)
# All 11 projects in 2026/05 should be intact
```

## I.4 Git Commit (in prompts repo, not projects!)

```bash
git add "G:\My Drive\prompts\SYSTEM-AUDIT-IMPLEMENTATION-SPEC.md"
git commit -m "ACTION:CREATE FILE: SYSTEM-AUDIT-IMPLEMENTATION-SPEC.md RATIONALE:Comprehensive implementation spec from projects-directory audit — PART I root .git remediation executed"
```

---

# PART II: CROSS-PROJECT-LEARNINGS.md — ADD 22 NEW LESSONS

## II.1 Pre-Modification Snapshot

```powershell
# Current lesson count
Select-String -Path "G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md" -Pattern "^### L\d+:" | Measure-Object | Select-Object -ExpandProperty Count
# Expected: 8 (L1-L8 for the table entries, L13-L18 for detailed lessons — L9-L12 were skipped in original numbering)
```

## II.2 New Lessons to Append

Append the following AFTER the last existing lesson (L18) in `G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md`. Also update the table at the top of the file to add the new entries.

### L19: Git branch may be renamed by concurrent processes

- **Category:** GIT
- **Issue:** The branch `feature/ultrametric-v2-ternary-tree` was renamed to `feature/tree-distance-cophenetic` mid-session by a parallel process. Commits continued under the old branch name, creating confusion about which branch contained the latest work.
- **Solution:** Check `git branch --show-current` before EVERY commit. If the branch has changed, use `git reflog` to recover the commit history and understand what happened. Never assume the branch name is stable across a session.
- **Prevention:** DEFAULT.md §9.2 Pre-Work Checklist (Step 2) and §9.4 Git Execution Audit already include branch verification. This lesson adds: verify branch name has not changed since last check — a rename by parallel process is a distinct failure mode from being on the wrong branch.
- **Cross-Project:** YES — any environment with parallel LLM sessions sharing a repo.

### L20: Never reuse branches across projects

- **Category:** GIT
- **Issue:** The branch `feature/ultrametric-v2-ternary-tree` was created for the ultrametric_v2 project, then reused for Tree Distance Cophenetic work. This caused git path discrepancies: a file committed as `ultrametric_v2/0.8.md` physically existed in `Tree Distance Cophenetic/0.8.md`. The branch name carried semantic meaning that conflicted with the actual project.
- **Solution:** Create project-specific branches from the start. Branch name = `feature/<project-name>-<task>`. When a project is completed and archived, its branches can be cleaned up. Never repurpose a branch for a different project.
- **Prevention:** At session start, verify the branch name matches the assigned project. If the branch name references a different project, create a new branch.
- **Cross-Project:** YES — applies to all multi-project workflows.

### L21: Backlog drift when files deleted by parallel sessions

- **Category:** METHODOLOGY
- **Issue:** Files `0.1.md` and `0.1.1.md` were removed by a parallel session. BACKLOG.md still referenced them as active files, making it stale. PROJECT STATE.md documented the deletion but BACKLOG.md was not updated. Running `os.path.exists()` on every referenced file revealed the drift.
- **Solution:** When files are deleted (by any process), immediately update ALL 7 documentation files that reference them. Use Python `os.path.exists()` to verify all referenced files exist at session start. A stale BACKLOG.md is worse than no BACKLOG.md — it actively misleads.
- **Prevention:** Add a file-existence audit to the session-start procedure: scan all 7 docs for file references and verify each exists on disk. Flag any stale references before beginning work.
- **Cross-Project:** YES — applies to any project with multiple parallel sessions or archival workflows.

### L22: Retroactive framing creates illusion of consilience

- **Category:** METHODOLOGY
- **Issue:** A convergence synthesis claimed four projects independently converged on the "cross-ratio." A source-document vocabulary audit revealed that 3 of 4 projects (Kapustin-Witten, Ultrametric Synthesis, Undecidability) never used the term "cross-ratio." The convergence was retroactively imposed by the synthesis author, not independently discovered. The synthesis was valid as an interpretive lens but invalid as a discovery claim.
- **Solution:** Before claiming consilience, audit the source documents for the claimed common vocabulary. If the unifying concept appears only in the synthesis document and not in the source projects, the convergence is a framing choice, not a discovery. Distinguish between (a) concepts native to source documents and (b) concepts imposed by the synthesis.
- **Prevention:** Any multi-project synthesis claiming convergence MUST include a source-document vocabulary audit. Flag terms that appear only in the synthesis, not in the sources. The audit itself should be part of the published methodology.
- **Cross-Project:** YES — any multi-project synthesis making convergence/consilience claims.

### L23: Equivocation weakens convergence arguments — shared name ≠ shared structure

- **Category:** METHODOLOGY
- **Issue:** Two projects used "cross-ratio" in different senses: one as a statistical ratio ($f_1/f_2$), the other as a projective invariant ($(AC \cdot BD)/(BC \cdot AD)$). The synthesis treated them as identical because they shared a name, creating an equivocation that undermined the convergence argument.
- **Solution:** Audit terminology before claiming mathematical identity. Shared name does NOT equal shared structure. When a term is used differently across projects, either (a) rename one usage to avoid confusion, or (b) excise the weak link. The synthesis is STRONGER with 4 genuine convergences than 5 with an equivocation.
- **Prevention:** For any synthesis claiming convergence, run a term-by-term audit: "Does project A's definition of X match project B's definition of X?" If definitions differ, the convergence claim is invalid for that term regardless of shared vocabulary.
- **Cross-Project:** YES — applies to any multi-domain synthesis.

### L24: Salvage requires trading the grand claim for the honest signal

- **Category:** METHODOLOGY
- **Issue:** When a convergence synthesis failed reader testing (the central claim of independent discovery was undermined by the vocabulary audit), the project could have been abandoned entirely. Instead, a systematic vocabulary audit revealed a genuine convergence signal (projective geometry, tree structures, Archimedean/non-Archimedean tension) that was present across source documents — just not the convergence originally claimed.
- **Solution:** Rather than defending the over-claim, rebuild from the data. The vocabulary audit provided an objective basis for identifying what actually converges vs. what was imposed. The salvage document trades the grand consilience narrative for a smaller, sharper, testable research program.
- **Prevention:** When a project's central claim is undermined by evidence, don't abandon — audit the source materials for what genuinely overlaps and rebuild from there. The signal may be different from what was claimed but may still be interesting. A smaller true claim beats a grand false one.
- **Cross-Project:** YES — any multi-project synthesis that fails reader testing.

### L25: Avoid role-labeling collaborators

- **Category:** METHODOLOGY
- **Issue:** A subagent essay characterized a collaborator as a "formal verification specialist" and framed an exchange as "physicist vs. formal verification specialist." This is reductive, creates an us-vs-them dynamic, and would be inflammatory if read by the person so labeled. It frames people by a single dimension of their expertise rather than as whole participants.
- **Solution:** Refer to people neutrally by name or not at all. Frame exchanges around the ideas, not the identities of participants. "The proposal received detailed technical feedback" is better than "a formal verification specialist reviewed it."
- **Prevention:** When writing about collaborative exchanges where participants may read the output, audit all characterizations of people. If a label could rankle, remove it. The rule: frame around ideas, not identities.
- **Cross-Project:** YES — applies to all writing that references specific people, especially potential collaborators.

### L26: Fresh-reader testing catches author blind spots

- **Category:** METHODOLOGY
- **Issue:** After multiple sessions refining a paper, the author assumed everything was clear. A fresh Claude subagent (zero context) caught 8-10 issues the author missed — the abstract framed results as quantum when it was classical simulation, "zero logical error" was statistically overstated, energy barrier mapping was unexplained, genre ambiguity, mathematical gaps, undefined terms. This pattern repeated across FOUR separate projects (Validation of Ultrametric Error Confinement, Statistical Genesis of Appearance, Force-Multiplier Playbook, Tree at the Bottom of Everything).
- **Solution:** Always run a blind reader test (fresh LLM with zero project context, full document inline, targeted reader questions) before declaring any document complete. Authors are blind to their own ambiguities. A reader without project history catches contradictions invisible after multiple revision rounds.
- **Prevention:** Mandatory reader testing before publication. Use REVIEWER subagent or fresh Claude session with: (a) full document text, (b) explicit reader questions ("What's confusing?", "What's missing?", "What contradicts?"), (c) zero prior context about the project.
- **Cross-Project:** YES — confirmed across 4 independent projects. Should be standard for all publication documents.

### L27: Two-round reader testing — first catches surface, second catches structure

- **Category:** METHODOLOGY
- **Issue:** First reader test on a general-audience essay caught obvious jargon ("ultrametric space"). The second round, after those fixes, caught deeper structural problems — the discrete-continuous bridge was more abstract than anything the first reader flagged, and the closing paragraph added in v2 still needed work. One round would have left significant problems undetected.
- **Solution:** Plan for at least two rounds of reader testing when polishing for a general audience. The first round catches surface problems (jargon, undefined terms, confusing sentences). The second round catches structural problems (logical gaps, unclear transitions, missing context) that were hidden behind the surface issues.
- **Prevention:** After every substantive manuscript edit, run a fresh reader test. Don't assume one round suffices. Budget for at least two rounds in project timelines.
- **Cross-Project:** YES — applies to all document production.

### L28: Reader testing catches genre ambiguity and mathematical gaps

- **Category:** METHODOLOGY
- **Issue:** Blind reader testing of a synthesis document revealed 8 issues the authors did not notice: no mathematical derivations, Compton wavelength $2\pi$ ambiguity, $\alpha$ running ignored, unfalsifiability, undefined "agent," genre ambiguity (is this a review? a proposal? a proof?), why $\alpha$ alone, and load-bearing acknowledged gaps. The document read differently to someone without project context.
- **Solution:** Created a revised version with a 7-section structure addressing all 8 issues: Python-verified derivations, operational agent definition, structured limitations, explicit testability pathways. The revision was guided entirely by reader feedback — issues the authors were blind to.
- **Prevention:** Before considering a synthesis document complete, ask a fresh reader: "What genre is this document?" If they can't answer clearly, the document has a genre problem that needs structural reorganization. Math claims must be verified by Python execution, not asserted.
- **Cross-Project:** YES — reader testing should be standard for any document intended for external consumption.

### L29: Describe architecture that WAS used, not aspirational

- **Category:** METHODOLOGY
- **Issue:** A methodology paper's Section 3 described a Docker/API/Overleaf stack that was never used to produce any results. The actual architecture — DeepChat conversation with integrated file I/O, Python execution, and git — was simpler, faster (zero setup vs. 15 minutes), and had already produced two published papers. Describing an aspirational stack as if it were the actual implementation undermines credibility and obscures the real methodological insight.
- **Solution:** Rewrote the methodology section to describe the real architecture. Kept the Docker specification in an appendix labeled as aspirational/future deployment. Added a second validation case study confirming the same architecture worked in a completely different domain.
- **Prevention:** When documenting methodology, audit every architectural claim: "Did we actually use this, or did we only design it?" Only the former belongs in the main text. Aspirational designs go in appendices or Future Work.
- **Cross-Project:** YES — applies to all methodology papers and technical documentation.

### L30: Mutual exclusion is stronger signal than correlation

- **Category:** METHODOLOGY
- **Issue:** A Sapir-Whorf meta-regression looked for a positive correlation between frequency load and effect size and found none. The reframed analysis looked for co-occurrence patterns of mandatory categories and found a striking zero intersection: 0 languages with both epistemic AND ontological obligation. A zero cell in a contingency table is a stronger finding than a weak correlation coefficient.
- **Solution:** Absence of co-occurrence in a well-chosen sample is evidence for a universal constraint. Correlation analysis can miss structural relationships that contingency analysis reveals. The design space may be characterized more by what combinations are impossible than by what tendencies exist.
- **Prevention:** For cross-linguistic typology or any comparative analysis, always check for mutual exclusion patterns before running regressions. A zero cell in a properly sampled contingency table is a finding, not a failure.
- **Cross-Project:** YES — applicable to any typological or comparative analysis.

### L31: Permutation tests detect structure that pairwise tests miss

- **Category:** METHODOLOGY
- **Issue:** Individual pairwise tests for mutual exclusion were mostly non-significant due to low base rates (e.g., only 2 languages have spatial obligation). A naive analysis would conclude "no significant mutual exclusion" — missing the global structure. The global permutation test aggregated across all pairs: 10 observed zero intersections vs. 3.7 expected under random assignment, $p < 0.0001$.
- **Solution:** For sparse contingency tables with structural constraints, use global permutation/distribution tests rather than pairwise tests. The signal may be in the pattern of zeros, not in any individual cell.
- **Prevention:** When individual cells are sparsely populated, aggregate. A pattern of many individually non-significant zeros can be globally highly significant.
- **Cross-Project:** YES — applicable to any sparse typological/classification analysis.

### L32: The Archimedean assumption is invisible until challenged

- **Category:** METHODOLOGY
- **Issue:** Standard QM assumes $\mathbb{C}$ with the Archimedean norm so deeply that alternatives are unthinkable. The Ultrametric Synthesis critique revealed this as a hidden assumption — a choice of norm that shapes the entire mathematical framework without being acknowledged as a choice. Once the assumption is surfaced, alternative geometries (non-Archimedean, ultrametric) become visible as genuine alternatives.
- **Solution:** For any foundational framework, systematically ask: what changes under a different norm, a different metric, a different topology? The assumptions that are never questioned are the ones that most constrain thought.
- **Prevention:** In any foundational analysis, include an "assumption audit": list the mathematical structures taken as given and ask what alternatives exist. The Archimedean assumption is one example; others include Euclidean metric, continuous manifolds, real-valued probabilities.
- **Cross-Project:** YES — applies to any foundational or axiomatic analysis.

### L33: Cite actual tools used, not aspirational ones

- **Category:** METHODOLOGY
- **Issue:** A paper's Acknowledgments claimed "The LLM (Claude, Anthropic) served as..." but the actual work was executed with DeepSeek V4 Pro in the DeepChat desktop application. The docker-compose.yml hardcoded `claude-sonnet-4-20250514` as the default model. A reference cited "& Claude" instead of "& DeepSeek." This falsely attributed the work to a different platform.
- **Solution:** Corrected Acknowledgments to credit DeepSeek V4 Pro + DeepChat with explicit environment details (platform-native desktop app, integrated Python/PowerShell/filesystem, no Docker). Fixed all references. The platform-native aspect matters: DeepChat's agentic capabilities enable the task execution/completion/iteration cycle within a single LLM chat thread.
- **Prevention:** Before finalizing any paper, audit every platform/tool/vendor name: "Did we actually use this, or is this what the original template said?" Templates and skill files may describe a different platform than the one executing the work.
- **Cross-Project:** YES — applies whenever methodology papers describe tools.

### L34: When a theoretical framework produces internal contradictions, it needs replacement, not patching

- **Category:** METHODOLOGY
- **Issue:** Three fundamental problems with a linguistic relativity framing: (1) it reversed causal direction (frequency is a symptom of obligatoriness, not a cause of cognition), (2) it violated Zipf's own logic (high frequency = low information, the opposite of what the hypothesis needed), and (3) it required cross-domain commensurability that doesn't exist. The framework produced internal contradictions that could not be resolved by adjusting parameters.
- **Solution:** The Jakobson/Shannon/Grice/Greenberg framework replaced the Sapir-Whorf framing entirely. Shannon entropy provided a language-independent metric. Gricean surplus quantified forced over-informativeness. Greenbergian universals provided testable predictions about co-occurrence constraints. The replacement framework solved all three problems simultaneously.
- **Prevention:** When a theoretical framework produces internal contradictions (like assuming high frequency = high importance while using a law that states the opposite), the framework needs replacement, not patching. Don't add epicycles.
- **Cross-Project:** YES — applies to any theoretical framework evaluation.

### L35: Terminology shifts must be explicitly explained in synthesis documents

- **Category:** WRITING
- **Issue:** A synthesis draft shifted from "Bruhat–Tits tree" language (used in May 1–12 releases) to "cophenetic distance on rooted trees" (used from May 15 onward) without explaining the relationship. A reader familiar with the earlier papers sees an unexplained terminological rupture and reasonably asks whether previous claims are being abandoned.
- **Solution:** Added an explicit "Note on Terminology" section stating: (1) the Bruhat–Tits tree IS a rooted tree, (2) cophenetic distance applies to it, (3) the shift is generalization, not contradiction, (4) the generalization enables cross-domain reach. Readers should never have to guess whether a language change signals a correction or a generalization.
- **Prevention:** Any document that changes established terminology from prior releases MUST include an explicit "Note on Terminology" section explaining the relationship between old and new language. This is not pedantry — it's intellectual honesty.
- **Cross-Project:** YES — any multi-release research program where terminology evolves over time.

### L36: Distance definitions must survive naive first reading

- **Category:** WRITING
- **Issue:** A distance metric was defined as both "breadth of deepest shared cut" and "shallowness of first separating cut." A fresh reader flagged these as ambiguous — they point in opposite directions on a naive reading even though they're mathematically equivalent. The reader had to reconstruct the intended meaning from examples.
- **Solution:** Use a single, directional definition: "distance = how far back toward the trunk before the fork where they separate. The earlier the fork, the greater the distance." No reformulation needed. One concrete example beats two abstract formulations.
- **Prevention:** When defining a non-standard metric, state the definition in ONE way with a concrete example, not two ways that a naive reader could read as contradictory. Test the definition on a reader without mathematical training.
- **Cross-Project:** YES — applies to any exposition that redefines a familiar concept (distance, similarity, difference) in an unfamiliar way.

### L37: Iterative drafting converges faster with clear feedback rules

- **Category:** WRITING
- **Issue:** An email draft went through ~12 iterations before converging. Early iterations were verbose and apologetic; the user had to repeatedly correct tone. Once the user established clear rules — (1) no apologizing, (2) direct style, (3) no math formulas in email, (4) acknowledge uncertainty without false humility — iterations converged in 2–3 rounds.
- **Solution:** Ask for tone/style preferences BEFORE starting the first draft. Use a "tone sample" from the user. Explicit rules eliminate the guesswork that drives iteration count.
- **Prevention:** Before drafting any user-facing communication, ask: "What tone do you want? Any specific rules?" Document the preferences and apply them systematically.
- **Cross-Project:** YES — applicable to all email/direct-response drafting tasks.

### L38: Null-byte placeholder math fix corrupts files — use ASCII-safe markers

- **Category:** PYTHON
- **Issue:** A math remediation script used `\x00` (null byte) as placeholder delimiters for protected regions (code blocks, `$...$`). When writing the fixed content to disk, null bytes were stripped by the file system, leaving visible `PROTECT0`, `PROTECT1` artifacts in 8 of 15 files. The corrupted content was committed before detection. Recovery required restoring all 8 files from git and rewriting the fix script.
- **Solution:** Use triple-bracket ASCII markers (`[[[PROTECTED_N]]]`) instead of control characters. Verify zero marker leaks before writing. Always stage+commit and audit immediately after automated file modifications.
- **Prevention:** Never use non-printable ASCII control characters (`\x00`–`\x1F`) as in-band markers in text files. Use distinctive ASCII-safe patterns (`[[[MARKER_N]]]`, `<<<MARKER_N>>>`) and verify no leaks before writing.
- **Cross-Project:** YES — applies to any automated text transformation that uses placeholder markers.

### L39: Subagent output truncation at ~32K tokens — parent must complete long content

- **Category:** TOOL-USE
- **Issue:** A subagent tasked with writing a ~3,000-word essay produced excellent content but the session terminated ("error" status) at ~32K tokens, cutting off mid-sentence in the penultimate section. The essay was structurally complete through Section 5.2 but required the parent to finish Sections 5.2–6. This was discovered in two separate projects (Can Math Prove Physics, Tree at the Bottom of Everything).
- **Solution:** For long-form content generation via subagents, either (a) split into smaller sequential sections using chain mode, or (b) expect the parent to complete truncated output. Subagents reliably produce ~2,000–2,500 words before hitting token limits. For content >2,000 words, use chain mode with section-level tasks.
- **Prevention:** When delegating writing tasks to subagents, estimate output length. If >2,000 words, break into sections. Ask subagents to output in compact format (single markdown table) to survive truncation for structured outputs.
- **Cross-Project:** YES — applies to any subagent-based long-form writing.

### L40: Write tool may silently fail after multiple calls — fall back to Python

- **Category:** TOOL-USE
- **Issue:** After ~4 successful writes, subsequent writes returned permission-like errors despite valid paths. The tool reported success but files did not exist on disk. This created a false sense of completion.
- **Solution:** Fall back to Python `exec` for batch file writes when the write tool shows signs of failure. Always verify with `Test-Path` + `Get-Content -First 5` after every write operation regardless of tool.
- **Prevention:** Don't trust a sequence of successful writes to continue indefinitely. After 3-4 writes, verify aggressively. For batch operations (>5 files), prefer Python script execution over individual write calls.
- **Cross-Project:** YES — applies to any session with multiple sequential file writes.

## II.3 Table Update

Update the table at the top of CROSS-PROJECT-LEARNINGS.md to add rows for L19-L40. The table should match the existing format:

```
| L19 | GIT | Symmetric Extension | Git branch may be renamed by concurrent processes — check before every commit |
| L20 | GIT | Tree Distance Cophenetic | Never reuse branches across projects |
| L21 | METHODOLOGY | Tree Distance Cophenetic | Backlog drift when files deleted by parallel sessions — update all 7 docs |
| L22 | METHODOLOGY | Arithmetic Gauge | Retroactive framing creates illusion of consilience — audit source documents |
| L23 | METHODOLOGY | Arithmetic Gauge | Equivocation weakens convergence — shared name ≠ shared structure |
| L24 | METHODOLOGY | Arithmetic Gauge | Salvage: trade grand claim for honest signal — rebuild from data |
| L25 | METHODOLOGY | Can Math Prove Physics | Avoid role-labeling collaborators — frame around ideas, not identities |
| L26 | METHODOLOGY | Validation / Statistical Genesis / Force-Multiplier / Tree at Bottom | Fresh-reader testing catches author blind spots (4 projects confirm) |
| L27 | METHODOLOGY | Tree at Bottom of Everything | Two-round reader testing — first catches surface, second catches structure |
| L28 | METHODOLOGY | Statistical Genesis of Appearance | Reader testing catches genre ambiguity and mathematical gaps |
| L29 | METHODOLOGY | Force-Multiplier Playbook | Describe architecture that WAS used, not aspirational |
| L30 | METHODOLOGY | Language-Info-Architecture | Mutual exclusion is stronger signal than correlation |
| L31 | METHODOLOGY | Language-Info-Architecture | Permutation tests detect structure that pairwise tests miss |
| L32 | METHODOLOGY | Arithmetic Gauge | The Archimedean assumption is invisible until challenged |
| L33 | METHODOLOGY | Force-Multiplier Playbook | Cite actual tools used, not aspirational ones |
| L34 | METHODOLOGY | Language-Info-Architecture | Internal contradictions → replacement, not patching |
| L35 | WRITING | Ultrametric Geometry as Common Structure | Terminology shifts must be explicitly explained |
| L36 | WRITING | Every Point is the Center | Distance definitions must survive naive first reading |
| L37 | WRITING | Can Math Prove Physics | Iterative drafting converges faster with clear feedback rules |
| L38 | PYTHON | Statistical Genesis of Appearance | Null-byte placeholder math fix corrupts files — use ASCII-safe markers |
| L39 | TOOL-USE | Can Math Prove Physics / Tree at Bottom | Subagent output truncation at ~32K tokens — parent must complete |
| L40 | TOOL-USE | Symmetric Extension | Write tool may silently fail after multiple calls — fall back to Python |
```

## II.4 Verification

```powershell
# Count lessons after update
Select-String -Path "G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md" -Pattern "^### L\d+:" | Measure-Object | Select-Object -ExpandProperty Count
# Expected: 30 (L1-L8 + L13-L18 + L19-L40 — note L9-L12 were skipped in original numbering)

# Verify table rows
Select-String -Path "G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md" -Pattern "^\\| L\d+ \\|" | Measure-Object | Select-Object -ExpandProperty Count
# Expected: 30 rows in table
```

---

# PART III: SYSTEM PROMPT UPDATES

## III.1 ARCHITECTURE.md — Fix Slot ID Mismatch

**File:** `G:\My Drive\prompts\ARCHITECTURE.md`
**Current version:** v1.1
**New version:** v1.2

### Change 1: Layer 6 — Subagent Slot IDs (line ~103-108)

**FIND:**
```
| `self` | **EXPLORER** — Divergent Thinking | Inline text only | Brainstorming, alternatives, edge-case discovery | LLM only (~35% file I/O) |
| `slot-mp80dr5g-oh9g` | **IMPLEMENTER** — Convergent Execution | Inline text only | Drafting, structured output, content generation | LLM only (~35% file I/O) |
| `slot-mp80e4mj-5s1l` | **REVIEWER** — Critical Evaluation | Inline text only | Blind validation, reader testing, gap analysis | LLM only (~35% file I/O) |
```

**REPLACE WITH:**
```
| `slot-mp80a5ry-e7hn` | **EXPLORER** — Divergent Thinking | Inline text only | Brainstorming, alternatives, edge-case discovery | LLM only (~35% file I/O) |
| `slot-mp80ay3u-yzqo` | **IMPLEMENTER** — Convergent Execution | Inline text only | Drafting, structured output, content generation | LLM only (~35% file I/O) |
| `slot-mp80b6bl-iix2` | **REVIEWER** — Critical Evaluation | Inline text only | Blind validation, reader testing, gap analysis | LLM only (~35% file I/O) |
```

### Change 2: Layer 7 — Agent Description Files (line ~68)

Verify the slot IDs in the agent description file table match the live system. If the `agents/` files exist, update their slot references.

### Change 3: Version Bump

**FIND:** `*Architecture v1.1 — documents the DeepChat agent system taxonomy*`
**REPLACE WITH:** `*Architecture v1.2 — slot IDs synced to live DEFAULT.md v1.10; documents the DeepChat agent system taxonomy*`

Also update the version reference in Section 5 (File Reference table):
**FIND:** `| `ARCHITECTURE.md` | This document — high-level taxonomy | v1.1 |`
**REPLACE WITH:** `| `ARCHITECTURE.md` | This document — high-level taxonomy | v1.2 |`

---

## III.2 AGENT-CONFIG.md — Fix Slot ID Mismatch

**File:** `G:\My Drive\prompts\AGENT-CONFIG.md`
**Current version:** v5.1
**New version:** v5.2

### Change 1: EXPLORER Slot (line ~85)

**FIND:**
```
### EXPLORER (slot: `self`)
```

**REPLACE WITH:**
```
### EXPLORER (slot: `slot-mp80a5ry-e7hn`)
```

### Change 2: IMPLEMENTER Slot (line ~98)

**FIND:**
```
### IMPLEMENTER (slot: `slot-mp80dr5g-oh9g`)
```

**REPLACE WITH:**
```
### IMPLEMENTER (slot: `slot-mp80ay3u-yzqo`)
```

### Change 3: REVIEWER Slot (line ~111)

**FIND:**
```
### REVIEWER (slot: `slot-mp80e4mj-5s1l`)
```

**REPLACE WITH:**
```
### REVIEWER (slot: `slot-mp80b6bl-iix2`)
```

### Change 4: Version Bump

**FIND:** `# DEEPCHAT AGENT/SETUP CONFIGURATION (v5.1)`
**REPLACE WITH:** `# DEEPCHAT AGENT/SETUP CONFIGURATION (v5.2)`

**FIND:** `*Agent Configuration v5.1 — 3 agents mapped to 3 write boundaries*`
**REPLACE WITH:** `*Agent Configuration v5.2 — slot IDs synced to live DEFAULT.md v1.10; 3 agents mapped to 3 write boundaries*`

---

## III.3 DEFAULT.md — Add Branch-Rename Awareness + L19-L40 References

**File:** `G:\My Drive\prompts\DEFAULT.md`
**Current version:** v1.10
**New version:** v1.11

### Change 1: §0.2 Multi-Process Interference Detection — Add Branch Rename

**FIND (in §0.2):**
```
1. `git branch --show-current` → Has the branch changed since your last check?
   - **If CHANGED:** Another process or user switched branches. Do NOT silently continue.
     - Run `git status --short` to assess the new state.
     - If now on `main`/`master`: switch back to a feature branch immediately (`git checkout -b feature/<name>` or `git checkout <original-branch>`).
     - If on a different feature branch: acknowledge the switch, note the new branch, and proceed — another process may have legitimately changed context.
   - **If UNCHANGED:** Proceed to 0.3.
```

**REPLACE WITH:**
```
1. `git branch --show-current` → Has the branch changed since your last check?
   - **If CHANGED to a DIFFERENT branch name:** Another process or user switched branches. Do NOT silently continue.
     - Run `git status --short` and `git log -1 --oneline` to assess the new state.
     - If now on `main`/`master`: switch back to a feature branch immediately (`git checkout -b feature/<name>` or `git checkout <original-branch>`).
     - If on a different feature branch: acknowledge the switch, note the new branch, and proceed — another process may have legitimately changed context.
   - **If CHANGED to a RENAMED version of the same branch (e.g., `feature/ultrametric-v2` → `feature/tree-distance`):** A parallel process renamed the branch (CPL L19). Run `git reflog` to identify the rename point. Continue work on the renamed branch. Update PROJECT STATE.md with the new branch name.
   - **If UNCHANGED:** Proceed to 0.3.
```

### Change 2: §9 Git Protocol — Add Post-Commit Branch Verification

In §9.4 Git Execution Audit, after the existing verification table, add:

```
**Branch Rename Detection (CPL L19):** After every commit, compare the current branch name against the branch name recorded in PROJECT STATE.md. If they differ, the branch was renamed by a parallel process. Update PROJECT STATE.md with the new name. Use `git reflog` to confirm the rename is benign (same commit history, different label).
```

### Change 3: §0.7 LEARNINGS.md Format — Add Reference to CPL L19-L40

In §0.7, after the LEARNINGS.md format template, add:

```
**Cross-Reference:** Project-level lessons that generalize across projects are candidates for `G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md`. Currently 30 lessons catalogued (L1-L40). Read the full CPL file during §0.8 Due Diligence.
```

### Change 4: §8 Edge Cases — Add Branch Rename Scenario

Add to the edge cases section:

```
### GIT BRANCH RENAMED BY PARALLEL PROCESS
If `git branch --show-current` returns a different name than expected, but `git log` shows the same commit history:
1. Check `git reflog` to identify when the rename occurred.
2. Update PROJECT STATE.md with the new branch name.
3. Continue work on the renamed branch.
4. Document the rename in CHANGELOG.md.
5. This is a benign rename — CPL L19. Do NOT create yet another branch.
```

### Change 5: CONFIGURATION Block — Add CPL Reference

At the end of the CONFIGURATION block (top of DEFAULT.md), add:

```
**IMPORTANT — Cross-Project Lessons (CPL L19-L40):** 22 new cross-project lessons were added 2026-05-18 from a comprehensive audit of 11 archived projects. These cover: git branch renaming (L19-L20), backlog drift (L21), retroactive framing (L22), equivocation (L23), salvage methodology (L24), collaborator labeling (L25), reader testing (L26-L28), architecture honesty (L29), mutual exclusion analysis (L30-L31), hidden assumptions (L32), tool citation (L33), framework replacement (L34), terminology shifts (L35), distance definitions (L36), drafting feedback rules (L37), null-byte safety (L38), subagent truncation (L39), and write-tool failures (L40). See `G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md` for full text.
```

### Change 6: Version Bump

**FIND:** `**Version:** v1.10`
**REPLACE WITH:** `**Version:** v1.11`

**FIND:** `**Last updated:** 2026-05-16`
**REPLACE WITH:** `**Last updated:** 2026-05-18`

### Change 7: Update Change Log Note

Add to the version description line:
```
**Designed for:** THE ONE system prompt for all project work — general research, writing, coding, email management (Outlook COM, multi-account, v1.2 email prompts), with hard project isolation enforcement, mandatory 7-file documentation standards, Pre-Project Due Diligence (§0.8 internal literature review across projects/Archive/Obsidian), cross-project learning (30 lessons, L1-L40), semi-autonomous sprint-driven progression (WHAT'S NEXT? PROCEED / RESUME), and branch-rename detection (§0.2, CPL L19).
```

---

## III.4 Verification: Slot ID Consistency

```python
import re, os

prompts_dir = r"G:\My Drive\prompts"
files_to_check = ["DEFAULT.md", "ARCHITECTURE.md", "AGENT-CONFIG.md"]

# The ground truth slot IDs (from live DEFAULT.md tool definitions)
GROUND_TRUTH = {
    "EXPLORER": "slot-mp80a5ry-e7hn",
    "IMPLEMENTER": "slot-mp80ay3u-yzqo",
    "REVIEWER": "slot-mp80b6bl-iix2"
}

all_pass = True
for fname in files_to_check:
    fpath = os.path.join(prompts_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    
    found_slots = set(re.findall(r"slot-mp80[a-z0-9]{4}-[a-z0-9]{4}", text))
    expected = set(GROUND_TRUTH.values())
    
    if found_slots == expected:
        print(f"  PASS: {fname}")
    elif found_slots == set():
        print(f"  OK (no slots): {fname}")
    else:
        extra = found_slots - expected
        missing = expected - found_slots
        if extra:
            print(f"  FAIL: {fname} has OUTDATED slots: {extra}")
        if missing:
            print(f"  FAIL: {fname} MISSING slots: {missing}")
        all_pass = False

if all_pass:
    print("\n  ALL FILES CONSISTENT — slot IDs match live DEFAULT.md")
else:
    print("\n  INCONSISTENCY DETECTED — fix before proceeding")
```

---

# PART IV: PROCESS ENHANCEMENTS — NEW MANDATORY PROCEDURES

## IV.1 New Mandatory Check: Branch Rename Detection (§0.2 Enhancement)

Already covered in Part III Change 1. This adds the "branch was renamed by parallel process" detection to the pre-work checklist.

## IV.2 New Mandatory Check: File-Existence Audit at Session Start

Add to §0.1.5 (Project Documentation Verification), after step 4:

```
5. **File-existence audit (CPL L21):** Run a Python script that scans all 7 documentation files for file references (paths matching project file patterns) and verifies each with `os.path.exists()`. Flag any stale references. Update documentation files that reference deleted files BEFORE beginning work.
```

Python verification script to add to the project template:
```python
import os, re

project_dir = os.getcwd()
doc_files = ["README.md", "PROJECT STATE.md", "SPRINT.md", "CHANGELOG.md", 
             "BACKLOG.md", "LEARNINGS.md", "DECISIONS.md"]

stale_refs = []
for doc in doc_files:
    path = os.path.join(project_dir, doc)
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    # Find potential file references (markdown links, bare paths, versioned filenames)
    refs = re.findall(r'(?:\.\/|(?:\d+\.\d+(?:\.\d+)?\.\w+))', text)
    for ref in refs:
        full = os.path.join(project_dir, ref)
        if not os.path.exists(full):
            stale_refs.append((doc, ref))

if stale_refs:
    print(f"STALE FILE REFERENCES ({len(stale_refs)}):")
    for doc, ref in stale_refs:
        print(f"  {doc} → {ref} (MISSING)")
else:
    print("All file references verified — no stale links.")
```

## IV.3 New Mandatory Check: Pre-Commit Branch Name Verification

Add to §9.3 Post-Work Git Checklist, between steps 4 and 5:

```
4b. **Verify branch name consistency (CPL L19):** Compare current branch name against the branch recorded in PROJECT STATE.md. If they differ: (a) check `git reflog` to confirm rename is benign, (b) update PROJECT STATE.md with new name, (c) note in CHANGELOG.md. Do NOT create yet another branch to "fix" the name.
```

## IV.4 New Section: Reader Testing Protocol (After §11 Publication Standards)

Add a new section to DEFAULT.md:

```
## 11.5 Reader Testing Protocol (Mandatory for Publication Documents)

Before ANY document is declared publication-ready, it MUST pass blind reader testing.

### Protocol

1. **Prepare:** Supply the FULL document text inline to a REVIEWER subagent or fresh LLM session. Provide ZERO context about the project, the author's intent, or prior versions.

2. **Reader questions (minimum 5):**
   - "What genre is this document?" (Tests genre clarity)
   - "What is the single most confusing sentence or paragraph?" (Tests clarity)
   - "What seems to be missing that a reader would expect?" (Tests completeness)
   - "Are there any claims that seem unsupported or contradictory?" (Tests evidence)
   - "If you had to summarize this in 3 sentences, what would you say?" (Tests thesis clarity)

3. **Severity classification:**
   - `[BLOCKING]` — Reader fundamentally misunderstands the thesis. Do not publish.
   - `[MAJOR]` — Reader caught a contradiction, missing section, or unclear claim. Fix before publishing.
   - `[MINOR]` — Reader flagged jargon, ambiguous phrasing, or style issues. Fix before publishing.
   - `[SUGGESTION]` — Reader offered improvement ideas. Optional.

4. **Two-round minimum (CPL L27):** First round catches surface problems (jargon, confusing sentences). Second round (after fixes applied) catches structural problems (logical gaps, missing context). Plan for at least 2 rounds.

5. **Document results:** Reader test feedback and fixes applied must be documented in CHANGELOG.md and, for publication documents, in a "Reader Testing" appendix.

### Pre-Publication Gate

No document proceeds to release (§11.4) until:
- [x] At least one round of blind reader testing completed
- [x] All `[BLOCKING]` and `[MAJOR]` issues resolved
- [x] Reader testing results documented in CHANGELOG.md
```

## IV.5 New Section: Multi-Project Synthesis Audit (After the Reader Testing Protocol)

```
## 11.6 Multi-Project Synthesis Audit (For Convergence/Consilience Claims)

When a document claims that multiple projects independently converge on a common finding, framework, or vocabulary, a mandatory audit is required BEFORE the claim is published.

### Audit Steps

1. **Source Document Vocabulary Audit (CPL L22):** For each claimed convergence, search the original source documents for the unifying term or concept. If the term appears ONLY in the synthesis document and NOT in the source projects, the convergence is a framing choice, not a discovery. Flag as `[IMPOSED-SYNTHESIS]`.

2. **Definition Equivalence Check (CPL L23):** For each term claimed as convergent, verify that the DEFINITION in each source document matches. Shared name ≠ shared structure. If Project A uses "cross-ratio" as a statistical ratio and Project B uses it as a projective invariant, they are NOT convergent despite sharing vocabulary. Flag as `[EQUIVOCATION]`.

3. **Salvage Protocol (CPL L24):** If the central convergence claim fails the vocabulary audit: (a) do not abandon the project, (b) audit source documents for what GENUINELY overlaps, (c) rebuild the synthesis around the actual convergence signal, (d) label the original over-claim honestly, (e) a smaller true claim beats a grand false one.

4. **Terminology Shift Documentation (CPL L35):** If the synthesis introduces terminology that differs from prior releases, include an explicit "Note on Terminology" section explaining the relationship between old and new language.

### Documentation

The audit results must be included in the synthesis document (as a methodology section or appendix) and in DECISIONS.md.
```

---

# PART V: SELF-LEARNING/AUDIT PROTOCOL — PERIODIC SYSTEM HEALTH CHECK

## V.1 Purpose

This protocol enables the system to audit itself periodically — checking for git contamination, documentation drift, prompt consistency, and cross-project lesson accumulation. It can be triggered by the user with a single command or run autonomously during low-activity periods.

## V.2 Trigger

User command: **"RUN SYSTEM AUDIT"** or **"SYSTEM HEALTH CHECK"**

Alternatively, the agent should SUGGEST running the audit when:
- A project is archived and the session count exceeds 5 since last audit
- A new cross-project lesson is discovered (trigger full audit to check for other uncollected lessons)
- System prompts are modified (trigger slot ID consistency check)

## V.3 Audit Checklist

```
SYSTEM HEALTH AUDIT — [YYYY-MM-DD]

PART A: GIT CONTAMINATION CHECK
[ ] A1. Test-Path "G:\My Drive\projects\.git" → should be FALSE
[ ] A2. Test-Path "G:\My Drive\projects\_shared\.git" → should be FALSE
[ ] A3. Get-ChildItem "G:\My Drive\projects" -Recurse -Directory -Filter ".git" -Depth 2 → should return NOTHING
[ ] A4. Each project in Archive has its own .git/ (only if actively working from Archive)

PART B: PROMPT CONSISTENCY CHECK
[ ] B1. DEFAULT.md slot IDs match live tool definitions (run Python comparison script)
[ ] B2. ARCHITECTURE.md slot IDs match DEFAULT.md
[ ] B3. AGENT-CONFIG.md slot IDs match DEFAULT.md
[ ] B4. ARCHITECTURE.md version ≤ DEFAULT.md version (architecture should not claim newer version than the prompt it documents)
[ ] B5. All slot IDs referenced in ARCHITECTURE.md exist in DEFAULT.md's subagent_orchestrator tool definition

PART C: DOCUMENTATION DRIFT CHECK
[ ] C1. CROSS-PROJECT-LEARNINGS.md exists and is non-empty
[ ] C2. CROSS-PROJECT-LEARNINGS.md lesson count matches expected (currently 30: L1-L8 + L13-L18 + L19-L40)
[ ] C3. No archived project LEARNINGS.md files contain uncollected Cross-Project: YES lessons

PART D: ARCHIVE INTEGRITY CHECK
[ ] D1. Archive\projects\ directory structure follows YYYY\MM convention
[ ] D2. No orphan files at G:\My Drive\projects\ root (only _shared\ should exist)
[ ] D3. Each archived project has 7 mandatory docs (or close-out note explaining absence)
[ ] D4. Obsidian\releases\ structure follows YYYY\MM convention
[ ] D5. Cross-reference: each release in Obsidian corresponds to an archived project

PART E: LESSON ACCUMULATION CHECK
[ ] E1. Scan all LEARNINGS.md in Archive\projects\YYYY\MM\ for lessons marked "Cross-Project: YES"
[ ] E2. Compare against CROSS-PROJECT-LEARNINGS.md — flag any uncollected lessons
[ ] E3. For each uncollected lesson: assess impact (HIGH/MEDIUM/LOW), propose addition

PART F: PROCESS IMPROVEMENT CHECK
[ ] F1. Review last 5 CHANGELOG.md entries for repeated failure patterns
[ ] F2. Check if any DEFAULT.md edge case handlers are missing for recent failures
[ ] F3. Review subagent slot tool availability (~35% assumption still holding?)
```

## V.4 Audit Execution Script

```python
# save as: G:\My Drive\prompts\system_audit.py
import os, re, subprocess
from datetime import datetime

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

print(f"=== SYSTEM HEALTH AUDIT — {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")

# PART A: Git Contamination
print("PART A: GIT CONTAMINATION CHECK")
parent_git = os.path.exists(r"G:\My Drive\projects\.git")
print(f"  A1. Parent .git exists: {parent_git} {'⚠️ FAIL' if parent_git else '✅ PASS'}")
shared_git = os.path.exists(r"G:\My Drive\projects\_shared\.git")
print(f"  A2. _shared .git exists: {shared_git} {'⚠️ FAIL' if shared_git else '✅ PASS'}")

# PART B: Prompt Consistency
print("\nPART B: PROMPT CONSISTENCY CHECK")
prompts_dir = r"G:\My Drive\prompts"
files = {}
for fname in ["DEFAULT.md", "ARCHITECTURE.md", "AGENT-CONFIG.md"]:
    fpath = os.path.join(prompts_dir, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            files[fname] = f.read()

if "DEFAULT.md" in files:
    d_slots = set(re.findall(r"slot-mp80[a-z0-9]{4}-[a-z0-9]{4}", files["DEFAULT.md"]))
    # Ground truth from live tool definitions
    gt_slots = {"slot-mp80a5ry-e7hn", "slot-mp80ay3u-yzqo", "slot-mp80b6bl-iix2"}
    if d_slots == gt_slots:
        print(f"  B1. DEFAULT.md slots match ground truth: ✅ PASS")
    else:
        print(f"  B1. DEFAULT.md slots: {d_slots} vs expected {gt_slots} ⚠️ FAIL")

for fname in ["ARCHITECTURE.md", "AGENT-CONFIG.md"]:
    if fname in files:
        f_slots = set(re.findall(r"slot-mp80[a-z0-9]{4}-[a-z0-9]{4}", files[fname]))
        if f_slots == gt_slots:
            print(f"  B2/B3. {fname} slots match DEFAULT.md: ✅ PASS")
        elif f_slots == set():
            print(f"  B2/B3. {fname} has no slot IDs (may use 'self'): ⚠️ CHECK")
        else:
            print(f"  B2/B3. {fname} MISMATCH: {f_slots} vs {gt_slots} ⚠️ FAIL")

# PART C: Documentation Drift
print("\nPART C: DOCUMENTATION DRIFT CHECK")
cpl_path = r"G:\My Drive\projects\_shared\CROSS-PROJECT-LEARNINGS.md"
if os.path.exists(cpl_path):
    with open(cpl_path, "r", encoding="utf-8") as f:
        cpl = f.read()
    lesson_count = len(re.findall(r"^### L\d+:", cpl, re.MULTILINE))
    print(f"  C1/C2. CPL lessons: {lesson_count} (expected 30) {'✅ PASS' if lesson_count >= 30 else '⚠️ CHECK'}")
else:
    print(f"  C1. CROSS-PROJECT-LEARNINGS.md MISSING ⚠️ FAIL")

# PART D: Archive Integrity
print("\nPART D: ARCHIVE INTEGRITY CHECK")
projects_root = r"G:\My Drive\projects"
orphans = [f for f in os.listdir(projects_root) 
           if f not in ["_shared", ".git", "__pycache__"] 
           and os.path.isfile(os.path.join(projects_root, f))]
if orphans:
    print(f"  D2. Orphan files at projects root: {orphans} ⚠️ FAIL")
else:
    print(f"  D2. No orphan files at projects root: ✅ PASS")

# Count releases
releases_dir = r"G:\My Drive\Obsidian\releases"
if os.path.exists(releases_dir):
    release_count = 0
    for root, dirs, files in os.walk(releases_dir):
        release_count += len([f for f in files if f.endswith('.md')])
    print(f"  D4/D5. Release documents: {release_count} ✅")

print(f"\n=== AUDIT COMPLETE ===")
```

## V.5 Integration with Project Lifecycle

The self-audit should be integrated into the project lifecycle at these gates:

| Gate | Trigger | Audit Scope |
|:-----|:--------|:------------|
| **P0 Initiation** | New project created | Parts A, B (ensure clean starting state) |
| **P5 Close-Out** | Project archived | Parts A, C, D, E (ensure lessons collected, archive intact) |
| **Periodic** | Every 5 sessions or user command "SYSTEM HEALTH CHECK" | All parts A-F |
| **Post-Prompt-Edit** | DEFAULT.md or ARCHITECTURE.md modified | Parts B (slot ID consistency) |

## V.6 Self-Improvement Loop

After each audit:
1. Document findings in a dated audit report saved to `G:\My Drive\prompts\audit-reports\YYYY-MM-DD.md`
2. If new cross-project lessons found: propose addition to CROSS-PROJECT-LEARNINGS.md
3. If prompt inconsistencies found: generate fix specification (like this document)
4. If process gaps found: propose DEFAULT.md enhancement (like Part IV of this document)
5. Track audit history to measure improvement over time

---

# EXECUTION ORDER SUMMARY

```
1. PART I: Cleanup root .git (needs user confirmation)
2. PART II: Update CROSS-PROJECT-LEARNINGS.md with 22 new lessons
3. PART III.1: Fix ARCHITECTURE.md slot IDs
4. PART III.2: Fix AGENT-CONFIG.md slot IDs
5. PART III.3: Update DEFAULT.md (5 changes + version bump)
6. PART IV: Add Reader Testing Protocol + Synthesis Audit to DEFAULT.md
7. PART V: Save system_audit.py script to prompts directory
8. Run PART III.4 verification script — all files must pass
9. Commit all changes on feature branch
10. Report completion to user
```

---

*SYSTEM-AUDIT-IMPLEMENTATION-SPEC v1.0 — generated 2026-05-18 from comprehensive projects-directory audit. Covers: root .git remediation, 22 new cross-project lessons (L19-L40), system prompt slot ID sync, new mandatory procedures (reader testing, synthesis audit), and self-learning audit protocol.*
