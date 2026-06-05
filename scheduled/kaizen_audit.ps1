# kaizen_audit.ps1 — Daily Kaizen audit (runs via Windows Task Scheduler)
# Pulls kaizen_engine.py from R2, runs audit, logs improvements

$ErrorActionPreference = "Continue"
$logFile = "G:\My Drive\prompts\audit\scheduled\kaizen_audit_$(Get-Date -Format 'yyyyMMdd').log"
New-Item -ItemType Directory -Path (Split-Path $logFile) -Force | Out-Null

Write-Output "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Starting daily Kaizen audit..." | Tee-Object -FilePath $logFile -Append

try {
    $env:CLOUDFLARE_API_TOKEN = (Get-Content "$env:USERPROFILE\.cloudflare\api-token" -Raw).Trim()
    
    # Pull kaizen_engine.py from R2
    npx wrangler r2 object get qnfo/tools/kaizen_engine.py --remote --file=_kaizen_engine.py *>&1 | Out-Null
    
    if (Test-Path _kaizen_engine.py) {
        Set-Location "G:\My Drive\prompts"
        $output = python _kaizen_engine.py --audit 2>&1
        Add-Content -Path $logFile -Value $output
        Write-Output "Kaizen audit complete" | Tee-Object -FilePath $logFile -Append
        
        # Check for critical findings
        if ($output -match "CRITICAL|Health Score: 0%") {
            Write-Output "[WARN] Kaizen found critical issues — review audit/kaizen/" | Tee-Object -FilePath $logFile -Append
        }
        
        Remove-Item _kaizen_engine.py -Force
    } else {
        Write-Output "[ERROR] Failed to pull kaizen_engine.py from R2" | Tee-Object -FilePath $logFile -Append
    }
} catch {
    Write-Output "[ERROR] $($_.Exception.Message)" | Tee-Object -FilePath $logFile -Append
}

Write-Output "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Daily Kaizen audit complete" | Tee-Object -FilePath $logFile -Append
