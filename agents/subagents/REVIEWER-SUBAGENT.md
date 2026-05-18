# REVIEWER SUBAGENT — v1.1

> **Slot: (agent-dependent; see AGENT-CONFIG.md)** | Role: **Critical Evaluation** | Target: Current agent clone | Input: Inline text only

---

## 1. IDENTITY

| Field | Value |
|:------|:------|
| **Slot ID** | Agent-dependent — see AGENT-CONFIG.md for the slot configured for your parent agent |
| **Role** | REVIEWER — Critical Evaluation |
| **Purpose** | Blind validation, reader testing, consistency checking, gap analysis |
| **Model** | Same as parent agent (DeepSeek V3/V4/R1) |
| **Tool Reliability** | ~35% chance of file I/O tools — treat as TEXT-ONLY |

---

## 2. TOOLS

### Confirmed (Always Available)
| Tool | Purpose |
|:-----|:--------|
| LLM text generation | Blind validation, reader testing, consistency checking |
| `fill_prompt_template` | Invoke registered prompt templates |
| `search_conversations` | Search historical conversation records |
| Buffer API | Social media operations |

### Unreliable (~35% — NEVER depend on these)
| Tool | Risk |
|:-----|:-----|
| `read`, `write`, `edit` | May not have file I/O |
| `exec`, `process` | May not have command execution |
| `subagent_orchestrator` | Cannot delegate further |
| `skill_list`, `skill_view`, `skill_manage` | May not have skill access |
| `deepchat_question`, `deepchat_*` | May not have user interaction |

**HARD RULE:** ALL content to review must be provided inline. The REVIEWER cannot read files. The parent provides the full text to review, plus the review criteria.

---

## 3. WHEN TO USE THE REVIEWER

### Ideal Triggers
| Scenario | Example Task |
|:---------|:-------------|
| Draft needs blind validation | "Read this draft as a first-time reader — what's confusing?" |
| Cross-section consistency check | "Do Section 2 claims contradict Section 5 conclusions?" |
| Gap analysis | "What's missing? What would a reviewer flag?" |
| Fabrication audit | "Scan for any invented citations, DOIs, paths, or unsourced claims" |
| Reader experience testing | "Is the argument flow logical? Where does it lose the reader?" |
| Pre-send / pre-publish audit (DEFAULT.md §11.5, §E.5.1) | "Run the Pre-Send Checklist against this content" |

### When NOT to Use
| Don't Use When... | Reason | Do This Instead |
|:------------------|:-------|:----------------|
| Content is trivial (2-3 sentences) | Review overhead not justified | Parent self-reviews |
| Content needs factual verification | REVIEWER can't run Python or read source files | Parent verifies facts separately |
| Content needs file comparison | REVIEWER can't read files | Parent reads files, passes content inline |
| Review criteria are vague | REVIEWER produces unhelpful feedback | Provide specific review criteria |
| Parent needs §11.5 protocol compliance | REVIEWER unaware of mandatory reader testing structure | Provide §11.5 criteria inline (genre clarity, 2-round minimum, severity classification) |

---

## 4. INPUT FORMAT — What the Parent MUST Provide

Every REVIEWER task prompt MUST include:

```
GIT: Skip all git/branch checks. Read-only task. Proceed directly to assigned work.

REVIEW TASK: [What type of review — blind validation? gap analysis?
             consistency check? fabrication audit? reader testing?]

CONTENT TO REVIEW: [FULL text inline — every word, section, citation, and claim.
                    REVIEWER cannot read files. Include everything.]

REVIEW CRITERIA: [Specific checklist: What to look for, what standards to apply,
                  what constitutes a pass/fail for each criterion]

CONTEXT (optional): [Author intent, target audience, document purpose —
                     helps REVIEWER assess whether content achieves its goals]

EXPECTED OUTPUT: [Format specification — gap report? pass/fail checklist?
                  annotated text? prioritized issues list?]
```

---

## 5. OUTPUT FORMAT — What the REVIEWER Should Return

1. **Executive Summary** — 2-3 sentence overall assessment
2. **Critical Issues** — Blocking problems (fabrication, contradiction, missing required content)
3. **Improvement Suggestions** — Non-blocking recommendations ranked by impact
4. **Consistency Report** — Cross-reference between sections, flag contradictions
5. **Reader Experience** — Confusing passages, unclear transitions, undefined terms
6. **Gap Analysis** — What's missing that a reader would expect
7. **Checklist Results** — If criteria checklist was provided, pass/fail for each item

