# prompts/ — DeepSeek System Prompt Library

## Active Files (12)

| File | Size | Purpose |
|:-----|:-----|:--------|
| `DEFAULT.md` | 16 KB | **Daily driver** — brainstorming, research, writing (v1.1-NO-WEB-SEARCH) |
| `META-PROMPT-DEEPSEEK.md` | 8 KB | **Tier 1 compiler** — creates & audits system prompts (v3.1-NO-WEB-SEARCH) |
| `README.md` | — | This file |
| `SOCIAL-BROADCAST-v1.0.md` | 32 KB | Publication-to-social (v1.0) — deprecated, superseded by v2.0 orchestrator |
| `SOCIAL-BROADCAST-ORCHESTRATOR-v2.0.md` | 35 KB | **SOCIAL-BROADCAST Orchestrator** — 5-platform publication-to-social pipeline |
| `scholar/STAGE-1-SETUP.md` | 13 KB | OMEGA-SCHOLAR Stage 1: Context + Search Manifest + Blueprint |
| `scholar/STAGE-2-DRAFT.md` | 9 KB | Stage 2: Python-only evidence + narrative |
| `scholar/STAGE-3-REVIEW.md` | 9 KB | Stage 3: File-backed audit + anti-fabrication |
| `scholar/STAGE-4-PUBLISH.md` | 7 KB | Stage 4: Final assembly with source labels |
| `social-broadcast/TWITTER-BLUESKY-v2.0.md` | 15 KB | Short-form microblogging specialist (Twitter/X + Bluesky) |
| `social-broadcast/MASTODON-v2.0.md` | 16 KB | Mastodon specialist (hashtag-optimized fediverse posts) |
| `social-broadcast/LINKEDIN-v2.0.md` | 22 KB | LinkedIn specialist (professional posts + longform articles) |
| `social-broadcast/SUBSTACK-v2.0.md` | 22 KB | Substack specialist (newsletter + Notes promotion) |

## SOCIAL-BROADCAST Pipeline (v2.0)

**Purpose:** Transform publication releases from `G:\My Drive\Obsidian\releases\` into platform-optimized social media content for 5 platforms.

**Architecture:** Orchestrator + 4 platform-specific sub-prompts

```
SOCIAL-BROADCAST-ORCHESTRATOR-v2.0.md  (main entry point)
  |
  +-- social-broadcast/TWITTER-BLUESKY-v2.0.md  (Twitter/X + Bluesky)
  +-- social-broadcast/MASTODON-v2.0.md          (Mastodon)
  +-- social-broadcast/LINKEDIN-v2.0.md          (LinkedIn posts + articles)
  +-- social-broadcast/SUBSTACK-v2.0.md          (Substack newsletter + Notes)
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

**Output format:** Plain ASCII text only — no markdown tables, no special formatting. Optimized for direct copy/paste into Buffer, Bluesky, Substack, and LinkedIn.

## Key Constraints

- **NO Web Search** in DeepChat — MCP/skills not enabled
- **Python is the ONLY source of quantitative truth** (Article V: Anti-Fabrication Mandate)
- **All citations must be file-backed** (`[EXTERNAL-SOURCE: filename]`)
- **All claims labeled**: `[LLM-INFERRED]`, `[EXTERNAL-SOURCE]`, or `[CODE-EXECUTED]`
- **Search Manifest Protocol** — when external search needed, agent outputs queries for external execution

## DeepChat Settings

- **Active system prompt**: DEFAULT-DEEPSEEK (v1.1-NO-WEB-SEARCH)
- **Available prompts**: DEFAULT, META-PROMPT (in system_prompts.json)
- **Templates**: 10+ (DEFAULT + META-PROMPT + 4 OMEGA-SCHOLAR stages + 5 SOCIAL-BROADCAST prompts)
- **Default for all agents**: DEFAULT-DEEPSEEK v1.1

## Archives

All deprecated/specialized content at `G:\My Drive\Archive\prompts\`

## Git

Branch: `main`. Full audit trail. Pushed to GitHub.
