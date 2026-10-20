$ErrorActionPreference = 'Stop'
$privateRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$privateDirectory = Join-Path $privateRoot '.private-runtime'
$privateSecret = Join-Path $privateDirectory 'postgres-password'
if (-not (Test-Path -LiteralPath $privateSecret)) {
    New-Item -ItemType Directory -Path $privateDirectory -Force | Out-Null
    $privateBytes = New-Object byte[] 32
    $privateRandom = [Security.Cryptography.RandomNumberGenerator]::Create()
    try { $privateRandom.GetBytes($privateBytes) } finally { $privateRandom.Dispose() }
    [IO.File]::WriteAllText($privateSecret, [Convert]::ToBase64String($privateBytes), [Text.Encoding]::ASCII)
}
Write-Output 'Private local database secret is ready. Existing secret preserved.'
