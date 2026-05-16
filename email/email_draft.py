#!/usr/bin/env python3
"""
Create an email draft in Outlook (for review before sending).
Usage: python email_draft.py --to addr --subject "text" --body "text" [--account NAME]
"""
import argparse
import sys

from _email_utils import resolve_account, resolve_store, get_folder_in_store

def main():
    parser = argparse.ArgumentParser(description="Create an Outlook email draft")
    parser.add_argument("--to", required=True, help="Recipient(s), comma-separated")
    parser.add_argument("--cc", default="", help="CC recipient(s)")
    parser.add_argument("--bcc", default="", help="BCC recipient(s)")
    parser.add_argument("--subject", required=True, help="Subject line")
    parser.add_argument("--body", default="", help="Plain text body")
    parser.add_argument("--body-file", default="", help="Read body from file")
    parser.add_argument("--html", action="store_true", help="Body is HTML")
    parser.add_argument("--attachment", action="append", default=[], help="File to attach (repeatable)")
    parser.add_argument("--open", action="store_true", help="Open the draft in Outlook window")
    parser.add_argument("--account", default="rowan.quni@outlook.com", help="Account to use")
    args = parser.parse_args()

    body = args.body
    if args.body_file:
        try:
            with open(args.body_file, "r", encoding="utf-8") as f:
                body = f.read()
        except Exception as e:
            print(f"ERROR: Cannot read body file '{args.body_file}': {e}")
            sys.exit(1)

    if not body.strip():
        print("ERROR: Body is empty. Provide --body or --body-file.")
        sys.exit(2)

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
        sys.exit(3)

    try:
        account = resolve_account(namespace, args.account)
    except (ValueError, RuntimeError) as e:
        print(f"ERROR: {e}")
        sys.exit(4)

    try:
        mail = outlook.CreateItem(0)
        mail.SendUsingAccount = account

        mail.Subject = args.subject
        mail.To = args.to
        if args.cc:
            mail.CC = args.cc
        if args.bcc:
            mail.BCC = args.bcc

        if args.html:
            mail.HTMLBody = body
        else:
            mail.Body = body

        for fpath in args.attachment:
            mail.Attachments.Add(fpath)

        # Move to correct Drafts BEFORE saving
        store, _ = resolve_store(namespace, args.account)
        drafts_folder = get_folder_in_store(store, "drafts")
        mail = mail.Move(drafts_folder)
        mail.Save()

        print(f"DRAFT SAVED from {account.SmtpAddress}: '{args.subject}' to {args.to}")
        print("  Review in Outlook Drafts folder before sending.")

        if args.open:
            mail.Display()
            print("  Draft opened in Outlook window.")

    except Exception as e:
        print(f"ERROR: Failed to create draft. {e}")
        sys.exit(5)

if __name__ == "__main__":
    main()
