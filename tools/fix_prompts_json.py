"""fix_prompts_json.py — Convert the bare-array prompts.json to DeepChat-importable format.

DeepChat import expects: {"prompts": [{"id":..., "name":..., "content":..., "enabled":..., ...}]}
rebuild_prompts_json.py produces a bare array: [{"id":..., "name":..., "content":..., ...}]

This script:
1. Reads the bare-array prompts.json from rebuild_prompts_json.py
2. Wraps it in {"prompts": [...]} for DeepChat import compatibility
3. Adds required fields: enabled, createdAt, updatedAt, description (if missing)
4. Writes back to prompts.json
"""
import json, time, sys

INPUT = 'prompts.json'
OUTPUT = 'prompts.json'

with open(INPUT, 'r', encoding='utf-8') as f:
    data = json.load(f)

# If already wrapped, extract
if isinstance(data, dict) and 'prompts' in data:
    entries = data['prompts']
    print(f"Already wrapped. {len(entries)} entries.")
elif isinstance(data, list):
    entries = data
    print(f"Bare array. {len(entries)} entries. Wrapping...")
else:
    print(f"ERROR: Unknown format: {type(data).__name__}")
    sys.exit(1)

# Ensure all required fields and deduplicate by name
seen = {}
unique_entries = []
now = str(int(time.time() * 1000))

for entry in entries:
    name = entry.get('name', '')
    if name in seen:
        print(f"  [DUPLICATE SKIPPED] {name}")
        continue
    seen[name] = True
    
    # Ensure all required DeepChat fields
    if 'id' not in entry:
        entry['id'] = now
    if 'description' not in entry:
        entry['description'] = f'Auto-regenerated from templates/{name}.md'
    if 'enabled' not in entry:
        entry['enabled'] = True
    if 'createdAt' not in entry:
        entry['createdAt'] = now
    if 'updatedAt' not in entry:
        entry['updatedAt'] = now
    if 'parameters' not in entry:
        entry['parameters'] = []
    if 'source' not in entry:
        entry['source'] = 'local'
    
    unique_entries.append(entry)

output = {"prompts": unique_entries}

with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nWrote {OUTPUT} with {len(unique_entries)} unique entries (wrapped format).")
print(f"Duplicates removed: {len(entries) - len(unique_entries)}")
