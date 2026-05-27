# AGENT-CONFIG.md — Agent Write Boundaries, Tool Lists, Slot IDs (v5.3)

> **Detailed per-agent configuration.** Referenced by META-PROMPT-DEEPSEEK.md §0 and README.md.
> Paired with ARCHITECTURE.md for complete system understanding.

---

## 1. Agent Inventory

| # | Agent | System Prompt | DeepChat Paste | Write Sandbox |
|:--|:------|:-------------|:---------------|:--------------|
| 1 | **Projects** | `DEFAULT.md` | Paste ENTIRE DEFAULT.md | `G:\My Drive\projects\<name>\` |
| 2 | **QWAV** | `QWAV-DEFAULT.md` | Paste ENTIRE QWAV-DEFAULT.md | `G:\My Drive\QWAV\` |
| 3 | **Prompts** | `META-PROMPT-DEEPSEEK.md` | Paste ENTIRE META-PROMPT | `G:\My Drive\prompts\` |

---

## 2. Tool Lists Per Agent

### 2.1 Projects Agent (DEFAULT.md)

**Core Tools (Always Available):**
| Tool | Purpose |
|:-----|:--------|
| `read` | Read any file (read-only scope all directories) |
| `write` | Write files within `G:\My Drive\projects\<name>\` |
| `edit` | Precise text replacement within sandbox |
| `exec` | PowerShell, Python, git, gh CLI |
| `process` | Manage background exec sessions |
| `deepchat_question` | User clarification/confirmation |
| `fill_prompt_template` | Invoke prompt templates |
| `subagent_orchestrator` | Delegate to EXPLORER/IMPLEMENTER/REVIEWER |
| `skill_list`, `skill_view`, `skill_manage` | Skill management |
| `search_messages`, `get_conversation_history` | Conversation search |
| `brave_web_search`, `brave_local_search` | Web search |
| `get_browser_status`, `load_url`, `cdp_send` | YoBrowser |

**Subagent Slots:**
| Role | Slot ID | Use |
|:-----|:--------|:----|
| EXPLORER | `self` | Divergent thinking, alternatives |
| IMPLEMENTER | `slot-mp80dr5g-oh9g` | Convergent drafting |
| REVIEWER | `slot-mp80e4mj-5s1l` | Blind validation |

**Buffer API (Platform-Level):**
| Tool | Purpose |
|:-----|:--------|
| `get_account`, `list_channels`, `get_channel` | Buffer org/channel management |
| `list_posts`, `get_post`, `create_post`, `edit_post`, `delete_post` | Social media post management |
| `create_idea` | Content idea creation |
| `introspect_schema`, `execute_query`, `execute_mutation` | GraphQL operations |

**LinkedIn (Platform-Level):**
| Tool | Purpose |
|:-----|:--------|
| `get_person_profile`, `search_people`, `get_my_profile` | LinkedIn profile/search |
| `get_company_profile`, `search_companies`, `get_company_employees` | Company research |
| `search_jobs`, `get_job_details` | Job search |
| `get_inbox`, `get_conversation`, `send_message` | LinkedIn messaging |
| `get_feed`, `get_sidebar_profiles`, `connect_with_person` | Feed and networking |

### 2.2 QWAV Agent (QWAV-DEFAULT.md)

Same core tools as Projects agent, with additional program-level GitHub operations:
- `gh issue list --label "program" --state open` — program-wide work
- `gh repo list qnfo --limit 50` — portfolio overview
- `gh project item-list` — QWAV Program Board management
- `gh issue create --repo qnfo/<repo>` — cross-repo issue creation

**Subagent slots:** Same as Projects agent.

### 2.3 Prompts Agent (META-PROMPT-DEEPSEEK.md)

Same core tools, write sandbox constrained to `G:\My Drive\prompts\`.
Read scope: `G:\My Drive\prompts\` + `G:\My Drive\projects\_shared\`.

**Subagent slots:** Same as Projects agent.

**Additional templates:** `list_all_prompt_template_names`, `get_prompt_template_parameters`.

---

## 3. Subagent Slot ID Registry

> **⚠️ SLOT IDs ARE AGENT-DEPENDENT.** Verify against live AGENT-CONFIG.md before pasting.

| Role | Typical Slot | Confirmed Slots |
|:-----|:-------------|:----------------|
| EXPLORER | `self` (auto-clone) | Verify in DeepChat settings |
| IMPLEMENTER | Varies per agent config | `slot-mp80dr5g-oh9g` (verified in session) |
| REVIEWER | Varies per agent config | `slot-mp80e4mj-5s1l` (verified in session) |

**To verify live slots:**
1. Open DeepChat → Settings → Agents → [Agent Name] → Subagents
2. Check the slot IDs listed under each configured subagent
3. Update this file if slots change

---

## 4. Write Boundary Enforcement

| Agent | Write Path Pattern | Violation Response |
|:------|:-------------------|:-------------------|
| Projects | Must start with `G:\My Drive\projects\` | `[ISOLATION-VIOLATION]` + STOP |
| QWAV | Must start with `G:\My Drive\QWAV\` | `[ISOLATION-VIOLATION]` + STOP |
| Prompts | Must start with `G:\My Drive\prompts\` | `[ISOLATION-VIOLATION]` + STOP |

---

## 5. GitHub Organization Default

| Setting | Value |
|:--------|:------|
| Default org | `qnfo` |
| Personal account | `rwnq8` (NEVER create repos here) |
| Required gh scopes | `repo, workflow, read:org, gist` |

---

## 6. Model Configuration

| Setting | Value |
|:--------|:------|
| Temperature | `0.0` |
| Top P | `1.0` |
| Frequency Penalty | `0.0` |
| Presence Penalty | `0.0` |

---

## 7. Version History

| Version | Date | Changes |
|:--------|:-----|:--------|
| v5.3 | 2026-05-27 | Initial creation — synthesized from META-PROMPT, README, and live session agent configs |
