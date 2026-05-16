#!/usr/bin/env python3
"""
List available Outlook folders.
Usage: python email_folders.py [--json] [--account NAME]
"""
import argparse
import sys
import json

from _email_utils import resolve_store, get_all_folders

def main():
    parser = argparse.ArgumentParser(description="List Outlook folders")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--account", default="rowan.quni@outlook.com", help="Account to use")
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

    try:
        store, store_name = resolve_store(namespace, args.account)
    except (ValueError, RuntimeError) as e:
        print(f"ERROR: {e}")
        sys.exit(3)

    all_folders = get_all_folders(store)

    if args.json:
        print(json.dumps({"account": store_name, "folders": all_folders}, indent=2))
    else:
        print(f"Account: {store_name}")
        for f in all_folders:
            unread = f" [{f['unread_count']} unread]" if f['unread_count'] else ""
            print(f"  {f['name']} ({f['item_count']} items){unread}")

if __name__ == "__main__":
    main()
