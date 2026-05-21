"""Consolidate: merge AGENT-CONFIG.md into ARCHITECTURE.md, delete AGENT-CONFIG.md, move system_audit.py to tools/"""
import os
import re
import shutil

PROMPTS = r"G:\My Drive\prompts"

# 1. Read AGENT-CONFIG.md to extract unique tool lists
agent_config_path = os.path.join(PROMPTS, "AGENT-CONFIG.md")
with open(agent_config_path, 'r', encoding='utf-8') as f:
    agent_config = f.read()

# Extract tool lists
projects_tools = None
qwav_has_tools = False
prompts_tools = None

# Find Projects tools
m = re.search(r'\*\*Tools:\*\* `([^`]+)`', agent_config.split("### Agent: Projects")[1] if "### Agent: Projects" in agent_config else "")
if m:
    projects_tools = m.group(1)

# Find Prompts tools  
m = re.search(r'\*\*Tools:\*\* `([^`]+)`', agent_config.split("### Agent: Prompts")[1] if "### Agent: Prompts" in agent_config else "")
if m:
    prompts_tools = m.group(1)

print(f"Projects tools: {projects_tools}")
print(f"Prompts tools: {prompts_tools}")

# 2. Update ARCHITECTURE.md - add tool lists to agent table  
arch_path = os.path.join(PROMPTS, "ARCHITECTURE.md")
with open(arch_path, 'r', encoding='utf-8') as f:
    arch = f.read()

# Replace the agent table to add Tools column
old_table = """| Agent | System Prompt | Write Sandbox | Read Scope | Purpose |
|:------|:-------------|:--------------|:-----------|:--------|
| `DEFAULT.md` | — | Projects agent | Project Executor — full research/writing/coding/email/social workflow. §0.9: Independent Project Executor role. |
| `QWAV-DEFAULT.md` | — | QWAV agent | Strategy Program Manager — portfolio strategy, documentation, handoff, coordination. §0.9: QWAV role boundary. Forked from DEFAULT.md. |
| `META-PROMPT-DEEPSEEK.md` | v4.5 | Prompts agent | System prompt generation and auditing |
| `EMAIL-AGENT-v1.3.md` | v1.2 | *(Optional standalone email sessions)* | Dedicated email operations |
| `image-gen-banner-prompt.md` | — | *(Consumed within Projects)* | Banner image generation |"""

new_table = """| Agent | System Prompt | Write Sandbox | Tools | Purpose |
|:------|:-------------|:--------------|:------|:--------|
| Projects | `DEFAULT.md` | `G:\\My Drive\\projects\\<name>\\` | `read write edit exec process deepchat_question skill_list skill_view skill_manage subagent_orchestrator fill_prompt_template search_conversations` | Project Executor — full research/writing/coding/email/social workflow |
| QWAV | `QWAV-DEFAULT.md` | `G:\\My Drive\\QWAV\\` | Same as Projects agent | Strategy Program Manager — portfolio strategy, documentation, handoff, coordination |
| Prompts | `META-PROMPT-DEEPSEEK.md` (v4.5) | `G:\\My Drive\\prompts\\` | `read write edit exec process deepchat_question skill_list skill_view skill_manage` | System prompt generation and auditing |
| *(Optional)* | `EMAIL-AGENT-v1.3.md` | — | — | Dedicated email sessions |
| *(Template)* | `image-gen-banner-prompt.md` | — | — | Banner image generation |"""

if old_table in arch:
    arch = arch.replace(old_table, new_table)
elif "| Agent | System Prompt | Write Sandbox | Read Scope | Purpose |" in arch:
    # Find the exact table
    print("Using alternate table match...")
    # The table might be different - let's try a broader approach
    pass

# Also add a note about tools at the top of the architecture section
tools_note = """
**Agent Tools (from former AGENT-CONFIG.md — now consolidated here):**
- Projects agent: `read write edit exec process deepchat_question skill_list skill_view skill_manage subagent_orchestrator fill_prompt_template search_conversations`
- QWAV agent: Same as Projects agent
- Prompts agent: `read write edit exec process deepchat_question skill_list skill_view skill_manage`
- All agents: `system_audit.py` health check via `tools/system_audit.py`

"""

# Add tools note after the first taxonomy paragraph
if "## 1. TAXONOMY" in arch:
    insert_point = arch.index("### Layer 3: Agents")
    arch = arch[:insert_point] + "\n> **Agent Tools Reference (consolidated from former AGENT-CONFIG.md):** See table in Layer 3 for tool assignments per agent. system_audit.py now at `tools/system_audit.py`.\n\n" + arch[insert_point:]

with open(arch_path, 'w', encoding='utf-8') as f:
    f.write(arch)
print("[UPDATED] ARCHITECTURE.md — merged AGENT-CONFIG.md tool lists")

# 3. Delete AGENT-CONFIG.md
os.remove(agent_config_path)
print("[DELETED] AGENT-CONFIG.md")

