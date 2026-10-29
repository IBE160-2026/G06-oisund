#requires -Version 7.2
$ErrorActionPreference = 'Stop'
$report = Get-ChildItem -LiteralPath $PSScriptRoot -Filter 'access-expiry-capture-*.json' | Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1
if (-not $report) { throw 'No capture report.' }
$capture = Get-Content -LiteralPath $report.FullName -Raw | ConvertFrom-Json
if (-not $capture.before_control_passed -or -not $capture.signature_valid -or $capture.issuer -ne 'https://bussassistent.cloudflareaccess.com') { throw 'Capture not qualified.' }
if ($capture.expires_utc -is [DateTime]) {
    $deadline = ([DateTimeOffset]$capture.expires_utc).AddSeconds(10)
} else {
    $deadline = [DateTimeOffset]::Parse($capture.expires_utc, [Globalization.CultureInfo]::InvariantCulture).AddSeconds(10)
}
$statusPath = Join-Path $PSScriptRoot 'access-expiry-runner.json'
@{state='waiting'; target_utc=$deadline.ToString('o'); process_id=$PID} | ConvertTo-Json | Set-Content -LiteralPath $statusPath
while ([DateTimeOffset]::UtcNow -lt $deadline) { Start-Sleep -Seconds 15 }
$result = & (Join-Path $PSHOME 'pwsh.exe') -NoProfile -ExecutionPolicy RemoteSigned -File (Join-Path $PSScriptRoot 'Test-AccessExpiry.ps1') -Action Replay -Team bussassistent -Audience $capture.audience -StateDirectory 'C:\Users\Jonas\AppData\Local\BussassistentAccessExpiry' -ReportDirectory $PSScriptRoot
$exitCode = $LASTEXITCODE
# The invoked helper emits only fixed messages, timestamps, status codes and report paths.
$result | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'access-expiry-runner-result.txt')
@{state='finished'; finished_utc=[DateTimeOffset]::UtcNow.ToString('o'); exit_code=$exitCode; process_id=$PID} | ConvertTo-Json | Set-Content -LiteralPath $statusPath
exit $exitCode
