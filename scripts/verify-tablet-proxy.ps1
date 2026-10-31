# Uses existing local images, isolated internal network, no host ports/DB/volumes.
param(
    [string]$PythonImage = 'ibe160-tablet-access-gate-tests:11-6',
    [string]$GatewayImage = 'ibe160-tablet-gateway:11-6'
)
$ErrorActionPreference = 'Stop'
$tabletRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$tabletId = 'ibe160-tablet-probe-' + [guid]::NewGuid().ToString('N')
$tabletNetworkCreated = $false
$tabletUpstreamCreated = $false
$tabletGatewayCreated = $false
function Invoke-TabletDocker {
    & docker @args
    if ($LASTEXITCODE -ne 0) { throw "Docker command failed with exit $LASTEXITCODE" }
}
try {
    Invoke-TabletDocker network create --internal $tabletId | Out-Null
    $tabletNetworkCreated = $true
    Invoke-TabletDocker run -d --pull never --name ($tabletId + '-api') --network $tabletId --network-alias private-api --network-alias access-gate --user 10001:10001 --cap-drop ALL --security-opt no-new-privileges:true --read-only --tmpfs /tmp --mount "type=bind,source=$PSScriptRoot,target=/probe,readonly" --mount "type=bind,source=$tabletRoot/deploy/tablet/access_gate,target=/gate-test,readonly" -e PYTHONPATH=/gate-test $PythonImage python /probe/tablet-proxy-probe.py server | Out-Null
    $tabletUpstreamCreated = $true
    Invoke-TabletDocker run -d --pull never --name ($tabletId + '-gateway') --network $tabletId --network-alias gateway --user 101:101 --cap-drop ALL --security-opt no-new-privileges:true --read-only --tmpfs /tmp:mode=1777 -e TABLET_HOST=bus.owner-domain.no $GatewayImage | Out-Null
    $tabletGatewayCreated = $true
    Invoke-TabletDocker run --rm --pull never --name ($tabletId + '-client') --network $tabletId --read-only --mount "type=bind,source=$PSScriptRoot,target=/probe,readonly" $PythonImage python /probe/tablet-proxy-probe.py client
    foreach ($probeContainer in @(($tabletId + '-gateway'), ($tabletId + '-api'))) {
        $probeLogs = (& docker logs $probeContainer 2>&1 | Out-String)
        if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect synthetic proxy logs' }
        if ($probeLogs.Contains('synthetic-password-log-probe')) { throw 'Synthetic password body appeared in proxy test logs' }
    }
    Write-Output 'PASS: synthetic password body absent from gateway and probe upstream logs'
    Invoke-TabletDocker stop -t 1 ($tabletId + '-api') | Out-Null
    Invoke-TabletDocker run --rm --pull never --name ($tabletId + '-client') --network $tabletId --read-only --mount "type=bind,source=$PSScriptRoot,target=/probe,readonly" $PythonImage python /probe/tablet-proxy-probe.py down
} finally {
    if ($tabletGatewayCreated) { & docker rm -f ($tabletId + '-gateway') | Out-Null }
    if ($tabletUpstreamCreated) { & docker rm -f ($tabletId + '-api') | Out-Null }
    if ($tabletNetworkCreated) { & docker network rm $tabletId | Out-Null }
}
