#!/usr/bin/env python3
"""R2 Object List via Cloudflare REST API — bypasses wrangler overhead.

Usage:
    python tools/r2_list.py --prefix projects/ --limit 10
    python tools/r2_list.py --prefix projects/quantum-cryptanalysis-blockchain/ --limit 5

Requires: CLOUDFLARE_API_TOKEN environment variable
Canonical: G:/My Drive/prompts/tools/r2_list.py
R2: qnfo/tools/r2_list.py

This is 10-50x faster than wrangler r2 object list for enumerating R2 contents.
"""

import argparse
import json
import os
import ssl
import sys
import urllib.request
from urllib.parse import quote

ACCOUNT_ID = 'edb167b78c9fb901ea5bca3ce58ccc4b'
BUCKET = 'qnfo'


def main():
    parser = argparse.ArgumentParser(description='List R2 objects via Cloudflare REST API')
    parser.add_argument('--prefix', default='', help='Object key prefix filter')
    parser.add_argument('--limit', type=int, default=20, help='Max results (default 20)')
    parser.add_argument('--bucket', default=BUCKET, help='R2 bucket name')
    parser.add_argument('--json', action='store_true', help='Output raw JSON')
    args = parser.parse_args()

    token = os.environ.get('CLOUDFLARE_API_TOKEN', '')
    if not token:
        print('ERROR: CLOUDFLARE_API_TOKEN not set', file=sys.stderr)
        sys.exit(1)

    encoded_prefix = quote(args.prefix, safe='')
    url = (
        f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}'
        f'/r2/buckets/{args.bucket}/objects'
        f'?prefix={encoded_prefix}&limit={args.limit}'
    )

    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    })

    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=15)
        data = json.loads(resp.read())
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    if not data.get('success'):
        for err in data.get('errors', []):
            print(f'API Error: {err.get("message", err)}', file=sys.stderr)
        sys.exit(1)

    result = data.get('result', [])
    if isinstance(result, dict):
        objects = result.get('objects', [])
    else:
        objects = result

    print(f'Found {len(objects)} objects with prefix "{args.prefix}":')
    for obj in objects:
        key = obj.get('key', '?')
        size = obj.get('size', 0)
        uploaded = obj.get('uploaded', '?')
        print(f'  {key:60s} {size:>10,} bytes  {uploaded}')


if __name__ == '__main__':
    main()
