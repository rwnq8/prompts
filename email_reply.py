#!/usr/bin/env python3
"""
Reply to or forward an email.
Usage: python email_reply.py --index 3 --body "Thanks!"
       python email_reply.py --index 0 --body "FYI" --forward
       python email_reply.py --search "invoice" --index 0 --body "Received, thanks"
"""
import argparse
import sys

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
    parser = argparse.ArgumentParser(description="Reply to or forward an Outlook email")
    parser.add_argument("--index", type=int, default=0, help="Message index (0=most recent)")
    parser.add_argument("--folder", default="inbox", help="Folder name")
    parser.add_argument("--search", default="", help="Filter messages by text before indexing")
    parser.add_argument("--body", required=True, help="Reply body text")
    parser.add_argument("--forward", action="store_true", help="Forward instead of reply")
    parser.add_argument("--reply-all", action="store_true", help="Reply to all recipients")
    parser.add_argument("--draft", action="store_true", help="Save as draft instead of sending")
    parser.add_argument("--attachment", action="append", default=[], help="Additional attachment (repeatable)")
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

    target = None
    matched = 0
    for msg in messages:
        if args.search:
            text = f"{msg.Subject} {msg.SenderName} {msg.Body[:500]}".lower()
            if args.search.lower() not in text:
                continue
        if matched == args.index:
            target = msg
            break
        matched += 1

    if target is None:
        print(f"ERROR: Message index {args.index} not found (matched {matched}).")
        sys.exit(4)

    try:
        # Create reply or forward
        if args.forward:
            reply = target.Forward()
            action = "FORWARD"
        elif args.reply_all:
            reply = target.ReplyAll()
            action = "REPLY ALL"
        else:
            reply = target.Reply()
            action = "REPLY"

        # Set body (prepended before original)
        reply.Body = args.body + "\n\n" + reply.Body

        # Additional attachments
        for fpath in args.attachment:
            reply.Attachments.Add(fpath)

        if args.draft:
            reply.Save()
            print(f"DRAFT {action} saved: Re: {target.Subject}")
        else:
            reply.Send()
            print(f"SENT {action} to: Re: {target.Subject}")

    except Exception as e:
        print(f"ERROR: Failed. {e}")
        sys.exit(5)

if __name__ == "__main__":
    main()
