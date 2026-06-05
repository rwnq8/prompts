#!/usr/bin/env python3
"""
fast_r2_upload.py — Cloudflare R2 REST API Uploader (v1.1 with retry+backoff)

Uses the Cloudflare REST API directly (NOT wrangler CLI) for high-speed uploads.
~250x faster than wrangler for batch operations.

Authentication: CLOUDFLARE_API_TOKEN env var, or ~/.cloudflare/api-token file.
Account ID is auto-detected from the token.

Usage:
    python fast_r2_upload.py <file> <r2_path>                    # Single upload
    python fast_r2_upload.py --batch <manifest.txt>              # Batch upload
    python fast_r2_upload.py --dir <local_dir> --prefix <r2_prefix>  # Directory upload

Manifest format (one per line):
    <local_path>|<r2_path>

RETRY LOGIC (v1.1):
    - HTTP 429 (Rate Limit): Wait Retry-After header, exponential backoff up to 5 retries
    - HTTP 500/502/503/504: Exponential backoff 1s, 2s, 4s, 8s, 16s (5 retries)
    - Connection errors: Exponential backoff same as 5xx
"""

import os
import sys
import json
import time
import hashlib
import argparse
import urllib.request
import urllib.error
import ssl

# ── Configuration ──────────────────────────────────────────────────
ACCOUNT_ID = None  # Auto-detected
BUCKET_NAME = "qnfo"
API_BASE = "https://api.cloudflare.com/client/v4"
MAX_RETRIES = 5
BASE_DELAY = 1.0  # seconds

# ── Token Management ───────────────────────────────────────────────
def get_api_token():
    """Get Cloudflare API token from env or file."""
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
    
    print("[ERROR] No Cloudflare API token found. Set CLOUDFLARE_API_TOKEN or create ~/.cloudflare/api-token")
    sys.exit(1)

def get_account_id(token):
    """Auto-detect account ID from token verification."""
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

# ── Retry Logic ────────────────────────────────────────────────────
def upload_with_retry(url, headers, data, filepath, max_retries=MAX_RETRIES):
    """Upload with exponential backoff retry for rate limits and server errors."""
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="PUT")
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read())
                if result.get("success"):
                    return True, result
                else:
                    errors = result.get("errors", [])
                    error_msg = "; ".join(e.get("message", str(e)) for e in errors)
                    raise Exception(f"API error: {error_msg}")
                    
        except urllib.error.HTTPError as e:
            status = e.code
            last_error = f"HTTP {status}"
            
            if status == 429:  # Rate limit
                retry_after = int(e.headers.get("Retry-After", "0"))
                delay = max(retry_after, BASE_DELAY * (2 ** attempt))
                if attempt < max_retries:
                    print(f"  [RATE-LIMIT] HTTP 429 — waiting {delay:.0f}s (attempt {attempt+1}/{max_retries})")
                    time.sleep(delay)
                    continue
            
            elif status in (500, 502, 503, 504):  # Server error
                delay = BASE_DELAY * (2 ** attempt)
                if attempt < max_retries:
                    print(f"  [SERVER-ERROR] HTTP {status} — retrying in {delay:.0f}s (attempt {attempt+1}/{max_retries})")
                    time.sleep(delay)
                    continue
            
            else:
                # Non-retryable HTTP error
                body = e.read().decode('utf-8', errors='replace')
                raise Exception(f"HTTP {status}: {body[:500]}")
                
        except (urllib.error.URLError, ConnectionError, TimeoutError, ssl.SSLError) as e:
            last_error = str(e)[:100]
            delay = BASE_DELAY * (2 ** attempt)
            if attempt < max_retries:
                print(f"  [CONN-ERROR] {last_error} — retrying in {delay:.0f}s (attempt {attempt+1}/{max_retries})")
                time.sleep(delay)
                continue
    
    return False, f"All {max_retries} retries exhausted. Last error: {last_error}"

