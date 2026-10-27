# Downloads and verifies a portable client only. Never installs or runs it.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'protect-tablet-path.ps1')
$tabletClientVersion = '2026.10.4'
$tabletExpectedHash = '411b16d40c8d872243efeb52c550053d00af0a8a97fbb32e730fb8aba429eaa8'
$tabletDownloadUrl = 'https://github.com/cloudflare/cloudflared/releases/download/2026.10.4/cloudflared-windows-amd64.exe'
if (-not [Environment]::Is64BitOperatingSystem) { throw 'This preparation requires 64-bit Windows.' }
if (-not $env:LOCALAPPDATA -or -not [IO.Path]::IsPathRooted($env:LOCALAPPDATA)) { throw 'Local application data path is missing or relative.' }
$tabletClientRoot = Join-Path $env:LOCALAPPDATA 'BussassistentTabletPilot'
$tabletClientBin = Join-Path $tabletClientRoot 'bin'
foreach ($tabletDirectory in @($env:LOCALAPPDATA, $tabletClientRoot, $tabletClientBin)) {
    if (-not (Test-Path -LiteralPath $tabletDirectory)) {
        if ($tabletDirectory -eq $env:LOCALAPPDATA) { throw 'Local application data directory is missing.' }
        [void](New-Item -ItemType Directory -Path $tabletDirectory -ErrorAction Stop)
    }
    $tabletDirectoryItem = Get-Item -LiteralPath $tabletDirectory -Force
    if (-not $tabletDirectoryItem.PSIsContainer -or ($tabletDirectoryItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Refusing a non-directory or reparse point.' }
    if ($tabletDirectory -ne $env:LOCALAPPDATA) { Protect-TabletPath $tabletDirectory }
}
$tabletClientTarget = Join-Path $tabletClientBin ('cloudflared-' + $tabletClientVersion + '.exe')
function Assert-TabletClientFile([string]$LiteralPath) {
    $tabletClientItem = Get-Item -LiteralPath $LiteralPath -Force
    if ($tabletClientItem.PSIsContainer -or ($tabletClientItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Refusing a non-file or reparse point.' }
    if ((Get-FileHash -LiteralPath $LiteralPath -Algorithm SHA256).Hash -ne $tabletExpectedHash) { throw 'Client SHA-256 mismatch. Nothing executed.' }
    $tabletClientSignature = Get-AuthenticodeSignature -LiteralPath $LiteralPath
    if ($tabletClientSignature.Status -ne 'Valid' -or $tabletClientSignature.SignerCertificate.Subject -notmatch 'O="?Cloudflare, Inc\.') { throw 'Client signature or publisher mismatch. Nothing executed.' }
}
if (Test-Path -LiteralPath $tabletClientTarget) {
    Assert-TabletClientFile $tabletClientTarget
    Protect-TabletPath $tabletClientTarget
    Write-Output 'Eksisterende klient kontrollert: SHA-256 og signatur OK. Ingenting startet.'
    return
}
$tabletClientTemporary = Join-Path $tabletClientBin ([guid]::NewGuid().ToString('N') + '.download.exe')
$tabletPreviousTls = [Net.ServicePointManager]::SecurityProtocol
try {
    [Net.ServicePointManager]::SecurityProtocol = $tabletPreviousTls -bor [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $tabletDownloadUrl -OutFile $tabletClientTemporary -UseBasicParsing
    Assert-TabletClientFile $tabletClientTemporary
    Protect-TabletPath $tabletClientTemporary
    # File.Move refuses an existing target. Never replace a different client.
    [IO.File]::Move($tabletClientTemporary, $tabletClientTarget)
    Write-Output 'Portabel klient lagret: SHA-256 og Cloudflare-signatur OK. Ingen installasjon, tunnelstart eller DNS-endring.'
} finally {
    [Net.ServicePointManager]::SecurityProtocol = $tabletPreviousTls
    # Only this invocation's random temporary file, never recursive deletion.
    if (Test-Path -LiteralPath $tabletClientTemporary -PathType Leaf) { Remove-Item -LiteralPath $tabletClientTemporary -Force }
}
