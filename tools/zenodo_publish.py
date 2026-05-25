#!/usr/bin/env python3
"""
Zenodo API Client --- Autonomous DOI Registration

Creates Zenodo depositions, uploads files, adds metadata, and publishes.
Supports both sandbox (testing) and production.

Usage:
  # Test with sandbox (no real DOI):
  python zenodo_publish.py --sandbox --token YOUR_TOKEN --title "..." --author "..." --file "paper.pdf"

  # Production (creates real DOI):
  python zenodo_publish.py --token YOUR_TOKEN --title "Title" --author "Author" --file "paper.md"
  
  # With full metadata:
  python zenodo_publish.py --token TOKEN --title "..." --author "..." --file "paper.pdf" --abstract "..." --keywords "kw1,kw2" --doi "10.5281/zenodo.XXXXXXXX"  # for new versions

Token source: https://zenodo.org/account/settings/applications/
Create a "Personal access token" with "deposit:actions" and "deposit:write" scopes.
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime

# -- API Endpoints -----------------------------------------
PRODUCTION = "https://zenodo.org/api"
SANDBOX = "https://sandbox.zenodo.org/api"

# -- Custom License Registry -------------------------------
# Maps license identifiers to metadata for Zenodo's 'rights' field.
# Standard SPDX licenses use the 'license' metadata field directly.
# Custom licenses (not in SPDX) use the 'rights' metadata field.
CUSTOM_LICENSES = {
    "QNFO-1.1": {
        "title": "QNFO Content License Agreement v1.1",
        "description": (
            "Non-commercial, non-transferable, revocable license. "
            "Full terms: https://github.com/QNFO/license/"
        ),
        "uri": "https://github.com/QNFO/license/",
    }
}


def extract_yaml_license(file_path):
    """Extract 'license' from YAML frontmatter of a markdown file.

    Supports .md, .qmd, .rmd, .yaml, .yml files.
    Recognises both 'license:' and 'licence:' spelling.
    Returns the license identifier string, or None if not found.
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ('.md', '.qmd', '.rmd', '.yaml', '.yml'):
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(8192)
    except (OSError, UnicodeDecodeError):
        return None

    if not content.startswith('---'):
        return None

    end_idx = content.find('\n---', 3)
    if end_idx < 0:
        return None

    frontmatter = content[3:end_idx]
    for line in frontmatter.split('\n'):
        line = line.strip()
        if line.startswith('license:') or line.startswith('licence:'):
            val = line.split(':', 1)[1].strip()
            val = val.strip('"').strip("'").strip()
            return val if val else None
    return None

# -- Core API Functions ------------------------------------

def api_request(method, url, token, data=None, file_path=None):
    """Make an authenticated request to Zenodo API."""
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    body = None
    if data is not None and file_path is None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"  API Error [{e.code}]: {error_body[:500]}")
        return None


def upload_file(deposition_id, file_path, token, base_url):
    """Upload a file to a Zenodo deposition using the bucket URL."""
    # Get deposition to find bucket URL
    dep_url = f"{base_url}/deposit/depositions/{deposition_id}"
    dep = api_request("GET", dep_url, token)
    if not dep:
        return None
    
    bucket_url = dep.get("links", {}).get("bucket", "")
    if not bucket_url:
        print("  No bucket URL found in deposition")
        return None
    
    filename = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    print(f"  Uploading: {filename} ({file_size:,} bytes)")
    print(f"  Bucket: {bucket_url}/{filename}")
    
    # Upload file
    upload_url = f"{bucket_url}/{urllib.parse.quote(filename)}"
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    req = urllib.request.Request(upload_url, data=file_data, method="PUT")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/octet-stream")
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            print(f"  [OK] Uploaded: {result.get('key', filename)}")
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"  Upload failed [{e.code}]: {error_body[:500]}")
        return None


