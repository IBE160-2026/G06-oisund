$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
$api = 'http://127.0.0.1:8000'
$operation = Invoke-RestMethod -TimeoutSec 10 -Method Post "$api/operations"
$fixture = Invoke-RestMethod -TimeoutSec 10 "$api/fixture"
$body = @{ operation_id = $operation.operation_id; day = $fixture } | ConvertTo-Json -Depth 20 -Compress
try {
    docker compose stop db
    if ($LASTEXITCODE -ne 0) { throw 'DB stop failed' }
    $status = 0
    try { $null = Invoke-WebRequest -TimeoutSec 10 -UseBasicParsing -Method Post -ContentType 'application/json' -Body $body "$api/days" } catch {
        if ($_.Exception.Response) { $status = [int]$_.Exception.Response.StatusCode }
    }
    if ($status -ne 503) { throw "Expected DB-down 503; got $status" }
    docker compose up -d --wait db api
    if ($LASTEXITCODE -ne 0) { throw 'Recovery failed' }
    $saved = Invoke-RestMethod -TimeoutSec 10 -Method Post -ContentType 'application/json' -Body $body "$api/days"
    docker compose stop api
    if ($LASTEXITCODE -ne 0) { throw 'API stop failed' }
    $unavailable = $false
    try { $null = Invoke-RestMethod -TimeoutSec 5 "$api/days/$($saved.id)" } catch { $unavailable = $true }
    if (-not $unavailable) { throw 'Stopped API unexpectedly returned a day' }
} finally {
    docker compose up -d --wait
    if ($LASTEXITCODE -ne 0) { throw 'Assessment services did not recover' }
}
$reopened = Invoke-RestMethod -TimeoutSec 10 "$api/days/$($saved.id)"
if ($reopened.id -ne $saved.id) { throw 'Recovery returned a different record' }
Write-Output 'PASS: actual database stop returned 503; explicit retry recovered; stopped API could not return a day; services restored.'
