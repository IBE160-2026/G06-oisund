#requires -Version 7.2
param(
    [Parameter(Mandatory)][ValidateSet('Capture','Replay','Cleanup')][string]$Action,
    [Parameter(Mandatory)][ValidatePattern('^[a-z0-9][a-z0-9-]{0,62}$')][string]$Team,
    [Parameter(Mandatory)][ValidatePattern('^[a-f0-9]{64}$')][string]$Audience,
    [string]$StateDirectory = (Join-Path $env:LOCALAPPDATA 'BussassistentAccessExpiry'),
    [string]$ReportDirectory = $PSScriptRoot
)
$ErrorActionPreference = 'Stop'
# Fixed read-only targets. No redirects, cookie jar, browser automation or app session.
$service = 'https://app.bussassistent.com'
$issuer = 'https://' + $Team + '.cloudflareaccess.com'
$secretFile = Join-Path $StateDirectory 'token.dpapi'
$bindingFile = Join-Path $StateDirectory 'binding.json'
function Decode64([string]$Value) {
    $v = $Value.Replace('-', '+').Replace('_', '/')
    $v += '=' * ((4 - $v.Length % 4) % 4)
    return ,([Convert]::FromBase64String($v))
}
function Digest([byte[]]$Bytes) { [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($Bytes)).ToLowerInvariant() }
function New-Client {
    $h = [Net.Http.HttpClientHandler]::new()
    $h.AllowAutoRedirect = $false; $h.UseCookies = $false
    $c = [Net.Http.HttpClient]::new($h)
    $c.Timeout = [TimeSpan]::FromSeconds(20)
    $c.DefaultRequestHeaders.UserAgent.ParseAdd('Mozilla/5.0 AccessExpiryVerification/1.0')
    return $c
}
function Probe([string]$Path, [string]$Token) {
    $c = New-Client
    $req = [Net.Http.HttpRequestMessage]::new([Net.Http.HttpMethod]::Get, $service + $Path)
    $null = $req.Headers.TryAddWithoutValidation('Cookie', 'CF_Authorization=' + $Token)
    try {
        $r = $c.SendAsync($req).GetAwaiter().GetResult()
        $bytes = $r.Content.ReadAsByteArrayAsync().GetAwaiter().GetResult()
        $loc = $r.Headers.Location
        $redirectHost = $null; $redirectPath = $null
        if ($loc) {
            $absolute = [Uri]::new([Uri]$service, $loc)
            $redirectHost = $absolute.Host
            $redirectPath = $absolute.AbsolutePath # Never persist query/fragment.
        }
        $text = [Text.Encoding]::UTF8.GetString($bytes)
        $record = [ordered]@{
            path=$Path; time_utc=[DateTimeOffset]::UtcNow.ToString('o'); status=[int]$r.StatusCode
            redirect_host=$redirectHost; redirect_path=$redirectPath
            cache_control=[string]$r.Headers.CacheControl
            bytes=$bytes.Length
            app_shell=($text -match '<script[^>]+src="/assets/')
            app_login_required=([int]$r.StatusCode -eq 401)
            body_sha256=(Digest $bytes)
        }
        # Body is never written or emitted. A 401 alone is not proof of Access rejection.
        $r.Dispose()
        return $record
    } catch { throw 'HTTP probe failed; no response or exception details saved. Test is inconclusive.' }
    finally { $req.Dispose(); $c.Dispose() }
}
try {
    if (-not $IsWindows) { throw 'Windows DPAPI is required.' }
    if ((Test-Path -LiteralPath $StateDirectory) -and ((Get-Item -LiteralPath $StateDirectory).Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw 'State directory must not be a reparse point.' }
    if ($Action -eq 'Cleanup') {
        foreach ($p in @($secretFile,$bindingFile)) {
            if (Test-Path -LiteralPath $p) { Remove-Item -LiteralPath $p }
        }
        if ((Test-Path -LiteralPath $StateDirectory) -and @(Get-ChildItem -LiteralPath $StateDirectory -Force).Count -eq 0) { Remove-Item -LiteralPath $StateDirectory }
        Write-Output 'Removed this test token and binding. Sanitized reports retained.'
        exit 0
    }
    if ($Action -eq 'Capture') {
        if (Test-Path -LiteralPath $StateDirectory) { throw 'State directory already exists; inspect or clean the previous test first.' }
        $null = New-Item -ItemType Directory -Path $StateDirectory
        $sid = [Security.Principal.WindowsIdentity]::GetCurrent().User
        $acl = [Security.AccessControl.DirectorySecurity]::new()
        $acl.SetAccessRuleProtection($true,$false)
        foreach ($id in @($sid,[Security.Principal.SecurityIdentifier]::new('S-1-5-18'))) {
            $acl.AddAccessRule([Security.AccessControl.FileSystemAccessRule]::new($id,'FullControl','ContainerInherit,ObjectInherit','None','Allow'))
        }
        Set-Acl -LiteralPath $StateDirectory -AclObject $acl
        $secure = Read-Host 'Paste ONLY the app CF_Authorization value here (hidden)' -AsSecureString
    } else {
        $binding = Get-Content -LiteralPath $bindingFile -Raw | ConvertFrom-Json
        if ($binding.issuer -ne $issuer -or $binding.audience -ne $Audience -or $binding.service -ne $service) { throw 'Configuration differs from capture.' }
        $secure = (Get-Content -LiteralPath $secretFile -Raw).Trim() | ConvertTo-SecureString
    }
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try { $token = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
    if ($token -notmatch '^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$' -or $token.Length -gt 16384) { throw 'Input is not a compact JWT.' }
    $parts = $token.Split('.')
    $header = [Text.Encoding]::UTF8.GetString((Decode64 $parts[0])) | ConvertFrom-Json
    $claims = [Text.Encoding]::UTF8.GetString((Decode64 $parts[1])) | ConvertFrom-Json
    if ($header.alg -ne 'RS256' -or $header.crit -or -not $header.kid) { throw 'Unsupported token header.' }
    $c = New-Client
    try {
        $response = $c.GetAsync($issuer + '/cdn-cgi/access/certs').GetAwaiter().GetResult()
        if ([int]$response.StatusCode -ne 200) { throw 'Fixed JWKS endpoint unavailable.' }
        $jwks = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult() | ConvertFrom-Json
        $response.Dispose()
    } finally { $c.Dispose() }
    $keys = @($jwks.keys | Where-Object { $_.kid -ceq $header.kid -and $_.kty -eq 'RSA' })
    if ($keys.Count -ne 1) { throw 'No unique signing key.' }
    $rsa = [Security.Cryptography.RSA]::Create()
    $parameters = [Security.Cryptography.RSAParameters]::new()
    $parameters.Modulus = Decode64 $keys[0].n; $parameters.Exponent = Decode64 $keys[0].e
    $rsa.ImportParameters($parameters)
    $valid = $rsa.VerifyData([Text.Encoding]::ASCII.GetBytes($parts[0]+'.'+$parts[1]),(Decode64 $parts[2]),[Security.Cryptography.HashAlgorithmName]::SHA256,[Security.Cryptography.RSASignaturePadding]::Pkcs1)
    $rsa.Dispose()
    if (-not $valid -or $claims.iss -cne $issuer -or $Audience -cnotin @($claims.aud) -or $claims.type -ne 'app' -or -not $claims.sub -or -not $claims.email) { throw 'Signature or service claims failed.' }
    if ($claims.exp -isnot [long] -and $claims.exp -isnot [int]) { throw 'Invalid expiry.' }
    if ($claims.iat -isnot [long] -and $claims.iat -isnot [int]) { throw 'Invalid issued-at.' }
    $now = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
    if ($claims.exp -le $claims.iat -or $claims.iat -gt $now -or ($claims.nbf -and $claims.nbf -gt $now)) { throw 'Invalid token lifetime.' }
    $digest = Digest ([Text.Encoding]::ASCII.GetBytes($token))
    if ($Action -eq 'Capture') {
        if ($claims.exp -le $now + 120) { throw 'Need a valid token with at least two minutes remaining.' }
    } else {
        if ($digest -cne $binding.token_sha256) { throw 'Token differs from capture.' }
        if ($now -le $claims.exp + 5) { throw 'Not yet past actual expiry plus five seconds; no replay sent.' }
    }
    $results = @(Probe '/private' $token; Probe '/private-api/drafts' $token)
    $prePassed = $results[0].status -eq 200 -and $results[0].app_shell -and $results[1].status -eq 401
    $meta = [ordered]@{
        test_id='CF-EXP-01'; phase=$Action; time_utc=[DateTimeOffset]::UtcNow.ToString('o')
        service=$service; issuer=$issuer; audience=$Audience; signature_valid=$valid
        issued_utc=[DateTimeOffset]::FromUnixTimeSeconds($claims.iat).ToString('o')
        expires_utc=[DateTimeOffset]::FromUnixTimeSeconds($claims.exp).ToString('o')
        exact_token_match=($Action -eq 'Replay'); before_control_passed=$prePassed
        results=$results; attribution='External boundary only; origin gate not independently observed'
    }
    $null = New-Item -ItemType Directory -Force -Path $ReportDirectory
    $report = Join-Path $ReportDirectory ('access-expiry-' + $Action.ToLowerInvariant() + '-' + [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ') + '.json')
    $meta | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $report
    if ($Action -eq 'Capture') {
        if (-not $prePassed) { throw 'Before-expiry control failed; sanitized attempt retained, token not saved.' }
        $secure | ConvertFrom-SecureString | Set-Content -LiteralPath $secretFile
        @{issuer=$issuer; audience=$Audience; service=$service; token_sha256=$digest} | ConvertTo-Json | Set-Content -LiteralPath $bindingFile
    }
    Write-Output ('Sanitized report: ' + $report)
    Write-Output ('Actual expiry UTC: ' + $meta.expires_utc)
    Write-Output ('HTTP status: ' + (($results | ForEach-Object { $_.status }) -join ', '))
} catch {
    # Do not emit raw exceptions: network/parser errors can embed sensitive input.
    Write-Output 'Test did not complete. No token or raw error is printed. Inspect sanitized reports; do not share token values.'
    exit 1
} finally {
    $token = $null; $claims = $null; $parts = $null
    if ($secure) { $secure.Dispose() }
}