def create_deposition(token, base_url):
    """Create a new empty deposition."""
    url = f"{base_url}/deposit/depositions"
    data = {}  # Empty deposition
    result = api_request("POST", url, token, data=data)
    if result:
        print(f"  Created deposition ID: {result['id']}")
        return result
    return None


def update_metadata(deposition_id, metadata, token, base_url):
    """Update metadata for a deposition."""
    url = f"{base_url}/deposit/depositions/{deposition_id}"
    data = {"metadata": metadata}
    result = api_request("PUT", url, token, data=data)
    if result:
        print(f"  [OK] Metadata updated")
        return result
    return None


def publish_deposition(deposition_id, token, base_url):
    """Publish a deposition --- this makes it public and assigns a DOI."""
    url = f"{base_url}/deposit/depositions/{deposition_id}/actions/publish"
    result = api_request("POST", url, token)
    if result:
        doi = result.get("doi", "UNKNOWN")
        print(f"  [OK] Published! DOI: {doi}")
        return result
    return None


# -- Main --------------------------------------------------

def build_metadata(args):
    """Build metadata dict from CLI args.

    License resolution priority:
      1. YAML frontmatter in the uploaded file
      2. Explicit --license CLI flag
      3. Default (QNFO-1.1)
    """
    today = datetime.now().strftime("%Y-%m-%d")

    # -- License resolution --
    license_id = None
    source = "default"

    # 1. Try YAML frontmatter
    if args.file:
        yaml_lic = extract_yaml_license(args.file)
        if yaml_lic:
            license_id = yaml_lic
            source = "YAML frontmatter"

    # 2. CLI flag
    if not license_id and args.license:
        license_id = args.license
        source = "CLI --license"

    # 3. Default
    if not license_id:
        license_id = "QNFO-1.1"

    print(f"  License: {license_id} (source: {source})")

    # -- Build metadata --
    metadata = {
        "title": args.title,
        "upload_type": args.upload_type or "publication",
        "publication_date": args.date or today,
        "creators": [
            {
                "name": args.author,
                "orcid": args.orcid or "0009-0002-4317-5604"
            }
        ],
        "description": args.abstract or args.title,
        "access_right": "open",
        "language": "eng",
    }

    # License: custom licenses use 'rights' field (per Zenodo Issue #2547).
    # Standard SPDX licenses use the 'license' field directly.
    if license_id in CUSTOM_LICENSES:
        custom = CUSTOM_LICENSES[license_id]
        metadata["rights"] = [
            {
                "rights": custom["title"],
                "rightsUri": custom["uri"],
                "rightsIdentifier": license_id,
                "rightsIdentifierScheme": "other",
            }
        ]
        # Zenodo API requires a valid SPDX identifier in 'license'.
        # The 'rights' field carries the actual license displayed to users.
        metadata["license"] = "cc-by-4.0"
    else:
        metadata["license"] = license_id

    if args.keywords:
        metadata["keywords"] = [k.strip() for k in args.keywords.split(",")]

    if args.doi:
        metadata["doi"] = args.doi

    return metadata


