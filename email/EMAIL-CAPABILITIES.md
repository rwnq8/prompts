# EMAIL CAPABILITIES MODULE v1.0

> **Drop-in section for any DeepChat system prompt.**
> Append this to your agent's system prompt (e.g., at the end of `DEFAULT.md`) to give it full Outlook email access — read, search, compose, reply, and manage attachments.

---

## E.1 What This Module Provides

Your agent gains access to **7 email tools** via Python scripts in `G:\My Drive\prompts\`. Each tool is a standalone CLI script that communicates with your local Outlook desktop application via COM (Windows only, Outlook must be running).

| Tool | Script | Purpose | Destructive? |
|:-----|:-------|:--------|:---:|
| **Inbox Check** | `email_inbox.py` | List recent emails from any folder | No |
| **Email Read** | `email_read.py` | Read a specific email with full body and attachments | No |
| **Email Search** | `email_search.py` | Full-text search across folder (sender, date, body) | No |
| **Email Send** | `email_send.py` | Compose and send immediately | **YES** |
| **Draft Create** | `email_draft.py` | Compose and save as draft (review before sending) | No |
| **Reply/Forward** | `email_reply.py` | Reply, reply-all, or forward an email | **YES** |
| **Folder List** | `email_folders.py` | List all Outlook folders and message counts | No |

**All write operations (send, reply)** require explicit user confirmation before execution. Drafts are safe — they save for human review.

---

## E.2 How to Invoke Email Tools

All tools run via `exec` from the `G:\My Drive\prompts\` directory. The agent **must** execute the script file — never attempt inline Python for email operations.

### E.2.1 Check Inbox — `email_inbox.py`

```bash
python "G:\My Drive\prompts\email\email_inbox.py" --folder inbox --limit 10
python "G:\My Drive\prompts\email\email_inbox.py" --folder inbox --unread-only
python "G:\My Drive\prompts\email\email_inbox.py" --folder sent --limit 5
python "G:\My Drive\prompts\email\email_inbox.py" --folder inbox --limit 20 --json
```

**Parameters:**
| Flag | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `--folder` | string | `inbox` | Folder name (inbox, sent, drafts, deleted, junk, archive, or custom name) |
| `--limit` | int | 20 | Maximum messages to return |
| `--unread-only` | flag | off | Show only unread messages |
| `--json` | flag | off | Output as structured JSON instead of text |

**Output:** List of messages with index, sender, subject, date, read status, and attachment flags. The `--json` flag produces machine-parseable output for the agent to process further.

### E.2.2 Read Email — `email_read.py`

```bash
python "G:\My Drive\prompts\email\email_read.py" --index 0                          # Most recent
python "G:\My Drive\prompts\email\email_read.py" --index 3 --folder sent            # 4th message in Sent
python "G:\My Drive\prompts\email\email_read.py" --search "invoice" --index 0        # First match for "invoice"
python "G:\My Drive\prompts\email\email_read.py" --index 0 --attachments-dir "G:\My Drive\temp\attachments"
python "G:\My Drive\prompts\email\email_read.py" --index 0 --full                    # No body truncation
```

**Parameters:**
| Flag | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `--index` | int | 0 | 0 = most recent, 1 = second most recent, etc. |
| `--folder` | string | `inbox` | Folder to read from |
| `--search` | string | — | Only consider messages matching this text (subject + sender). Index counts within matches. |
| `--html` | flag | off | Show HTML body instead of plain text |
| `--attachments-dir` | path | — | Save all attachments to this directory |
| `--full` | flag | off | Show complete body (default truncates at 5000 chars) |

### E.2.3 Search Emails — `email_search.py`

```bash
python "G:\My Drive\prompts\email\email_search.py" "quarterly report"
python "G:\My Drive\prompts\email\email_search.py" "" --sender "boss@company.com" --limit 10
python "G:\My Drive\prompts\email\email_search.py" "invoice" --folder sent --body-search
python "G:\My Drive\prompts\email\email_search.py" "" --since 2026-05-01 --limit 30
python "G:\My Drive\prompts\email\email_search.py" "urgent" --json
```

**Parameters:**
| Flag | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `query` | positional | — | Search term (matches subject; add `--body-search` to search body) |
| `--folder` | string | `inbox` | Folder to search |
| `--limit` | int | 20 | Max results |
| `--body-search` | flag | off | Also search email body (slower on large folders) |
| `--sender` | string | — | Filter by sender name or email address |
| `--since` | date | — | Only messages after YYYY-MM-DD |
| `--json` | flag | off | JSON output |

### E.2.4 Send Email — `email_send.py` ⚠️ DESTRUCTIVE

```
⚠️ WARNING: This sends immediately. Always confirm with the user first.
   For safer composition, use email_draft.py instead.
