"""
Outlook Email MCP Server v1.0
=============================
Production-grade MCP server for Microsoft Graph API email access.
Supports: list, read, search, send, draft, reply, forward, folders, move, delete.

Authentication: Device code flow (OAuth 2.0) — no web redirect URI needed.
Token persistence: Automatic caching to token_cache.json.

Setup:
  1. Register app at https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps
  2. Set redirect URI to: http://localhost
  3. Copy client_id below
  4. Run: python server.py
  5. Visit https://microsoft.com/devicelogin and enter the code shown
"""

import json
import os
import sys
import time
import logging
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CLIENT_ID = os.environ.get("OUTLOOK_CLIENT_ID", "YOUR_CLIENT_ID_HERE")
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPES = [
    "Mail.ReadWrite",
    "Mail.Send",
    "User.Read",
    "offline_access",
]
GRAPH_BASE = "https://graph.microsoft.com/v1.0"
TOKEN_CACHE_FILE = Path(__file__).parent / "token_cache.json"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)
log = logging.getLogger("outlook-mcp")

# ---------------------------------------------------------------------------
# Authentication (MSAL Device Code Flow)
# ---------------------------------------------------------------------------

class TokenManager:
    """Handles OAuth 2.0 device code flow and token caching."""

    def __init__(self):
        self._access_token: Optional[str] = None
        self._app = None

    def _get_app(self):
        if self._app is None:
            import msal
            self._app = msal.PublicClientApplication(
                client_id=CLIENT_ID,
                authority=AUTHORITY,
                token_cache=self._load_cache(),
            )
        return self._app

    def _load_cache(self):
        import msal
        cache = msal.SerializableTokenCache()
        if TOKEN_CACHE_FILE.exists():
            try:
                with open(TOKEN_CACHE_FILE, "r") as f:
                    cache.deserialize(f.read())
                log.info("Loaded token cache from %s", TOKEN_CACHE_FILE)
            except Exception:
                log.warning("Failed to load token cache - starting fresh")
        return cache

    def _save_cache(self):
        if self._app and self._app.token_cache:
            with open(TOKEN_CACHE_FILE, "w") as f:
                f.write(self._app.token_cache.serialize())
            log.info("Token cache saved to %s", TOKEN_CACHE_FILE)

    def acquire_token(self) -> str:
        """Get a valid access token (cached, refreshed, or new device code flow)."""
        app = self._get_app()

        # Try silent (cached token or refresh)
        accounts = app.get_accounts()
        if accounts:
            result = app.acquire_token_silent(SCOPES, account=accounts[0])
            if result and "access_token" in result:
                log.info("Token acquired silently (cached/refreshed)")
                self._access_token = result["access_token"]
                self._save_cache()
                return self._access_token

        # Device code flow
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            raise RuntimeError(f"Failed to start device flow: {flow.get('error_description', flow)}")

        print("\n" + "=" * 60)
        print("  MICROSOFT AUTHENTICATION REQUIRED")
        print("=" * 60)
        print(f"\n  1. Visit:  {flow['verification_uri']}")
        print(f"  2. Enter:  {flow['user_code']}")
        print(f"\n  Waiting for you to complete sign-in...")
        print("=" * 60 + "\n")

        result = app.acquire_token_by_device_flow(flow)

        if "access_token" not in result:
            error = result.get("error_description", str(result))
            raise RuntimeError(f"Authentication failed: {error}")

        log.info("Token acquired via device code flow")
        self._access_token = result["access_token"]
        self._save_cache()
        return self._access_token

    def get_token(self) -> str:
        """Return a valid token, refreshing or re-authenticating as needed."""
        try:
            return self.acquire_token()
        except Exception as e:
            log.error("Token acquisition failed: %s", e)
            raise

# ---------------------------------------------------------------------------
# Microsoft Graph API Client
# ---------------------------------------------------------------------------

