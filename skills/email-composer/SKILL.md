---
name: email-composer
description: Compose, draft, and send emails via Outlook COM automation. Use when the agent needs to send project updates, collaboration emails, or publication announcements.
tools: exec, fill_prompt_template
---
# Email Composer

## When to Use
- Drafting project update emails
- Sending collaboration outreach
- Publication announcements
- Any email composition/sending task

## Quick Start
```python
# Template invocation (preferred)
fill_prompt_template("EMAIL-AGENT-TEMPLATE", {...})

# Direct COM (for custom emails)
python -c "
import win32com.client
outlook = win32com.client.Dispatch('Outlook.Application')
mail = outlook.CreateItem(0)
mail.To = 'recipient@example.com'
mail.Subject = 'Subject'
mail.Body = 'Body'
mail.Display()  # or mail.Send()
"
```

## Workflow
1. Gather content (subject, body, recipients, attachments)
2. Fill EMAIL-AGENT-TEMPLATE via fill_prompt_template
3. If template handles it: use template output directly
4. If custom: use COM automation (see Reference below)
5. Always Draft first (Display) unless user explicitly says "send now"
6. Verify draft in Outlook before sending

## Recipient Resolution
- Check Outlook contacts first: `outlook.Session.GetDefaultFolder(10).Items`
- Fall back to user confirmation via deepchat_question
- Never guess email addresses

## COM Automation Reference

### Create and Display Draft
```python
import win32com.client
outlook = win32com.client.Dispatch('Outlook.Application')
mail = outlook.CreateItem(0)  # 0 = olMailItem
mail.To = 'recipient@example.com'
mail.CC = 'cc@example.com'
mail.BCC = 'bcc@example.com'
mail.Subject = 'Subject line'
mail.Body = 'Plain text body'
# OR for HTML:
mail.HTMLBody = '<html><body>HTML content</body></html>'

# Attachments
mail.Attachments.Add(r'C:\path\to\file.pdf')

# Display (don't send yet)
mail.Display()

# Save to Drafts
mail.Save()
```

### Send Directly (User Must Confirm)
```python
mail.Send()  # Sends immediately — require user confirmation first
```

### Read Inbox
```python
inbox = outlook.Session.GetDefaultFolder(6)  # 6 = olFolderInbox
messages = inbox.Items
messages.Sort('[ReceivedTime]', True)  # Newest first
for msg in messages[:10]:
    print(f'{msg.ReceivedTime}: {msg.Subject} from {msg.SenderName}')
```

### Failure Scenarios
| Failure | Cause | Recovery |
|:--------|:------|:---------|
| COM object creation fails | Outlook not installed/running | Report [BLOCKED: Outlook unavailable] |
| win32com not found | Dependency missing | `pip install pywin32` |
| Recipient not found | Not in contacts | Ask user with deepchat_question |
| Send fails | No network or permissions | Save to Drafts, report failure |
| encode error in body | Non-ASCII characters | Use HTMLBody with proper encoding |

## Pre-Send Checklist
- [ ] Recipient verified (contact lookup or user confirmation)
- [ ] Subject line concise and descriptive
- [ ] Body reviewed for fabrication
- [ ] Attachments verified (Test-Path)
- [ ] Draft viewed first (unless user said "send")
