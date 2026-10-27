# Dedicated disposable internal network, in-memory PostgreSQL, no host ports/volumes.
param([string]$ApiImage = 'ibe160-tablet-api:11-6-security1')
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'protect-tablet-path.ps1')
$tabletProbeRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$tabletProbeId = 'ibe160-tablet-api-probe-' + [guid]::NewGuid().ToString('N')
$tabletProbeDir = Join-Path $tabletProbeRoot ('tmp/' + $tabletProbeId)
$tabletProbeNetwork = $false
$tabletProbeDb = $false
function Invoke-TabletProbeDocker {
    & docker @args
    if ($LASTEXITCODE -ne 0) { throw "Disposable API probe Docker failure: $LASTEXITCODE" }
}
try {
    New-Item -ItemType Directory -Path $tabletProbeDir -Force | Out-Null
    Protect-TabletPath $tabletProbeDir
    $tabletProbePassword = Join-Path $tabletProbeDir 'app-password'
    # Disposable test credential, never used by any ordinary/pilot service.
    [IO.File]::WriteAllText($tabletProbePassword, ([guid]::NewGuid().ToString('N') + [guid]::NewGuid().ToString('N')))
    Protect-TabletPath $tabletProbePassword
    Invoke-TabletProbeDocker network create --internal $tabletProbeId | Out-Null
    $tabletProbeNetwork = $true
    Invoke-TabletProbeDocker run -d --pull never --name ($tabletProbeId + '-db') --network $tabletProbeId --network-alias private-db --user postgres --read-only --cap-drop ALL --security-opt no-new-privileges:true --tmpfs /tmp:mode=1777 --tmpfs /var/run/postgresql:mode=1777 --tmpfs '/var/lib/postgresql/data:uid=70,gid=70,mode=0700' -e POSTGRES_USER=tablet_bootstrap -e POSTGRES_DB=private_work -e POSTGRES_PASSWORD_FILE=/run/secrets/tablet_postgres_password --mount "type=bind,source=$tabletProbePassword,target=/run/secrets/tablet_postgres_password,readonly" --mount "type=bind,source=$tabletProbeRoot/deploy/tablet/init-private-role.sql,target=/docker-entrypoint-initdb.d/010-private-role.sql,readonly" postgres:17-alpine@sha256:b0f9560a2de083e2cc7382e75f808c7381a32852a7ec49117deedb300e552b24 | Out-Null
    $tabletProbeDb = $true
    $tabletProbeReady = $false
    for ($tabletProbeAttempt = 0; $tabletProbeAttempt -lt 30; $tabletProbeAttempt++) {
        & docker exec ($tabletProbeId + '-db') pg_isready -U tablet_bootstrap -d private_work -h 127.0.0.1 *> $null
        if ($LASTEXITCODE -eq 0) { $tabletProbeReady = $true; break }
        Start-Sleep -Seconds 1
    }
    if (-not $tabletProbeReady) { throw 'Disposable database readiness timeout' }
    Invoke-TabletProbeDocker run --rm --pull never --name ($tabletProbeId + '-client') --network $tabletProbeId --user 10001:10001 --read-only --cap-drop ALL --security-opt no-new-privileges:true --tmpfs /tmp -e TABLET_DISPOSABLE_PROBE=1 -e APP_MODE=private-local -e PRIVATE_HTTPS_DEPLOYMENT=1 -e PRIVATE_ORIGIN=https://app.bussassistent.com -e PRIVATE_DATABASE_URL=postgresql://private_work@private-db/private_work -e PRIVATE_DATABASE_PASSWORD_FILE=/run/secrets/password --mount "type=bind,source=$tabletProbePassword,target=/run/secrets/password,readonly" --mount "type=bind,source=$PSScriptRoot/tablet-api-probe.py,target=/probe.py,readonly" -e PYTHONPATH=/app $ApiImage python /probe.py
} finally {
    if ($tabletProbeDb) { & docker rm -f ($tabletProbeId + '-db') | Out-Null }
    if ($tabletProbeNetwork) { & docker network rm $tabletProbeId | Out-Null }
    # Only the generated credential file is removed; no recursive deletion.
    if (Test-Path -LiteralPath (Join-Path $tabletProbeDir 'app-password')) {
        Remove-Item -LiteralPath (Join-Path $tabletProbeDir 'app-password') -Force
    }
    if (Test-Path -LiteralPath $tabletProbeDir) { Remove-Item -LiteralPath $tabletProbeDir }
}
