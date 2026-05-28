#!/usr/bin/env python3
"""
vectorize-papers.py — Populate qwav-research Vectorize index with paper embeddings

Reads rendered paper HTML, extracts text, generates 768d embeddings via
Cloudflare Workers AI (bge-small-en-v1.5), and upserts to Vectorize index.

Usage:
  python tools/vectorize-papers.py              # Process all 412 papers
  python tools/vectorize-papers.py --limit 10   # Test with first 10
  python tools/vectorize-papers.py --dry-run    # Preview only

v1.0 — 2026-05-27
"""

import os
import sys
import re
import json
import time
import hashlib
import argparse
import subprocess
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError

# --- Configuration ---------------------------------------------------
CF_ACCOUNT_ID = "edb167b78c9fb901ea5bca3ce58ccc4b"
CF_TOKEN = "xI9xdmu0kCy8AYMkoaK-E9LSRsVEssF9QeJPjngaxfY.wqX_R6LtykAxKcCb8fvHMXqE_K2WPbhk5PEkItJCs3g"
AI_MODEL = "@cf/baai/bge-base-en-v1.5"
AI_ENDPOINT = "https://api.cloudflare.com/client/v4/accounts/{}/ai/run/{}".format(
    CF_ACCOUNT_ID, AI_MODEL)
VECTORIZE_INDEX = "qwav-research"
PAPERS_DIR = Path(r"G:\My Drive\QWAV\papers")
WRANGLER_CMD = r"C:\Users\LENOVO\AppData\Local\Programs\DeepChat\resources\app.asar.unpacked\runtime\node\wrangler.cmd"
MAX_CHARS_PER_CHUNK = 2000  # ~512 tokens per chunk for bge-base
CHUNK_OVERLAP = 200  # Characters of overlap between chunks
MAX_TOTAL_CHARS = 12000  # Extract up to 12K chars per paper (title + body sampling)


def extract_text(html_path):
    """Extract readable text from rendered paper HTML, sampling key sections."""
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    # Strip HTML tags
    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    
    if len(text) <= MAX_TOTAL_CHARS:
        return text
    
    # Smart sampling for long papers: beginning + middle + end
    first = text[:MAX_TOTAL_CHARS * 3 // 5]
    mid_start = len(text) // 3
    middle = text[mid_start:mid_start + MAX_TOTAL_CHARS // 5]
    last = text[-MAX_TOTAL_CHARS // 5:]
    return first + " " + middle + " " + last


def chunk_text(text, chunk_size=MAX_CHARS_PER_CHUNK, overlap=CHUNK_OVERLAP):
    """Split long text into overlapping chunks for embedding."""
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start:start + chunk_size]
        if len(chunk) < 100:
            break
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks if chunks else [text[:chunk_size]]


def get_embedding(text, dry_run=False):
    """Get 768d embedding from Workers AI."""
    if dry_run:
        return [0.0] * 768
    
    text_input = text[:MAX_CHARS_PER_PAPER]
    body = json.dumps({"text": [text_input]}).encode("utf-8")
    
    req = Request(
        AI_ENDPOINT,
        data=body,
        headers={
            "Authorization": "Bearer " + CF_TOKEN,
            "Content-Type": "application/json",
        },
    )
    
    try:
        with urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
        if result.get("success") and result.get("result", {}).get("data"):
            return result["result"]["data"][0]
        else:
            print("  [ERR] API: " + json.dumps(result.get("errors", []))[:200])
            return None
    except URLError as e:
        print("  [ERR] HTTP: " + str(e)[:200])
        return None


def upsert_batch(vectors, dry_run=False):
    """Upsert vectors to Vectorize index via wrangler (NDJSON format)."""
    if not vectors:
        return True
    
    if dry_run:
        print("  [DRY] Would upsert {} vectors".format(len(vectors)))
        return True
    
    # Write vectors as NDJSON (newline-delimited JSON, one object per line)
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".ndjson", delete=False, encoding="utf-8"
    ) as f:
        for v in vectors:
            f.write(json.dumps(v, ensure_ascii=False) + "\n")
        tmp_path = f.name
    
    result = subprocess.run(
        [WRANGLER_CMD, "vectorize", "upsert", VECTORIZE_INDEX, "--file", tmp_path],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120
    )
    
    os.unlink(tmp_path)
    
    if result.returncode == 0:
        return True
    else:
        print("  [ERR] Upsert: " + result.stderr[:300])
        return False


def main():
    parser = argparse.ArgumentParser(description="Populate qwav-research Vectorize index")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0, help="Limit papers (0=all)")
    parser.add_argument("--batch-size", type=int, default=10, help="Vectors per upsert batch")
    args = parser.parse_args()
    
    dry = args.dry_run
    limit = args.limit
    batch_size = args.batch_size
    mode = "DRY RUN" if dry else "LIVE"
    
    print("=" * 60)
    print("VECTORIZE PIPELINE v1.0 — " + mode)
    print("Model: {} (768d)".format(AI_MODEL))
    print("Index: {}".format(VECTORIZE_INDEX))
    print("=" * 60)
    
    # Scan papers
    html_files = sorted(PAPERS_DIR.glob("*.html"))
    # Filter out index.html and other non-paper files
    html_files = [f for f in html_files if f.name != "index.html"]
    
    if limit > 0:
        html_files = html_files[:limit]
    
    print("\n[SCAN] {} paper HTML files".format(len(html_files)))
    
    # Process papers
    vectors_batch = []
    processed = 0
    failed = 0
    start_time = time.time()
    
    for i, html_path in enumerate(html_files):
        title = html_path.stem
        slug = html_path.name
        
        # Extract text
        text = extract_text(html_path)
        if not text or len(text) < 50:
            print("[{} / {}] SKIP: {} ({} chars)".format(i + 1, len(html_files), title[:60], len(text)))
            continue
        
        # Get embedding
        embedding = get_embedding(text, dry_run=dry)
        if embedding is None:
            failed += 1
            continue
        
        # Generate stable ID
        paper_id = hashlib.md5(title.encode()).hexdigest()[:16]
        
        # Add to batch
        vectors_batch.append({
            "id": paper_id,
            "values": embedding,
            "metadata": {
                "title": title,
                "slug": slug,
                "url": "https://deep.qwav.tech/papers/" + slug,
                "chars": len(text),
            },
        })
        
        processed += 1
        
        # Upsert when batch is full
        if len(vectors_batch) >= batch_size:
            if not upsert_batch(vectors_batch, dry_run=dry):
                failed += len(vectors_batch)
                vectors_batch = []
            else:
                elapsed = time.time() - start_time
                rate = processed / max(elapsed, 0.1)
                print("[{} / {}] Upserted {} vectors ({:.0f}/min)".format(
                    processed, len(html_files), len(vectors_batch), rate * 60))
                vectors_batch = []
            
            time.sleep(0.5)  # Rate limiting
    
    # Final batch
    if vectors_batch:
        if not upsert_batch(vectors_batch, dry_run=dry):
            failed += len(vectors_batch)
        else:
            print("[{} / {}] Upserted final {} vectors".format(
                processed, len(html_files), len(vectors_batch)))
    
    elapsed = time.time() - start_time
    print("\n[DONE] {} / {} papers embedded ({:.0f}s, {:.1f}/min)".format(
        processed, len(html_files), elapsed, processed / max(elapsed / 60, 0.01)))
    print("  Embedded: {}".format(processed))
    print("  Failed: {}".format(failed))
    
    if dry:
        print("\n[DRY RUN] No embeddings generated. Remove --dry-run to execute.")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
