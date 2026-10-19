$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$api = 'http://127.0.0.1:8000'
$operation = Invoke-RestMethod -TimeoutSec 10 -Method Post "$api/operations"
$fixture = Invoke-RestMethod -TimeoutSec 10 "$api/fixture"
$body = @{ operation_id = $operation.operation_id; day = $fixture } | ConvertTo-Json -Depth 20 -Compress
$saved = Invoke-RestMethod -TimeoutSec 10 -Method Post -ContentType 'application/json' -Body $body "$api/days"
docker compose restart db api
if ($LASTEXITCODE -ne 0) { throw 'Restart failed' }
$healthy = $false
for ($attempt = 0; $attempt -lt 40; $attempt++) {
    try { $null = Invoke-RestMethod -TimeoutSec 10 "$api/health"; $healthy = $true; break } catch { Start-Sleep -Seconds 1 }
}
if (-not $healthy) { throw 'Health did not recover' }
$reopened = Invoke-RestMethod -TimeoutSec 10 "$api/days/$($saved.id)"
if (($saved | ConvertTo-Json -Depth 20 -Compress) -ne ($reopened | ConvertTo-Json -Depth 20 -Compress)) { throw 'Persisted values differ' }
$replayed = Invoke-RestMethod -TimeoutSec 10 -Method Post -ContentType 'application/json' -Body $body "$api/days"
if ($replayed.id -ne $saved.id) { throw 'Replay created a duplicate' }
Write-Output "PASS: actual DB/API restart retained identical acknowledged record $($saved.id) and replay identity."
