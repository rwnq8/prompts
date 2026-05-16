#!/usr/bin/env python3
"""
Reply to or forward an email.
Usage: python email_reply.py --index 3 --body "Thanks!" [--account NAME]
"""
import argparse
import sys

from _email_utils import resolve_store, get_folder_in_store, resolve_account

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

    try:
        account = resolve_account(namespace, args.account)
    except (ValueError, RuntimeError) as e:
        print(f"ERROR: {e}")
        sys.exit(5)

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
        sys.exit(5)

    try:
        if args.forward:
            reply = target.Forward()
            action = "FORWARD"
        elif args.reply_all:
            reply = target.ReplyAll()
            action = "REPLY ALL"
        else:
            reply = target.Reply()
            action = "REPLY"

        reply.SendUsingAccount = account
        # Set body and attachments
        reply.Body = args.body + "\n\n" + reply.Body

        for fpath in args.attachment:
            reply.Attachments.Add(fpath)

        if args.draft:
            # Move to correct Drafts before saving
            drafts_folder = get_folder_in_store(store, "drafts")
            reply = reply.Move(drafts_folder)
            reply.Save()
            print(f"DRAFT {action} saved from {account.SmtpAddress}: Re: {target.Subject}")
        else:
            # Move to correct Outbox before sending
            outbox = get_folder_in_store(store, "outbox")
            reply = reply.Move(outbox)
            reply.Send()
            print(f"SENT {action} from {account.SmtpAddress}: Re: {target.Subject}")

    except Exception as e:
        print(f"ERROR: Failed. {e}")
        sys.exit(6)

if __name__ == "__main__":
    main()
