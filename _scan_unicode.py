"""Scan a Python file for non-ASCII characters — ASCII-safe output only."""
import sys
from collections import defaultdict

target = sys.argv[1] if len(sys.argv) > 1 else r"G:\My Drive\prompts\tools\zenodo_publish.py"

with open(target, 'r', encoding='utf-8') as f:
    lines = f.readlines()

non_ascii = []
for i, line in enumerate(lines, 1):
    for j, ch in enumerate(line):
        if ord(ch) > 127:
            non_ascii.append((i, j + 1, ch, ord(ch)))

if not non_ascii:
    print("No non-ASCII characters found.")
else:
    print(f"Found {len(non_ascii)} non-ASCII characters.")
    
    problematic = defaultdict(list)
    for ln, col, ch, code in non_ascii:
        cat = "other"
        if 0x2500 <= code <= 0x257F: cat = "box-drawing"
        elif 0x2070 <= code <= 0x2089 or code in (0x00B2, 0x00B3): cat = "sub/superscript"
        elif code in (0x2713, 0x26A0, 0x2717): cat = "symbols"
        elif code in (0x2013, 0x2014): cat = "dashes"
        elif code in (0x2018, 0x2019, 0x201C, 0x201D): cat = "quotes"
        elif code > 0xFFFF: cat = "emoji/astral"
        problematic[cat].append((ln, col, code))

    print("\nProblematic categories:")
    for cat, items in sorted(problematic.items()):
        unique_lines = sorted(set(ln for ln, _, _ in items))
        print(f"  {cat}: {len(items)} occurrences on lines {unique_lines}")

    # Sample details for first 10 per category
    print("\nSample details (U+codepoint at line:col):")
    for cat, items in sorted(problematic.items()):
        for ln, col, code in items[:3]:
            print(f"  {cat}: U+{code:04X} at line {ln}:{col}")
