#!/usr/bin/env python3
"""Migration Scanner — scan, classify, and report on local files for R2 migration.

Usage:
    python _migration_scanner.py --scan <dir> [--scan <dir2> ...] --output <report.json>
    python _migration_scanner.py --report <report.json>

Canonical path: G:/My Drive/prompts/tools/migration_scanner.py
R2 mirror: qnfo/tools/migration_scanner.py
"""

import os
import json
import argparse
from datetime import datetime, timezone


# Classification rules
SKIP_DIRS = {'.git', '.wrangler', '__pycache__', 'node_modules', 'target', '.venv', 'venv'}
SKIP_EXTENSIONS = {'.exe', '.dll', '.so', '.dylib', '.wasm', '.bin'}
ORPHAN_PATTERN = lambda name: name.startswith('_')
BUILD_EXTENSIONS = {'.o', '.d', '.rmeta', '.rlib', '.a', '.lib', '.class', '.pyc', '.pyo'}
SOURCE_EXTENSIONS = {
    '.md', '.py', '.json', '.html', '.css', '.js', '.jsx', '.ts', '.tsx',
    '.tex', '.pdf', '.txt', '.csv', '.toml', '.yaml', '.yml', '.lock',
    '.rs', '.ipynb', '.xml', '.svg', '.png', '.jpg', '.jpeg', '.gif',
    '.webp', '.ico', '.woff', '.woff2', '.ttf', '.eot', '.mp4', '.webm',
    '.mp3', '.wav', '.zip', '.tar', '.gz', '.bz2', '.xz', '.cfg', '.ini',
    '.env', '.sample', '.template', '.nix', '.sh', '.bash', '.ps1', '.bat',
    '.tf', '.hcl', '.proto', '.graphql', '.sql', '.r', '.jl', '.go', '.c',
    '.h', '.cpp', '.hpp', '.java', '.kt', '.swift', '.scala', '.rb', '.php',
    '.wasm', '.wat', '.css.map', '.js.map',
}
IMPORT_SURFACE_PREFIX = os.path.normpath('G:/My Drive/prompts')


def classify_file(filepath, size_bytes):
    """Classify a single file."""
    name = os.path.basename(filepath)
    ext = os.path.splitext(name)[1].lower()
    norm = os.path.normpath(filepath)

    # Import surface — never touch
    if norm.startswith(IMPORT_SURFACE_PREFIX):
        return 'IMPORT-SURFACE'

    # Check parent directories for skip patterns
    parts = norm.replace('\\', '/').split('/')
    for part in parts:
        if part in SKIP_DIRS:
            if part == '.git':
                return 'GIT-OBJECTS'
            elif part == '.wrangler':
                return 'WRANGLER-CACHE'
            elif part == '__pycache__':
                return 'PYTHON-CACHE'
            elif part in ('node_modules', 'target', '.venv', 'venv'):
                return 'BUILD-ARTIFACT'

    # Orphaned ephemeral files
    if ORPHAN_PATTERN(name):
        return 'ORPHANED-EPHEMERAL'

    # Build artifacts by extension
    if ext in BUILD_EXTENSIONS:
        return 'BUILD-ARTIFACT'

    # Binary/skip extensions
    if ext in SKIP_EXTENSIONS:
        return 'BUILD-ARTIFACT'

    # Known source files — migration candidates
    if ext in SOURCE_EXTENSIONS or ext == '':
        return 'R2-MIGRATION-CANDIDATE'

    # Unknown
    return 'UNKNOWN'


def determine_r2_path(filepath, classification):
    """Determine the R2 destination path for a file."""
    norm = os.path.normpath(filepath).replace('\\', '/')

    if norm.startswith('G:/My Drive/projects/'):
        rel = norm[len('G:/My Drive/projects/'):]
        return f'qnfo/projects/{rel}'
    elif norm.startswith('G:/My Drive/QWAV/'):
        rel = norm[len('G:/My Drive/QWAV/'):]
        return f'qnfo/qwav/{rel}'
    elif norm.startswith('G:/My Drive/Archive/'):
        rel = norm[len('G:/My Drive/Archive/'):]
        return f'qnfo/archive/{rel}'
    else:
        return f'qnfo/migrated/{os.path.basename(filepath)}'


def scan_directory(target_dir):
    """Scan a directory and classify all files."""
    results = {
        'ORPHANED-EPHEMERAL': [],
        'GIT-OBJECTS': [],
        'WRANGLER-CACHE': [],
        'PYTHON-CACHE': [],
        'BUILD-ARTIFACT': [],
        'IMPORT-SURFACE': [],
        'R2-MIGRATION-CANDIDATE': [],
        'UNKNOWN': [],
    }

    for root, dirs, files in os.walk(target_dir):
        for f in files:
            filepath = os.path.join(root, f)
            try:
                size = os.path.getsize(filepath)
            except OSError:
                size = 0

            classification = classify_file(filepath, size)
            entry = {
                'local_path': filepath.replace('\\', '/'),
                'size_bytes': size,
                'classification': classification,
            }

            if classification == 'R2-MIGRATION-CANDIDATE':
                entry['r2_path'] = determine_r2_path(filepath, classification)

            if classification in results:
                results[classification].append(entry)

    return results


