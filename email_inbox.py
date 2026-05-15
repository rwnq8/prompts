#!/usr/bin/env python3
"""
List recent emails from an Outlook folder.
Usage: python email_inbox.py [--folder NAME] [--limit N] [--unread-only]
"""
import argparse
import sys
import json

FOLDER_MAP = {
    "inbox": 6, "sent": 5, "drafts": 16, "deleted": 3,
    "outbox": 4, "junk": 23, "archive": 45,
}

def get_folder_id(name, namespace):
    """Resolve folder by name or return default folders by enum."""
    name_lower = name.lower()
    if name_lower in FOLDER_MAP:
        return namespace.GetDefaultFolder(FOLDER_MAP[name_lower])
    # Try recursive search for custom folders
    for folder in namespace.Folders:
        for f in _walk_folders(folder):
            if f.Name.lower() == name_lower:
                return f
    return None

def _walk_folders(folder):
    yield folder
    for sub in folder.Folders:
        yield from _walk_folders(sub)

def main():
    parser = argparse.ArgumentParser(description="List Outlook emails")
    parser.add_argument("--folder", default="inbox", help="Folder name (default: inbox)")
    parser.add_argument("--limit", type=int, default=20, help="Max messages (default: 20)")
    parser.add_argument("--unread-only", action="store_true", help="Show only unread")
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

    folder = get_folder_id(args.folder, namespace)
    if folder is None:
        print(f"ERROR: Folder '{args.folder}' not found.")
        sys.exit(3)

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
        print(json.dumps({"folder": args.folder, "count": len(results), "messages": results}, indent=2))
    else:
        print(f"Folder: {args.folder} ({len(results)} messages)")
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
