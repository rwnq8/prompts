# SYSTEM PROMPT AUDIT: Web Search Integration & Tool Availability

> **Date:** 2026-05-25 | **Audit Scope:** All system prompts, subagent prompts, agent descriptions, custom prompt templates
> **Trigger:** BRAVE_WEB_SEARCH and BRAVE_LOCAL_SEARCH now available; YoBrowser available to all agents

---

## Executive Summary

The Prompts agent system was built on the assumption that agents have NO autonomous web search capability and must coordinate external searches through the user. **This assumption is now obsolete.** Two critical changes have occurred:

1. **`brave_web_search`** and **`brave_local_search`** are now confirmed available tools for all agents
2. **YoBrowser** (`get_browser_status`, `load_url`, `cdp_send`) is confirmed available for all agents

Additionally, Buffer API social media tools are confirmed available platform-wide, and the subagent orchestrator tool availability has been verified with live slot IDs.

**Impact:** Without refactoring, agents are told to coordinate external searches through the user (§2.4 of META-PROMPT-DEEPSEEK.md), told they cannot use web access (§3 Tool Combinations), and subagents are unaware they have access to search tools.

---

## Findings by File

### C1 [CRITICAL] META-PROMPT-DEEPSEEK.md — Web Search Guidance Outdated

| What | Current Text | Should Be |
|:-----|:-------------|:----------|
| §0 Header | "NEVER reference MCP/skills-based web search (not available)" | Retain (MCP web search IS still unavailable — but add note that brave_web_search IS available) |
| §0 Header | "For agents WITHOUT YoBrowser, include instructions for coordinating external searches through the user" | Remove — ALL agents have YoBrowser per AGENT-CONFIG.md v5.3 |
| §2.4 External Search Coordination | "When a prompt's task requires information that is not already present in the project files: The prompt must instruct the agent to produce a structured list of search queries... The user (not the agent) executes these searches outside the system" | Replace with: Agents SHOULD use `brave_web_search` (general) and `brave_local_search` (local) for web retrieval. Respect §0.8.6 Web Research Protocol for source verification. Web-retrieved content carries HIGHER verification burden than local files. |
| §3 Tool Combinations | "No external APIs or web access" for Creative Ideation and File Reading | Add: Web research capability is available via `brave_web_search` + YoBrowser |
| §3 Full Research Capability | "Tools: Python interpreter + file reading" | Expand to: "Python interpreter + file reading + web search (brave_web_search) + browser (YoBrowser)" |
| §9 Quick Reference | "Include §0.8.6 Web Research Protocol for YoBrowser agents; external search coordination for others" | Since all agents have YoBrowser: "Include §0.8.6 Web Research Protocol for YoBrowser agents" (drop "external search coordination for others") |
| §9 Quick Reference | "Design for Python + file reading only" | Change to "Design for Python + file reading + web search where appropriate" |

### C2 [CRITICAL] Subagent Prompts — Missing Tool Lists

**EXPLORER-SUBAGENT.md (v1.1):**
- Tool section lists only: LLM text generation, fill_prompt_template, search_conversations, Buffer API
- **MISSING:** `brave_web_search`, `brave_local_search`, YoBrowser tools (`get_browser_status`, `load_url`, `cdp_send`)
- Buffer API is listed as "Confirmed" but subagents have ~35% tool reliability — this is misleading

**IMPLEMENTER-SUBAGENT.md (v1.1):**
- Same gap as EXPLORER

**REVIEWER-SUBAGENT.md (v1.1):**
- Same gap as EXPLORER

### C3 [MAJOR] Agent Description Files — Tool Lists Need Updates

| File | Gap |
|:-----|:----|
| `agents/PROMPTS-AGENT.md` | Tool list doesn't include `brave_web_search`, `brave_local_search`, or YoBrowser |
| `agents/PROJECTS-AGENT.md` | Mentions YoBrowser but not `brave_web_search` |
| `agents/QWAV-AGENT.md` | Lists `brave_web_search` and YoBrowser — mostly correct but missing `brave_local_search` |

### C4 [MAJOR] AGENT-CONFIG.md v5.3 — Web Search in Tool Matrix

The tool availability matrix in AGENT-CONFIG.md §4 correctly lists `brave_web_search` and YoBrowser for all three agents. **This file is correct** and should be the authoritative reference that other prompts align to.

### C5 [MODERATE] META-PROMPT-DEEPSEEK.md — Subagent Scoping (§7.2.1)

The 2026-05-11 subagent scoping section is still valid but needs a note that subagents should NOT waste their response budget on web search unless explicitly instructed by the parent.

