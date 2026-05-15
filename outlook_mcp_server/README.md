# Outlook Email MCP Server

Production-grade MCP server that connects DeepChat agents to Microsoft Outlook / Exchange Online via Microsoft Graph API. Supports all major email operations with typed, discoverable tools.

---

## Quick Start

### 1. Install dependencies

```powershell
pip install -r requirements.txt
```

### 2. Register an Azure AD app

1. Go to [Azure App Registrations](https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps)
2. Click **New registration**
3. Name: `DeepChat Email` (or anything you like)
4. Supported account types: **Accounts in any organizational directory and personal Microsoft accounts**
5. Redirect URI: Under **Mobile and desktop applications**, add `http://localhost`
6. Click **Register**
7. Copy the **Application (client) ID**
8. Under **API Permissions** → Add:
   - `Mail.ReadWrite`
   - `Mail.Send`
   - `User.Read`
9. Click **Grant admin consent** (if available) or skip — device code flow handles consent

### 3. Set the client ID

**Option A — Environment variable (recommended):**
```powershell
$env:OUTLOOK_CLIENT_ID = "your-client-id-here"
```

**Option B — Edit the file:**
Open `server.py` and replace `YOUR_CLIENT_ID_HERE` on line 30.

### 4. Run the server

```powershell
python "G:\My Drive\prompts\outlook_mcp_server\server.py"
```

On first run, you'll see:
```
============================================
  MICROSOFT AUTHENTICATION REQUIRED
============================================

  1. Visit:  https://microsoft.com/devicelogin
  2. Enter:  ABC12DEF3

  Waiting for you to complete sign-in...
============================================
```

Visit the URL, enter the code, and sign in with your Microsoft account. The token is cached in `token_cache.json` — you won't need to authenticate again.

### 5. Register with DeepChat

Add the server to your DeepChat MCP configuration. The exact registration method depends on your DeepChat setup — typically a JSON config entry like:

```json
{
  "mcpServers": {
    "outlook": {
      "command": "python",
      "args": ["G:\\My Drive\\prompts\\outlook_mcp_server\\server.py"]
    }
  }
}
```

---

## Available Tools

| Tool | Category | Description |
|:-----|:---------|:------------|
| `outlook_list_messages` | Read | List messages from any folder with filters and search |
| `outlook_get_message` | Read | Get full details of a specific message by ID |
| `outlook_search_messages` | Read | Full-text search across subject, body, sender |
| `outlook_list_folders` | Read | List all mail folders with message counts |
| `outlook_get_attachments` | Read | List/download attachments from a message |
| `outlook_create_draft` | Write | Create a draft email (safe, no send) |
| `outlook_send_message` | Write | Send an email immediately |
| `outlook_reply_message` | Write | Reply or reply-all (with draft option) |
| `outlook_forward_message` | Write | Forward a message (with draft option) |
| `outlook_move_message` | Write | Move a message to another folder |
| `outlook_delete_message` | Write | Delete a message to Deleted Items |

---

## Architecture

```
DeepChat Agent
     │
     │ MCP protocol (stdio)
     ▼
outlook_mcp_server/server.py
     │
     │ OAuth 2.0 (device code flow)
     │ Token cached in token_cache.json
     ▼
Microsoft Graph API  ────  Outlook / Exchange Online
```

---

## Comparison with COM Scripts

| Feature | COM Scripts (email_*.py) | MCP Server (this) |
|:--------|:------------------------|:------------------|
| **Requires Outlook.exe** | Yes — must be running | No — cloud API |
| **Works cross-platform** | Windows only | Anywhere |
| **Tool discovery** | Manual — agent reads docs | Automatic — MCP introspection |
| **Type safety** | CLI strings | Pydantic models |
| **O365 features** | ❌ Categories, mentions, etc. | ✅ Full Graph API |
| **Calendar** | Possible via COM | Addable — `/me/calendar` |
| **Attachment download** | COM (slow for large files) | Direct download URLs |
| **Error messages** | Exit codes + stdout | Structured JSON errors |
| **Setup time** | 1 minute (pip install pywin32) | ~10 minutes (Azure app registration) |

**Recommendation:** Use COM scripts for quick testing. Migrate to the MCP server for production use.

---

## Adding Calendar Support

The MCP server can be extended with calendar tools. Add these endpoints:

| Endpoint | Purpose |
|:---------|:--------|
| `GET /me/calendar/events` | List calendar events |
| `POST /me/calendar/events` | Create calendar event |
| `PATCH /me/calendar/events/{id}` | Update event |
| `DELETE /me/calendar/events/{id}` | Delete event |

Requires the `Calendars.ReadWrite` API permission in Azure.

---

## Troubleshooting

| Problem | Solution |
|:--------|:---------|
| `CLIENT_ID not configured` | Set `OUTLOOK_CLIENT_ID` env var or edit server.py line 30 |
| `Authentication failed` | Check internet, re-run — token may have expired |
| `Graph API error [403]` | Missing API permissions in Azure → add Mail.ReadWrite, Mail.Send |
| `Graph API error [404]` | Message/folder ID invalid → re-query with `outlook_list_messages` |
| `ModuleNotFoundError: msal` | Run `pip install -r requirements.txt` |
| Token keeps expiring | Ensure `offline_access` is in SCOPES (it is by default) |
