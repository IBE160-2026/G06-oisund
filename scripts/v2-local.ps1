#Requires -Version 7.2
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [ValidateSet('Test', 'Owner')]
    [string]$Mode,
    [switch]$ApisOnly,
    [switch]$Stop
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true
$testMode = $Mode -eq 'Test'
$project = if ($testMode) { 'ibe160-v2-tests' } else { 'ibe160-v2-owner' }
$firstPort = if ($testMode) { 19651 } else { 19661 }
$config = Join-Path $PSScriptRoot '../compose.v2.yaml'
$root = Split-Path $PSScriptRoot
$routeDirectory = Join-Path $root '.private-runtime/route'
$routeArchive = Get-Item -LiteralPath (Join-Path $routeDirectory 'troms-netex-1795129398375617.zip') -ErrorAction SilentlyContinue
$environment = @{
    V2_UI_PORT = "$firstPort"
    V2_FICTIONAL_PORT = "$($firstPort + 1)"
    V2_PRIVATE_PORT = "$($firstPort + 2)"
    V2_SUBNET = $(if ($testMode) { '10.247.206.0/28' } else { '10.247.207.0/28' })
    V2_DB_SECRET_FILE = "./.private-runtime/$project-password"
    V2_TEST_MARKER = $(if ($testMode) { 'ibe160-private-tests' } else { 'disabled' })
    V2_NOTICE_REFRESH = $(if ($testMode) { 'off' } else { 'on' })
    V2_ROUTE_ARCHIVE = $(if (!$testMode -and $routeArchive) { "/reference/$($routeArchive.Name)" })
    V2_ROUTE_OBSERVED_AT = $(if (!$testMode -and $routeArchive) { '2026-11-20T01:13:54.5323574Z' })
    VITE_FICTIONAL_API = "http://127.0.0.1:$($firstPort + 1)"
    VITE_PRIVATE_API = "http://127.0.0.1:$($firstPort + 2)"
    VITE_PRIVATE_API_BASE = $null
}
$previous = @{}
foreach ($name in $environment.Keys) {
    $previous[$name] = [Environment]::GetEnvironmentVariable($name)
    [Environment]::SetEnvironmentVariable($name, $environment[$name])
}

Push-Location $root
try {
    if ($Stop) {
        docker compose -p $project -f $config stop
        return
    }
    $runtime = Join-Path $root '.private-runtime'
    $null = New-Item -ItemType Directory -Path $runtime -Force
    $null = New-Item -ItemType Directory -Path $routeDirectory -Force
    $source = Join-Path $root $environment.V2_DB_SECRET_FILE
    if (-not (Test-Path -LiteralPath $source)) {
        $stream = [IO.File]::Open($source, 'CreateNew')
        try { $stream.Write([Text.Encoding]::ASCII.GetBytes([Convert]::ToHexString([Security.Cryptography.RandomNumberGenerator]::GetBytes(32)))) }
        finally { $stream.Dispose() }
    }
    $active = @(docker compose -p $project -f $config ps --status running --services)
    foreach ($pair in @(@(($firstPort + 1), 'api'), @(($firstPort + 2), 'private-api'))) {
        if ($pair[1] -notin $active -and (Get-NetTCPConnection -LocalPort $pair[0] -State Listen -ErrorAction SilentlyContinue)) {
            throw "Port $($pair[0]) is in use outside the selected V2 service."
        }
    }
    if (-not $ApisOnly -and (Get-NetTCPConnection -LocalPort $firstPort -State Listen -ErrorAction SilentlyContinue)) {
        throw "UI port $firstPort is already in use."
    }
    docker compose -p $project -f $config up -d --build --wait
    foreach ($port in ($firstPort + 1), ($firstPort + 2)) { "Health http://127.0.0.1:$port/health" }
    if ($ApisOnly) { return }

    Push-Location frontend
    try {
        npm ci --no-audit --no-fund
        $dist = "dist-$project"
        npm run build -- --outDir $dist
        "Open http://127.0.0.1:$firstPort/private"
        npm run start -- --outDir $dist --host 127.0.0.1 --port $firstPort
    }
    finally { Pop-Location }
}
finally {
    Pop-Location
    foreach ($name in $previous.Keys) { [Environment]::SetEnvironmentVariable($name, $previous[$name]) }
}
