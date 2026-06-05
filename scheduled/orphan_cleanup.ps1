# orphan_cleanup.ps1 — Weekly ephemeral file cleanup (runs via Windows Task Scheduler)
# Scans G:\My Drive\prompts for orphaned _* files and __pycache__ directories

$ErrorActionPreference = "Continue"
$logFile = "G:\My Drive\prompts\audit\scheduled\orphan_cleanup_$(Get-Date -Format 'yyyyMMdd').log"
New-Item -ItemType Directory -Path (Split-Path $logFile) -Force | Out-Null

Write-Output "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Starting weekly orphan cleanup..." | Tee-Object -FilePath $logFile -Append

$targetDir = "G:\My Drive\prompts"
$deletedCount = 0

# Scan for _* ephemeral files
$orphans = Get-ChildItem -Path $targetDir -File -Name | Where-Object { $_ -match '^_' }
foreach ($orphan in $orphans) {
    try {
        Remove-Item (Join-Path $targetDir $orphan) -Force
        Write-Output "  CLEANED: $orphan" | Tee-Object -FilePath $logFile -Append
        $deletedCount++
    } catch {
        Write-Output "  ERROR: $orphan — $($_.Exception.Message)" | Tee-Object -FilePath $logFile -Append
    }
}

# Scan for __pycache__ directories
$pycaches = Get-ChildItem -Path $targetDir -Directory -Recurse -Name | Where-Object { $_ -match '__pycache__' }
foreach ($pyc in $pycaches) {
    try {
        Remove-Item (Join-Path $targetDir $pyc) -Recurse -Force
        Write-Output "  CLEANED: $pyc" | Tee-Object -FilePath $logFile -Append
        $deletedCount++
    } catch {
        Write-Output "  ERROR: $pyc — $($_.Exception.Message)" | Tee-Object -FilePath $logFile -Append
    }
}

Write-Output "Total cleaned: $deletedCount items" | Tee-Object -FilePath $logFile -Append
Write-Output "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Weekly orphan cleanup complete" | Tee-Object -FilePath $logFile -Append
