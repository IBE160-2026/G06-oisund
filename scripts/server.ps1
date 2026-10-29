param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('Status','Logs','Check','Backup','Deploy','Rollback')]
    [string]$Action,
    [ValidatePattern('^[a-zA-Z0-9_.@-]+$')]
    [string]$Server = 'jonas@192.168.1.139',
    [string]$KeyFile = (Join-Path $env:USERPROFILE '.ssh/ibe160_server_ed25519'),
    [string]$Revision,
    [string]$BackupDirectory = (Join-Path $env:LOCALAPPDATA 'BussassistentServer/backups')
)
$ErrorActionPreference = 'Stop'
$sshOptions = @('-i', $KeyFile, '-o', 'IdentitiesOnly=yes', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=10', '-o', 'ServerAliveInterval=15', '-o', 'ServerAliveCountMax=2', '-o', 'StrictHostKeyChecking=yes')
function Invoke-Server([string]$Command) {
    & ssh @sshOptions $Server $Command
    if ($LASTEXITCODE -ne 0) { throw "Server command failed ($LASTEXITCODE)." }
}
if ($Action -in @('Status','Logs','Check')) {
    Invoke-Server ('sudo -n /usr/local/sbin/bussassistentctl ' + $Action.ToLowerInvariant())
    exit
}
if ($Action -eq 'Backup') {
    $result = @(Invoke-Server 'sudo -n /usr/local/sbin/bussassistentctl backup')
    $remoteFile = @($result | Where-Object { $_ -match '^/var/backups/bussassistent/[0-9TZ]+-[a-f0-9]{40}\.dump$' })
    if ($remoteFile.Count -ne 1) { throw 'No unique backup path returned.' }
    New-Item -ItemType Directory -Force -Path $BackupDirectory | Out-Null
    $BackupDirectory = (Resolve-Path -LiteralPath $BackupDirectory).Path
    & icacls $BackupDirectory /inheritance:r /grant:r "$($env:USERNAME):(OI)(CI)F" | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'Unable to protect local backup directory.' }
    $destination = Join-Path $BackupDirectory ([IO.Path]::GetFileName($remoteFile[0]))
    & scp @sshOptions ($Server + ':' + $remoteFile[0]) ($destination + '.partial')
    if ($LASTEXITCODE -ne 0) { throw 'Backup copy failed; previous backups preserved.' }
    $remoteHash = @(Invoke-Server ('sha256sum ' + $remoteFile[0]))[0].Split(' ')[0]
    if ((Get-FileHash -LiteralPath ($destination + '.partial') -Algorithm SHA256).Hash.ToLowerInvariant() -ne $remoteHash) {
        throw 'Backup transfer digest mismatch.'
    }
    Move-Item -LiteralPath ($destination + '.partial') -Destination $destination
    # Retention applies only to our generated backup filenames in the chosen directory.
    Get-ChildItem -LiteralPath $BackupDirectory -File | Where-Object {
        $_.Name -match '^[0-9TZ]+-[a-f0-9]{40}\.dump$' -and $_.LastWriteTimeUtc -lt [DateTime]::UtcNow.AddHours(-48)
    } | Remove-Item
    Write-Output "Verified backup: $destination"
    exit
}
if ($Revision -notmatch '^[a-f0-9]{40}$') { throw 'Supply a full 40-character commit SHA with -Revision.' }
if ($Action -eq 'Rollback') {
    Invoke-Server ('sudo -n /usr/local/sbin/bussassistentctl rollback ' + $Revision)
    exit
}
$repo = (& git -C $PSScriptRoot rev-parse --show-toplevel)
if ($LASTEXITCODE -ne 0) { throw 'Git checkout required.' }
$resolved = (& git -C $repo rev-parse --verify ($Revision + '^{commit}'))
if ($LASTEXITCODE -ne 0 -or $resolved -ne $Revision) { throw 'Commit not found.' }
# Archive committed files only. Local secrets, node_modules and uncommitted files are excluded.
$archive = Join-Path ([IO.Path]::GetTempPath()) ($Revision + '.tar')
if (Test-Path -LiteralPath $archive) { throw 'Temporary archive already exists; inspect before retrying.' }
try {
    & git -C $repo archive --format=tar --output=$archive $Revision backend frontend deploy
    if ($LASTEXITCODE -ne 0) { throw 'Git archive failed.' }
    $digest = (Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLowerInvariant()
    Invoke-Server 'umask 077; mkdir -p /home/jonas/ibe160-upload'
    & scp @sshOptions $archive ($Server + ':/home/jonas/ibe160-upload/' + $Revision + '.tar')
    if ($LASTEXITCODE -ne 0) { throw 'Release transfer failed.' }
    Invoke-Server ('sudo -n /usr/local/sbin/bussassistentctl stage ' + $Revision + ' ' + $digest)
    Invoke-Server ('sudo -n /usr/local/sbin/bussassistentctl install-tools ' + $Revision)
    Invoke-Server ('sudo -n /usr/local/sbin/bussassistentctl deploy ' + $Revision)
} finally {
    if (Test-Path -LiteralPath $archive) { Remove-Item -LiteralPath $archive }
}
