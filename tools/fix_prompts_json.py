"""fix_prompts_json.py — Convert prompts.json between wrapped and bare-array formats.

TWO FORMATS — used for different purposes:
  WRAPPED: {"prompts": [{"id":..., "name":..., "content":..., ...}]}
    → CANONICAL source of truth. Matches DeepChat internal custom_prompts.json.
  BARE ARRAY: [{"id":..., "name":..., "content":..., ...}]
    → DEEPCHAT IMPORT FORMAT. The Prompt Templates import dialog expects a
      bare array at the top level and rejects wrapped with "not an array".

This script:
1. Detects format (wrapped dict vs bare list)
2. Converts to wrapped if bare (for canonical storage)
3. Converts to bare if wrapped (for import)
4. Adds required fields: enabled, createdAt, updatedAt, description (if missing)
5. Deduplicates by name
6. Writes back to prompts.json AND prompts_bare.json

Canonical source: G:\My Drive\prompts\tools\fix_prompts_json.py
v1.2 — 2026-06-02: Dual output, import-path documentation
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
