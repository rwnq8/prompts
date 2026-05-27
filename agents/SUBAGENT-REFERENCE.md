# SUBAGENT REFERENCE — v1.0

> **Audience: Parent Agents Only** | Not loaded into subagent context | Source of truth for delegation decisions

This document contains the parent-facing content that was removed from subagent system prompts to reduce context bloat. Subagent files now contain only what the subagent needs to execute its task. Use this reference to decide when to delegate, how to chain subagents, and how to recover from failures.

---

## EXPLORER — Divergent Thinking

### When NOT to Use

| Don't Use When... | Reason | Do This Instead |
|:------------------|:-------|:----------------|
| Task is well-specified with clear output | Single-generation overhead not justified | Use IMPLEMENTER directly |
| Task requires file I/O | EXPLORER can't reliably read files | Parent reads files, passes content inline |
| Task requires Python execution | EXPLORER can't reliably execute code | Parent runs Python separately |
| Answer is a simple fact | Brainstorming overhead not justified | Answer directly |
| Parent hasn't done due diligence | EXPLORER lacks context for meaningful exploration | Complete due diligence first |
| Parent needs blind reader testing | EXPLORER generates alternatives, doesn't validate | Use REVIEWER |

### Chaining Patterns

| Pattern | Flow | When to Use |
|:--------|:-----|:------------|
| **Standard** | EXPLORER then IMPLEMENTER | Open-ended task needs alternatives then draft |
| **Parallel** | Multiple EXPLORERs on same task | Need diverse perspectives, then synthesize |
| **Standalone** | EXPLORER only | Idea generation only, no drafting needed |

### Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|:-------------|:-------------|:-----------------|
| Asking EXPLORER to read files | Unreliable file I/O | Parent reads, passes inline |
| Asking EXPLORER to run Python | Unreliable exec | Parent runs Python separately |
| Asking EXPLORER to commit to git | Unreliable exec | Parent handles all git |
| Not providing full context inline | EXPLORER operates in a vacuum | Include ALL relevant context |
| Using EXPLORER for simple yes/no | Overhead not justified | Answer directly |
| Expecting verified facts from EXPLORER | Output is [LLM-INFERRED] | Parent verifies any factual claims |

### Failure Modes and Recovery

| Failure | Symptom | Recovery |
|:--------|:--------|:---------|
| EXPLORER timeout | No response or partial | Parent re-runs with smaller scope |
| Too many alternatives (overwhelming) | 20+ undifferentiated options | Parent re-runs with tighter constraints |
| Too few alternatives (narrow) | 1-2 obvious options only | Parent re-runs with broader scope or "what's the craziest idea?" prompt |
| EXPLORER fabricates context | Claims reference files it can't read | Parent catches - EXPLORER can't read files |
| EXPLORER goes off-topic | Output unrelated to task | Parent re-runs with clearer task description |

---

## IMPLEMENTER — Convergent Execution

### When NOT to Use

| Don't Use When... | Reason | Do This Instead |
|:------------------|:-------|:----------------|
| Specifications are unclear or incomplete | IMPLEMENTER will guess/fabricate to fill gaps | Run EXPLORER first, then IMPLEMENTER |
| Task requires file I/O | IMPLEMENTER can't reliably write files | IMPLEMENTER returns text; parent writes to disk |
| Task requires Python execution | IMPLEMENTER can't reliably execute code | Parent runs Python separately |
| Task requires git operations | IMPLEMENTER can't reliably run git | Parent handles all git |
| Creative exploration is needed | IMPLEMENTER converges, doesn't diverge | Use EXPLORER |
| Output may exceed ~32K tokens (CPL L39) | Subagent output truncates mid-sentence | Parent splits task into sections using chain mode |

### Chaining Patterns

| Pattern | Flow | When to Use |
|:--------|:-----|:------------|
| **Standard** | EXPLORER then IMPLEMENTER | Alternatives selected then draft from best |
| **Direct** | IMPLEMENTER from known specs | Complete specs available, no exploration needed |
| **Iterative** | IMPLEMENTER then REVIEWER then IMPLEMENTER | Draft needs multiple revision passes |

### Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|:-------------|:-------------|:-----------------|
| Asking IMPLEMENTER to read source files | Unreliable file I/O | Parent reads files, passes content inline |
| Giving vague specs ("write a good paper") | IMPLEMENTER fabricates to fill gaps | Provide detailed specs, outline, source material |
| Asking IMPLEMENTER to execute code | Unreliable exec | Parent runs Python separately |
| Trusting IMPLEMENTER output as verified fact | Output is generated from provided input, not verified | Parent runs REVIEWER on output |
| Not labeling assumptions in specs | IMPLEMENTER treats guesses as facts | Be explicit about what's known vs assumed |
| Using IMPLEMENTER for open-ended exploration | Convergent, not divergent | Use EXPLORER |

### Failure Modes and Recovery

| Failure | Symptom | Recovery |
|:--------|:--------|:---------|
| IMPLEMENTER fabricates when specs insufficient | Made-up citations, invented data | Parent catches - tighten specs, re-run |
| IMPLEMENTER output too long/short | Wrong scope or detail level | Parent re-runs with explicit length/token target |
| IMPLEMENTER misses key points from source | Output incomplete | Parent re-runs with checklist of required points |
| IMPLEMENTER changes tone inconsistently | Mixed formal/informal voice | Parent provides explicit tone/style guide |
| IMPLEMENTER timeout on large task | Partial output | Parent breaks task into smaller chunks |

---

## REVIEWER — Critical Evaluation

### When NOT to Use

| Don't Use When... | Reason | Do This Instead |
|:------------------|:-------|:----------------|
| Content is trivial (2-3 sentences) | Review overhead not justified | Parent self-reviews |
| Content needs factual verification | REVIEWER can't run Python or read source files | Parent verifies facts separately |
| Content needs file comparison | REVIEWER can't read files | Parent reads files, passes content inline |
| Review criteria are vague | REVIEWER produces unhelpful feedback | Provide specific review criteria |
| Parent needs reader testing protocol compliance | REVIEWER unaware of mandatory structure | Provide protocol criteria inline |

### Chaining Patterns

| Pattern | Flow | When to Use |
|:--------|:-----|:------------|
| **Standard** | IMPLEMENTER then REVIEWER | Draft complete then blind validation |
| **Direct** | REVIEWER on parent content | Parent wrote content directly then validate before showing user |
| **Pre-Send Gate** | REVIEWER before email/publication | Final draft ready then must pass review before send |

### Anti-Patterns

| Anti-Pattern | Why It Fails | Correct Approach |
|:-------------|:-------------|:-----------------|
| Asking REVIEWER to verify facts against files | Cannot read files | Parent verifies facts; REVIEWER checks internal consistency |
| Asking REVIEWER to run Python validation | Cannot execute code | Parent runs Python; REVIEWER checks logical consistency |
| Not providing full content inline | REVIEWER reviews partial/incomplete content | Provide EVERY word of the content to review |
| Treating REVIEWER output as ground truth | REVIEWER output is [LLM-INFERRED] analysis | Parent uses REVIEWER as advisory, not authoritative |
| Vague review criteria ("is it good?") | REVIEWER produces vague feedback | Provide specific, measurable criteria |
| Skipping REVIEWER before important outputs | Fabrication goes undetected | REVIEWER gate before every send/publish |

### Failure Modes and Recovery

| Failure | Symptom | Recovery |
|:--------|:--------|:---------|
| REVIEWER misses a fabrication | Flagged as clean when it's not | Parent runs secondary audit with different criteria |
| REVIEWER too lenient | "Looks good" with no issues found | Parent re-runs with stricter criteria or adversarial prompt |
| REVIEWER too harsh | Everything flagged as critical | Parent re-runs with calibrated severity definitions |
| REVIEWER focuses on style, misses substance | Grammar suggestions, no content gaps | Parent re-runs with explicit content-focused criteria |
| REVIEWER timeout on long content | Partial review | Parent breaks content into sections, reviews sequentially |

---

*SUBAGENT-REFERENCE.md v1.0 — Parent-only delegation guide. Not loaded into subagent context.*
