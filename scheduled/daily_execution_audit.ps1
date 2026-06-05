# daily_execution_audit.ps1 — Daily execution audit (runs via Windows Task Scheduler)
# Scans DeepChat Downloads for recent exports and runs execution_audit.py

$ErrorActionPreference = "Continue"
$logFile = "G:\My Drive\prompts\audit\scheduled\execution_audit_$(Get-Date -Format 'yyyyMMdd').log"
New-Item -ItemType Directory -Path (Split-Path $logFile) -Force | Out-Null

Write-Output "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Starting daily execution audit..." | Tee-Object -FilePath $logFile -Append

# Pull execution_audit.py from R2
try {
    $env:CLOUDFLARE_API_TOKEN = (Get-Content "$env:USERPROFILE\.cloudflare\api-token" -Raw).Trim()
    npx wrangler r2 object get qnfo/tools/execution_audit.py --remote --file=_execution_audit.py *>&1 | Out-Null
    
    if (Test-Path _execution_audit.py) {
        # Run against latest export
        $latestExport = Get-ChildItem "$env:USERPROFILE\Downloads\export_deepchat_*.md" -ErrorAction SilentlyContinue `
            | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        
        if ($latestExport) {
            $output = python _execution_audit.py $latestExport.FullName --json 2>&1
            Add-Content -Path $logFile -Value $output
            Write-Output "Audit complete: $($latestExport.Name)" | Tee-Object -FilePath $logFile -Append
        } else {
            Write-Output "No recent export files found" | Tee-Object -FilePath $logFile -Append
        }
        
        Remove-Item _execution_audit.py -Force
    } else {
        Write-Output "[ERROR] Failed to pull execution_audit.py from R2" | Tee-Object -FilePath $logFile -Append
    }
} catch {
    Write-Output "[ERROR] $($_.Exception.Message)" | Tee-Object -FilePath $logFile -Append
}

Write-Output "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Daily execution audit complete" | Tee-Object -FilePath $logFile -Append
