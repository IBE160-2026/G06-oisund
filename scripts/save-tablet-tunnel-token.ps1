# Run interactively in the owner's local PowerShell. Never pass a token argument.
# Saves only a single remotely-managed tunnel token; starts nothing.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'protect-tablet-path.ps1')
$tabletLocalDirectory = $env:LOCALAPPDATA
if (-not $tabletLocalDirectory -or -not [IO.Path]::IsPathRooted($tabletLocalDirectory)) { throw 'Local application data path is missing or relative.' }
$tabletPilotDirectory = Join-Path $tabletLocalDirectory 'BussassistentTabletPilot'
$tabletTokenDirectory = Join-Path $tabletPilotDirectory 'credentials'
$tabletTokenPath = Join-Path $tabletTokenDirectory 'tunnel-token.txt'
# Prepare directories in the interactive user's environment, not the agent's.
# No secret is requested until both directories have restrictive ACLs.
foreach ($tabletTokenParent in @($tabletLocalDirectory, $tabletPilotDirectory, $tabletTokenDirectory)) {
    if (-not (Test-Path -LiteralPath $tabletTokenParent)) {
        if ($tabletTokenParent -eq $tabletLocalDirectory) { throw 'Local application data directory is missing.' }
        [void](New-Item -ItemType Directory -Path $tabletTokenParent -ErrorAction Stop)
    }
    $tabletDirectoryItem = Get-Item -LiteralPath $tabletTokenParent -Force
    if (-not $tabletDirectoryItem.PSIsContainer -or ($tabletDirectoryItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'Refusing a non-directory or reparse point.' }
    if ($tabletTokenParent -ne $tabletLocalDirectory) { Protect-TabletPath $tabletTokenParent }
}
if (Test-Path -LiteralPath $tabletTokenPath) { throw 'Existing tunnel token preserved; review rotation separately.' }
$tabletTokenSecure = Read-Host 'Lim inn tunnel-tokenet, eller Windows service install-kommandoen som TEKST (skjult; ingenting kjoeres)' -AsSecureString
$tabletTokenPointer = [IntPtr]::Zero
$tabletTokenText = $null
try {
    $tabletTokenPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($tabletTokenSecure)
    $tabletTokenText = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($tabletTokenPointer).Trim()
    # Treat a copied dashboard command strictly as data. No Invoke-Expression,
    # process invocation, token environment variable, clipboard read, or output.
    if ($tabletTokenText -match '^(?i:cloudflared(?:\.exe)?\s+service\s+install)\s+([A-Za-z0-9+/_=-]{80,8192})$') {
        $tabletTokenText = $Matches[1]
    }
    if ($tabletTokenText -cnotmatch '^[A-Za-z0-9+/_=-]{80,8192}$') { throw 'Input is not a recognized tunnel token or exact Windows install command. Nothing saved or executed.' }
    # CreateNew refuses an existing file even if another process created it
    # after the initial existence check. The directory ACL applies immediately.
    $tabletTokenStream = [IO.File]::Open($tabletTokenPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try {
        $tabletTokenBuffer = [Text.Encoding]::ASCII.GetBytes($tabletTokenText)
        $tabletTokenStream.Write($tabletTokenBuffer, 0, $tabletTokenBuffer.Length)
        [Array]::Clear($tabletTokenBuffer, 0, $tabletTokenBuffer.Length)
    } finally { $tabletTokenStream.Dispose() }
    Protect-TabletPath $tabletTokenPath
} finally {
    if ($tabletTokenPointer -ne [IntPtr]::Zero) { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($tabletTokenPointer) }
    $tabletTokenText = $null
    $Matches = $null
    if ($tabletTokenSecure) { $tabletTokenSecure.Dispose() }
}
Write-Output 'Tunnel-token lagret lokalt med begrenset ACL. Ingen installasjon, tjeneste, DNS-endring eller tunnelstart er utfoert. Ikke send filinnholdet i chat.'
