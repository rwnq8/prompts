#!/usr/bin/env python3
"""
List recent emails from an Outlook folder.
Usage: python email_inbox.py [--folder NAME] [--limit N] [--unread-only] [--account NAME]
"""
import argparse
import sys
import json

from _email_utils import resolve_store, get_folder_in_store

def main():
    parser = argparse.ArgumentParser(description="List Outlook emails")
    parser.add_argument("--folder", default="inbox", help="Folder name (default: inbox)")
    parser.add_argument("--limit", type=int, default=20, help="Max messages (default: 20)")
    parser.add_argument("--unread-only", action="store_true", help="Show only unread")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--account", default="rowan.quni@outlook.com", help="Account to use (default: rowan.quni@outlook.com)")
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

    try:
        folder = get_folder_in_store(store, args.folder)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(4)

    messages = folder.Items
    messages.Sort("[ReceivedTime]", True)

    results = []
    count = 0
    for msg in messages:
        if args.unread_only and not msg.UnRead:
            continue
        if count >= args.limit:
            break
        entry = {
            "index": count,
            "subject": str(msg.Subject),
            "sender_name": str(msg.SenderName),
            "sender_email": str(msg.SenderEmailAddress),
            "received": msg.ReceivedTime.strftime("%Y-%m-%d %H:%M"),
            "unread": bool(msg.UnRead),
            "has_attachments": bool(msg.Attachments.Count > 0),
            "size": msg.Size,
        }
        results.append(entry)
        count += 1

    if args.json:
        print(json.dumps({"account": store_name, "folder": args.folder, "count": len(results), "messages": results}, indent=2))
    else:
        print(f"Account: {store_name}  |  Folder: {args.folder}  |  {len(results)} messages")
        print("-" * 60)
        for entry in results:
            status = "[UNREAD]" if entry["unread"] else "        "
            attach = "[ATTACH]" if entry["has_attachments"] else "        "
            print(f"[{entry['index']:>3}] {entry['received']} {status} {attach}")
            print(f"      From: {entry['sender_name']} <{entry['sender_email']}>")
            print(f"      Subj: {entry['subject']}")
            print()

if __name__ == "__main__":
    main()