class GraphClient:
    """Thin wrapper around Microsoft Graph REST API."""

    def __init__(self, token_manager: TokenManager):
        self._tm = token_manager
        import requests
        self._session = requests.Session()

    def _headers(self):
        return {
            "Authorization": f"Bearer {self._tm.get_token()}",
            "Content-Type": "application/json",
        }

    def get(self, path: str, params: dict = None) -> dict:
        """GET request to Graph API."""
        url = f"{GRAPH_BASE}{path}"
        r = self._session.get(url, headers=self._headers(), params=params)
        return self._handle(r)

    def post(self, path: str, body: dict) -> dict:
        """POST request to Graph API."""
        url = f"{GRAPH_BASE}{path}"
        r = self._session.post(url, headers=self._headers(), json=body)
        return self._handle(r)

    def patch(self, path: str, body: dict) -> dict:
        """PATCH request to Graph API."""
        url = f"{GRAPH_BASE}{path}"
        r = self._session.patch(url, headers=self._headers(), json=body)
        return self._handle(r)

    def delete(self, path: str) -> bool:
        """DELETE request to Graph API."""
        url = f"{GRAPH_BASE}{path}"
        r = self._session.delete(url, headers=self._headers())
        if r.status_code == 204:
            return True
        self._handle(r)
        return True

    def _handle(self, response):
        """Parse response, raise on error."""
        if response.status_code in (200, 201, 202, 204):
            if response.status_code == 204:
                return {"status": "ok"}
            return response.json()

        try:
            error_data = response.json()
            msg = error_data.get("error", {}).get("message", response.text)
        except Exception:
            msg = response.text

        raise RuntimeError(f"Graph API error [{response.status_code}]: {msg}")

# ---------------------------------------------------------------------------
# Global instances (initialized on first use)
# ---------------------------------------------------------------------------

_token_manager: Optional[TokenManager] = None
_graph_client: Optional[GraphClient] = None

def get_graph() -> GraphClient:
    global _token_manager, _graph_client
    if _graph_client is None:
        if CLIENT_ID == "YOUR_CLIENT_ID_HERE":
            raise RuntimeError(
                "CLIENT_ID not configured. Set OUTLOOK_CLIENT_ID environment variable "
                "or edit the CLIENT_ID in server.py. "
                "Register an app at https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps"
            )
        _token_manager = TokenManager()
        _graph_client = GraphClient(_token_manager)
    return _graph_client

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _format_message(msg: dict, include_body: bool = False) -> dict:
    """Extract clean fields from a Graph API message object."""
    result = {
        "id": msg.get("id", ""),
        "subject": msg.get("subject", "(No Subject)"),
        "from": msg.get("from", {}).get("emailAddress", {}).get("name", "Unknown"),
        "from_email": msg.get("from", {}).get("emailAddress", {}).get("address", ""),
        "received": msg.get("receivedDateTime", ""),
        "sent": msg.get("sentDateTime", ""),
        "hasAttachments": msg.get("hasAttachments", False),
        "isRead": msg.get("isRead", False),
        "importance": msg.get("importance", "normal"),
        "categories": msg.get("categories", []),
        "flag": msg.get("flag", {}).get("flagStatus", "notFlagged"),
        "webLink": msg.get("webLink", ""),
    }

    # Recipients
    for field in ("toRecipients", "ccRecipients", "bccRecipients"):
        recipients = msg.get(field, [])
        if recipients:
            result[field] = [
                {
                    "name": r.get("emailAddress", {}).get("name", ""),
                    "address": r.get("emailAddress", {}).get("address", ""),
                }
                for r in recipients
            ]

    # Body
    if include_body:
        body = msg.get("body", {})
        result["bodyPreview"] = msg.get("bodyPreview", "")
        result["bodyContentType"] = body.get("contentType", "text")
        result["body"] = body.get("content", "")[:10000]  # truncate at 10k

    # Attachments summary
    if msg.get("hasAttachments"):
        result["attachmentCount"] = len(msg.get("attachments", []))

    return result

# ---------------------------------------------------------------------------
# MCP Server Definition
# ---------------------------------------------------------------------------

from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="Outlook Email Server",
    description="Microsoft Graph API email tools for Outlook / Exchange Online / Office 365",
)

# ---------------------------------------------------------------------------
# Tool: List Messages
# ---------------------------------------------------------------------------

class ListMessagesInput(BaseModel):
    folder: str = Field(
        default="inbox",
        description="Mail folder name: inbox, sentitems, drafts, deleteditems, archive, junkemail",
    )
    limit: int = Field(
        default=20, ge=1, le=100,
        description="Maximum messages to return (1-100)",
    )
    filter_query: str = Field(
        default="",
        description="OData filter (e.g., isRead eq false, importance eq 'high')",
    )
    search_query: str = Field(
        default="",
        description="Keyword search across subject, body, and attachments",
    )
    include_body: bool = Field(
        default=False,
        description="Include full message body in results",
    )

