#!/usr/bin/env python3
"""
Read a specific email by index or search term.
Usage: python email_read.py --index N [--html] [--attachments-dir PATH] [--account NAME]
       python email_read.py --search "invoice" --index 0
"""
import argparse
import sys
import os

from _email_utils import resolve_store, get_folder_in_store

def main():
    parser = argparse.ArgumentParser(description="Read an Outlook email")
    parser.add_argument("--index", type=int, default=0, help="Message index (0=most recent)")
    parser.add_argument("--folder", default="inbox", help="Folder name")
    parser.add_argument("--search", default="", help="Filter: only messages matching this text")
    parser.add_argument("--html", action="store_true", help="Show HTML body instead of plain text")
    parser.add_argument("--attachments-dir", default="", help="Save attachments to this directory")
    parser.add_argument("--full", action="store_true", help="Show full body (no truncation)")
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

    target = None
    matched = 0
    for msg in messages:
        if args.search:
            text = f"{msg.Subject} {msg.SenderName} {msg.SenderEmailAddress} {msg.Body[:1000]}".lower()
            if args.search.lower() not in text:
                continue
        if matched == args.index:
            target = msg
            break
        matched += 1

    if target is None:
        print(f"ERROR: Message index {args.index} not found (matched {matched}).")
        sys.exit(5)

    print(f"Account:   {store_name}")
    print(f"From:      {target.SenderName} <{target.SenderEmailAddress}>")
    print(f"To:        {target.To}")
    if target.CC:
        print(f"CC:        {target.CC}")
    print(f"Date:      {target.ReceivedTime}")
    print(f"Subject:   {target.Subject}")
    print(f"Attachments: {target.Attachments.Count}")
    print(f"Size:      {target.Size} bytes")
    print(f"Read:      {not target.UnRead}")
    print("=" * 70)

    body = target.HTMLBody if args.html else target.Body
    if not args.full and len(body) > 5000:
        body = body[:5000] + f"\n\n... [TRUNCATED at 5000 chars, {len(target.Body)} total. Use --full to see all]"
    # Sanitize for Windows console (replace non-cp1252 chars)
    body_safe = body.encode("cp1252", errors="replace").decode("cp1252")
    print(body_safe)

    if args.attachments_dir and target.Attachments.Count > 0:
        os.makedirs(args.attachments_dir, exist_ok=True)
        for i, att in enumerate(target.Attachments):
            fpath = os.path.join(args.attachments_dir, att.FileName)
            att.SaveAsFile(fpath)
            print(f"\n[SAVED] {fpath} ({att.Size} bytes)")

if __name__ == "__main__":
    main()
