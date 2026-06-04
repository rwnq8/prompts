#!/usr/bin/env python3
"""
Fast R2 Upload Tool (v1.0) — Cloudflare REST API Direct Upload

Uploads files to Cloudflare R2 using the REST API, bypassing wrangler's
per-file npx/node overhead (5s/file → 0.02s/file, 250x faster).

Usage:
    # Single file:
    python tools/fast_r2_upload.py --bucket qnfo --prefix projects/ --local "G:/My Drive/projects/file.md" --remote path/to/file.md

    # Batch from JSON list:
    python tools/fast_r2_upload.py --bucket qnfo --batch _upload_list.json --threads 20

    # Dry run (no upload, just validate):
    python tools/fast_r2_upload.py --bucket qnfo --batch _upload_list.json --dry-run

Batch JSON format (_upload_list.json):
    [{"local": "G:/My Drive/projects/file.md", "r2": "qnfo/projects/file.md"}, ...]

Requires: CLOUDFLARE_API_TOKEN environment variable (must have R2 Object Write permission)
Canonical: G:/My Drive/prompts/tools/fast_r2_upload.py
R2: qnfo/tools/fast_r2_upload.py

Based on the working implementation from 2026-06-04 session: 883 files uploaded
in 38 seconds (23 MB, zero failures) vs wrangler's projected 73 minutes.
"""

import argparse
import json
import os
import ssl
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from urllib.parse import quote

ACCOUNT_ID = 'edb167b78c9fb901ea5bca3ce58ccc4b'
DEFAULT_BUCKET = 'qnfo'
DEFAULT_THREADS = 20


def upload_file(local_path, remote_key, bucket, token, ctx):
    """Upload a single file to R2 via REST API. Returns (success, error_message)."""
    encoded_key = quote(remote_key, safe='')
    url = (
        f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}'
        f'/r2/buckets/{bucket}/objects/{encoded_key}'
    )
    try:
        with open(local_path, 'rb') as fh:
            data = fh.read()
        req = urllib.request.Request(url, data=data, method='PUT', headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/octet-stream',
            'Content-Length': str(len(data)),
        })
        resp = urllib.request.urlopen(req, context=ctx, timeout=30)
        result = json.loads(resp.read())
        if result.get('success'):
            return True, None
        else:
            errors = result.get('errors', [])
            return False, str(errors[0].get('message', str(errors)) if errors else 'Unknown API error')
    except FileNotFoundError:
        return False, f'File not found: {local_path}'
    except urllib.error.HTTPError as e:
        body = ''
        try:
            body = e.read().decode()[:200]
        except:
            pass
        return False, f'HTTP {e.code}: {body}'
    except Exception as e:
        return False, str(e)[:200]


