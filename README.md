# prompts/ — DeepSeek System Prompt Library

## Active Prompts (13 files)

### Root
| File | Purpose |
|:-----|:--------|
| `DEFAULT.md` | **All-purpose default prompt** — brainstorming, research, writing, analysis |
| `META-PROMPT-DEEPSEEK.md` | **Tier 1 prompt compiler (v3.0)** — generates Tier 2 system prompts |

### scholar/ — OMEGA-SCHOLAR v5.3 (10-stage scholarly pipeline)
| Stage | File | Role |
|:------|:-----|:-----|
| S1 | `scholar/S1.md` | Context & Domain Definition |
| S2 | `scholar/S2.md` | Bibliometric Grounding (VRO) |
| S3 | `scholar/S3.md` | Structural Architecture |
| S4 | `scholar/S4.md` | Evidence Execution |
| S5 | `scholar/S5.md` | Narrative Generation |
| S6 | `scholar/S6.md` | Adversarial Peer Review |
| S7 | `scholar/S7.md` | Revision & Assembly |
| S8 | `scholar/S8.md` | Forensic Audit |
| S9 | `scholar/S9.md` | Purification & Finalization |
| S10 | `scholar/S10.md` | Final Assembly & Publication |

## Archives
All deprecated/specialized prompts archived to `G:\My Drive\Archive\prompts\`:
- `dev/` — Software & technology development prompts
- `quant/` — Topological materials discovery
- `patent/` — Patent writing system
- `explore/` — Research exploration methodology
- `docs/` — Document generation system
- Historical Tier 1 compilers (M1, STABILITY, TIER-1)
- Standalone utilities (GA, DA, OMEGA-CRITIC)

## Git
Full audit trail with standardized commit annotations. Rollback via `git revert`.