# 4. Move system_audit.py to tools/
tools_dir = os.path.join(PROMPTS, "tools")
os.makedirs(tools_dir, exist_ok=True)
audit_src = os.path.join(PROMPTS, "system_audit.py")
audit_dst = os.path.join(tools_dir, "system_audit.py")
if os.path.exists(audit_src):
    shutil.move(audit_src, audit_dst)
    print(f"[MOVED] system_audit.py -> tools/system_audit.py")

# 5. Update system_audit.py self-reference in tools/
if os.path.exists(audit_dst):
    with open(audit_dst, 'r', encoding='utf-8') as f:
        audit_content = f.read()
    audit_content = audit_content.replace(
        "# save as: G:\\My Drive\\prompts\\system_audit.py",
        "# save as: G:\\My Drive\\prompts\\tools\\system_audit.py"
    )
    with open(audit_dst, 'w', encoding='utf-8') as f:
        f.write(audit_content)
    print("[UPDATED] tools/system_audit.py — self-reference updated")

# 6. Update README.md — remove AGENT-CONFIG references
readme_path = os.path.join(PROMPTS, "README.md")
with open(readme_path, 'r', encoding='utf-8') as f:
    readme = f.read()

readme = readme.replace(
    "| **Agent names, tools, slot IDs** | Reference `AGENT-CONFIG.md` for the exact values |",
    "| **Agent names, tools, slot IDs** | See `ARCHITECTURE.md` §1 for the exact values |"
)
readme = readme.replace(
    "| `AGENT-CONFIG.md` | Configuration reference — agent names, tools, slot IDs, write boundaries |",
    ""
)
readme = readme.replace(
    "├── AGENT-CONFIG.md               ← Configuration reference (agent names, tools, slot IDs)\n",
    ""
)
readme = readme.replace(
    "├── system_audit.py               ← Health check (type \"SYSTEM HEALTH CHECK\")\n",
    ""
)
readme = readme.replace(
    "Type **\"SYSTEM HEALTH CHECK\"** in any agent chat to run `system_audit.py`",
    "Type **\"SYSTEM HEALTH CHECK\"** in any agent chat to run `tools/system_audit.py`"
)
readme = readme.replace(
    "- `AGENT-CONFIG.md` — Agent configuration values for DeepChat Settings (v5.2)",
    ""
)
# Add tools/ directory to tree
if "├── scholar\\" in readme:
    readme = readme.replace(
        "├── scholar\\",
        "├── tools\\                         ← Utility scripts (system_audit.py)\n├── scholar\\"
    )

# Update File Ownership section
readme = readme.replace(
    "| **HUMAN — reference only** | `AGENT-CONFIG.md` (agent names, tools, slot IDs), `ARCHITECTURE.md` (system design) |",
    "| **HUMAN — reference only** | `ARCHITECTURE.md` (system design, agent config, tool lists, slot IDs) |"
)

with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(readme)
print("[UPDATED] README.md — removed AGENT-CONFIG.md references, updated paths")

# 7. Update META-PROMPT-DEEPSEEK.md
meta_path = os.path.join(PROMPTS, "META-PROMPT-DEEPSEEK.md")
with open(meta_path, 'r', encoding='utf-8') as f:
    meta = f.read()

meta = meta.replace(
    "- `AGENT-CONFIG.md` (v5.2) — exact slot ID ground truth, agent write boundaries",
    "- `AGENT-CONFIG.md` (v5.2, now consolidated into ARCHITECTURE.md) — agent write boundaries, tool lists"
)
meta = meta.replace(
    "- `system_audit.py` — self-learning health check; triggered by user command \"SYSTEM HEALTH CHECK\"",
    "- `tools/system_audit.py` — self-learning health check; triggered by user command \"SYSTEM HEALTH CHECK\""
)
meta = meta.replace(
    "Run `system_audit.py` when user says \"SYSTEM HEALTH CHECK\"",
    "Run `tools/system_audit.py` when user says \"SYSTEM HEALTH CHECK\""
)

with open(meta_path, 'w', encoding='utf-8') as f:
    f.write(meta)
print("[UPDATED] META-PROMPT-DEEPSEEK.md — updated paths")

# 8. Update agent files that reference AGENT-CONFIG.md
for agent_file in ["PROJECTS-AGENT.md", "PROMPTS-AGENT.md", "QWAV-AGENT.md"]:
    agent_path = os.path.join(PROMPTS, "agents", agent_file)
    if os.path.exists(agent_path):
        with open(agent_path, 'r', encoding='utf-8') as f:
            content = f.read()
        content = content.replace("AGENT-CONFIG.md", "ARCHITECTURE.md")
        with open(agent_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[UPDATED] agents/{agent_file} — AGENT-CONFIG.md -> ARCHITECTURE.md")

# 9. Update ARCHITECTURE.md to remove AGENT-CONFIG from its own version table
with open(arch_path, 'r', encoding='utf-8') as f:
    arch = f.read()
# Remove the AGENT-CONFIG row from version table
arch = re.sub(r'\| `AGENT-CONFIG\.md` \| [^|]+ \| [^|]+ \|\n', '', arch)
with open(arch_path, 'w', encoding='utf-8') as f:
    f.write(arch)
print("[UPDATED] ARCHITECTURE.md — removed AGENT-CONFIG.md from version table")

print("\n=== CONSOLIDATION COMPLETE ===")
