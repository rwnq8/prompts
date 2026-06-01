# Handoff: Physics Writing Style Integration ("No Bullshit")

**Type:** Session→Session
**Date:** 2026-06-01
**Issuing Authority:** META-PROMPT v5.3 (System Prompt Generator)
**Accepting Authority:** Next META-PROMPT session / Projects agent / QWAV agent

## Scope

### Included
- Integrated 18-rule physics writing style guide ("No Bullshit Allowed — Expanded Edition") into existing prompt infrastructure
- Expanded DEFAULT.md §0.0 Research Integrity Mandate with: Banned Words (operationally defined), Certainty Calibration (6 labels), Falsifiability Requirement, Postdiction Prevention, Philosophy Boundary, Attribution Standards
- Expanded DEFAULT.md §7.1 Publication Language Gate with 18-point Physics Writing Standards checklist
- Mirrored §0.0 changes to QWAV-DEFAULT.md §0.5
- Updated META-PROMPT-DEEPSEEK.md §0 template section — all future generated prompts now include expanded rules
- Created PHYSICS-STYLE.md template (injectable 18-rule checklist with self-check and before/after examples)
- Updated template-catalog SKILL.md (count 18→20, added PHYSICS-STYLE row)
- Updated subagent reference docs (EXPLORER, IMPLEMENTER, REVIEWER) with condensed Research Integrity expansion
- Deployed all changes to DeepChat runtime via `tools/deploy.py`

### Excluded
- Did NOT create standalone skill (rules are baked into prompts, not a separate workflow)
- Did NOT update ACP agent slot configurations (platform-managed, not file-based)
- Did NOT modify any project files outside `G:\My Drive\prompts\`

## Files Modified

| File | Version | Changes |
|:-----|:--------|:--------|
| DEFAULT.md | v3.10→v3.11 | §0.0 + §7.1 expanded |
| QWAV-DEFAULT.md | v3.9→v3.10 | §0.5 mirrored |
| META-PROMPT-DEEPSEEK.md | v5.2→v5.3 | §0 template expanded |
| skills/template-catalog/SKILL.md | v1.1 | Count + PHYSICS-STYLE row |
| agents/subagents/EXPLORER-SUBAGENT.md | — | Condensed RI expansion |
| agents/subagents/IMPLEMENTER-SUBAGENT.md | — | Condensed RI expansion |
| agents/subagents/REVIEWER-SUBAGENT.md | — | Condensed RI expansion |

## Files Created

| File | Version | Purpose |
|:-----|:--------|:--------|
| templates/PHYSICS-STYLE.md | v1.0 | Injectable 18-rule style checklist |

## Commits

| Hash | Description |
|:-----|:-----------|
| `0f86590` | Main integration: DEFAULT, QWAV, META-PROMPT, PHYSICS-STYLE template |
| `c6e69cf` | Gap close: template-catalog, subagent docs |

## Architecture Decisions

1. **Rules 1-6 (truth/integrity) → Research Integrity Mandate (§0.0):** Banned words, certainty labels, falsifiability, postdiction, philosophy boundary, attribution. These are universal — every agent inherits them.
2. **Rules 7-18 (style/craft) → Publication Language Gate (§7.1) + PHYSICS-STYLE template:** One claim per sentence, analogies, active voice, equations, numbers, structure. Enforced at publication time.
3. **Subagent condensation:** Subagents get a ~12-line condensed version (vs. ~50-line full expansion) to preserve response budget. All 6 certainty labels included.
4. **Template vs. skill:** Chose injectable template over dedicated skill — rules are already in DEFAULT.md, template provides the injection mechanism.
5. **No new files preference:** Modified 7 existing files, created 1 new file (PHYSICS-STYLE template).

## Deployment Status

| Asset | Status |
|:------|:------|
| DEFAULT.md (Projects agent) | Deployed (48K→56K chars) |
| META-PROMPT (Prompts agent) | Deployed (58K→59.7K chars) |
| QWAV-DEFAULT (QWAV agent) | Deployed (41K→43.7K chars) |
| PHYSICS-STYLE template | Installed in custom_prompts.json |
| template-catalog skill | Deployed |
| Git | Merged to main, pushed to origin |

## DeepChat Restart Required
System prompt changes require DeepChat restart to take effect. Templates and skills are available immediately.

## Incoming Agent — Next Steps

1. Restart DeepChat to activate updated system prompts
2. Test: ask any agent to write a physics paragraph — verify it uses certainty labels and avoids banned words
3. Test: `fill_prompt_template("PHYSICS-STYLE")` — verify 18-rule checklist injects
4. Watch for: agents flagging `[PHILOSOPHY]` and `[not yet falsifiable]` in their own output
5. Consider: adding `[established]` / `[speculative]` labels to existing QNFO publications retroactively
