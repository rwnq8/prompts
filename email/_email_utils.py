"""
Shared utilities for Outlook email COM scripts.
Handles multi-account store resolution and folder lookup.
"""

# Folder enum mapping for common Outlook folders
FOLDER_MAP = {
    "inbox": 6, "sent": 5, "drafts": 16, "deleted": 3,
    "outbox": 4, "junk": 23, "archive": 45,
}

def resolve_store(namespace, account_name=None):
    """
    Find the Outlook store matching the given account name.
    If account_name is None, returns the first store.
    Returns (store, store_name) or raises ValueError.
    """
    stores = list(namespace.Folders)
    if not stores:
        raise RuntimeError("No Outlook stores found. Is Outlook configured with an account?")

    if account_name is None:
        return stores[0], stores[0].Name

    account_lower = account_name.lower()
    for store in stores:
        if account_lower in store.Name.lower():
            return store, store.Name

    # Not found — list available stores for the user
    available = [s.Name for s in stores]
    raise ValueError(
        f"Account '{account_name}' not found. Available accounts: {', '.join(available)}"
    )


def _walk_folders(folder):
    """Recursively yield all subfolders of a folder."""
    yield folder
    for sub in folder.Folders:
        yield from _walk_folders(sub)


def get_folder_in_store(store, name):
    """
    Find a folder by name within a specific store.
    Handles both well-known folders (inbox, sent, etc.) and custom names.
    """
    name_lower = name.lower()

    # Try well-known folder by enum first
    if name_lower in FOLDER_MAP:
        try:
            return store.GetDefaultFolder(FOLDER_MAP[name_lower])
        except Exception:
            pass  # Fall through to recursive search

    # Recursive search for custom or unfound folders
    for folder in _walk_folders(store):
        if folder.Name.lower() == name_lower:
            return folder

    # Not found
    available = [f.Name for f in _walk_folders(store)]
    raise ValueError(
        f"Folder '{name}' not found in account '{store.Name}'. "
        f"Available folders: {', '.join(available[:20])}"
    )


def resolve_account(namespace, account_name=None):
    """
    Find the Outlook Account object matching the given account name.
    Returns the Account object or raises ValueError.
    This is needed for SendUsingAccount on new mail items.
    """
    account_lower = (account_name or "").lower()
    for i in range(namespace.Accounts.Count):
        acc = namespace.Accounts.Item(i + 1)  # 1-based
        if account_lower in acc.SmtpAddress.lower() or account_lower in acc.DisplayName.lower():
            return acc
    if account_name is None:
        return namespace.Accounts.Item(1)
    available = [namespace.Accounts.Item(i+1).SmtpAddress for i in range(namespace.Accounts.Count)]
    raise ValueError(
        f"Account '{account_name}' not found. Available: {', '.join(available)}"
    )


def get_all_folders(store):
    """Return a flat list of all folders in a store with metadata."""
    results = []
    for folder in _walk_folders(store):
        results.append({
            "name": folder.Name,
            "path": folder.FolderPath,
            "item_count": folder.Items.Count,
            "unread_count": getattr(folder, 'UnReadItemCount', None),
        })
    return results
