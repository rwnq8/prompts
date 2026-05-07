# prompts/ — DeepSeek System Prompt Library

## Active Files (8)

| File | Size | Purpose |
|:-----|:-----|:--------|
| `DEFAULT.md` | 16 KB | **Daily driver** — brainstorming, research, writing (v1.1-NO-WEB-SEARCH) |
| `META-PROMPT-DEEPSEEK.md` | 8 KB | **Tier 1 compiler** — creates & audits system prompts (v3.1-NO-WEB-SEARCH) |
| `README.md` | — | This file |
| `scholar/STAGE-1-SETUP.md` | 13 KB | OMEGA-SCHOLAR Stage 1: Context + Search Manifest + Blueprint |
| `scholar/STAGE-2-DRAFT.md` | 9 KB | Stage 2: Python-only evidence + narrative |
| `scholar/STAGE-3-REVIEW.md` | 9 KB | Stage 3: File-backed audit + anti-fabrication |
| `scholar/STAGE-4-PUBLISH.md` | 7 KB | Stage 4: Final assembly with source labels |

## Key Constraints

- **NO Web Search** in DeepChat — MCP/skills not enabled
- **Python is the ONLY source of quantitative truth** (Article V: Anti-Fabrication Mandate)
- **All citations must be file-backed** (`[EXTERNAL-SOURCE: filename]`)
- **All claims labeled**: `[LLM-INFERRED]`, `[EXTERNAL-SOURCE]`, or `[CODE-EXECUTED]`
- **Search Manifest Protocol** — when external search needed, agent outputs queries for external execution

## DeepChat Settings

- **Active system prompt**: DEFAULT-DEEPSEEK (v1.1-NO-WEB-SEARCH)
- **Available prompts**: DEFAULT, META-PROMPT (in system_prompts.json)
- **Templates**: 6 total (DEFAULT + META-PROMPT + 4 OMEGA-SCHOLAR stages)
- **Default for all agents**: DEFAULT-DEEPSEEK v1.1

## Archives

All deprecated/specialized content at `G:\My Drive\Archive\prompts\`

## Git

Branch: `main`. Full audit trail. Pushed to GitHub.