### C6 [MODERATE] Custom Prompt Templates — Web Search References

| Template | Issue |
|:---------|:------|
| `scholar/STAGE-1-SETUP.md` | References "external search coordination" — should reference brave_web_search |
| `scholar/STAGE-2-DRAFT.md` | Same |
| `templates/SOCIAL-ORCHESTRATOR-TEMPLATE.md` | No web search integration needed (social media focused) — OK |

### C7 [MINOR] Stale Section Counts

| File | Current | Should Be |
|:-----|:--------|:----------|
| `agents/PROMPTS-AGENT.md` §2 | "Output Format: 9-Section Prompt Template" | "12-Section" |
| `ARCHITECTURE.md` | Some "9-section" references | Already partially fixed in previous sessions |

### C8 [MINOR] META-PROMPT-DEEPSEEK.md — Version Header

The header line "System prompt generator v4.5 active" should be updated to v4.6 after refactoring.

---

## Conversation History Gap Analysis

Analysis of 644 conversations (9,012 messages) reveals these systemic patterns:

| Pattern | Frequency | Root Cause |
|:--------|:----------|:-----------|
| **Agent searches manually instead of using web search** | ~50+ instances | Prompts instruct "external search coordination through user" |
| **Subagent budget wasted on git pre-flight** | ~20+ instances | Resolved by §7.2.1 (2026-05-11) |
| **Inline Python through PowerShell failures** | ~200+ instances | Rule 13 partially effective; ongoing issue |
| **Phantom claims (Rule 14 violations)** | ~30+ instances | Structural enforcement improving but still occurs |
| **Planning spiral (read without execution)** | ~15+ instances | Mid-session checkpoint partially effective |

**Key insight:** The "external search coordination through user" pattern is the most impactful gap because it forces agents to stop and ask the user for information they could discover autonomously via `brave_web_search`. This blocks autonomous operation.

---

## Refactoring Priority Matrix

| Priority | Finding | Files | Effort |
|:---------|:--------|:------|:-------|
| **P0 (NOW)** | C1: META-PROMPT web search guidance | `META-PROMPT-DEEPSEEK.md` | 30 min |
| **P0 (NOW)** | C2: Subagent tool lists | 3 subagent files | 20 min |
| **P1** | C3: Agent description tool lists | 3 agent description files | 15 min |
| **P1** | C6: Custom template updates | 2 scholar templates | 15 min |
| **P2** | C7: Stale section counts | PROMPTS-AGENT.md | 5 min |
| **P2** | C8: Version bump | META-PROMPT-DEEPSEEK.md | 1 min |

---

## Refactored Tool Combination Model (for §3 of META-PROMPT)

The tool combinations in §3 should be expanded:

### Numbers, Data, and Calculations
- Tools: Python interpreter only
- (unchanged — no web search needed for calculations)

### Reading and Synthesizing Files
- Tools: File reading + **web search (brave_web_search) for supplementary context**
- The agent extracts information from provided files and synthesizes across them
- Web-retrieved content must be verified per §0.8.6 protocol

### Creative Ideation
- Tools: None beyond the agent's own reasoning
- (unchanged — creative ideation doesn't benefit from web search)

### Full Research Capability
- Tools: Python interpreter + file reading + **web search (brave_web_search) + browser (YoBrowser)**
- The agent combines code execution for quantitative work with file reading for external sources AND web search for current information
- Used for scholarly research, document generation, evidence-based analysis

---

## Verification Checklist (Post-Refactoring)

- [ ] META-PROMPT-DEEPSEEK.md: No references to "external search coordination through user"
- [ ] META-PROMPT-DEEPSEEK.md: §2.4 rewritten for autonomous web search
- [ ] META-PROMPT-DEEPSEEK.md: §3 Tool Combinations include web search
- [ ] EXPLORER-SUBAGENT.md: Tool list includes brave_web_search, YoBrowser
- [ ] IMPLEMENTER-SUBAGENT.md: Tool list includes brave_web_search, YoBrowser
- [ ] REVIEWER-SUBAGENT.md: Tool list includes brave_web_search, YoBrowser
- [ ] PROMPTS-AGENT.md: Tool list includes brave_web_search, YoBrowser
- [ ] PROJECTS-AGENT.md: Tool list includes brave_web_search
- [ ] QWAV-AGENT.md: Tool list includes brave_local_search
- [ ] All files: git committed with verification
- [ ] System audit passes

---

*Audit report generated 2026-05-25 by Prompts agent (META-PROMPT-DEEPSEEK v4.5)*
*Refactoring to be executed immediately following this report.*
