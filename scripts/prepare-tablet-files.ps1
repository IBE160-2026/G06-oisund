param(
    [Parameter(Mandatory)][string]$Hostname,
    [guid]$TunnelId,
    [Parameter(Mandatory)][string]$TeamName,
    [Parameter(Mandatory)][string]$Audience,
    [Parameter(Mandatory)][string]$ApprovedOwnerEmail,
    [string]$TunnelCredentialPath,
    [switch]$LocalOnly
)
$ErrorActionPreference = 'Stop'
$tabletRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
. (Join-Path $PSScriptRoot 'protect-tablet-path.ps1')
if ($Hostname -cnotmatch '^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z][a-z0-9-]{0,62}$' -or
    $Hostname -match '\.(invalid|example|test|local|localhost)$' -or $Hostname.Length -gt 253 -or
    $Hostname -in @('example.com','example.net','example.org')) { throw 'Use the actual canonical public DNS hostname.' }
if ($TeamName -notmatch '^[a-z0-9][a-z0-9-]*$') { throw 'Invalid Zero Trust team name.' }
if ($Audience -notmatch '^[a-fA-F0-9]{64}$') { throw 'Use the 64-character Access application AUD.' }
if ($Audience -eq ('0' * 64)) { throw 'Replace placeholder audience.' }
if (-not $LocalOnly -and (-not $TunnelId -or $TunnelId -eq [guid]::Empty)) { throw 'Actual tunnel ID required for tunnel configuration.' }
if ($LocalOnly -and ($TunnelId -or $TunnelCredentialPath)) { throw 'Local-only preparation must not supply tunnel identifiers or credentials.' }
if ($ApprovedOwnerEmail -cnotmatch '^[^\s@*,;<>]+@[^\s@*,;<>]+\.[^\s@*,;<>]+$' -or
    $ApprovedOwnerEmail -cne $ApprovedOwnerEmail.ToLowerInvariant() -or
    $ApprovedOwnerEmail -match '\.(invalid|test|example)$') { throw 'Use one explicitly approved canonical owner email, never a domain or list.' }
if (-not $LocalOnly) {
if (-not $TunnelCredentialPath -or -not [IO.Path]::IsPathFullyQualified($TunnelCredentialPath) -or
    $TunnelCredentialPath -match '[\r\n]') { throw 'Use an absolute local tunnel credential path.' }
$tabletCredentialFull = [IO.Path]::GetFullPath($TunnelCredentialPath)
if ($tabletCredentialFull.StartsWith($tabletRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Tunnel credentials must be outside this Git worktree.' }
}
$tabletDirectory = Join-Path $tabletRoot '.private-runtime/tablet'
$tabletEnv = Join-Path $tabletRoot '.env.tablet'
$tabletConfig = Join-Path $tabletDirectory 'cloudflared.yml'
$tabletPolicyPath = Join-Path $tabletDirectory 'access-policy.json'
if ((Test-Path -LiteralPath $tabletEnv) -or (Test-Path -LiteralPath $tabletConfig) -or (Test-Path -LiteralPath $tabletPolicyPath)) {
    throw 'Existing local configuration preserved. Review/edit it manually; no files changed.'
}
if (-not $LocalOnly) {
$tabletTemplate = [IO.File]::ReadAllText((Join-Path $tabletRoot 'deploy/tablet/cloudflared.example.yml'))
$tabletCredential = ConvertTo-Json ($TunnelCredentialPath.Replace('\','/')) -Compress
$tabletTemplate = $tabletTemplate.Replace('C:/Users/Jonas/.cloudflared/REPLACE-TUNNEL-UUID.json', $tabletCredential)
$tabletTemplate = $tabletTemplate.Replace('bus.YOUR-DOMAIN.invalid', $Hostname).Replace('REPLACE-TUNNEL-UUID', $TunnelId.ToString())
$tabletTemplate = $tabletTemplate.Replace('REPLACE-ZERO-TRUST-TEAM', $TeamName).Replace('REPLACE-PRIVATE-APPLICATION-AUD', $Audience)
}
foreach ($tabletCandidate in @((Join-Path $tabletRoot '.private-runtime'), $tabletDirectory)) {
    if ((Test-Path -LiteralPath $tabletCandidate) -and ((Get-Item -LiteralPath $tabletCandidate -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Refusing a private runtime reparse point.' }
}
New-Item -ItemType Directory -Path $tabletDirectory -Force | Out-Null
Protect-TabletPath $tabletDirectory
$tabletSecret = Join-Path $tabletDirectory 'postgres-password'
$tabletBootstrapSecret = Join-Path $tabletDirectory 'bootstrap-password'
foreach ($tabletSecretFile in @($tabletSecret, $tabletBootstrapSecret)) {
if (-not (Test-Path -LiteralPath $tabletSecretFile)) {
    $tabletBytes = New-Object byte[] 32
    $tabletRandom = [Security.Cryptography.RandomNumberGenerator]::Create()
    try { $tabletRandom.GetBytes($tabletBytes) } finally { $tabletRandom.Dispose() }
    [IO.File]::WriteAllText($tabletSecretFile, [Convert]::ToBase64String($tabletBytes), [Text.Encoding]::ASCII)
}
Protect-TabletPath $tabletSecretFile
}
[IO.File]::WriteAllText($tabletEnv, "TABLET_HOST=$Hostname`n", [Text.UTF8Encoding]::new($false))
Protect-TabletPath $tabletEnv
if (-not $LocalOnly) {
    [IO.File]::WriteAllText($tabletConfig, $tabletTemplate, [Text.UTF8Encoding]::new($false))
    Protect-TabletPath $tabletConfig
}
$tabletPolicy = @{ team=$TeamName; audience=$Audience.ToLowerInvariant(); owner_email=$ApprovedOwnerEmail } | ConvertTo-Json
[IO.File]::WriteAllText($tabletPolicyPath, $tabletPolicy, [Text.UTF8Encoding]::new($false))
Protect-TabletPath $tabletPolicyPath
if ($LocalOnly) {
    Write-Output 'Local-only tablet files prepared with current-user/SYSTEM ACL. No tunnel configuration or credentials created.'
} else {
    Write-Output 'Local tablet files prepared with current-user/SYSTEM ACL. No tunnel, DNS, service or container started.'
}