@mcp.tool(readOnlyHint=True, idempotentHint=True)
def outlook_list_messages(params: ListMessagesInput) -> dict:
    """
    List messages from a mail folder (inbox, sent items, drafts, etc.).
    Returns newest messages first with sender, subject, date, and status.
    Use filter_query for OData filters and search_query for keyword search.
    """
    g = get_graph()
    folder_map = {
        "inbox": "inbox", "sentitems": "sentitems", "drafts": "drafts",
        "deleteditems": "deleteditems", "archive": "archive", "junkemail": "junkemail",
    }
    folder_path = folder_map.get(params.folder.lower().replace(" ", ""), params.folder)

    query_params = {
        "$top": params.limit,
        "$orderby": "receivedDateTime desc",
    }
    if params.filter_query:
        query_params["$filter"] = params.filter_query
    if params.search_query:
        query_params["$search"] = f'"{params.search_query}"'
    if not params.include_body:
        query_params["$select"] = (
            "id,subject,from,toRecipients,ccRecipients,"
            "receivedDateTime,sentDateTime,hasAttachments,"
            "isRead,importance,categories,flag,webLink,bodyPreview"
        )

    data = g.get(f"/me/mailFolders/{folder_path}/messages", params=query_params)
    messages = [_format_message(msg, include_body=params.include_body) for msg in data.get("value", [])]

    return {"folder": params.folder, "count": len(messages), "messages": messages}

# ---------------------------------------------------------------------------
# Tool: Get Message
# ---------------------------------------------------------------------------

@mcp.tool(readOnlyHint=True, idempotentHint=True)
def outlook_get_message(message_id: str) -> dict:
    """
    Get full details of a specific email by its Graph message ID.
    Returns complete body, all headers, and attachment metadata.
    """
    g = get_graph()
    msg = g.get(f"/me/messages/{message_id}")
    return _format_message(msg, include_body=True)

# ---------------------------------------------------------------------------
# Tool: Search Messages
# ---------------------------------------------------------------------------

class SearchMessagesInput(BaseModel):
    query: str = Field(..., description="Search term (searches subject, body, and sender)")
    folder: str = Field(default="inbox", description="Folder to search in")
    limit: int = Field(default=20, ge=1, le=50, description="Max results")
    include_body: bool = Field(default=False, description="Include full body in results")

@mcp.tool(readOnlyHint=True, idempotentHint=True)
def outlook_search_messages(params: SearchMessagesInput) -> dict:
    """
    Full-text search across emails. Searches subject, body, sender name, and attachment content.
    """
    g = get_graph()
    folder_map = {
        "inbox": "inbox", "sentitems": "sentitems", "drafts": "drafts",
        "deleteditems": "deleteditems", "archive": "archive", "junkemail": "junkemail",
    }
    folder_path = folder_map.get(params.folder.lower().replace(" ", ""), params.folder)

    query_params = {
        "$search": f'"{params.query}"',
        "$top": params.limit,
        "$orderby": "receivedDateTime desc",
    }
    if not params.include_body:
        query_params["$select"] = (
            "id,subject,from,toRecipients,receivedDateTime,"
            "hasAttachments,isRead,importance,flag,webLink,bodyPreview"
        )

    data = g.get(f"/me/mailFolders/{folder_path}/messages", params=query_params)
    messages = [_format_message(msg, include_body=params.include_body) for msg in data.get("value", [])]

    return {"query": params.query, "folder": params.folder, "count": len(messages), "messages": messages}

# ---------------------------------------------------------------------------
# Tool: Send Message
# ---------------------------------------------------------------------------

class Recipient(BaseModel):
    address: str = Field(..., description="Email address")
    name: str = Field(default="", description="Display name (optional)")

class SendMessageInput(BaseModel):
    to: list[Recipient] = Field(..., description="Primary recipients (at least one required)")
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Email body content")
    content_type: str = Field(default="Text", description="'Text' or 'HTML'")
    cc: list[Recipient] = Field(default=[], description="CC recipients")
    bcc: list[Recipient] = Field(default=[], description="BCC recipients")
    importance: str = Field(default="normal", description="low, normal, or high")

