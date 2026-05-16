# DeepChat Email Agent — Setup & Usage Guide

> **Give DeepChat full access to your Outlook email** — check inbox, read messages, search, compose drafts, and send. All from within your existing LLM chat sessions.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Architecture — How It Works](#architecture--how-it-works)
- [Quick Start](#quick-start)
- [Three Ways to Use](#three-ways-to-use)
- [Tool Reference](#tool-reference)
- [Security Rules](#security-rules)
- [Multi-Account Setup](#multi-account-setup)
- [Troubleshooting](#troubleshooting)
- [MCP Server (Advanced — Microsoft Graph API)](#mcp-server-advanced--microsoft-graph-api)
- [Files in This Directory](#files-in-this-directory)

---

## Overview

The email system gives DeepChat agents **structured, discoverable access to Microsoft Outlook** via Windows COM automation. It consists of:

| Layer | What | Where |
|:------|:-----|:------|
| **7 Python scripts** | CLI tools that read/search/compose/send via Outlook | `email/email_*.py` |
| **1 shared utility** | Multi-account resolution and folder lookup | `email/_email_utils.py` |
| **2 system prompts** | Agent instructions — how to use the tools | `email/EMAIL-AGENT-v1.1.md` (lightweight) |
| **1 prompt module** | Drop-in section for any existing prompt | `email/EMAIL-CAPABILITIES.md` |
| **MCP server** | Production-grade Microsoft Graph API integration | `email/outlook_mcp_server/` |

The scripts talk to Outlook via COM (Windows only, Outlook must be running). The MCP server is a cloud alternative that works anywhere via Microsoft Graph API.

---

## Prerequisites

### Required
- **Windows** with **Microsoft Outlook** installed and running
- **Python 3.12+** (standard library only — no external packages needed for scripts)
- **pywin32** package (one-time install):
  ```powershell
  pip install pywin32
  ```

### Recommended
- Outlook configured with at least one email account
- Git (for tracking email-related file changes — optional)

---

## Architecture — How It Works

```
┌──────────────────────────────────────────────────────────┐
│  YOU (in DeepChat chat)                                   │
│  "Check my inbox"  /  "Reply to Richard"  /  "Send..."   │
└──────────────────────┬───────────────────────────────────┘
                       │ natural language
                       ▼
┌──────────────────────────────────────────────────────────┐
│  DEEPCHAT AGENT (loaded with system prompt)               │
│                                                           │
│  Reads the system prompt → learns what tools exist        │
│  Translates your request → structured CLI command         │
│  Calls exec(...) → runs the Python script                  │
│  Parses output → presents results back to you             │
└──────────────────────┬───────────────────────────────────┘
                       │ exec("python .../email_inbox.py")
                       ▼
┌──────────────────────────────────────────────────────────┐
│  PYTHON SCRIPT (email_inbox.py, email_draft.py, etc.)    │
│                                                           │
│  Connects to Outlook via COM (win32com.client)            │
│  Reads/searches/composes/sends email                     │
│  Returns structured output to agent                       │
└──────────────────────┬───────────────────────────────────┘
                       │ COM automation
                       ▼
┌──────────────────────────────────────────────────────────┐
│  MICROSOFT OUTLOOK (running locally)                      │
│  rowan.quni@outlook.com (primary)                         │
│  rwnquni@outlook.com (legacy, deprecated)                 │
└──────────────────────────────────────────────────────────┘
```

**Key principle:** The system prompt is the instruction manual. The agent reads it, learns the tools, and invokes them. There is no "installation" — just a prompt file and Python scripts.

---

## Quick Start

### 1. Install pywin32 (one time)

```powershell
pip install pywin32
```

### 2. Make sure Outlook is running

The COM connection requires `Outlook.exe` to be live. If Outlook is closed, the scripts will fail with a clear error message.

### 3. Load the email agent prompt in DeepChat

Choose one of the three methods below. The simplest: **load `EMAIL-AGENT-v1.1.md` as your system prompt.**

### 4. Start chatting

```
You: "Check my inbox"
Agent: [runs email_inbox.py, shows results]

You: "Read the email from Richard Goodman"
Agent: [runs email_read.py --index 0, shows full email]

You: "Draft a reply saying I'll get back to him tomorrow"
Agent: [runs email_reply.py --draft, confirms draft saved]
```

---

## Three Ways to Use

### Method A — Dedicated Email Agent Session **(Recommended for email-heavy sessions)**

Load `EMAIL-AGENT-v1.1.md` as the **system prompt** in DeepChat. This gives you:

- Full email capabilities with zero project management overhead
- No sprint workflow, no git protocol (except when creating files)
- All 7 tools documented with CLI syntax and workflow patterns
- 10 edge cases with recovery procedures
- 6 security rules (never send without confirmation, etc.)

**How to load:** Configure DeepChat to use `G:\My Drive\prompts\email\EMAIL-AGENT-v1.1.md` as the system prompt for email sessions.

---

### Method B — Default Prompt with Email **(For general sessions with occasional email)**

The email module is **already appended** to `DEFAULT.md` (v1.7+). When you use the default system prompt, your agent automatically has email capabilities alongside all other features.

**No action needed** — it's already there. Look for the `# EMAIL CAPABILITIES MODULE v1.0` section at the end of `DEFAULT.md`.

---

### Method C — Inject Into Any Prompt **(For one-off email tasks)**

Use `fill_prompt_template` with `additionalContent` to inject email capabilities into any existing template:

```
fill_prompt_template(
    templateName="Research Planning Agent — Step 1 of 4: Setup",
    additionalContent=<contents of EMAIL-CAPABILITIES.md>
)
```

The email section is appended to the end of the prompt for that session only. This works with any template — just pass the `EMAIL-CAPABILITIES.md` content as `additionalContent`.

---

## Tool Reference

All scripts support `--help` for full documentation. They default to `rowan.quni@outlook.com` (the primary account). Override with `--account`.

### Read Operations (Safe — No Confirmation Needed)

#### Check Inbox / Folder
```bash
python "G:\My Drive\prompts\email\email_inbox.py" --unread-only
python "G:\My Drive\prompts\email\email_inbox.py" --folder sent --limit 10
python "G:\My Drive\prompts\email\email_inbox.py" --folder drafts
```

Returns: Sender, subject, date, unread status, attachment flag. Add `--json` for structured output.

#### Read a Specific Email
```bash
python "G:\My Drive\prompts\email\email_read.py" --index 0           # Most recent
python "G:\My Drive\prompts\email\email_read.py" --search "invoice" --index 0
python "G:\My Drive\prompts\email\email_read.py" --index 0 --full    # No truncation
python "G:\My Drive\prompts\email\email_read.py" --index 0 --attachments-dir "G:\My Drive\temp"
```

Returns: Full headers, body (truncated at 5000 chars by default), attachment save paths.

#### Search Emails
```bash
python "G:\My Drive\prompts\email\email_search.py" "quarterly report"
python "G:\My Drive\prompts\email\email_search.py" "" --sender "alice@company.com"
python "G:\My Drive\prompts\email\email_search.py" "invoice" --body-search --since 2026-05-01
```

Returns: Matching messages with sender, date, subject, body preview.

#### List All Folders
```bash
python "G:\My Drive\prompts\email\email_folders.py"
python "G:\My Drive\prompts\email\email_folders.py" --json
```

Returns: Full folder tree with item counts and unread counts.

---

### Write Operations (⚠️ Gated Behind Confirmation)

> **Golden rule:** Always use `--draft` first. Only send when the user explicitly says "send it."

#### Create a Draft (SAFE)
```bash
python "G:\My Drive\prompts\email\email_draft.py" --to "bob@company.com" --subject "Q3 Report" --body "Please find attached..."
python "G:\My Drive\prompts\email\email_draft.py" --to "team@x.com" --subject "Meeting notes" --body "..." --attachment "report.pdf" --open
```

Drafts appear in Outlook's Drafts folder. The user reviews and sends manually. Add `--open` to open the draft in an Outlook window immediately.

#### Send an Email (DESTRUCTIVE — Confirm First)
```bash
python "G:\My Drive\prompts\email\email_send.py" --to "bob@company.com" --subject "Q3 Report" --body "Here is the report..."
python "G:\My Drive\prompts\email\email_send.py" --to "team@x.com" --cc "manager@x.com" --subject "Update" --body-file "G:\My Drive\draft.txt"
```

**Agent MUST confirm before executing.** The agent must state the recipient, subject, and ask "Shall I send?" before running this command.

#### Reply or Forward (DESTRUCTIVE — Use --draft for Safety)
```bash
python "G:\My Drive\prompts\email\email_reply.py" --index 0 --body "Thanks, received!" --draft
python "G:\My Drive\prompts\email\email_reply.py" --index 0 --body "FYI" --forward --draft
python "G:\My Drive\prompts\email\email_reply.py" --search "meeting" --index 0 --body "I'll be there"
```

Use `--draft` to save for review. Omit `--draft` only when the user explicitly confirms to send.

---

## Security Rules

These are **non-negotiable** and baked into every email system prompt:

| # | Rule | Enforcement |
|:--|:-----|:------------|
| 1 | **Never send without confirmation** | Write operations blocked until user says "send it" |
| 2 | **Drafts are always safe** | `email_draft.py` is the default; send requires explicit override |
| 3 | **Never exfiltrate email content** | Email content stays in conversation; file saves require user request |
| 4 | **Never auto-forward chains** | Each forward requires separate user instruction |
| 5 | **Recipient validation** | Before sending: agent reads back TO, CC, SUBJECT for confirmation |
| 6 | **Never guess email addresses** | If uncertain about an address, agent must ask |

**Why this matters:** The scripts can send real emails to real people. The system prompt enforces a human-in-the-loop gate before any send operation. There is no auto-send path.

---

## Multi-Account Setup

The scripts support multiple Outlook accounts. The default is `rowan.quni@outlook.com` (primary). The legacy `rwnquni@outlook.com` account is accessible via `--account`:

```bash
# Default (primary account)
python "G:\My Drive\prompts\email\email_inbox.py"

# Explicitly target legacy account
python "G:\My Drive\prompts\email\email_inbox.py" --account "rwnquni@outlook.com"

# List available accounts
python "G:\My Drive\prompts\email\email_folders.py"  # Shows all stores
```

**All 7 scripts** support `--account`. The shared utility (`_email_utils.py`) handles store resolution — it searches all Outlook stores for the matching account name.

**How it works technically:**
1. `resolve_account(namespace, "rowan.quni@outlook.com")` → finds the Outlook Account object
2. `resolve_store(namespace, "rowan.quni@outlook.com")` → finds the Outlook Store object
3. `get_folder_in_store(store, "inbox")` → finds the Inbox within that store
4. For send/draft: `Move()` to correct Outbox/Drafts BEFORE Save/Send (COM's `CreateItem` always creates in default store)

---

## Troubleshooting

| Problem | Cause | Fix |
|:--------|:------|:----|
| `ModuleNotFoundError: win32com` | pywin32 not installed | `pip install pywin32` |
| `Cannot connect to Outlook` | Outlook not running | Open Outlook and retry |
| `Folder 'X' not found` | Wrong folder name | Run `email_folders.py` to see available folders |
| `Message index N not found` | Index out of range | Try a lower index or broader search |
| `Send failed` / email stuck in Outbox | Outlook security policy | Use `email_draft.py` instead — review and send manually |
| Wrong account accessed | Script defaulted to wrong store | Add `--account "rowan.quni@outlook.com"` explicitly |
| Garbled characters in email body | Unicode outside cp1252 | Expected — the console can't display some Unicode chars. Original is preserved in Outlook. |
| `ERROR: Cannot move the items` | Move() called after Save() | This should not happen with v1.1+ scripts (Move is before Save/Send). Report if seen. |
| Draft in wrong account | CreateItem always uses default store | Fixed in v1.1 — Move() to correct Drafts before Save. If seen, update scripts. |

---

## MCP Server (Advanced — Microsoft Graph API)

For production use, cross-platform access, or O365 features (categories, mentions, cloud attachments), use the MCP server in `outlook_mcp_server/` instead of COM scripts.

### Advantages over COM scripts
- **No Outlook.exe required** — works via cloud API
- **Cross-platform** — Windows, Mac, Linux
- **Typed tools** — Pydantic schemas, automatic discovery
- **O365 features** — categories, mentions, Focused Inbox, cloud attachments
- **Calendar support** — addable via `/me/calendar` endpoints

### Quick start
```powershell
# 1. Install dependencies
pip install -r "G:\My Drive\prompts\email\outlook_mcp_server\requirements.txt"

# 2. Register Azure app (5 minutes)
#    Visit: https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps
#    See outlook_mcp_server/README.md for detailed steps

# 3. Set client ID
$env:OUTLOOK_CLIENT_ID = "your-client-id"

# 4. Run server
python "G:\My Drive\prompts\email\outlook_mcp_server\server.py"
```

### Available MCP tools (11 total)
`outlook_list_messages` · `outlook_get_message` · `outlook_search_messages` · `outlook_send_message` · `outlook_create_draft` · `outlook_reply_message` · `outlook_forward_message` · `outlook_list_folders` · `outlook_move_message` · `outlook_delete_message` · `outlook_get_attachments`

See `outlook_mcp_server/README.md` for the complete setup guide.

---

## Files in This Directory

```
email/
├── README.md                    ← You are here
│
├── _email_utils.py              Shared utility — account/store/folder resolution
│
├── email_inbox.py               List messages from any folder
├── email_read.py                Read full email + save attachments
├── email_search.py              Full-text search with filters
├── email_send.py                Send email (confirmation-gated)
├── email_draft.py               Create draft (safe — human reviews)
├── email_reply.py               Reply / reply-all / forward
├── email_folders.py             List all folders with counts
│
├── EMAIL-AGENT-v1.1.md         Lightweight system prompt (dedicated email sessions)
├── EMAIL-CAPABILITIES.md        Drop-in prompt module (append to any prompt)
│
└── outlook_mcp_server/          MCP server for Microsoft Graph API
    ├── server.py                Main server — 11 tools, device-code OAuth
    ├── requirements.txt         Python dependencies
    ├── README.md                Setup & usage guide
    └── .gitignore               Excludes token_cache.json
```

---

*DeepChat Email Agent — built 2026-05-15/16. Default account: rowan.quni@outlook.com. Scripts default to correct account; all destructive operations gated behind user confirmation.*
