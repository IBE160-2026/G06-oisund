function Protect-TabletPath([string]$LiteralPath) {
    # Call on the private DIRECTORY before creating a secret inside it.
    $tabletItem = Get-Item -LiteralPath $LiteralPath -Force
    if ($tabletItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Refusing a reparse point.' }
    $tabletOwner = [Security.Principal.WindowsIdentity]::GetCurrent().User
    $tabletSystem = [Security.Principal.SecurityIdentifier]::new('S-1-5-18')
    # Build only the access section. Reusing Get-Acl's descriptor with
    # Windows PowerShell 5.1 can also request audit/security privileges.
    # Preserve ownership and auditing; change only discretionary access.
    if ($tabletItem.PSIsContainer) {
        $tabletAcl = [Security.AccessControl.DirectorySecurity]::new()
    } else {
        $tabletAcl = [Security.AccessControl.FileSecurity]::new()
    }
    $tabletAcl.SetAccessRuleProtection($true, $false)
    $tabletInheritance = [Security.AccessControl.InheritanceFlags]::None
    if ($tabletItem.PSIsContainer) { $tabletInheritance = [Security.AccessControl.InheritanceFlags]'ContainerInherit, ObjectInherit' }
    foreach ($tabletSid in @($tabletOwner, $tabletSystem)) {
        $tabletRule = [Security.AccessControl.FileSystemAccessRule]::new($tabletSid, 'FullControl', $tabletInheritance, 'None', 'Allow')
        $tabletAcl.AddAccessRule($tabletRule)
    }
    if ($PSVersionTable.PSVersion.Major -le 5) {
        $tabletItem.SetAccessControl($tabletAcl)
    } else {
        [IO.FileSystemAclExtensions]::SetAccessControl($tabletItem, $tabletAcl)
    }
    $tabletActual = Get-Acl -LiteralPath $LiteralPath
    if (-not $tabletActual.AreAccessRulesProtected) { throw 'Private ACL inheritance was not disabled.' }
    foreach ($tabletRule in $tabletActual.Access) {
        $tabletSid = $tabletRule.IdentityReference.Translate([Security.Principal.SecurityIdentifier]).Value
        if ($tabletRule.AccessControlType -eq 'Allow' -and $tabletSid -notin @($tabletOwner.Value, $tabletSystem.Value)) {
            throw 'Unexpected principal in private ACL.'
        }
    }
}
