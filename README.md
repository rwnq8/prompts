# prompts/ — DeepSeek System Prompt Library

## Active Files (11)

| File | Size | Purpose |
|:-----|:-----|:--------|
| `DEFAULT.md` | 16 KB | **Daily driver** — brainstorming, research, writing (v1.1-NO-WEB-SEARCH) |
| `META-PROMPT-DEEPSEEK.md` | 8 KB | **Tier 1 compiler** — creates & audits system prompts (v3.1-NO-WEB-SEARCH) |
| `README.md` | — | This file |
| `social/SOCIAL-ORCHESTRATOR-v2.0.md` | 35 KB | **SOCIAL Orchestrator** — 5-platform publication-to-social pipeline |
| `scholar/STAGE-1-SETUP.md` | 13 KB | OMEGA-SCHOLAR Stage 1: Context + Search Manifest + Blueprint |
| `scholar/STAGE-2-DRAFT.md` | 9 KB | Stage 2: Python-only evidence + narrative |
| `scholar/STAGE-3-REVIEW.md` | 9 KB | Stage 3: File-backed audit + anti-fabrication |
| `scholar/STAGE-4-PUBLISH.md` | 7 KB | Stage 4: Final assembly with source labels |
| `social/TWITTER-BLUESKY-v2.0.md` | 15 KB | Short-form microblogging specialist (Twitter/X + Bluesky) |
| `social/MASTODON-v2.0.md` | 16 KB | Mastodon specialist (hashtag-optimized fediverse posts) |
| `social/LINKEDIN-v2.0.md` | 22 KB | LinkedIn specialist (professional posts + longform articles) |
| `social/SUBSTACK-v2.0.md` | 22 KB | Substack specialist (newsletter + Notes promotion) |

## SOCIAL Pipeline (v2.0)

**Purpose:** Transform publication releases from `G:\My Drive\Obsidian\releases\` into platform-optimized social media content for 5 platforms.

**Architecture:** All social prompts consolidated in `social/` — 1 orchestrator + 4 platform-specific Tier 2 prompts.

```
social/
  |
  +-- SOCIAL-ORCHESTRATOR-v2.0.md      (Tier 1 — main entry point, dispatches to Tier 2)
  +-- TWITTER-BLUESKY-v2.0.md          (Tier 2 — Twitter/X + Bluesky)
  +-- MASTODON-v2.0.md                 (Tier 2 — Mastodon)
  +-- LINKEDIN-v2.0.md                 (Tier 2 — LinkedIn posts + articles)
  +-- SUBSTACK-v2.0.md                 (Tier 2 — Substack newsletter + Notes)
```

**Platform coverage:**
| Platform | Via | Content Types |
|:---------|:----|:--------------|
| X/Twitter | Buffer | Post (280 chars), reply tweet, thread |
| Mastodon | Buffer | Post (500+ chars), thread, hashtag-optimized |
| LinkedIn | Buffer | Feed post + article teaser |
| LinkedIn | Direct | Longform article (800-2000 words) |
| Bluesky | Direct | Post (300 chars), thread |
| Substack | Direct | Newsletter + Notes promotion |

**Output format:** Plain ASCII text only — no markdown tables, no special formatting. **Flowing paragraphs with no mid-paragraph line breaks.** Each paragraph is one continuous line; blank lines (`\n\n`) separate paragraphs for readability. Every Tier 2 prompt enforces `validate_paragraph_flow()` via Python to detect and fix mid-paragraph `\n`/`\r` characters (Section 10). Optimized for clean copy/paste into Buffer, Bluesky, Substack, and LinkedIn.

## Key Constraints

- **NO Web Search** in DeepChat — MCP/skills not enabled
- **Python is the ONLY source of quantitative truth** (Article V: Anti-Fabrication Mandate)
- **All citations must be file-backed** (`[EXTERNAL-SOURCE: filename]`)
- **All claims labeled**: `[LLM-INFERRED]`, `[EXTERNAL-SOURCE]`, or `[CODE-EXECUTED]`
- **Search Manifest Protocol** — when external search needed, agent outputs queries for external execution
- **NO MID-PARAGRAPH LINE BREAKS** — each paragraph flows as one continuous line; blank lines between paragraphs are fine (enforced by Python `validate_paragraph_flow()` in every Tier 2 prompt)

## DeepChat Settings

- **Active system prompt**: DEFAULT-DEEPSEEK (v1.1-NO-WEB-SEARCH)
- **Available prompts**: DEFAULT, META-PROMPT (in system_prompts.json)
- **Templates**: 10+ (DEFAULT + META-PROMPT + 4 OMEGA-SCHOLAR stages + 5 SOCIAL prompts in `social/`)
- **Default for all agents**: DEFAULT-DEEPSEEK v1.1

## Archives

All deprecated content (including old `SOCIAL-v1.0.md`) at `G:\My Drive\Archive\prompts\`

## Git

Branch: `feature/fix-social-media-line-breaks`. Full audit trail. Pushed to GitHub.