```

```bash
python "G:\My Drive\prompts\email\email_send.py" --to "boss@company.com" --subject "Q2 Report" --body "Please find attached..."
python "G:\My Drive\prompts\email\email_send.py" --to "team@company.com" --cc "manager@company.com" --subject "Meeting notes" --body "Here are the notes from today..." --attachment "G:\My Drive\projects\notes.docx"
python "G:\My Drive\prompts\email\email_send.py" --to "a@x.com,b@x.com" --subject "Update" --body-file "G:\My Drive\projects\draft.txt"
```

**Parameters:**
| Flag | Type | Required | Description |
|:-----|:-----|:---------|:------------|
| `--to` | string | **Yes** | Recipient(s), comma-separated |
| `--subject` | string | **Yes** | Subject line |
| `--body` | string | — | Plain text body (use this OR `--body-file`) |
| `--body-file` | path | — | Read body from a file |
| `--cc` | string | — | CC recipient(s) |
| `--bcc` | string | — | BCC recipient(s) |
| `--html` | flag | — | Body is HTML |
| `--attachment` | path | — | File to attach (repeatable: `--attachment a.pdf --attachment b.png`) |

**Pre-send confirmation protocol:**
1. Agent MUST state: "I am about to send an email to [recipients] with subject '[subject]'. Shall I proceed?"
2. Agent MUST NOT execute the send command until the user explicitly confirms.
3. If there is ANY ambiguity about the recipient, subject, or body — use `email_draft.py` instead.

### E.2.5 Create Draft — `email_draft.py` ✅ SAFE

```bash
python "G:\My Drive\prompts\email\email_draft.py" --to "boss@company.com" --subject "Q2 Proposal" --body "Draft proposal for Q2 initiatives..."
python "G:\My Drive\prompts\email\email_draft.py" --to "team@x.com" --subject "Review" --body "..." --attachment "report.pdf" --open
```

**Parameters:** Same as `email_send.py`, plus:
| `--open` | flag | off | Open the draft in an Outlook window for immediate review |

Drafts appear in Outlook's Drafts folder. The user reviews and sends manually.

### E.2.6 Reply or Forward — `email_reply.py` ⚠️ DESTRUCTIVE

```bash
python "G:\My Drive\prompts\email\email_reply.py" --index 0 --body "Thanks, received!"
python "G:\My Drive\prompts\email\email_reply.py" --index 2 --body "FYI" --forward
python "G:\My Drive\prompts\email\email_reply.py" --search "meeting" --index 0 --body "I'll be there" --reply-all
python "G:\My Drive\prompts\email\email_reply.py" --index 0 --body "Draft reply" --draft
```

**Parameters:**
| Flag | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `--index` | int | 0 | Which message to reply to (within optional search filter) |
| `--folder` | string | `inbox` | Folder containing the original message |
| `--search` | string | — | Find the message by text before indexing |
| `--body` | string | **Yes** | Your reply text |
| `--forward` | flag | off | Forward instead of reply |
| `--reply-all` | flag | off | Reply to all recipients |
| `--draft` | flag | off | Save as draft instead of sending |
| `--attachment` | path | — | Additional attachment (repeatable) |

**Same confirmation protocol as `email_send.py` applies.** Use `--draft` for safety.

### E.2.7 List Folders — `email_folders.py`

```bash
python "G:\My Drive\prompts\email\email_folders.py"
python "G:\My Drive\prompts\email\email_folders.py" --json
```

Returns all Outlook folders with item counts and unread counts. Use this to discover available folder names before running inbox/read/search operations.

---

## E.3 Workflow Patterns

### Pattern A: "What's new in my inbox?"
```
1. exec: python "G:\My Drive\prompts\email\email_inbox.py" --unread-only --limit 10
2. Review output with user
3. If user wants to read a specific message:
   exec: python "G:\My Drive\prompts\email\email_read.py" --index N
