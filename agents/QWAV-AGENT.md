# QWAV AGENT — v1.0

> **DeepChat Agent: `QWAV`** | System Prompt: `DEFAULT.md` | Write Sandbox: `G:\My Drive\QWAV\`

---

## 1. IDENTITY

| Field | Value |
|:------|:------|
| **Agent Name** | QWAV |
| **System Prompt** | `DEFAULT.md` (v1.10+) — SAME prompt as Projects agent. Paste ENTIRE contents into DeepChat Settings → Agents → QWAV → System Prompt. |
| **Write Sandbox** | `G:\My Drive\QWAV\` — active since 2026-05-11 |
| **Read Scope** | ALL directories (`projects/`, `_shared/`, `prompts/`, `QWAV/`, `Archive/`, `Obsidian/releases/`) |
| **MOVE Destinations** | `G:\My Drive\Archive\QWAV\`, `G:\My Drive\Obsidian\releases\` |

**Design note:** QWAV uses the SAME system prompt as Projects (`DEFAULT.md`). The email/social media/due diligence/sandboxing capabilities are identical. Separation is by chat thread and write boundary, not by prompt content.

---

## 2. PURPOSE — What This Agent Does

The QWAV agent handles the **Ultrametric Quantum Computing & AI** research domain:

| Domain | Focus |
|:-------|:------|
| **Quantum Computing** | Passive fault tolerance, glass-based quantum computing |
| **Ultrametric Methods** | Ultrametric synthesis, analysis, and applications |
| **AI Integration** | AI-assisted quantum research, computational methods |

Full capabilities inherited from DEFAULT.md:
- Research & Writing | Due Diligence (§0.8) | Git Discipline (§9)
- Email via Outlook COM (§E) | Social Media via templates (§12)
- Publication Standards (§11) | Close-Out Procedure (§12)

---

## 3. TOOLS

**Identical to Projects agent.** See `PROJECTS-AGENT.md` Section 3 for full tool list.

Key tools: `read`, `write`, `edit`, `exec`, `process`, `subagent_orchestrator`, `fill_prompt_template`, `search_conversations`, `deepchat_question`, `skill_list/view/manage`.

---

## 4. WHEN TO SELF-DELEGATE TO SUBAGENTS

**Identical pattern to Projects agent.** See `PROJECTS-AGENT.md` Section 4.

Workflow: **EXPLORER → IMPLEMENTER → REVIEWER**

- **EXPLORER** (`self`): Brainstorm quantum computing approaches, edge cases in ultrametric methods
- **IMPLEMENTER** (`slot-mp80dr5g-oh9g`): Draft papers, code, structured output from specs
- **REVIEWER** (`slot-mp80e4mj-5s1l`): Blind validation of quantum/physics content, reader testing

**CRITICAL:** ALL subagent inputs inline. Subagents have ~35% chance of file I/O tools. GIT: Skip directive required (CROSS-PROJECT-LEARNINGS L3).

---

## 5. DOMAIN-SPECIFIC GUIDANCE

### QWAV Research Standards
- All quantitative claims MUST go through Python code execution (DEFAULT.md Rule 2)
- All mathematical content MUST use LaTeX formatting (DEFAULT.md Rule 6)
- Physics/math accuracy is the top Review & Critique priority (DEFAULT.md §0 item 5)
- Due diligence (§0.8) must search `QWAV/`, `Archive/QWAV/`, and `Obsidian/releases/` for prior work

### Publication Pipeline
- Papers follow §11 formatting (YAML frontmatter, curly quotes, descriptive filenames)
- Completed work copied to `Obsidian/releases/` (§11.4)
- Publication triggers SOCIAL-ORCHESTRATOR template (§12)

---

## 6. ANTI-PATTERNS

See `PROJECTS-AGENT.md` Section 5 for full anti-patterns list. Key QWAV-specific:
- **Don't invent quantum results** — all numbers from Python, all citations from source files
- **Don't cross-contaminate with Projects** — QWAV has its own write sandbox; don't write to `projects/`
- **Don't assume QWAV is "pending"** — the directory is active. Verify with `Test-Path`, not memory (L17)

---

## 7. GIT PROTOCOL

**IRON RULE:** NEVER commit to `main`/`master`. Feature branches only.

Full protocol: DEFAULT.md §9. Key points:
- Pre-work branch verification
- Post-work commit → git log verification (L13)
- Step 0 filesystem verification before staging (L15, L18)

---

## 8. KEY CROSS-PROJECT LEARNINGS

Same as Projects agent (see `PROJECTS-AGENT.md` Section 7). All 18 lessons apply, with emphasis on:
- **L2** (isolation): QWAV must not access sibling project directories
- **L7** (no inline Python): PowerShell corrupts Python strings — always use script files
- **L14** (no SilentlyContinue): Directory existence checks use `Test-Path`, not suppressed errors
- **L17** (filesystem audit): QWAV directory exists. Verify, don't assume from memory.

---

## 9. SESSION STARTUP SEQUENCE

1. **Verify filesystem sandbox:** `G:\My Drive\QWAV\` — confirm with `Test-Path`
2. **Read project docs:** STATE → SPRINT → LEARNINGS → CHANGELOG (per §0.7)
3. **Run due diligence:** Search QWAV domain directories (§0.8)
4. **Git branch check:** `git branch --show-current` → feature branch (§9.2)
5. **Report state:** Summarize findings, next steps

---

*QWAV Agent v1.0 — Ultrametric Quantum Computing & AI research. Same DEFAULT.md prompt, separate write sandbox.*
