---
name: email-composer
description: Outlook email composition, sending, reading, and management via COM automation. Use when the agent needs to send, read, search, or manage emails through Outlook.
version: 2.0
---
# EMAIL COMPOSER SKILL — v2.0

> **On-demand skill.** Load via `skill_view('email-composer')` when email operations are needed.
> Source: `EMAIL-AGENT-v1.3.md` (template) + email-composer skill

---

## Quick Start

For sending email, use `fill_prompt_template("EMAIL-AGENT-TEMPLATE", {...})` with all required parameters.
For reading/searching email, use the Python scripts in `G:\My Drive\projects\email-agent\`.

---

## Email Operations

### Read Inbox
```powershell
python "G:\My Drive\projects\email-agent\email_inbox.py" --folder "Inbox" --count 20
```

### Search Email
```powershell
python "G:\My Drive\projects\email-agent\email_search.py" --query "quantum computing" --folder "Inbox"
```

### Send Email
Use `fill_prompt_template("EMAIL-AGENT-TEMPLATE", {to, subject, body, cc, bcc, attachments})` then execute the generated script:
```powershell
python "G:\My Drive\projects\email-agent\email_send.py"
```

### Reply to Email
```powershell
python "G:\My Drive\projects\email-agent\email_reply.py" --message-id "<id>" --body "Response text"
```

### Archive Email
```powershell
python "G:\My Drive\projects\email-agent\email_archive.py" --message-id "<id>" --folder "Archive"
```

---

## Pre-Send Validation (MANDATORY)

Before sending ANY email, run through DEFAULT.md §E.5.1 checklist:
1. **WHO Gate:** Right person? Checked prior threads?
2. **WHEN Gate:** Right time? Recent activity? Trigger event?
3. **WHAT Gate:** Clear, concise, actionable? Appropriate tone?
4. **SOURCE AUDIT:** Every claim traceable to source?
5. **FABRICATION CHECK:** No invented papers, DOIs, paths?
6. **FILESYSTEM VERIFICATION:** All referenced files exist?

---

## Account Configuration

- **Default account:** rowan.quni@qnfo.org
- **Profile:** Outlook COM automation via `win32com.client`
- **Scripts:** `G:\My Drive\projects\email-agent\`

---

## Common Patterns

### Checking for Prior Threads
```powershell
python "G:\My Drive\projects\email-agent\email_search.py" --query "<contact-name>" --folder "Inbox"
python "G:\My Drive\projects\email-agent\email_search.py" --query "<contact-name>" --folder "Sent Items"
```

### Drafting Without Sending
Set `confirm_send: false` in the EMAIL-AGENT-TEMPLATE parameters. The script will save to Drafts.

---

## Failure Recovery

| Error | Cause | Fix |
|:------|:------|:----|
| `COM error: Outlook not running` | Outlook closed | Start Outlook manually |
| `Access denied` | Another process locking Outlook | Wait 5s, retry |
| `Recipient not found` | Invalid email address | Verify address format |
| `Attachment not found` | File path wrong | `Test-Path` the file first |

---

## Reference Files

- Agent template: `G:\My Drive\prompts\email\EMAIL-AGENT-v1.3.md`
- Test suite: `G:\My Drive\prompts\email\EMAIL-TEST-SUITE.md`
- Scripts: `G:\My Drive\projects\email-agent\email_*.py`
- Shared utilities: `G:\My Drive\projects\email-agent\_email_utils.py`

---

*email-composer skill v2.0 — Load on-demand via skill_view(). Email scripts moved to projects/email-agent/.*