```

### Pattern B: "Find that email about X"
```
1. exec: python "G:\My Drive\prompts\email\email_search.py" "X" --limit 10
2. Show results to user
3. If user selects one:
   exec: python "G:\My Drive\prompts\email\email_read.py" --search "X" --index N
```

### Pattern C: "Send an email for me"
```
1. Clarify: to, subject, body
2. ALWAYS use email_draft.py first (safe):
   exec: python "G:\My Drive\prompts\email\email_draft.py" --to "..." --subject "..." --body "..."
3. Show user the draft saved confirmation
4. Only use email_send.py when user explicitly says "send it"
```

### Pattern D: "Reply to the latest email from Y"
```
1. Find the message:
   exec: python "G:\My Drive\prompts\email\email_search.py" "" --sender "Y" --limit 5
2. Confirm with user which message to reply to
3. Draft the reply:
   exec: python "G:\My Drive\prompts\email\email_reply.py" --search "Y" --index 0 --body "..." --draft
4. User reviews in Outlook Drafts, or confirms to send
```

---

## E.4 Error Handling

### Error: "pywin32 is not installed"
```
→ Tell user: "Email tools require pywin32. Run: pip install pywin32"
→ Do NOT attempt to install it yourself (may require admin)
```

### Error: "Cannot connect to Outlook. Is it running?"
```
→ Tell user: "Outlook needs to be running for email access. Please open Outlook and try again."
→ Do NOT retry automatically — it won't help
```

### Error: "Folder 'X' not found"
```
→ Run: python "G:\My Drive\prompts\email\email_folders.py" to show available folders
→ Suggest closest match or ask user to clarify
```

### Error: "Message index N not found"
```
→ Message index is out of range. Show the user how many messages were matched.
→ Suggest a lower index or broader search.
```

### Error: "Failed to send"
```
→ Report the exact error to the user
→ Common causes: invalid recipient, Outlook security policy blocking automation
→ Suggest using email_draft.py as fallback
```

---

## E.5 Security and Privacy Rules

1. **Never send without confirmation.** Write operations (`email_send.py`, `email_reply.py` without `--draft`) must be preceded by an explicit confirmation prompt to the user.
2. **Drafts are always safe.** `email_draft.py` and `email_reply.py --draft` never send — they save for human review.
3. **Never exfiltrate email content.** Email bodies, subjects, and attachment contents read by the agent stay in the conversation. Do not write them to files unless the user explicitly requests it.
4. **Never auto-forward chains.** The forward feature requires explicit user instruction for each message.
5. **Attachment handling.** When saving attachments, always use a user-specified directory. Never save to system temp without asking.
6. **Recipient validation.** Before sending, read back the full recipient list and subject to the user for confirmation.

---

## E.6 Known Limitations

| Limitation | Impact | Workaround |
|:-----------|:-------|:-----------|
| **Outlook must be running** | COM requires a live Outlook.exe process | Ask user to open Outlook |
| **Windows only** | COM is Windows-only | For cross-platform, build an MCP server with Microsoft Graph API |
| **No O365-only features** | Categories, mentions, Focused Inbox, cloud attachments via COM are limited | Build MCP server for full Graph API access |
| **Single mailbox** | COM connects to the default Outlook profile | Configure default profile in Outlook |
| **No real-time push** | Agent must poll with `email_inbox.py` | Polling interval is manual |
| **Large attachments** | Saving via COM can be slow for large files | Warn user for attachments >10MB |

---

## E.7 Integration Instructions

### Option 1: Append to DEFAULT.md
Add this entire module at the end of your `DEFAULT.md` system prompt. All agents that use DEFAULT.md will inherit email capabilities.

### Option 2: Use as a standalone prompt
Load this module as the system prompt for a dedicated "Email Agent" session.

### Option 3: Inject via fill_prompt_template
Use `fill_prompt_template` with `additionalContent` to inject the email section into any existing template.

### Option 4: Future MCP Server
For production use, migrate from COM scripts to an MCP server wrapping Microsoft Graph API. This eliminates Outlook.exe dependency and adds O365 features. See the `mcp-builder` skill for the build guide.

---

*Email Capabilities Module v1.0 — drop-in section. Built for DeepChat agents using local Outlook COM automation.*
