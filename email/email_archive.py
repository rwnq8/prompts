#!/usr/bin/env python3
"""
Move an email to a different folder (archive, organize, clean inbox).
Usage: python email_archive.py --index 0 --destination Archive [--account NAME]
       python email_archive.py --search "Richard" --index 0 --destination Archive
       python email_archive.py --index 2 --folder inbox --destination "Project X" --mark-read
"""
import argparse
import sys

from _email_utils import resolve_store, get_folder_in_store


def main():
    parser = argparse.ArgumentParser(
        description="Move an Outlook email to a different folder"
    )
    parser.add_argument("--index", type=int, default=0,
                        help="Message index (0=most recent) in the source folder")
    parser.add_argument("--folder", default="inbox",
                        help="Source folder name (default: inbox)")
    parser.add_argument("--search", default="",
                        help="Filter messages by text before indexing (same as email_read.py)")
    parser.add_argument("--destination", default="Archive",
                        help="Destination folder name (default: Archive)")
    parser.add_argument("--mark-read", action="store_true",
                        help="Mark the message as read before moving")
    parser.add_argument("--account", default="rowan.quni@outlook.com",
                        help="Account to use")
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

    # Locate source folder
    try:
        source_folder = get_folder_in_store(store, args.folder)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(4)

    # Locate destination folder
    try:
        dest_folder = get_folder_in_store(store, args.destination)
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(5)

    messages = source_folder.Items
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
        print(f"ERROR: Message index {args.index} not found "
              f"(matched {matched} messages with search '{args.search}').")
        sys.exit(6)

    try:
        subject = str(target.Subject)
        sender = str(target.SenderName)

        if args.mark_read:
            target.UnRead = False
            target.Save()

        # Move the message to the destination folder
        moved = target.Move(dest_folder)

        print(f"MOVED from {store_name}/{args.folder} -> {args.destination}")
        print(f"  From: {sender}")
        print(f"  Subj: {subject}")
        if args.mark_read:
            print(f"  Marked as read.")
        print(f"  Destination has {dest_folder.Items.Count} items now.")

    except Exception as e:
        print(f"ERROR: Failed to move message. {e}")
        sys.exit(7)


if __name__ == "__main__":
    main()