@mcp.tool(destructiveHint=True)
def outlook_send_message(params: SendMessageInput) -> dict:
    """
    Send a new email immediately. Use with caution — there is no undo.
    For safety, prefer outlook_create_draft first.
    """
    g = get_graph()

    def _build(recipients):
        return [{"emailAddress": {"address": r.address, "name": r.name or r.address}} for r in recipients]

    payload = {
        "message": {
            "subject": params.subject,
            "body": {"contentType": params.content_type, "content": params.body},
            "toRecipients": _build(params.to),
            "importance": params.importance,
        },
        "saveToSentItems": True,
    }
    if params.cc:
        payload["message"]["ccRecipients"] = _build(params.cc)
    if params.bcc:
        payload["message"]["bccRecipients"] = _build(params.bcc)

    g.post("/me/sendMail", payload)
    to_addrs = ", ".join(r.address for r in params.to)
    return {"status": "sent", "to": to_addrs, "subject": params.subject}

# ---------------------------------------------------------------------------
# Tool: Create Draft
# ---------------------------------------------------------------------------

class CreateDraftInput(BaseModel):
    to: list[Recipient] = Field(..., description="Primary recipients")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body content")
    content_type: str = Field(default="Text", description="'Text' or 'HTML'")
    cc: list[Recipient] = Field(default=[], description="CC recipients")
    bcc: list[Recipient] = Field(default=[], description="BCC recipients")

@mcp.tool(idempotentHint=True)
def outlook_create_draft(params: CreateDraftInput) -> dict:
    """
    Create a draft email. Safe — does not send. Appears in your Drafts folder.
    """
    g = get_graph()

    def _build(recipients):
        return [{"emailAddress": {"address": r.address, "name": r.name or r.address}} for r in recipients]

    payload = {
        "subject": params.subject,
        "body": {"contentType": params.content_type, "content": params.body},
        "toRecipients": _build(params.to),
    }
    if params.cc:
        payload["ccRecipients"] = _build(params.cc)
    if params.bcc:
        payload["bccRecipients"] = _build(params.bcc)

    result = g.post("/me/messages", payload)
    return {
        "status": "draft_created",
        "draftId": result.get("id", ""),
        "webLink": result.get("webLink", ""),
        "subject": params.subject,
    }

# ---------------------------------------------------------------------------
# Tool: Reply to Message
# ---------------------------------------------------------------------------

class ReplyMessageInput(BaseModel):
    message_id: str = Field(..., description="ID of the message to reply to")
    body: str = Field(..., description="Reply body content")
    reply_all: bool = Field(default=False, description="Reply to all recipients")
    content_type: str = Field(default="Text", description="'Text' or 'HTML'")
    save_draft: bool = Field(default=False, description="Save as draft instead of sending")

@mcp.tool(destructiveHint=True)
def outlook_reply_message(params: ReplyMessageInput) -> dict:
    """
    Reply to an email. Use save_draft=True to review before sending.
    """
    g = get_graph()
    action = "replyAll" if params.reply_all else "reply"

    if params.save_draft:
        result = g.post(f"/me/messages/{params.message_id}/create{action.capitalize()}", {
            "comment": params.body,
        })
        return {"status": "draft_created", "draftId": result.get("id", ""), "action": action}

    g.post(f"/me/messages/{params.message_id}/{action}", {"comment": params.body})
    return {"status": "sent", "action": action, "messageId": params.message_id}

# ---------------------------------------------------------------------------
# Tool: Forward Message
# ---------------------------------------------------------------------------

class ForwardMessageInput(BaseModel):
    message_id: str = Field(..., description="ID of the message to forward")
    to: list[Recipient] = Field(..., description="Forward recipients")
    comment: str = Field(default="", description="Additional note to include above forwarded content")
    save_draft: bool = Field(default=False, description="Save as draft instead of sending")

@mcp.tool(destructiveHint=True)
def outlook_forward_message(params: ForwardMessageInput) -> dict:
    """
    Forward an email to new recipients. Use save_draft=True to review before sending.
    """
    g = get_graph()
    payload = {
        "message": {
            "toRecipients": [
                {"emailAddress": {"address": r.address, "name": r.name or r.address}}
                for r in params.to
            ],
        },
        "comment": params.comment,
    }

    if params.save_draft:
        result = g.post(f"/me/messages/{params.message_id}/createForward", payload)
        return {"status": "draft_created", "draftId": result.get("id", "")}

    g.post(f"/me/messages/{params.message_id}/forward", payload)
    return {"status": "sent", "action": "forward", "messageId": params.message_id}

# ---------------------------------------------------------------------------
# Tool: List Folders
# ---------------------------------------------------------------------------

