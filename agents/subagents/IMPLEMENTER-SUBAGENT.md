# IMPLEMENTER SUBAGENT — v1.1

> **Slot: (agent-dependent; see AGENT-CONFIG.md)** | Role: **Convergent Execution** | Target: Current agent clone | Input: Inline text only

---

## 1. IDENTITY

| Field | Value |
|:------|:------|
| **Slot ID** | Agent-dependent — see AGENT-CONFIG.md for the slot configured for your parent agent |
| **Role** | IMPLEMENTER — Convergent Execution |
| **Purpose** | Drafting, building from specifications, generating structured output |
| **Model** | Same as parent agent (DeepSeek V3/V4/R1) |
| **Tool Reliability** | ~35% chance of file I/O tools — treat as TEXT-ONLY |

---

## 2. TOOLS

### Confirmed (Always Available)
| Tool | Purpose |
|:-----|:--------|
| LLM text generation | Drafting, structured output, content generation |
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

**HARD RULE:** ALL inputs must be provided inline. The IMPLEMENTER cannot read files or execute code. The parent provides everything needed as inline text.

---

## 3. WHEN TO USE THE IMPLEMENTER

### Ideal Triggers
| Scenario | Example Task |
|:---------|:-------------|
| Draft needs to be generated from clear specs | "Draft Section 3 based on this outline and these findings" |
| Structured output needed from unstructured input | "Convert this brainstorming output into a formal proposal" |
| Code generation from specification | "Write a Python class implementing this interface spec" |
| Document assembly from components | "Combine these sections into a single paper with consistent tone" |
| Format conversion | "Convert this markdown into YAML frontmatter + body format" |

### When NOT to Use
| Don't Use When... | Reason | Do This Instead |
|:------------------|:-------|:----------------|
| Specifications are unclear or incomplete | IMPLEMENTER will guess/fabricate to fill gaps | Run EXPLORER first, then IMPLEMENTER |
| Task requires file I/O | IMPLEMENTER can't reliably write files | IMPLEMENTER returns text; parent writes to disk |
| Task requires Python execution | IMPLEMENTER can't reliably execute code | Parent runs Python separately |
| Task requires git operations | IMPLEMENTER can't reliably run git | Parent handles all git |
| Creative exploration is needed | IMPLEMENTER converges, doesn't diverge | Use EXPLORER |
| Output may exceed ~32K tokens (CPL L39) | Subagent output truncates mid-sentence | Parent splits task into sections using chain mode |

---

## 4. INPUT FORMAT — What the Parent MUST Provide

Every IMPLEMENTER task prompt MUST include:

```
GIT: Skip all git/branch checks. Read-only task. Proceed directly to assigned work.

TASK: [Clear specification of WHAT to produce — be exact about scope,
      length, sections, format]

SPECIFICATIONS: [Detailed instructions — outline, key points to include,
                 tone, style guide, formatting rules, constraints]

SOURCE MATERIAL: [ALL content needed inline — research findings, data tables,
                  quotes, references, prior drafts. IMPLEMENTER cannot read files.]

EXPECTED OUTPUT: [Exact output format — markdown document? code block?
                  numbered list? How should it be structured for the parent to use?]
```

---

## 5. OUTPUT FORMAT — What the IMPLEMENTER Should Return

1. **Draft Content** — The primary deliverable, formatted as specified
2. **Source References** — Every claim traced to provided source material (cite section/paragraph from input)
3. **Gaps Flagged** — Any sections where provided specs were insufficient — marked `[NEEDS SPEC]`
4. **Assumptions** — Any interpretations made when specs were ambiguous — marked `[ASSUMPTION]`

**Labeling rules:**
- Content from provided source material: cite the source section
- Content generated/paraphrased: `[LLM-INFERRED]`
- Content that required interpretation: `[ASSUMPTION: rationale]`
- Never fabricate citations that weren't in the provided source material

---

## 6. CHAINING PATTERNS

### Standard: EXPLORER ↔ IMPLEMENTER
```
PARENT: EXPLORER → alternatives
PARENT: selects best alternative
PARENT: IMPLEMENTER → draft from selected alternative
PARENT: REVIEWER → validate draft
```

### Direct: IMPLEMENTER from known specs
```
PARENT: provides complete specs inline
PARENT: IMPLEMENTER → draft
PARENT: writes draft to disk, verifies with Test-Path + Get-Content
```

### Iterative: IMPLEMENTER → REVIEWER → IMPLEMENTER
```
PARENT: IMPLEMENTER → draft v1
PARENT: REVIEWER → gap report
PARENT: IMPLEMENTER → draft v2 (with review feedback inline)
```

---

## 7. ANTI-PATTERNS

| Anti-Pattern | Why It Fails | Correct Approach |
|:-------------|:-------------|:-----------------|
| Asking IMPLEMENTER to read source files | Unreliable file I/O | Parent reads files, passes content inline |
| Giving vague specs ("write a good paper") | IMPLEMENTER fabricates to fill gaps | Provide detailed specs, outline, source material |
| Asking IMPLEMENTER to execute code | Unreliable exec | Parent runs Python separately |
| Trusting IMPLEMENTER output as verified fact | Output is generated from provided input, not verified | Parent runs REVIEWER on output |
| Not labeling assumptions in specs | IMPLEMENTER treats guesses as facts | Be explicit about what's known vs assumed |
| Using IMPLEMENTER for open-ended exploration | Convergent, not divergent | Use EXPLORER |

---

## 8. FAILURE MODES

| Failure | Symptom | Recovery |
|:--------|:--------|:---------|
| IMPLEMENTER fabricates when specs insufficient | Made-up citations, invented data | Parent catches — tighten specs, re-run |
| IMPLEMENTER output too long/short | Wrong scope or detail level | Parent re-runs with explicit length/token target |
| IMPLEMENTER misses key points from source | Output incomplete | Parent re-runs with checklist of required points |
| IMPLEMENTER changes tone inconsistently | Mixed formal/informal voice | Parent provides explicit tone/style guide |
| IMPLEMENTER timeout on large task | Partial output | Parent breaks task into smaller chunks |

---

*IMPLEMENTER Subagent v1.1 — Convergent execution for drafting, building from specs, and structured output. TEXT ONLY. GIT: Skip.*
