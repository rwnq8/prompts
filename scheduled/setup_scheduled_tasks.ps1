# setup_scheduled_tasks.ps1 — Windows Task Scheduler Setup for QNFO
# Run ONCE as Administrator: powershell -ExecutionPolicy Bypass -File setup_scheduled_tasks.ps1
# Creates 3 scheduled tasks: Daily Audit, Weekly Cleanup, Daily Kaizen

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "=== QNFO Scheduled Tasks Setup ===" -ForegroundColor Cyan

# ── Task 1: Daily Execution Audit (runs at 6:00 AM) ──────────────────────
$taskName1 = "QNFO Daily Execution Audit"
$script1 = Join-Path $scriptDir "daily_execution_audit.ps1"

if (Get-ScheduledTask -TaskName $taskName1 -ErrorAction SilentlyContinue) {
    Write-Host "[SKIP] $taskName1 already exists" -ForegroundColor Yellow
} else {
    $action1 = New-ScheduledTaskAction -Execute "powershell.exe" `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$script1`""
    $trigger1 = New-ScheduledTaskTrigger -Daily -At "06:00AM"
    $settings1 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
        -StartWhenAvailable -RunOnlyIfNetworkAvailable
    
    Register-ScheduledTask -TaskName $taskName1 -Action $action1 -Trigger $trigger1 `
        -Settings $settings1 -Description "Daily QNFO execution audit: analyzes conversation exports for plan:execution ratios"
    Write-Host "[CREATED] $taskName1 (daily at 6:00 AM)" -ForegroundColor Green
}

# ── Task 2: Weekly Orphan Cleanup (runs Sunday at 3:00 AM) ───────────────
$taskName2 = "QNFO Weekly Orphan Cleanup"
$script2 = Join-Path $scriptDir "orphan_cleanup.ps1"

if (Get-ScheduledTask -TaskName $taskName2 -ErrorAction SilentlyContinue) {
    Write-Host "[SKIP] $taskName2 already exists" -ForegroundColor Yellow
} else {
    $action2 = New-ScheduledTaskAction -Execute "powershell.exe" `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$script2`""
    $trigger2 = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At "03:00AM"
    $settings2 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
        -StartWhenAvailable -RunOnlyIfNetworkAvailable
    
    Register-ScheduledTask -TaskName $taskName2 -Action $action2 -Trigger $trigger2 `
        -Settings $settings2 -Description "Weekly QNFO orphan file cleanup: scans for _* ephemeral files and __pycache__ dirs"
    Write-Host "[CREATED] $taskName2 (weekly Sunday 3:00 AM)" -ForegroundColor Green
}

# ── Task 3: Daily Kaizen Audit (runs at 6:30 AM) ─────────────────────────
$taskName3 = "QNFO Daily Kaizen Audit"
$script3 = Join-Path $scriptDir "kaizen_audit.ps1"

if (Get-ScheduledTask -TaskName $taskName3 -ErrorAction SilentlyContinue) {
    Write-Host "[SKIP] $taskName3 already exists" -ForegroundColor Yellow
} else {
    $action3 = New-ScheduledTaskAction -Execute "powershell.exe" `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$script3`""
    $trigger3 = New-ScheduledTaskTrigger -Daily -At "06:30AM"
    $settings3 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
        -StartWhenAvailable -RunOnlyIfNetworkAvailable
    
    Register-ScheduledTask -TaskName $taskName3 -Action $action3 -Trigger $trigger3 `
        -Settings $settings3 -Description "Daily Kaizen audit: pulls kaizen_engine.py from R2, runs audit, reports improvements"
    Write-Host "[CREATED] $taskName3 (daily at 6:30 AM)" -ForegroundColor Green
}

# ── Summary ─────────────────────────────────────────────────────────────
Write-Host "`n=== Setup Complete ===" -ForegroundColor Cyan
Get-ScheduledTask -TaskName "QNFO*" | Select-Object TaskName, State, Triggers | Format-Table -AutoSize
Write-Host "`nOpen Task Scheduler: taskschd.msc" -ForegroundColor Gray
Write-Host "View task history: Get-ScheduledTask -TaskName 'QNFO*' | Get-ScheduledTaskInfo" -ForegroundColor Gray