# ── Upload Functions ───────────────────────────────────────────────
def upload_file(local_path, r2_path, token, account_id):
    """Upload a single file to R2."""
    if not os.path.exists(local_path):
        print(f"  [SKIP] File not found: {local_path}")
        return False, "File not found"
    
    file_size = os.path.getsize(local_path)
    
    # Compute SHA-256
    sha256 = hashlib.sha256()
    with open(local_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    
    url = f"{API_BASE}/accounts/{account_id}/r2/buckets/{BUCKET_NAME}/objects/{r2_path}"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    
    with open(local_path, 'rb') as f:
        file_data = f.read()
    
    success, result = upload_with_retry(url, headers, file_data, local_path)
    
    if success:
        print(f"  [OK] {local_path} → qnfo/{r2_path} ({file_size:,} bytes)")
    else:
        print(f"  [FAIL] {local_path} → qnfo/{r2_path}: {result}")
    
    return success, result

def upload_directory(local_dir, prefix, token, account_id):
    """Upload all files in a directory to R2."""
    total = 0
    success_count = 0
    
    for root, dirs, files in os.walk(local_dir):
        for filename in files:
            local_path = os.path.join(root, filename)
            if '__pycache__' in local_path or filename.endswith('.pyc'):
                continue
            rel_path = os.path.relpath(local_path, local_dir).replace('\\', '/')
            r2_path = f"{prefix}/{rel_path}"
            ok, _ = upload_file(local_path, r2_path, token, account_id)
            total += 1
            if ok:
                success_count += 1
    
    print(f"\nUpload complete: {success_count}/{total} files ({total - success_count} failures)")
    return success_count == total

def upload_batch(manifest_path, token, account_id):
    """Upload files from a manifest (local_path|r2_path per line)."""
    total = 0
    success_count = 0
    failures = []
    
    with open(manifest_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('|', 1)
            if len(parts) != 2:
                print(f"  [SKIP] Invalid manifest line: {line}")
                continue
            local_path, r2_path = parts[0].strip(), parts[1].strip()
            ok, err = upload_file(local_path, r2_path, token, account_id)
            total += 1
            if ok:
                success_count += 1
            else:
                failures.append((local_path, str(err)))
    
    print(f"\nBatch complete: {success_count}/{total} files")
    if failures:
        print(f"Failures ({len(failures)}):")
        for path, err in failures[:10]:
            print(f"  {path}: {err}")
    
    return success_count == total

# ── Main ────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Fast Cloudflare R2 uploader via REST API")
    parser.add_argument("file", nargs="?", help="Local file to upload")
    parser.add_argument("r2_path", nargs="?", help="R2 object path (e.g., qnfo/tools/script.py)")
    parser.add_argument("--batch", help="Batch upload from manifest file")
    parser.add_argument("--dir", help="Upload entire directory")
    parser.add_argument("--prefix", help="R2 prefix for directory upload")
    parser.add_argument("--account-id", help="Cloudflare account ID (auto-detected if not provided)")
    
    args = parser.parse_args()
    
    token = get_api_token()
    account_id = args.account_id or get_account_id(token)
    
    if not account_id:
        print("[ERROR] Could not determine Cloudflare account ID")
        sys.exit(1)
    
    print(f"Account: {account_id[:8]}... | Bucket: {BUCKET_NAME}")
    start_time = time.time()
    
    if args.batch:
        if not os.path.exists(args.batch):
            print(f"[ERROR] Manifest file not found: {args.batch}")
            sys.exit(1)
        ok = upload_batch(args.batch, token, account_id)
    elif args.dir:
        if not os.path.isdir(args.dir):
            print(f"[ERROR] Directory not found: {args.dir}")
            sys.exit(1)
        prefix = args.prefix or ""
        ok = upload_directory(args.dir, prefix, token, account_id)
    elif args.file and args.r2_path:
        ok, _ = upload_file(args.file, args.r2_path, token, account_id)
    else:
        parser.print_help()
        sys.exit(1)
    
    elapsed = time.time() - start_time
    print(f"Elapsed: {elapsed:.1f}s")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