def main():
    parser = argparse.ArgumentParser(
        description='Fast R2 Upload — Cloudflare REST API (250x faster than wrangler)'
    )
    parser.add_argument('--bucket', default=DEFAULT_BUCKET, help='R2 bucket name')
    parser.add_argument('--prefix', help='Object key prefix (for single file mode)')
    parser.add_argument('--local', help='Local file path (for single file mode)')
    parser.add_argument('--remote', help='Remote object key (for single file mode)')
    parser.add_argument('--batch', help='JSON file with upload list: [{"local":"...", "r2":"..."}]')
    parser.add_argument('--threads', type=int, default=DEFAULT_THREADS, help=f'Parallel threads (default {DEFAULT_THREADS})')
    parser.add_argument('--dry-run', action='store_true', help='Validate only, do not upload')
    parser.add_argument('--quiet', action='store_true', help='Suppress progress output')
    args = parser.parse_args()

    token = os.environ.get('CLOUDFLARE_API_TOKEN', '')
    if not token:
        print('ERROR: CLOUDFLARE_API_TOKEN environment variable not set', file=sys.stderr)
        print('Set it: $env:CLOUDFLARE_API_TOKEN = "cfat_..."', file=sys.stderr)
        sys.exit(1)

    ctx = ssl.create_default_context()

    # --- SINGLE FILE MODE ---
    if args.local and args.remote:
        key = args.remote
        if args.prefix:
            key = f'{args.prefix.rstrip("/")}/{args.remote.lstrip("/")}'

        if args.dry_run:
            print(f'[DRY-RUN] Would upload: {args.local} -> {args.bucket}/{key}')
            print(f'  File exists: {os.path.exists(args.local)}')
            print(f'  File size: {os.path.getsize(args.local) if os.path.exists(args.local) else "N/A"} bytes')
            return

        if not os.path.exists(args.local):
            print(f'ERROR: File not found: {args.local}', file=sys.stderr)
            sys.exit(1)

        start = time.time()
        success, error = upload_file(args.local, key, args.bucket, token, ctx)
        elapsed = time.time() - start

        if success:
            print(f'OK ({elapsed:.1f}s): {key}')
        else:
            print(f'FAIL ({elapsed:.1f}s): {key} — {error}', file=sys.stderr)
            sys.exit(1)
        return

    # --- BATCH MODE ---
    if args.batch:
        if not os.path.exists(args.batch):
            print(f'ERROR: Batch file not found: {args.batch}', file=sys.stderr)
            sys.exit(1)

        with open(args.batch) as f:
            uploads = json.load(f)

        if not isinstance(uploads, list):
            print('ERROR: Batch file must be a JSON array', file=sys.stderr)
            sys.exit(1)

        if args.dry_run:
            print(f'[DRY-RUN] {len(uploads)} files would be uploaded to {args.bucket}')
            total_size = 0
            for u in uploads:
                local = u.get('local', '?')
                exists = os.path.exists(local)
                size = os.path.getsize(local) if exists else 0
                total_size += size
                if len(uploads) <= 20:
                    print(f'  {"OK" if exists else "MISSING"}: {local} -> {u.get("r2", "?")}')
            print(f'  Total: {total_size / (1024*1024):.2f} MB')
            missing = sum(1 for u in uploads if not os.path.exists(u.get('local', '')))
            if missing:
                print(f'  WARNING: {missing} files not found locally')
            return

        # Real upload
        stats = {'ok': 0, 'fail': 0}
        errors = []
        lock = Lock()
        start = time.time()

        def worker(u):
            local = u.get('local', '')
            r2_key = u.get('r2', '')
            if not local or not r2_key:
                with lock:
                    stats['fail'] += 1
                return

            # Strip bucket prefix from r2 key if present
            bucket_prefix = f'{args.bucket}/'
            if r2_key.startswith(bucket_prefix):
                r2_key = r2_key[len(bucket_prefix):]

            success, error = upload_file(local, r2_key, args.bucket, token, ctx)
            with lock:
                if success:
                    stats['ok'] += 1
                else:
                    stats['fail'] += 1
                    if len(errors) < 10:
                        errors.append(f'{os.path.basename(local)}: {error}')
                done = stats['ok'] + stats['fail']
                if not args.quiet and done % 50 == 0:
                    elapsed = time.time() - start
                    rate = done / elapsed if elapsed > 0 else 0
                    print(f'{done}/{len(uploads)} ({rate:.1f}/s) ok={stats["ok"]} fail={stats["fail"]}', flush=True)

        print(f'Uploading {len(uploads)} files via REST API ({args.threads} threads)...', flush=True)
        with ThreadPoolExecutor(max_workers=args.threads) as ex:
            futures = [ex.submit(worker, u) for u in uploads]
            for f in as_completed(futures):
                f.result()

        elapsed = time.time() - start
        done = stats['ok'] + stats['fail']
        print(f'\n=== DONE: {done}/{len(uploads)} ok={stats["ok"]} fail={stats["fail"]} ({elapsed:.0f}s) ===')

        if errors:
            print(f'\nErrors ({len(errors)}):')
            for err in errors:
                print(f'  - {err}')

        if stats['fail'] > 0:
            sys.exit(1)
        return

    # --- No mode selected ---
    parser.print_help()
    print('\nExamples:')
    print('  Single: python tools/fast_r2_upload.py --local file.md --remote projects/file.md')
    print('  Batch:  python tools/fast_r2_upload.py --batch _upload_list.json --threads 20')
    print('  Dry:    python tools/fast_r2_upload.py --batch _upload_list.json --dry-run')


if __name__ == '__main__':
    main()
