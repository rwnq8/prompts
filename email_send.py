#!/usr/bin/env python3
"""
Send an email via Outlook.
Usage: python email_send.py --to addr [--cc addr] [--subject "text"] [--body "text"]
       python email_send.py --to addr --body-file path.txt --subject "text"

SECURITY: This script sends immediately. Use email_draft.py to review first.
"""
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Send an email via Outlook")
    parser.add_argument("--to", required=True, help="Recipient email(s), comma-separated")
    parser.add_argument("--cc", default="", help="CC recipient(s)")
    parser.add_argument("--bcc", default="", help="BCC recipient(s)")
    parser.add_argument("--subject", required=True, help="Email subject line")
    parser.add_argument("--body", default="", help="Plain text body")
    parser.add_argument("--body-file", default="", help="Read body from a file")
    parser.add_argument("--html", action="store_true", help="Body is HTML")
    parser.add_argument("--attachment", action="append", default=[], help="File to attach (repeatable)")
    args = parser.parse_args()

    # Resolve body
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
    except Exception as e:
        print(f"ERROR: Cannot connect to Outlook. Is it running? ({e})")
        sys.exit(3)

    try:
        mail = outlook.CreateItem(0)  # 0 = olMailItem
        mail.Subject = args.subject

        # Set recipients
        mail.To = args.to
        if args.cc:
            mail.CC = args.cc
        if args.bcc:
            mail.BCC = args.bcc

        # Set body
        if args.html:
            mail.HTMLBody = body
        else:
            mail.Body = body

        # Attachments
        for fpath in args.attachment:
            mail.Attachments.Add(fpath)

        mail.Send()
        print(f"SENT: '{args.subject}' to {args.to}")
        if args.cc:
            print(f"  CC: {args.cc}")
        if args.attachment:
            print(f"  Attachments: {len(args.attachment)} file(s)")

    except Exception as e:
        print(f"ERROR: Failed to send. {e}")
        sys.exit(4)

if __name__ == "__main__":
    main()
