param([Parameter(Mandatory=$true)][string]$RuntimeRoot)
$ErrorActionPreference = 'Stop'
$RuntimeRoot = (Resolve-Path -LiteralPath $RuntimeRoot).Path
$identity = Get-Content -LiteralPath (Join-Path $RuntimeRoot 'build-identity.json') -Raw | ConvertFrom-Json
foreach ($service in @('api','gateway')) {
    $expected = $identity.$service
    $actual = (& docker image inspect $expected.tag | ConvertFrom-Json)[0]
    if ($LASTEXITCODE -ne 0 -or $actual.Id -ne $expected.id -or
        $actual.Config.Labels.'org.opencontainers.image.revision' -ne $identity.source) {
        throw "Image identity mismatch: $service"
    }
}
& docker compose --env-file (Join-Path $RuntimeRoot '.env.tablet') -f (Join-Path $RuntimeRoot 'compose.yaml') --profile tablet up -d --no-build --wait --wait-timeout 90
if ($LASTEXITCODE -ne 0) { throw 'Production compose startup failed' }
$clientRoot = 'C:\Users\Jonas\AppData\Local\BussassistentTabletPilot'
$client = Join-Path $clientRoot 'bin\cloudflared-2026.10.4.exe'
$tokenFile = Join-Path $clientRoot 'credentials\tunnel-token.txt'
if (-not (Test-Path -LiteralPath $tokenFile) -or
    (Get-FileHash -LiteralPath $client -Algorithm SHA256).Hash -ne '411B16D40C8D872243EFEB52C550053D00AF0A8A97FBB32E730FB8ABA429EAA8' -or
    (Get-AuthenticodeSignature -LiteralPath $client).Status -ne 'Valid') { throw 'Tunnel credential or signed client check failed' }
$running = @(Get-CimInstance Win32_Process -Filter "name='cloudflared-2026.10.4.exe' OR name='cloudflared.exe'")
if ($running.Count) {
    if ($running.Count -ne 1 -or $running[0].ExecutablePath -ne $client -or
        $running[0].CommandLine -notlike '*4aecb83e-cf83-4112-8f76-9a564252e1fe*') { throw 'Unexpected existing connector; inspect before starting another' }
    Write-Output "Existing tunnel process: $($running[0].ProcessId)"
} else {
    $args = @('tunnel','--no-autoupdate','--metrics','127.0.0.1:18083','run','--token-file',('"' + $tokenFile + '"'),'4aecb83e-cf83-4112-8f76-9a564252e1fe')
    $process = Start-Process -FilePath $client -ArgumentList $args -WorkingDirectory $RuntimeRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $RuntimeRoot 'tunnel.stdout.log') -RedirectStandardError (Join-Path $RuntimeRoot 'tunnel.stderr.log')
    $process.Id | Set-Content -LiteralPath (Join-Path $RuntimeRoot 'tunnel.pid')
    Write-Output "Started tunnel process: $($process.Id)"
}
# Deliberately no service installation, scheduled task, DNS or Access changes.
