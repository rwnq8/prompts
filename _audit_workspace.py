"""Deep audit of prompts workspace - identify active, historical, redundant, consolidatable files"""
import os, hashlib

PROMPTS = r'G:\My Drive\prompts'

# Exclude .git from file count
total_files = 0
total_size = 0
all_files = []

for root, dirs, files in os.walk(PROMPTS):
    # Skip .git
    if '.git' in dirs:
        dirs.remove('.git')
    for f in files:
        fp = os.path.join(root, f)
        sz = os.path.getsize(fp)
        total_files += 1
        total_size += sz
        all_files.append((os.path.relpath(fp, PROMPTS), sz))

print(f"Total files: {total_files}")
print(f"Total size: {total_size:,} bytes (~{total_size/1024/1024:.1f} MB)")
print()

# === 1. STALE PM FILES ===
print("=== 1. STALE PM FILES ===")
stale_patterns = ['PROJECT-STATE', 'SPRINT', 'BACKLOG', 'CHANGELOG', 'LEARNINGS', 'DECISIONS', 'PROJECT STATE']
for relpath, sz in all_files:
    fname = os.path.basename(relpath)
    for pat in stale_patterns:
        if pat in fname and 'Archive' not in relpath and 'deprecated' not in relpath:
            print(f"  STALE: {relpath} ({sz:,} bytes)")

# === 2. VERSION HISTORY / OLD DEFAULTS ===
print("\n=== 2. VERSION HISTORY FILES ===")
default_size = None
for relpath, sz in all_files:
    if os.path.basename(relpath) == 'DEFAULT.md':
        default_size = sz
        break

for relpath, sz in all_files:
    fname = os.path.basename(relpath)
    if ('THE-ONE' in fname or (fname.startswith('DEFAULT') and fname != 'DEFAULT.md')):
        pct = f" ({sz/default_size*100:.0f}% of DEFAULT.md)" if default_size else ""
        print(f"  {relpath} ({sz:,} bytes){pct}")

# === 3. LARGE FILES ===
print("\n=== 3. LARGEST FILES (>50KB) ===")
for relpath, sz in sorted(all_files, key=lambda x: -x[1]):
    if sz > 50000:
        print(f"  {sz:>10,} bytes  {relpath}")

# === 4. DIRECTORY BREAKDOWN ===
print("\n=== 4. DIRECTORY BREAKDOWN ===")
dirs = {}
for relpath, sz in all_files:
    d = os.path.dirname(relpath) or '(root)'
    if d not in dirs:
        dirs[d] = {'count': 0, 'size': 0}
    dirs[d]['count'] += 1
    dirs[d]['size'] += sz

for d, info in sorted(dirs.items(), key=lambda x: -x[1]['size']):
    print(f"  {d}: {info['count']} files, {info['size']:,} bytes (~{info['size']/1024/1024:.1f} MB)")

# === 5. POTENTIAL CONSOLIDATION TARGETS ===
print("\n=== 5. POTENTIAL CONSOLIDATION TARGETS ===")

# Config/plan files that may be stale
config_files = ['DEVELOPMENT.md', 'KAIZEN-PLAN.md', 'CONFIG-CONSOLIDATION-PLAN.md',
                'DOI-PREFIX-MAP.md', 'DOI-SUFFIX-MAP.md', 'SECURITY-AUDIT.md',
                'CLEANUP-AUDIT.md', 'FINAL-AUDIT-REPORT.md']
for relpath, sz in all_files:
    fname = os.path.basename(relpath)
    if fname in config_files:
        print(f"  CONFIG/AUDIT: {relpath} ({sz:,} bytes)")

# Python scripts that may be one-time tools
print("\n  Python scripts in root:")
for relpath, sz in all_files:
    if relpath.startswith('(root)') and relpath.endswith('.py'):
        print(f"    {relpath} ({sz:,} bytes)")

# === 6. ARCHIVE ANALYSIS ===
print("\n=== 6. ARCHIVE CONTENTS ===")
for relpath, sz in sorted(all_files):
    if relpath.startswith('Archive'):
        print(f"  {relpath} ({sz:,} bytes)")

# === 7. EMAIL DIRECTORY ===
print("\n=== 7. EMAIL DIRECTORY FILES ===")
for relpath, sz in sorted(all_files):
    if relpath.startswith('email'):
        print(f"  {relpath} ({sz:,} bytes)")

# === 8. RECOMMENDATIONS ===
print("\n=== 8. RECOMMENDED ACTIONS ===")
print("Based on this audit:")
