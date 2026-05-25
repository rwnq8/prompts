#!/usr/bin/env python3
r"""rebuild_prompts_json.py -- Scan templates/scholar/email/agents directories and rebuild prompts.json.

Extracted from prompts-json-regen.yml inline python -c (F5 fix).
Canonical source: G:\My Drive\prompts\tools\rebuild_prompts_json.py
"""
import os
import json
import glob
import hashlib
import sys

DIRS = ['templates', 'scholar', 'email', 'agents']
OUTPUT = 'prompts.json'

def rebuild():
    entries = []
    for d in DIRS:
        if not os.path.exists(d):
            print(f"  [SKIP] Directory not found: {d}")
            continue
        for f in sorted(glob.glob(f'{d}/**/*.md', recursive=True)):
            with open(f, 'r', encoding='utf-8') as fh:
                content = fh.read()
            name = os.path.splitext(os.path.basename(f))[0]
            entries.append({
                'id': str(len(entries) + 1),
                'name': name,
                'description': f'Auto-regenerated from {f}',
                'content': content,
                'parameters': [],
                'source': 'local'
            })
            print(f"  [{len(entries)}] {name} <- {f}")

    with open(OUTPUT, 'w', encoding='utf-8') as fh:
        json.dump(entries, fh, indent=2, ensure_ascii=False)

    print(f"\nRebuilt {OUTPUT} with {len(entries)} entries from {len(DIRS)} directories.")
    return len(entries)

if __name__ == '__main__':
    count = rebuild()
    sys.exit(0)
