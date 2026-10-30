param([switch]$RunNow)
$ErrorActionPreference = 'Stop'
$taskName = 'Bussassistent-Backup'
$runtime = Join-Path $env:LOCALAPPDATA 'BussassistentServer'
$scriptPath = Join-Path $runtime 'server.ps1'
$log = Join-Path $runtime 'backup-task.log'
$source = Join-Path $PSScriptRoot 'server.ps1'
if (-not (Test-Path -LiteralPath $source)) { throw 'server.ps1 is missing.' }
$data = [Convert]::ToBase64String([IO.File]::ReadAllBytes($source))
# Write a pinned, self-contained copy inside the actual scheduled-task user session.
# Only script source is encoded; no passwords, private keys or tunnel tokens.
$quotedRuntime = $runtime.Replace("'", "''")
$quotedScript = $scriptPath.Replace("'", "''")
$quotedLog = $log.Replace("'", "''")
$command = '$ErrorActionPreference=''Stop''; [IO.Directory]::CreateDirectory(''' +
    $quotedRuntime + ''') | Out-Null; try { [IO.File]::WriteAllBytes(''' +
    $quotedScript + ''',[Convert]::FromBase64String(''' + $data +
    ''')); & ''' + $quotedScript + ''' -Action Backup *> ''' + $quotedLog +
    '''; exit 0 } catch { $_ | Out-String | Add-Content -LiteralPath ''' +
    $quotedLog + '''; exit 1 }'
$encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($command))
$exe = Join-Path $env:WINDIR 'System32/WindowsPowerShell/v1.0/powershell.exe'
$action = New-ScheduledTaskAction -Execute $exe -Argument (
    '-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy RemoteSigned -EncodedCommand ' + $encoded
) -WorkingDirectory $env:USERPROFILE
$user = [Security.Principal.WindowsIdentity]::GetCurrent().Name
$principal = New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Limited
$triggers = @(
    (New-ScheduledTaskTrigger -Daily -At '04:00'),
    (New-ScheduledTaskTrigger -AtLogOn -User $user)
)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable -ExecutionTimeLimit (
    New-TimeSpan -Minutes 10
) -MultipleInstances IgnoreNew -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -RestartCount 3 -RestartInterval (
    New-TimeSpan -Minutes 5
)
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing -and -not $existing.Description.StartsWith('Bussassistent:')) {
    throw 'Refusing to replace an unrelated scheduled task.'
}
Register-ScheduledTask -TaskName $taskName -Action $action -Principal $principal -Trigger $triggers -Settings $settings -Description (
    'Bussassistent: verified PostgreSQL backup over SSH; 04:00 and logon; three retries; requires Jonas logged in.'
) -Force | Select-Object TaskName,State
if ($RunNow) { Start-ScheduledTask -TaskName $taskName }
