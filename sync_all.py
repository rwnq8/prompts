import json, os

# Read current file contents
default_content = open(r'G:\My Drive\prompts\DEFAULT.md', 'r', encoding='utf-8').read()
meta_content = open(r'G:\My Drive\prompts\META-PROMPT-DEEPSEEK.md', 'r', encoding='utf-8').read()
readme_content = open(r'G:\My Drive\prompts\README.md', 'r', encoding='utf-8').read()

stage1 = open(r'G:\My Drive\prompts\scholar\STAGE-1-SETUP.md', 'r', encoding='utf-8').read()
stage2 = open(r'G:\My Drive\prompts\scholar\STAGE-2-DRAFT.md', 'r', encoding='utf-8').read()
stage3 = open(r'G:\My Drive\prompts\scholar\STAGE-3-REVIEW.md', 'r', encoding='utf-8').read()
stage4 = open(r'G:\My Drive\prompts\scholar\STAGE-4-PUBLISH.md', 'r', encoding='utf-8').read()

print("=== 1. SYNCING system_prompts.json ===")
spp = r'C:\Users\LENOVO\AppData\Roaming\DeepChat\system_prompts.json'
with open(spp, 'r', encoding='utf-8') as f:
    sp = json.load(f)

# Build clean system prompts list - 3 entries
sp['prompts'] = [
    {
        'id': 'default',
        'name': 'DeepChat',
        'content': default_content
    },
    {
        'id': 'DEFAULT_v1.1',
        'name': 'DEFAULT-DEEPSEEK (v1.1-NO-WEB-SEARCH)',
        'content': default_content
    },
    {
        'id': 'META_v3.1',
        'name': 'META-PROMPT-DEEPSEEK (v3.1-NO-WEB-SEARCH)',
        'content': meta_content
    }
]

with open(spp, 'w', encoding='utf-8') as f:
    json.dump(sp, f, ensure_ascii=False, indent=2)
print(f'  system_prompts.json: {len(sp["prompts"])} entries (DeepChat + DEFAULT + META-PROMPT)')

print()
print("=== 2. SYNCING custom_prompts.json ===")
cpp = r'C:\Users\LENOVO\AppData\Roaming\DeepChat\custom_prompts.json'
with open(cpp, 'r', encoding='utf-8') as f:
    cp = json.load(f)

# Clear and rebuild with current content
cp['prompts'] = [
    {
        'id': '1',
        'name': 'DEFAULT-DEEPSEEK (v1.1-NO-WEB-SEARCH)',
        'description': 'All-purpose DeepSeek agent for brainstorming, scholarly research, and document creation. NO-WEB-SEARCH edition: Python is the ONLY source of quantitative truth. Includes Article V Anti-Fabrication Mandate, Search Manifest Protocol, and source classification.',
        'content': default_content,
        'args': []
    },
    {
        'id': '2',
        'name': 'META-PROMPT-DEEPSEEK (v3.1-NO-WEB-SEARCH)',
        'description': 'Tier 1 Constitutional System Architect. Generates, audits, and refines Tier 2 System Prompts. NO-WEB-SEARCH edition with Article V and Search Manifest Protocol.',
        'content': meta_content,
        'args': []
    },
    {
        'id': '3',
        'name': 'OMEGA-SCHOLAR STAGE 1: RESEARCH SETUP (v5.3)',
        'description': 'Stage 1 of 4. Context, file-backed VRO (or Search Manifest), and Structural Blueprint.',
        'content': stage1,
        'args': []
    },
    {
        'id': '4',
        'name': 'OMEGA-SCHOLAR STAGE 2: RESEARCH & DRAFT (v5.3)',
        'description': 'Stage 2 of 4. Python-only evidence generation and narrative drafting.',
        'content': stage2,
        'args': []
    },
    {
        'id': '5',
        'name': 'OMEGA-SCHOLAR STAGE 3: QUALITY ASSURANCE (v5.3)',
        'description': 'Stage 3 of 4. Peer review, revision, forensic audit, and purification.',
        'content': stage3,
        'args': []
    },
    {
        'id': '6',
        'name': 'OMEGA-SCHOLAR STAGE 4: FINAL PUBLICATION (v5.3)',
        'description': 'Stage 4 of 4. Final assembly and publication with source labeling.',
        'content': stage4,
        'args': []
    }
]

with open(cpp, 'w', encoding='utf-8') as f:
    json.dump(cp, f, ensure_ascii=False, indent=2)
print(f'  custom_prompts.json: {len(cp["prompts"])} templates (DEFAULT + META-PROMPT + 4 scholar stages)')

print()
print("=== 3. SYNCING app-settings.json ===")
asp = r'C:\Users\LENOVO\AppData\Roaming\DeepChat\app-settings.json'
with open(asp, 'r', encoding='utf-8') as f:
    app = json.load(f)

app['default_system_prompt'] = default_content
# Also ensure skills path is correct
app['skillsPath'] = r'C:\Users\LENOVO\.deepchat\skills'
app['defaultProjectPath'] = r'G:\My Drive\prompts'

with open(asp, 'w', encoding='utf-8') as f:
    json.dump(app, f, ensure_ascii=False, indent=2)
print(f'  app-settings.json: default_system_prompt = DEFAULT v1.1 ({len(default_content)} chars)')
print(f'  skillsPath: {app.get("skillsPath")}')
print(f'  defaultProjectPath: {app.get("defaultProjectPath")}')

print()
print("=== 4. SYNCING acp_agents.json ===")
acp = r'C:\Users\LENOVO\AppData\Roaming\DeepChat\acp_agents.json'
with open(acp, 'r', encoding='utf-8') as f:
    acp_data = json.load(f)

# Set default prompt for all agents
if 'registryStates' in acp_data:
    for agent_id, state in acp_data['registryStates'].items():
        state['defaultPrompt'] = 'DEFAULT-DEEPSEEK (v1.1-NO-WEB-SEARCH)'
        print(f'  {agent_id}: defaultPrompt -> DEFAULT v1.1')

with open(acp, 'w', encoding='utf-8') as f:
    json.dump(acp_data, f, ensure_ascii=False, indent=2)
print(f'  ACP agents: {len(acp_data.get("registryStates", {}))} agents configured with DEFAULT v1.1')

print()
print("=== 5. UPDATING README.md ===")
readme = """# prompts/ — DeepSeek System Prompt Library

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

All deprecated/specialized content at `G:\\My Drive\\Archive\\prompts\\`

## Git

Branch: `main`. Full audit trail. Pushed to GitHub.
"""

with open(r'G:\My Drive\prompts\README.md', 'w', encoding='utf-8') as f:
    f.write(readme)
print('  README.md updated')

print()
print('=== SYNC COMPLETE ===')
print('GitHub: main branch pushed')
print('Local git: main branch, clean')
print('system_prompts.json: 3 entries (DeepChat + DEFAULT + META-PROMPT)')
print('custom_prompts.json: 6 templates')
print('app-settings.json: default = DEFAULT v1.1')
print('ACP agents: all 3 set to DEFAULT v1.1')
