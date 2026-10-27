# Read-only local admission/isolation check. No valid Access token or data writes.
$ErrorActionPreference = 'Stop'
$tabletCheckRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
Push-Location $tabletCheckRoot
try {
    $tabletCheckNames = @('ibe160-tablet-prep-private-db-1','ibe160-tablet-prep-private-api-1','ibe160-tablet-prep-access-gate-1','ibe160-tablet-prep-gateway-1')
    $tabletCheckRaw = & docker inspect @tabletCheckNames
    if ($LASTEXITCODE -ne 0) { throw 'Pilot inspect failed' }
    $tabletCheckContainers = ($tabletCheckRaw -join "`n") | ConvertFrom-Json
    foreach ($tabletCheckContainer in $tabletCheckContainers) {
        if ($tabletCheckContainer.Config.Labels.'com.docker.compose.project' -ne 'ibe160-tablet-prep' -or
            -not $tabletCheckContainer.State.Running -or -not $tabletCheckContainer.HostConfig.ReadonlyRootfs -or
            $tabletCheckContainer.HostConfig.Privileged -or 'ALL' -notin $tabletCheckContainer.HostConfig.CapDrop -or
            'no-new-privileges:true' -notin $tabletCheckContainer.HostConfig.SecurityOpt -or
            $tabletCheckContainer.HostConfig.RestartPolicy.Name -ne 'no') { throw 'Pilot runtime isolation mismatch' }
        if ($tabletCheckContainer.Name -match 'private-(api|db)-1$' -and $tabletCheckContainer.State.Health.Status -ne 'healthy') { throw 'Pilot API/database not healthy' }
        $tabletCheckPublished = @($tabletCheckContainer.NetworkSettings.Ports.PSObject.Properties | ForEach-Object { $_.Value } | Where-Object { $_ })
        if ($tabletCheckContainer.Name -eq '/ibe160-tablet-prep-gateway-1') {
            if ($tabletCheckPublished.Count -ne 1 -or $tabletCheckPublished[0].HostIp -ne '127.0.0.1' -or $tabletCheckPublished[0].HostPort -ne '18081') { throw 'Gateway actual binding is not exclusively loopback' }
        } elseif ($tabletCheckPublished.Count) { throw 'API/database/admission host port must not exist' }
        foreach ($tabletCheckMount in $tabletCheckContainer.Mounts) {
            if ($tabletCheckMount.Type -eq 'volume' -and $tabletCheckMount.Name -ne 'ibe160-tablet-prep_tablet_pg') { throw 'Unexpected pilot volume' }
            if ($tabletCheckMount.Source -match '(?i)(docker\.sock|D:[/\\]IBE160(?:[/\\]|$))') { throw 'Forbidden ordinary source/socket mount' }
        }
    }
    $tabletCheckNetworks = (& docker network inspect ibe160-tablet-prep_app ibe160-tablet-prep_storage ibe160-tablet-prep_front ibe160-tablet-prep_keys | ConvertFrom-Json)
    if ($LASTEXITCODE -ne 0) { throw 'Pilot network inspect failed' }
    foreach ($tabletCheckNet in $tabletCheckNetworks) {
        if ($tabletCheckNet.Name -match '_(app|storage)$' -and -not $tabletCheckNet.Internal) { throw 'Private network must be internal' }
        if ($tabletCheckNet.Name -eq 'ibe160-tablet-prep_front' -and
            ($tabletCheckNet.EnableIPv6 -or $tabletCheckNet.Options.'com.docker.network.bridge.host_binding_ipv4' -ne '127.0.0.1')) { throw 'Unexpected publishing network' }
        foreach ($tabletCheckPeer in $tabletCheckNet.Containers.PSObject.Properties.Value) {
            if ($tabletCheckPeer.Name -notin $tabletCheckNames) { throw 'Unexpected peer on pilot network' }
            if ($tabletCheckNet.Name -eq 'ibe160-tablet-prep_front' -and $tabletCheckPeer.Name -ne 'ibe160-tablet-prep-gateway-1') { throw 'Only gateway may use front network' }
        }
    }
    $tabletCheckAssets = @(& docker exec ibe160-tablet-prep-gateway-1 find /usr/share/nginx/html/assets -name '*.js')
    if ($LASTEXITCODE -ne 0 -or -not $tabletCheckAssets.Count) { throw 'Built private asset missing' }
    $tabletCheckAssetPath = '/assets/' + [IO.Path]::GetFileName($tabletCheckAssets[0])
    $tabletCheckCases = @(
        @{Method='GET';Path='/'}, @{Method='GET';Path='/private'},
        @{Method='GET';Path=$tabletCheckAssetPath},
        @{Method='GET';Path='/private-api/auth/session'},
        @{Method='GET';Path='/private-api/drafts'},
        @{Method='POST';Path='/private-api/drafts'}
    )
    New-Item -ItemType Directory -Path tmp/tablet-local-pilot -Force | Out-Null
    $tabletCheckHeaderFile = Join-Path $tabletCheckRoot 'tmp/tablet-local-pilot/denial-response-headers.txt'
    $tabletCheckCount = 0
    foreach ($tabletCheckToken in @('', 'not.a.jwt', 'eyJhbGciOiJub25lIn0.e30.')) {
        foreach ($tabletCheckCase in $tabletCheckCases) {
            $tabletCheckCurl = @('--noproxy','*','--max-time','5','--silent','--output','NUL','--write-out','%{http_code}',
                '--dump-header',$tabletCheckHeaderFile,'--header','Host: app.bussassistent.com','--request',$tabletCheckCase.Method)
            if ($tabletCheckToken) { $tabletCheckCurl += @('--header', ('Cf-Access-Jwt-Assertion: ' + $tabletCheckToken)) }
            if ($tabletCheckCase.Method -eq 'POST') { $tabletCheckCurl += @('--header','Content-Type: application/json','--data','{}') }
            $tabletCheckCurl += 'http://127.0.0.1:18081' + $tabletCheckCase.Path
            $tabletCheckCode = & curl.exe @tabletCheckCurl
            if ($LASTEXITCODE -ne 0 -or $tabletCheckCode -ne '403') { throw 'Expected local Access denial was not observed' }
            if ([IO.File]::ReadAllText($tabletCheckHeaderFile) -notmatch '(?im)^Cache-Control:\s*no-store\s*$') { throw 'Denied response must be no-store' }
            $tabletCheckCount++
        }
    }
    $tabletCheckWrongHost = & curl.exe --noproxy '*' --max-time 5 --silent --output NUL --write-out '%{http_code}' --header 'Host: wrong.invalid' http://127.0.0.1:18081/
    if ($LASTEXITCODE -ne 52 -or $tabletCheckWrongHost -ne '000') { throw 'Expected wrong-host connection close' }
    $tabletCheckInternal = & curl.exe --noproxy '*' --max-time 5 --silent --output NUL --write-out '%{http_code}' --header 'Host: app.bussassistent.com' http://127.0.0.1:18081/_access_verify
    if ($LASTEXITCODE -ne 0 -or $tabletCheckInternal -ne '404') { throw 'Admission subrequest must be internal only' }
    if (Test-Path -LiteralPath .private-runtime/tablet/cloudflared.yml) { throw 'Local-only pilot must not have tunnel configuration' }
    Write-Output "PASS: $tabletCheckCount live localhost denials (pages, built asset, API GET/POST x missing/malformed/alg-none); no-store; wrong Host and internal auth denied; runtime ports, own volume/networks, read-only/caps/restart isolation. No public requests or data writes."
} finally { Pop-Location }
