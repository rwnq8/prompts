#!/usr/bin/env python3
"""
Read a specific email by index or search term.
Usage: python email_read.py --index N [--html] [--attachments-dir PATH]
       python email_read.py --search "invoice" --index 0
"""
import argparse
import sys
import os

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
    parser = argparse.ArgumentParser(description="Read an Outlook email")
    parser.add_argument("--index", type=int, default=0, help="Message index (0=most recent)")
    parser.add_argument("--folder", default="inbox", help="Folder name")
    parser.add_argument("--search", default="", help="Filter: only messages matching this text")
    parser.add_argument("--html", action="store_true", help="Show HTML body instead of plain text")
    parser.add_argument("--attachments-dir", default="", help="Save attachments to this directory")
    parser.add_argument("--full", action="store_true", help="Show full body (no truncation)")
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

    # Find target message
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
        sys.exit(4)

    # Display header
    print(f"From:      {target.SenderName} <{target.SenderEmailAddress}>")
    print(f"To:        {target.To}")
    if target.CC:
        print(f"CC:        {target.CC}")
    if target.BCC:
        print(f"BCC:       {target.BCC}")
    print(f"Date:      {target.ReceivedTime}")
    print(f"Subject:   {target.Subject}")
    print(f"Attachments: {target.Attachments.Count}")
    print(f"Size:      {target.Size} bytes")
    print(f"Read:      {not target.UnRead}")
    print("=" * 70)

    # Display body
    body = target.HTMLBody if args.html else target.Body
    if not args.full and len(body) > 5000:
        body = body[:5000] + f"\n\n... [TRUNCATED at 5000 chars, {len(target.Body)} total. Use --full to see all]"
    print(body)

    # Save attachments
    if args.attachments_dir and target.Attachments.Count > 0:
        os.makedirs(args.attachments_dir, exist_ok=True)
        for i, att in enumerate(target.Attachments):
            fpath = os.path.join(args.attachments_dir, att.FileName)
            att.SaveAsFile(fpath)
            print(f"\n[SAVED] {fpath} ({att.Size} bytes)")

if __name__ == "__main__":
    main()
