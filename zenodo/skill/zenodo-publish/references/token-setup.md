# Zenodo Token Setup

## Create a Token

1. Go to https://zenodo.org/account/settings/applications/
2. Under "Personal access tokens", click "New token"
3. Name: e.g., "CLI publishing"
4. Scopes (check both):
   - `deposit:actions` — create and manage depositions
   - `deposit:write` — upload files and publish
5. Click "Create"
6. Copy the token immediately — it's shown only once

## Save the Token (Windows)

```powershell
# Save to persistent file
"your-token-here" | Out-File -FilePath "$env:USERPROFILE\.zenodo_token" -NoNewline -Encoding ASCII
```

## Verify

```powershell
# Check file exists and length is ~60 chars
Test-Path "$env:USERPROFILE\.zenodo_token"
(Get-Content "$env:USERPROFILE\.zenodo_token").Length
```

## Token Security

- Token is stored as plaintext at `%USERPROFILE%\.zenodo_token`
- Never commit this file to git
- Never share the token
- Revoke and regenerate if compromised
- The script reads from this file OR `--token` flag OR `ZENODO_TOKEN` env var
