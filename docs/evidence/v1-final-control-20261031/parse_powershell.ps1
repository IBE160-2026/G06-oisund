$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))
$files = @(git -C $root ls-files '*.ps1')
$results = @()
foreach ($name in $files) {
    $tokens = $null; $errors = $null
    $null = [Management.Automation.Language.Parser]::ParseFile((Join-Path $root $name), [ref]$tokens, [ref]$errors)
    $results += @{path=$name; errors=@($errors).Count}
}
$readme = Get-Content -LiteralPath (Join-Path $root 'README.md') -Raw
$blocks = [regex]::Matches($readme, '(?s)```powershell\r?\n(.*?)```')
$i = 0
foreach ($block in $blocks) {
    $i++; $tokens = $null; $errors = $null
    $null = [Management.Automation.Language.Parser]::ParseInput($block.Groups[1].Value, [ref]$tokens, [ref]$errors)
    $results += @{path=('README.md block ' + $i); errors=@($errors).Count}
}
$result = @{at_utc=[DateTimeOffset]::UtcNow.ToString('o'); powershell_version=$PSVersionTable.PSVersion.ToString(); parser_only=$true; scripts=$files.Count; readme_blocks=$blocks.Count; results=$results; passed=(@($results | Where-Object errors -ne 0).Count -eq 0)}
$result | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'powershell-parse.json')
if (-not $result.passed) { throw 'PowerShell parse failure' }
Write-Output ('PASS parser-only: ' + $files.Count + ' scripts and ' + $blocks.Count + ' README blocks')
