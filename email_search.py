#!/usr/bin/env python3
"""
Search Outlook emails across folders.
Usage: python email_search.py "keyword" [--folder inbox] [--limit 20] [--body-search]
"""
import argparse
import sys
import json

FOLDER_MAP = {
    "inbox": 6, "sent": 5, "drafts": 16, "deleted": 3,
    "outbox": 4, "junk": 23, "archive": 45,
}

def get_folder(name, namespace):
    name_lower = name.lower()
    if name_lower in FOLDER_MAP:
        return namespace.GetDefaultFolder(FOLDER_MAP[name_lower])
    for fld in namespace.Folders:
        for f in _walk(fld):
            if f.Name.lower() == name_lower:
                return f
    return None

def _walk(folder):
    yield folder
    for sub in folder.Folders:
        yield from _walk(sub)

def main():
    parser = argparse.ArgumentParser(description="Search Outlook emails")
    parser.add_argument("query", nargs="?", default="", help="Search query")
    parser.add_argument("--folder", default="inbox", help="Folder to search (default: inbox)")
    parser.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    parser.add_argument("--body-search", action="store_true", help="Search email body too (slower)")
    parser.add_argument("--sender", default="", help="Filter by sender name/email")
    parser.add_argument("--since", default="", help="Only after date (YYYY-MM-DD)")
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

    folder = get_folder(args.folder, namespace)
    if folder is None:
        print(f"ERROR: Folder '{args.folder}' not found.")
        sys.exit(3)

    messages = folder.Items
    messages.Sort("[ReceivedTime]", True)

    query_lower = args.query.lower() if args.query else ""
    sender_lower = args.sender.lower() if args.sender else ""

    results = []
    for msg in messages:
        if len(results) >= args.limit:
            break

        # Date filter
        if args.since:
            try:
                from datetime import datetime
                since_dt = datetime.strptime(args.since, "%Y-%m-%d")
                if msg.ReceivedTime.replace(tzinfo=None) < since_dt:
                    continue
            except ValueError:
                pass

        # Sender filter
        if sender_lower:
            sname = str(msg.SenderName).lower()
            smail = str(msg.SenderEmailAddress).lower()
            if sender_lower not in sname and sender_lower not in smail:
                continue

        # Text search
        if query_lower:
            text = str(msg.Subject).lower()
            if args.body_search:
                text += " " + str(msg.Body[:2000]).lower()
            if query_lower not in text:
                continue

        results.append({
            "subject": str(msg.Subject),
            "sender_name": str(msg.SenderName),
            "sender_email": str(msg.SenderEmailAddress),
            "received": msg.ReceivedTime.strftime("%Y-%m-%d %H:%M"),
            "unread": bool(msg.UnRead),
            "has_attachments": bool(msg.Attachments.Count > 0),
            "body_preview": str(msg.Body)[:300].replace("\n", " "),
        })

    if args.json:
        print(json.dumps({"query": args.query, "count": len(results), "results": results}, indent=2))
    else:
        print(f"Search: '{args.query}' in {args.folder} — {len(results)} results")
        print("-" * 60)
        for i, r in enumerate(results):
            status = "[UNREAD]" if r["unread"] else ""
            attach = "[ATTACH]" if r["has_attachments"] else ""
            print(f"[{i}] {r['received']} {status} {attach}")
            print(f"    {r['sender_name']} <{r['sender_email']}>")
            print(f"    {r['subject']}")
            print(f"    ...{r['body_preview'][:150]}")
            print()

if __name__ == "__main__":
    main()
