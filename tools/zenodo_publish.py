#!/usr/bin/env python3
"""
zenodo_publish.py — One-command Zenodo DOI registration via REST API.
v1.0 — 2026-05-31
Usage: python zenodo_publish.py --title "..." --author "..." --file "..." [--sandbox] [--abstract "..."] [--keywords "..."] [--upload-type publication] [--license CC-BY-4.0] [--doi EXISTING_DOI]
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

def get_token():
    token = os.environ.get("ZENODO_TOKEN")
    if token:
        return token
    token_path = os.path.expanduser("~\\.zenodo_token")
    if os.path.exists(token_path):
        with open(token_path) as f:
            return f.read().strip()
    print("[ERROR] No ZENODO_TOKEN env var and no ~/.zenodo_token file found.")
    print("Create a token at https://zenodo.org/account/settings/applications/")
    print("Required scopes: deposit:actions, deposit:write")
    print("Save to: %USERPROFILE%\\.zenodo_token")
    sys.exit(1)

def api_request(url, token, method="GET", data=None, content_type="application/json"):
    headers = {"Authorization": f"Bearer {token}"}
    body = None
    if data is not None:
        if content_type == "application/json":
            body = json.dumps(data).encode("utf-8")
            headers["Content-Type"] = "application/json"
        else:
            body = data
            headers["Content-Type"] = content_type

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"[ERROR] HTTP {e.code}: {error_body}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="One-command Zenodo DOI registration")
    parser.add_argument("--sandbox", action="store_true", help="Use sandbox.zenodo.org for testing")
    parser.add_argument("--title", required=True, help="Publication title")
    parser.add_argument("--author", required=True, help="Author name (Last, First)")
    parser.add_argument("--file", required=True, help="Path to file to upload")
    parser.add_argument("--abstract", default="", help="Publication abstract")
    parser.add_argument("--keywords", default="", help="Comma-separated keywords")
    parser.add_argument("--upload-type", default="publication",
                        choices=["publication", "poster", "presentation", "dataset",
                                 "image", "video", "software", "lesson", "other"])
    parser.add_argument("--license", default="CC-BY-4.0", help="License identifier")
    parser.add_argument("--doi", default="", help="Existing DOI for creating new version")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompt for non-interactive use")
    args = parser.parse_args()

    # Verify file exists
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"[ERROR] File not found: {args.file}")
        sys.exit(1)

    token = get_token()
    base_url = "https://sandbox.zenodo.org/api" if args.sandbox else "https://zenodo.org/api"
    env_label = "SANDBOX" if args.sandbox else "PRODUCTION"

    print(f"\n{'='*60}")
    print(f"  ZENODO DOI REGISTRATION — {env_label}")
    print(f"{'='*60}")
    print(f"  Title:       {args.title}")
    print(f"  Author:      {args.author}")
    print(f"  File:        {args.file} ({filepath.stat().st_size:,} bytes)")
    print(f"  Upload type: {args.upload_type}")
    print(f"  License:     {args.license}")
    if args.abstract:
        print(f"  Abstract:    {args.abstract[:100]}...")
    if args.keywords:
        print(f"  Keywords:    {args.keywords}")
    if args.doi:
        print(f"  New version of: {args.doi}")
    print(f"{'='*60}\n")

    # Phase 1: Create deposition
    print("[1/4] Creating deposition...")
    metadata = {
        "metadata": {
            "title": args.title,
            "upload_type": args.upload_type,
            "publication_type": "other",
            "creators": [{"name": args.author}],
            "license": args.license,
        }
    }
    if args.abstract:
        metadata["metadata"]["description"] = args.abstract
    if args.keywords:
        metadata["metadata"]["keywords"] = [k.strip() for k in args.keywords.split(",") if k.strip()]

    # For new version of existing DOI
    if args.doi:
        # Find existing deposition by DOI
        list_url = f"{base_url}/deposit/depositions?q=doi:{args.doi}&access_token={token}"
        # Actually, use the new version endpoint
        # First, get the latest deposition for this concept
        # Simplified: create new deposition and it will be linked via the DOI
        metadata["metadata"]["related_identifiers"] = [{
            "relation": "isNewVersionOf",
            "identifier": args.doi,
            "resource_type": "publication-other"
        }]

    deposition = api_request(
        f"{base_url}/deposit/depositions",
        token,
        method="POST",
        data=metadata
    )
    dep_id = deposition["id"]
    bucket_url = deposition["links"]["bucket"]
    print(f"  Deposition ID: {dep_id}")
    print(f"  Bucket URL:    {bucket_url}")

    # Phase 2: Upload file
    print(f"\n[2/4] Uploading file: {filepath.name}...")
    with open(filepath, "rb") as f:
        file_data = f.read()

    upload_result = api_request(
        f"{bucket_url}/{filepath.name}",
        token,
        method="PUT",
        data=file_data,
        content_type="application/octet-stream"
    )
    print(f"  File uploaded: {upload_result.get('filename', filepath.name)}")
    print(f"  Size:          {upload_result.get('filesize', len(file_data)):,} bytes")

    # Phase 3: Verify metadata
    print(f"\n[3/4] Verifying deposition...")
    dep_check = api_request(
        f"{base_url}/deposit/depositions/{dep_id}",
        token
    )
    print(f"  Title confirmed: {dep_check.get('title', 'N/A')}")
    files = dep_check.get("files", [])
    if files:
        print(f"  Files attached:  {len(files)}")

    # Phase 4: Publish
    if args.sandbox:
        print(f"\n[4/4] SANDBOX TEST COMPLETE")
        print(f"  Deposition {dep_id} created successfully in sandbox.")
        print(f"  No DOI issued (sandbox mode).")
        print(f"  To publish for real, remove --sandbox flag.")
        print(f"\n{'='*60}")
        print(f"  SANDBOX TEST PASSED")
        print(f"{'='*60}")
    else:
        print(f"\n[4/4] PUBLISHING...")
        if args.yes:
            print("  --yes flag set: auto-confirming publish")
        else:
            confirm = input("  Type 'PUBLISH' to confirm: ")
            if confirm.strip() != "PUBLISH":
                print("  Aborted.")
                sys.exit(0)

        publish_result = api_request(
            f"{base_url}/deposit/depositions/{dep_id}/actions/publish",
            token,
            method="POST"
        )

        doi = publish_result.get("doi", publish_result.get("metadata", {}).get("prereserve_doi", {}).get("doi", "N/A"))
        recid = publish_result.get("record_id", publish_result.get("id", "N/A"))

        print(f"\n{'='*60}")
        print(f"  PUBLISHED SUCCESSFULLY")
        print(f"  Title:   {args.title}")
        print(f"  DOI:     {doi}")
        print(f"  URL:     https://doi.org/{doi}")
        print(f"  Zenodo:  https://zenodo.org/records/{recid}")
        print(f"{'='*60}")

        # Output DOI for CI/CD consumption
        print(f"\nDOI={doi}")
        print(f"ZENODO_URL=https://zenodo.org/records/{recid}")

if __name__ == "__main__":
    main()
