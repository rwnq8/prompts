# SYSTEM PROMPT SIZING GUIDE — v1.0

> **Why this exists:** Claude Code best practice: "Keep it concise. For each line, ask: 'Would removing this cause mistakes?' If not, cut it. Bloated CLAUDE.md files cause Claude to ignore your actual instructions!" DEFAULT.md currently exceeds this threshold severely.

---

## Size Benchmarks

| Size | Rating | Risk | Claude Code Guidance |
|:-----|:-------|:-----|:---------------------|
| < 5K chars | Optimal | None | "Keep it short and human-readable" |
| 5K-15K | Good | Low | Acceptable for complex domain-specific agents |
| 15K-30K | Concerning | Medium | "Bloated prompts cause Claude to ignore actual instructions" |
| 30K-100K | Problematic | High | Critical rules get lost; agent degrades as context fills |
| 100K+ | Extreme | Critical | DEEP RISK: core guardrails (Rule 13, Rule 14, Anti-Phantom) buried in noise |

## Current System Prompt Sizes

| File | Size | Rating | Risk |
|:-----|:-----|:-------|:-----|
| `DEFAULT.md` | ~177K chars (~45 pages) | 🔴 EXTREME | Critical guardrails buried; core rules lost in noise |
| `META-PROMPT-DEEPSEEK.md` | ~41K chars (~10 pages) | 🟡 Moderate | Acceptable for prompt engineering; needs periodic audit |
| `QWAV-DEFAULT.md` | ~35K chars (~9 pages) | 🟡 Moderate | Fork of DEFAULT.md; shares bloat concerns |

## DEFAULT.md Bloat Breakdown (~177K chars)

| Section | ~Chars | ~% | Extractable? |
|:--------|:-------|:----|:-------------|
| §0 Persistent Preferences + Config | ~8K | 4.5% | Some tool configs could be templates |
| §0.6.4 Templates (ALL `fill_prompt_template` reference docs) | ~53K | 30% | ✅ YES — move to `templates/REFERENCE.md` |
| §0.8 Due Diligence + Research Protocol | ~5K | 3% | Core — keep |
| §Delegation to Other Agents | ~2K | 1% | Core — keep |
| §9 Git Protocol (comprehensive) | ~8K | 4.5% | Some failure scenarios could be reference |
| §11 Publication Standards | ~4K | 2% | Core — keep |
| §E Email (Outlook COM automation) | ~25K | 14% | ✅ YES — move to `templates/EMAIL-REFERENCE.md` |
| §12 Close-Out + Social Media | ~5K | 3% | Core — keep |
| Templates body content | ~60K | 34% | ⚠️ Embedded template bodies |
| Core Rules + Verification | ~17K | 10% | Core — MUST KEEP |

## Extraction Priority

### P0 — Extract Now (30% reduction to ~124K)
1. **§0.6.4 Template Reference Documentation (~53K)** → `templates/REFERENCE.md`
   - All `fill_prompt_template` parameter tables and usage docs
   - Agent just needs: "Use `fill_prompt_template` for these templates: [list names]"
   - Full parameter docs in separate reference

2. **§E Email Outlook COM (~25K)** → `templates/EMAIL-REFERENCE.md`
   - All COM automation details, failure scenarios, recipient resolution
   - Agent just needs: "For email, use `fill_prompt_template('EMAIL-COMPOSER')`"
   - COM internals in separate reference

### P1 — Extract Next (additional 20% reduction to ~100K)
3. **Templates body content (~60K embedded)** → Reference files
   - Most template bodies are embedded inline; could be `fill_prompt_template` calls
   - Already have `templates/` directory for some

### What MUST Stay Inline (Core, Non-Negotiable)
- Rules 1-6, 12-14 (verbatim)
- §0.8 Due Diligence Protocol
- §Delegation to Other Agents (heuristics table)
- §9 Git Protocol (branch discipline, pre/post-work checklists, the Iron Rule)
- Publication Quality Gates
- Edge Cases and Recovery
- Source Labeling requirements

## CLAUDE.md Conflict

DEFAULT.md currently instructs setting CLAUDE.md to `"NO_CONTEXT"` — blanking it entirely. This contradicts Claude Code's best practice:
- "CLAUDE.md is a special file that Claude reads at the start of every conversation"
- "This gives Claude persistent context it can't infer from code alone"
- "The /init command analyzes your codebase to detect build systems, test frameworks, and code patterns"

**Resolution:** If the concern is that CLAUDE.md adds to context bloat, the fix is to make CLAUDE.md concise (as Claude Code recommends), not to blank it. A concise CLAUDE.md with project-specific commands and conventions is more effective than forcing the entire system prompt to carry that context.

---

*SYSTEM-PROMPT-SIZING.md v1.0 — Reference for prompt bloat management. See Claude Code docs: code.claude.com/docs/en/best-practices*