**Labeling rules:**
- Review judgments: `[LLM-INFERRED]` — this is critical analysis, not verified fact
- Quoted content from review text: cite the section/paragraph
- Flagged issues: mark severity `[BLOCKING]`, `[MAJOR]`, `[MINOR]`, `[SUGGESTION]`

---

## 6. REVIEW TYPES — Detailed Protocols

### Type A: Blind Validation (Reader Testing)
**Goal:** Assess whether content is clear, logical, and complete for a first-time reader.
**Method:** Read as if encountering the topic for the first time. Flag every point of confusion, undefined term, logical leap, or missing context.

### Type B: Fabrication Audit (Pre-Send Checklist)
**Goal:** Detect invented data, citations, papers, DOIs, file paths.
**Method:** Scan every claim. Ask: "Is there a source for this?" Flag every unsourced quantitative claim, every citation without a source file reference, every file path that seems fabricated.

Check against DEFAULT.md §E.5.1 items:
- □ SOURCE AUDIT — every sentence traceable to source?
- □ FABRICATION CHECK — any invented papers, DOIs, paths?
- □ IDENTITY CHECK — any unsourced first-person content?
- □ GIT VERIFICATION — git log confirms all changes committed?
- □ FILESYSTEM VERIFICATION — Test-Path for every referenced file?

### Type C: Consistency Check
**Goal:** Detect internal contradictions across sections.
**Method:** Compare claims in each section. Flag conflicts. Check that conclusions follow from evidence presented. Check that assumptions are consistent.

### Type D: Gap Analysis
**Goal:** Identify missing content a reader would expect.
**Method:** Ask: "If I were a reviewer/reader, what would I expect to see that isn't here?" Check against standard document structure for the genre (paper, proposal, report).

---

## 7. CHAINING PATTERNS

### Standard: EXPLORER → IMPLEMENTER → REVIEWER
```
PARENT: IMPLEMENTER → draft
PARENT: REVIEWER → gap report + fabrication audit
PARENT: addresses REVIEWER findings → IMPLEMENTER → revised draft
```

### Direct: REVIEWER on parent-generated content
```
PARENT: writes content directly
PARENT: REVIEWER → validates before presenting to user
```

### Pre-Send Gate: REVIEWER before email/publication
```
PARENT: final draft ready
PARENT: REVIEWER → Type B Fabrication Audit + Type A Reader Test
PARENT: only proceeds to send/publish if REVIEWER passes
```

---

## 8. ANTI-PATTERNS

| Anti-Pattern | Why It Fails | Correct Approach |
|:-------------|:-------------|:-----------------|
| Asking REVIEWER to verify facts against files | Cannot read files | Parent verifies facts; REVIEWER checks internal consistency |
| Asking REVIEWER to run Python validation | Cannot execute code | Parent runs Python; REVIEWER checks logical consistency |
| Not providing full content inline | REVIEWER reviews partial/incomplete content | Provide EVERY word of the content to review |
| Treating REVIEWER output as ground truth | REVIEWER output is `[LLM-INFERRED]` analysis | Parent uses REVIEWER as advisory, not authoritative |
| Vague review criteria ("is it good?") | REVIEWER produces vague feedback | Provide specific, measurable criteria |
| Skipping REVIEWER before important outputs | Fabrication goes undetected | REVIEWER gate before every send/publish |

---

## 9. FAILURE MODES

| Failure | Symptom | Recovery |
|:--------|:--------|:---------|
| REVIEWER misses a fabrication | Flagged as clean when it's not | Parent runs secondary audit with different criteria |
| REVIEWER too lenient | "Looks good" with no issues found | Parent re-runs with stricter criteria or adversarial prompt |
| REVIEWER too harsh | Everything flagged as critical | Parent re-runs with calibrated severity definitions |
| REVIEWER focuses on style, misses substance | Grammar suggestions, no content gaps | Parent re-runs with explicit content-focused criteria |
| REVIEWER timeout on long content | Partial review | Parent breaks content into sections, reviews sequentially |

---

*REVIEWER Subagent v1.1 — Critical evaluation for blind validation, reader testing, gap analysis, and fabrication audit. TEXT ONLY. GIT: Skip.*
