param([string]$EnvironmentFile = '.env.tablet')
$ErrorActionPreference = 'Stop'
$tabletRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
Push-Location $tabletRoot
try {
    $tabletJson = & docker compose --env-file $EnvironmentFile -f compose.tablet.yaml --profile tablet config --format json
    if ($LASTEXITCODE -ne 0) { throw 'Compose configuration failed.' }
    $tablet = ($tabletJson -join "`n") | ConvertFrom-Json
    if ($tablet.name -ne 'ibe160-tablet-prep') { throw 'Unexpected project name.' }
    if ($tablet.services.'private-api'.ports -or $tablet.services.'private-db'.ports -or $tablet.services.'access-gate'.ports) { throw 'API/database/gate must have no host ports.' }
    foreach ($tabletName in @('gateway','private-api','access-gate')) {
        $tabletService = $tablet.services.$tabletName
        if (-not $tabletService.read_only -or $tabletService.user -notmatch '^(101:101|10001:10001)$' -or
            'ALL' -notin $tabletService.cap_drop -or 'no-new-privileges:true' -notin $tabletService.security_opt -or
            $tabletService.privileged -or $tabletService.network_mode -eq 'host') { throw "Missing isolation: $tabletName" }
    }
    if (-not $tablet.networks.app.internal -or -not $tablet.networks.storage.internal) { throw 'App/storage networks must be internal.' }
    if ($tablet.networks.front.internal -or $tablet.networks.front.enable_ipv6 -or
        $tablet.networks.front.driver -ne 'bridge' -or
        $tablet.networks.front.driver_opts.'com.docker.network.bridge.host_binding_ipv4' -ne '127.0.0.1') { throw 'Gateway publishing network must use loopback defaults and no IPv6.' }
    if (@($tablet.services.gateway.networks.PSObject.Properties.Name).Count -ne 2 -or
        -not $tablet.services.gateway.networks.PSObject.Properties['front'] -or
        -not $tablet.services.gateway.networks.PSObject.Properties['app'] -or
        $tablet.services.'private-api'.networks.PSObject.Properties['front'] -or
        $tablet.services.'private-db'.networks.PSObject.Properties['front'] -or
        $tablet.services.'access-gate'.networks.PSObject.Properties['front']) { throw 'Only gateway may join the publishing network.' }
    foreach ($tabletName in @('gateway','private-api','private-db')) {
        foreach ($tabletTmpfs in @($tablet.services.$tabletName.tmpfs)) {
            if ($tabletTmpfs -notmatch '^/') { throw "Invalid tmpfs mount: $tabletName" }
        }
    }
    if (@($tablet.services.'private-api'.tmpfs).Count -ne 1 -or
        @($tablet.services.gateway.tmpfs).Count -ne 1) { throw 'Unexpected API/gateway tmpfs count; quote comma-separated YAML options.' }
    if ($tablet.services.'private-db'.user -ne 'postgres' -or -not $tablet.services.'private-db'.read_only -or
        'ALL' -notin $tablet.services.'private-db'.cap_drop -or
        $tablet.services.'private-db'.environment.POSTGRES_USER -ne 'tablet_bootstrap' -or
        $tablet.services.'private-api'.secrets.source -contains 'tablet_bootstrap_password') { throw 'Database/bootstrap isolation missing.' }
    if ($tablet.services.gateway.ports.Count -ne 1 -or
        $tablet.services.gateway.ports[0].host_ip -ne '127.0.0.1' -or
        $tablet.services.gateway.ports[0].published -ne '18081') { throw 'Unexpected gateway binding.' }
    if ($tablet.volumes.tablet_pg.name -ne 'ibe160-tablet-prep_tablet_pg' -or $tablet.volumes.tablet_pg.external) { throw 'Unexpected volume.' }
    if ($tablet.services.'private-api'.environment.PRIVATE_LOOPBACK_DEVELOPMENT -or
        $tablet.services.'private-api'.environment.PRIVATE_HTTPS_DEPLOYMENT -ne '1') { throw 'Conflicting transport modes.' }
    Write-Output 'PASS: standalone project, loopback gateway, unpublished API/database, separate volume, explicit HTTPS mode. No services started.'
} finally { Pop-Location }