@mcp.tool(readOnlyHint=True, idempotentHint=True)
def outlook_list_folders() -> dict:
    """
    List all mail folders with message counts and unread counts.
    Use this to discover folder IDs before moving messages.
    """
    g = get_graph()
    data = g.get("/me/mailFolders", params={"$top": 50})
    folders = []
    for f in data.get("value", []):
        folders.append({
            "id": f["id"],
            "displayName": f["displayName"],
            "parentFolderId": f.get("parentFolderId", ""),
            "totalItemCount": f.get("totalItemCount", 0),
            "unreadItemCount": f.get("unreadItemCount", 0),
            "childFolderCount": f.get("childFolderCount", 0),
        })
    return {"count": len(folders), "folders": folders}

# ---------------------------------------------------------------------------
# Tool: Move Message
# ---------------------------------------------------------------------------

class MoveMessageInput(BaseModel):
    message_id: str = Field(..., description="ID of the message to move")
    destination_folder_id: str = Field(..., description="Target folder ID (from outlook_list_folders)")

@mcp.tool(destructiveHint=True)
def outlook_move_message(params: MoveMessageInput) -> dict:
    """
    Move a message to a different folder. Get destination folder IDs from outlook_list_folders.
    """
    g = get_graph()
    result = g.post(f"/me/messages/{params.message_id}/move", {"destinationId": params.destination_folder_id})
    return {"status": "moved", "messageId": result.get("id", ""), "folderId": result.get("parentFolderId", "")}

# ---------------------------------------------------------------------------
# Tool: Delete Message
# ---------------------------------------------------------------------------

@mcp.tool(destructiveHint=True)
def outlook_delete_message(message_id: str) -> dict:
    """
    Delete a message (moves to Deleted Items folder).
    WARNING: Deleted items may be permanently purged later.
    """
    g = get_graph()
    g.delete(f"/me/messages/{message_id}")
    return {"status": "deleted", "messageId": message_id}

# ---------------------------------------------------------------------------
# Tool: Get Attachments
# ---------------------------------------------------------------------------

class GetAttachmentsInput(BaseModel):
    message_id: str = Field(..., description="ID of the message")
    save_dir: str = Field(default="", description="Local directory to save attachments (optional)")

@mcp.tool(readOnlyHint=True, idempotentHint=True)
def outlook_get_attachments(params: GetAttachmentsInput) -> dict:
    """
    List all attachments on a message. Optionally download them to a local directory.
    """
    g = get_graph()
    data = g.get(f"/me/messages/{params.message_id}/attachments")
    attachments = []
    for att in data.get("value", []):
        info = {
            "id": att["id"], "name": att.get("name", "unnamed"),
            "contentType": att.get("contentType", ""), "size": att.get("size", 0),
            "isInline": att.get("isInline", False),
        }
        if params.save_dir and att.get("@microsoft.graph.downloadUrl"):
            import requests as req
            save_path = Path(params.save_dir) / att["name"]
            save_path.parent.mkdir(parents=True, exist_ok=True)
            r = req.get(att["@microsoft.graph.downloadUrl"])
            r.raise_for_status()
            save_path.write_bytes(r.content)
            info["savedTo"] = str(save_path)
        attachments.append(info)
    return {"messageId": params.message_id, "count": len(attachments), "attachments": attachments}

# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

def main():
    if CLIENT_ID == "YOUR_CLIENT_ID_HERE":
        print("=" * 60)
        print("  FIRST-TIME SETUP REQUIRED")
        print("=" * 60)
        print()
        print("  1. Visit https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps")
        print("  2. Register a new app (e.g., 'DeepChat Email')")
        print("  3. Under Authentication, add platform: 'Mobile and desktop applications'")
        print("  4. Set redirect URI: http://localhost")
        print("  5. Under API Permissions, add: Mail.ReadWrite, Mail.Send, User.Read")
        print("  6. Copy the Application (client) ID")
        print()
        print("  Then either:")
        print("    $env:OUTLOOK_CLIENT_ID='your-client-id'   (PowerShell)")
        print("    set OUTLOOK_CLIENT_ID=your-client-id      (CMD)")
        print()
        sys.exit(1)

    log.info("Testing authentication...")
    try:
        g = get_graph()
        user = g.get("/me")
        log.info("Authenticated as: %s (%s)", user.get("displayName"), user.get("userPrincipalName"))
    except Exception as e:
        log.error("Authentication failed: %s", e)
        sys.exit(1)

    log.info("Starting Outlook Email MCP Server...")
    mcp.run()

if __name__ == "__main__":
    main()
