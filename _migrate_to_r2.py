#!/usr/bin/env python3
"""
MIGRATE ALL PROMPTS FILES TO R2 AS CANONICAL SOURCE.
Uploads everything under G:\My Drive\prompts\ (excluding .git, __pycache__, ephemeral _*)
to Cloudflare R2 under qnfo/prompts/.
"""
import os, sys, subprocess, json, hashlib
from pathlib import Path
from datetime import datetime

CANONICAL_ROOT = Path(r"G:\My Drive\prompts")
R2_PREFIX = "qnfo/prompts"

EXCLUDE_DIRS = {".git", "__pycache__", ".wrangler", ".deepchat"}
EXCLUDE_PREFIXES = ("_",)  # Ephemeral files
EXCLUDE_FILES = {".gitignore"}

def should_upload(path):
    """Check if a file should be uploaded to R2."""
    rel = path.relative_to(CANONICAL_ROOT)
    parts = rel.parts
    
    # Skip excluded directories
    for part in parts:
        if part in EXCLUDE_DIRS:
            return False
    
    # Skip ephemeral files
    if path.name.startswith("_"):
        return False
    
    # Skip excluded files
    if path.name in EXCLUDE_FILES:
        return False
    
    return True

def upload_file(local_path, r2_path):
    """Upload a single file to R2."""
    cmd = [
        "npx", "wrangler", "r2", "object", "put", r2_path,
        "--file", str(local_path), "--remote"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        return True, result.stdout.strip()
    else:
        return False, result.stderr.strip()

def main():
    print("=" * 70)
    print("PROMPTS → R2 MIGRATION")
    print(f"Time: {datetime.now().isoformat()}")
    print(f"Source: {CANONICAL_ROOT}")
    print(f"Target: {R2_PREFIX}/ on qnfo bucket")
    print("=" * 70)
    
    # Collect all files
    all_files = []
    for f in sorted(CANONICAL_ROOT.rglob("*")):
        if f.is_file() and should_upload(f):
            rel = str(f.relative_to(CANONICAL_ROOT)).replace("\\", "/")
            all_files.append((f, rel))
    
    print(f"\nFiles to upload: {len(all_files)}")
    
    # Group by directory
    dirs = {}
    for f, rel in all_files:
        d = str(Path(rel).parent)
        if d == ".":
            d = "(root)"
        dirs.setdefault(d, []).append(rel)
    
    for d in sorted(dirs):
        print(f"  {d}: {len(dirs[d])} files")
    
    # Upload
    print(f"\n--- UPLOADING ---")
    results = {"success": [], "failed": []}
    
    for i, (local_path, rel) in enumerate(all_files):
        r2_path = f"{R2_PREFIX}/{rel}"
        print(f"  [{i+1}/{len(all_files)}] {rel} ({local_path.stat().st_size:,}B)...", end=" ")
        
        ok, msg = upload_file(local_path, r2_path)
        if ok:
            results["success"].append(rel)
            print("OK")
        else:
            results["failed"].append((rel, msg))
            print(f"FAILED: {msg[:100]}")
    
    # Summary
    print(f"\n--- RESULTS ---")
    print(f"  Uploaded: {len(results['success'])} files")
    print(f"  Failed:   {len(results['failed'])} files")
    
    if results["failed"]:
        print("\n  FAILURES:")
        for rel, msg in results["failed"]:
            print(f"    {rel}: {msg[:200]}")
    
    # Write manifest
    manifest = {
        "migrated_at": datetime.now().isoformat(),
        "source": str(CANONICAL_ROOT),
        "r2_prefix": R2_PREFIX,
        "total_files": len(all_files),
        "uploaded": len(results["success"]),
        "failed": len(results["failed"]),
        "success_files": results["success"],
        "failed_files": [f[0] for f in results["failed"]]
    }
    
    manifest_path = CANONICAL_ROOT / "_MIGRATION_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\n  Manifest written to {manifest_path}")
    
    # Also upload the manifest itself
    print("\n  Uploading manifest...")
    ok, _ = upload_file(manifest_path, f"{R2_PREFIX}/MIGRATION_MANIFEST.json")
    print(f"  {'OK' if ok else 'FAILED'}")
    
    return len(results["failed"]) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
