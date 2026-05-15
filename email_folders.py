#!/usr/bin/env python3
"""
List available Outlook folders.
Usage: python email_folders.py [--json]
"""
import argparse
import sys
import json

def _walk(folder, depth=0):
    """Recursively walk folders with depth tracking."""
    results = []
    info = {
        "name": folder.Name,
        "path": folder.FolderPath,
        "depth": depth,
        "item_count": folder.Items.Count,
        "unread_count": folder.UnReadItemCount if hasattr(folder, 'UnReadItemCount') else None,
    }
    results.append(info)
    for sub in folder.Folders:
        results.extend(_walk(sub, depth + 1))
    return results

def main():
    parser = argparse.ArgumentParser(description="List Outlook folders")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    try:
        import win32com.client
    except ImportError:
        print("ERROR: pywin32 is not installed. Run: pip install pywin32")
        sys.exit(1)

    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
    except Exception as e:
        print(f"ERROR: Cannot connect to Outlook. Is it running? ({e})")
        sys.exit(2)

    all_folders = []
    for store in namespace.Folders:
        all_folders.extend(_walk(store))

    if args.json:
        print(json.dumps({"store_count": len(list(namespace.Folders)), "folders": all_folders}, indent=2))
    else:
        for f in all_folders:
            indent = "  " * f["depth"]
            unread = f" [{f['unread_count']} unread]" if f["unread_count"] else ""
            print(f"{indent}{f['name']} ({f['item_count']} items){unread}")

if __name__ == "__main__":
    main()
