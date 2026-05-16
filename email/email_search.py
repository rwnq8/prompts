#!/usr/bin/env python3
"""
Search Outlook emails across folders.
Usage: python email_search.py "keyword" [--folder inbox] [--limit 20] [--body-search] [--account NAME]
"""
import argparse
import sys
import json

from _email_utils import resolve_store, get_folder_in_store

def main():
    parser = argparse.ArgumentParser(description="Search Outlook emails")
    parser.add_argument("query", nargs="?", default="", help="Search query")
    parser.add_argument("--folder", default="inbox", help="Folder to search (default: inbox)")
    parser.add_argument("--limit", type=int, default=20, help="Max results (default: 20)")
    parser.add_argument("--body-search", action="store_true", help="Search email body too (slower)")
    parser.add_argument("--sender", default="", help="Filter by sender name/email")
    parser.add_argument("--since", default="", help="Only after date (YYYY-MM-DD)")
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

    try:
        folder = get_folder_in_store(store, args.folder)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(4)

    messages = folder.Items
    messages.Sort("[ReceivedTime]", True)

    query_lower = args.query.lower() if args.query else ""
    sender_lower = args.sender.lower() if args.sender else ""

    results = []
    for msg in messages:
        if len(results) >= args.limit:
            break
        if args.since:
            try:
                from datetime import datetime
                since_dt = datetime.strptime(args.since, "%Y-%m-%d")
                if msg.ReceivedTime.replace(tzinfo=None) < since_dt:
                    continue
            except ValueError:
                pass
        if sender_lower:
            sname = str(msg.SenderName).lower()
            smail = str(msg.SenderEmailAddress).lower()
            if sender_lower not in sname and sender_lower not in smail:
                continue
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
        print(json.dumps({"account": store_name, "query": args.query, "count": len(results), "results": results}, indent=2))
    else:
        print(f"Account: {store_name}  |  Search: '{args.query}' in {args.folder}  |  {len(results)} results")
        print("-" * 60)
        for i, r in enumerate(results):
            status = "[UNREAD]" if r["unread"] else ""
            attach = "[ATTACH]" if r["has_attachments"] else ""
            print(f"[{i}] {r['received']} {status} {attach}")
            print(f"    {r['sender_name']} <{r['sender_email']}>")
            print(f"    {r['subject']}")
            if args.body_search:
                print(f"    ...{r['body_preview'][:150]}")
            print()

if __name__ == "__main__":
    main()
