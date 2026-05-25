"""Fix non-ASCII characters in zenodo_publish.py for Windows cp1252 safety (Rule 12).

Replacements:
  - Box-drawing (U+2500-U+257F) -> ASCII dashes
  - Em dashes (U+2014) -> '---'
  - Warning symbol (U+26A0) + variation selector (U+FE0F) -> '[WARN]'
  - Any remaining non-ASCII -> ASCII fallback
"""
import sys

target = sys.argv[1] if len(sys.argv) > 1 else r"G:\My Drive\prompts\tools\zenodo_publish.py"

with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    '\N{EM DASH}': '---',       # U+2014
    '\N{WARNING SIGN}\N{VARIATION SELECTOR-16}': '[WARN]',  # U+26A0 + U+FE0F
    '\N{WARNING SIGN}': '[WARN]',  # U+26A0 alone (fallback)
}

# Box-drawing characters: replace each with ASCII dash
for cp in range(0x2500, 0x2580):
    replacements[chr(cp)] = '-'

# Remove variation selectors
for cp in range(0xFE00, 0xFE10):
    replacements[chr(cp)] = ''

count = 0
for old, new in replacements.items():
    if old in content:
        n = content.count(old)
        content = content.replace(old, new)
        count += n
        if n > 0:
            codes = ','.join(f'U+{ord(c):04X}' for c in old)
            print(f"  Replaced {n}x [{codes}] -> '{new}'")

# Scan for any remaining non-ASCII
remaining = []
for i, ch in enumerate(content):
    if ord(ch) > 127:
        # Find line number
        line_num = content[:i].count('\n') + 1
        remaining.append(f"  Line {line_num}: U+{ord(ch):04X}")

if remaining:
    print(f"\nWARNING: {len(remaining)} non-ASCII characters remain after replacement:")
    for r in remaining[:10]:
        print(r)
    if len(remaining) > 10:
        print(f"  ... and {len(remaining) - 10} more")
else:
    print("\nAll non-ASCII characters replaced successfully.")

with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nTotal replacements: {count}")
print(f"File updated: {target}")
