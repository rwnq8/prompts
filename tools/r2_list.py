#!/usr/bin/env python3
"""
r2_list.py — Cloudflare R2 REST API Object Lister (v1.0)

Lists objects in a Cloudflare R2 bucket using the REST API.
Supports prefix filtering. 10x faster than wrangler r2 object get for listing.

Authentication: CLOUDFLARE_API_TOKEN env var, or ~/.cloudflare/api-token file.

Usage:
    python r2_list.py                          # List all objects
    python r2_list.py --prefix qnfo/tools/     # Filter by prefix
    python r2_list.py --prefix qnfo/tools/ --json  # JSON output
    python r2_list.py --count-only             # Just count objects
"""

import os
import sys
import json
import time
import argparse
import urllib.request
import urllib.error

API_BASE = "https://api.cloudflare.com/client/v4"
BUCKET_NAME = "qnfo"
MAX_OBJECTS = 10000  # R2 API limit per request (adjusted for pagination)
PAGE_SIZE = 1000

def get_api_token():
    token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
    if token:
        return token.strip()
    token_paths = [
        os.path.expanduser("~/.cloudflare/api-token"),
        r"C:\Users\LENOVO\.cloudflare\api-token",
    ]
    for p in token_paths:
        if os.path.exists(p):
            with open(p, 'r') as f:
                token = f.read().strip()
            if token:
                return token
    print("[ERROR] No Cloudflare API token found.")
    sys.exit(1)

def get_account_id(token):
    req = urllib.request.Request(
        f"{API_BASE}/accounts",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            if data.get("success") and data.get("result"):
                return data["result"][0]["id"]
    except Exception as e:
        print(f"[ERROR] Failed to detect account ID: {e}")
    return None

def list_objects(token, account_id, prefix=None, cursor=None):
    """List objects in R2 bucket. Returns (objects, cursor, truncated)."""
    url = f"{API_BASE}/accounts/{account_id}/r2/buckets/{BUCKET_NAME}/objects"
    params = []
    if prefix:
        params.append(f"prefix={urllib.parse.quote(prefix, safe='')}")
    if cursor:
        params.append(f"cursor={cursor}")
    params.append(f"limit={PAGE_SIZE}")
    if params:
        url += "?" + "&".join(params)
    
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                if data.get("success"):
                    result = data.get("result", {})
                    objects = result.get("objects", [])
                    cursor = result.get("cursor")
                    truncated = result.get("truncated", False)
                    return objects, cursor, truncated
                else:
                    print(f"[ERROR] API error: {data.get('errors')}")
                    return [], None, False
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                print(f"[ERROR] Failed after 3 attempts: {e}")
                return [], None, False

def main():
    parser = argparse.ArgumentParser(description="List R2 bucket objects via REST API")
    parser.add_argument("--prefix", help="Filter objects by prefix")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--count-only", action="store_true", help="Only show count")
    parser.add_argument("--account-id", help="Cloudflare account ID (auto-detected)")
    
    args = parser.parse_args()
    
    token = get_api_token()
    account_id = args.account_id or get_account_id(token)
    
    if not account_id:
        print("[ERROR] Could not determine Cloudflare account ID")
        sys.exit(1)
    
    all_objects = []
    cursor = None
    pages = 0
    
    while True:
        objects, cursor, truncated = list_objects(token, account_id, args.prefix, cursor)
        all_objects.extend(objects)
        pages += 1
        
        if not truncated or not cursor or len(all_objects) >= MAX_OBJECTS:
            break
    
    if args.count_only:
        print(f"Objects matching prefix '{args.prefix or '(all)'}': {len(all_objects)}")
    elif args.json:
        output = [
            {"key": obj.get("key"), "size": obj.get("size"), "etag": obj.get("etag"),
             "uploaded": obj.get("uploaded"), "httpMetadata": obj.get("httpMetadata")}
            for obj in all_objects
        ]
        print(json.dumps(output, indent=2))
    else:
        if not all_objects:
            print(f"No objects found with prefix '{args.prefix or '(all)'}'")
        else:
            # Sort by key for readability
            all_objects.sort(key=lambda o: o.get("key", ""))
            for obj in all_objects:
                key = obj.get("key", "")
                size = obj.get("size", 0)
                uploaded = obj.get("uploaded", "")[:19].replace("T", " ")
                print(f"  {size:>10,}  {uploaded}  {key}")
            print(f"\nTotal: {len(all_objects)} objects")

if __name__ == "__main__":
    main()
