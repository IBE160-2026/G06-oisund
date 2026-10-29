$ErrorActionPreference = 'Stop'
$tabletScript = Get-Content -Raw (Join-Path $PSScriptRoot 'prepare-tablet-files.ps1')
# Run the actual validation prelude, before any file-system mutation.
$tabletPrelude = $tabletScript.Substring(0, $tabletScript.IndexOf('$tabletDirectory ='))
$tabletPrelude = $tabletPrelude.Replace(". (Join-Path `$PSScriptRoot 'protect-tablet-path.ps1')", '')
$tabletPrelude = $tabletPrelude.Replace('$PSScriptRoot', "'" + $PSScriptRoot.Replace("'", "''") + "'")
$failures = 0
foreach ($case in @(
    @{ Team='Upper'; Owner='owner@owner-domain.no' },
    @{ Team='a' * 64; Owner='owner@owner-domain.no' },
    @{ Team='trailing-'; Owner='owner@owner-domain.no' },
    @{ Team='replace-team'; Owner='owner@owner-domain.no' },
    @{ Team='synthetic-team'; Owner='øwner@owner-domain.no' }
    @{ Team="synthetic-team`n"; Owner='owner@owner-domain.no' },
    @{ Team='synthetic-team'; Owner="owner@owner-domain.no`n" }
)) {
    $refused = $false
    try { & ([scriptblock]::Create($tabletPrelude)) -Hostname 'bus.owner-domain.no' -TeamName $case.Team -Audience ('1' * 64) -ApprovedOwnerEmail $case.Owner -LocalOnly }
    catch { $refused = $true }
    if (-not $refused) { Write-Output 'FAIL invalid policy reached write boundary'; $failures++ }
}
foreach ($team in @('a', ('a' * 63))) {
    & ([scriptblock]::Create($tabletPrelude)) -Hostname 'bus.owner-domain.no' -TeamName $team -Audience ('1' * 64) -ApprovedOwnerEmail 'owner@owner-domain.no' -LocalOnly
}
if ($failures) { throw "$failures invalid policies admitted by preparation" }
Write-Output 'PASS preparation rejects non-parity policies before file creation'