def main():
    parser = argparse.ArgumentParser(
        description="Zenodo API Client --- Autonomous DOI Registration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test in sandbox first:
  python zenodo_publish.py --sandbox --token YOUR_TOKEN --title "Test" --author "Name" --file "test.md"

  # Production publication:
  python zenodo_publish.py --token TOKEN --title "Paper Title" --author "Author" --file "paper.md" --abstract "..." --keywords "kw1,kw2"

Token: Visit https://zenodo.org/account/settings/applications/
       Create token with "deposit:actions" and "deposit:write" scopes.
        """
    )
    
    parser.add_argument("--token", help="Zenodo API token (or set ZENODO_TOKEN env var)")
    parser.add_argument("--sandbox", action="store_true", help="Use sandbox (test) environment")
    parser.add_argument("--title", required=True, help="Publication title")
    parser.add_argument("--author", required=True, help="Author name (format: 'Last, First')")
    parser.add_argument("--orcid", help="Author ORCID (default: 0009-0002-4317-5604)")
    parser.add_argument("--file", required=True, help="Path to file to upload")
    parser.add_argument("--abstract", help="Publication abstract")
    parser.add_argument("--keywords", help="Comma-separated keywords")
    parser.add_argument("--upload-type", help="Zenodo upload type (publication, poster, presentation, dataset, etc.)")
    parser.add_argument("--license", default=None, help="License identifier (default: QNFO-1.1; use cc-by-4.0, mit, etc. for standard licenses)")
    parser.add_argument("--date", help="Publication date (YYYY-MM-DD, default: today)")
    parser.add_argument("--doi", help="DOI for new version of existing record")
    
    args = parser.parse_args()
    
    # Token resolution
    token = args.token or os.environ.get("ZENODO_TOKEN")
    if not token:
        print("\nERROR: No Zenodo token provided.")
        print("  Option A: --token YOUR_TOKEN")
        print("  Option B: set ZENODO_TOKEN environment variable")
        print("  Get token: https://zenodo.org/account/settings/applications/")
        sys.exit(1)
    
    # Validate file
    if not os.path.exists(args.file):
        print(f"\nERROR: File not found: {args.file}")
        sys.exit(1)
    
    base_url = SANDBOX if args.sandbox else PRODUCTION
    env_name = "SANDBOX (testing)" if args.sandbox else "PRODUCTION"
    
    print(f"\n{'='*60}")
    print(f"ZENODO {env_name} PUBLICATION")
    print(f"{'='*60}")
    print(f"  Title: {args.title}")
    print(f"  Author: {args.author}")
    print(f"  File: {args.file}")
    print(f"  Environment: {env_name}")
    print(f"{'='*60}\n")
    
    # Step 1: Create deposition
    print("Step 1: Creating deposition...")
    dep = create_deposition(token, base_url)
    if not dep:
        print("FAILED: Could not create deposition.")
        sys.exit(1)
    
    deposition_id = dep["id"]
    
    # Step 2: Build and set metadata
    print("\nStep 2: Setting metadata...")
    metadata = build_metadata(args)
    dep = update_metadata(deposition_id, metadata, token, base_url)
    if not dep:
        print("WARNING: Metadata update issue, continuing...")
    
    # Step 3: Upload file
    print("\nStep 3: Uploading file...")
    file_result = upload_file(deposition_id, args.file, token, base_url)
    if not file_result:
        print("FAILED: Could not upload file.")
        sys.exit(1)
    
    # Step 4: Publish
    if args.sandbox:
        print(f"\nStep 4: [SANDBOX] Would publish here. Testing complete.")
        print(f"  Deposition ID: {deposition_id}")
        print(f"  View at: {base_url.replace('/api', '')}/deposit/{deposition_id}")
    else:
        print(f"\n[WARN]  WARNING: You are about to PUBLISH to Zenodo PRODUCTION.")
        print(f"  This will create a real DOI that cannot be deleted.")
        confirm = input("  Type 'PUBLISH' to confirm: ")
        if confirm.strip() != "PUBLISH":
            print("  Cancelled. Deposition saved as draft.")
            print(f"  View at: https://zenodo.org/deposit/{deposition_id}")
            sys.exit(0)
        
        print("\nStep 4: Publishing...")
        result = publish_deposition(deposition_id, token, base_url)
        if not result:
            print("FAILED: Could not publish.")
            sys.exit(1)
        
        doi = result.get("doi", "UNKNOWN")
        print(f"\n{'='*60}")
        print(f"PUBLISHED SUCCESSFULLY")
        print(f"{'='*60}")
        print(f"  Title: {result.get('title', '')}")
        print(f"  DOI: {doi}")
        print(f"  URL: https://doi.org/{doi}")
        print(f"  Zenodo: {result.get('links', {}).get('html', '')}")
        print(f"{'='*60}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