def run_scan(targets, output_path):
    """Full scan of all targets."""
    combined = {
        'scan_time': datetime.now(timezone.utc).isoformat(),
        'targets': targets,
    }

    # Initialize categories
    for category in ['ORPHANED-EPHEMERAL', 'GIT-OBJECTS', 'WRANGLER-CACHE',
                     'PYTHON-CACHE', 'BUILD-ARTIFACT', 'IMPORT-SURFACE',
                     'R2-MIGRATION-CANDIDATE', 'UNKNOWN']:
        combined[category] = []

    total_size = 0
    total_files = 0

    for target in targets:
        if not os.path.isdir(target):
            print(f'WARNING: {target} does not exist, skipping')
            continue
        print(f'Scanning {target}...')
        results = scan_directory(target)
        for category, entries in results.items():
            combined[category].extend(entries)
            total_files += len(entries)
            for e in entries:
                total_size += e.get('size_bytes', 0)

    # Build summary
    combined['totals'] = {
        'files_found': total_files,
        'total_size_bytes': total_size,
        'total_size_mb': round(total_size / (1024 * 1024), 2),
    }

    combined['by_classification'] = {}
    for category in ['ORPHANED-EPHEMERAL', 'GIT-OBJECTS', 'WRANGLER-CACHE',
                     'PYTHON-CACHE', 'BUILD-ARTIFACT', 'IMPORT-SURFACE',
                     'R2-MIGRATION-CANDIDATE', 'UNKNOWN']:
        entries = combined[category]
        cat_size = sum(e.get('size_bytes', 0) for e in entries)
        combined['by_classification'][category] = {
            'count': len(entries),
            'size_mb': round(cat_size / (1024 * 1024), 2),
        }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(combined, f, indent=2, ensure_ascii=False)

    print(f'\nScan complete: {total_files} files ({combined["totals"]["total_size_mb"]} MB)')
    print(f'Report written to {output_path}')
    return combined


def print_report(report_path):
    """Print a human-readable summary of the scan report."""
    with open(report_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    totals = data.get('totals', {})
    by_class = data.get('by_classification', {})

    print('=' * 60)
    print('MIGRATION SCAN REPORT')
    print('=' * 60)
    print(f'Scan time: {data.get("scan_time", "unknown")}')
    print(f'Targets: {", ".join(data.get("targets", []))}')
    print(f'Total files: {totals.get("files_found", 0)}')
    print(f'Total size: {totals.get("total_size_mb", 0)} MB')
    print()

    action_map = {
        'ORPHANED-EPHEMERAL': '🗑️  DELETE (abandoned ephemeral)',
        'GIT-OBJECTS': '⏭️  SKIP (git-managed)',
        'WRANGLER-CACHE': '⏭️  SKIP (wrangler-managed)',
        'PYTHON-CACHE': '🗑️  DELETE (regenerated)',
        'BUILD-ARTIFACT': '🗑️  DELETE (regenerated from source)',
        'IMPORT-SURFACE': '🔒 SKIP (import surface — NEVER delete)',
        'R2-MIGRATION-CANDIDATE': '☁️  UPLOAD to R2',
        'UNKNOWN': '❓ ASK USER',
    }

    for cat in ['ORPHANED-EPHEMERAL', 'PYTHON-CACHE', 'BUILD-ARTIFACT',
                'R2-MIGRATION-CANDIDATE', 'GIT-OBJECTS', 'WRANGLER-CACHE',
                'IMPORT-SURFACE', 'UNKNOWN']:
        info = by_class.get(cat, {})
        count = info.get('count', 0)
        size = info.get('size_mb', 0)
        action = action_map.get(cat, '?')
        if count > 0:
            print(f'  {action:50s} | {count:>6d} files | {size:>8.2f} MB')

    print()
    print('=' * 60)

    # Show R2 destinations summary
    candidates = data.get('R2-MIGRATION-CANDIDATE', [])
    if candidates:
        prefixes = {}
        for c in candidates:
            r2 = c.get('r2_path', 'unknown')
            prefix = '/'.join(r2.split('/')[:3])
            if prefix not in prefixes:
                prefixes[prefix] = {'count': 0, 'size': 0}
            prefixes[prefix]['count'] += 1
            prefixes[prefix]['size'] += c.get('size_bytes', 0)

        print('\nR2 UPLOAD DESTINATIONS:')
        for prefix, info in sorted(prefixes.items()):
            print(f'  {prefix}/  ({info["count"]} files, {info["size"] / (1024*1024):.2f} MB)')

    print()


def main():
    parser = argparse.ArgumentParser(description='Migration Scanner')
    parser.add_argument('--scan', action='append', dest='targets', help='Directory to scan')
    parser.add_argument('--output', help='Output JSON report path')
    parser.add_argument('--report', help='Print summary of an existing report')
    args = parser.parse_args()

    if args.report:
        print_report(args.report)
    elif args.targets and args.output:
        run_scan(args.targets, args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
