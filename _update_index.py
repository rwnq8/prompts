import json

with open(r'G:\My Drive\prompts\_discovery_index.json', 'r', encoding='utf-8') as f:
    idx = json.load(f)

if 'skills' not in idx:
    idx['skills'] = {}

idx['skills']['knowledge-graph'] = {
    'name': 'knowledge-graph',
    'version': '1.0',
    'description': 'QNFO Knowledge Graph querying for due diligence, impact analysis, and cross-system discovery',
    'path': 'skills/knowledge-graph/SKILL.md',
    'api_endpoint': 'https://graph-api.q08.workers.dev',
    'created': '2026-06-01',
    'status': 'active'
}

if '_metadata' not in idx:
    idx['_metadata'] = {}
idx['_metadata']['last_updated'] = '2026-06-01T20:57:00Z'
idx['_metadata']['updated_by'] = 'META-PROMPT (v5.3)'
idx['_metadata']['total_skills'] = len(idx['skills'])

count = len(idx['skills'])
print(f"Skills registered: {count}")
for name, skill in idx['skills'].items():
    print(f"  {name}: v{skill.get('version', '?')}")

with open(r'G:\My Drive\prompts\_discovery_index.json', 'w', encoding='utf-8') as f:
    json.dump(idx, f, indent=2, ensure_ascii=False)
print("Discovery Index updated locally.")
