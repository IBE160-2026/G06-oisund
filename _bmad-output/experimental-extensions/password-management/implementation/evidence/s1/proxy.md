# S1 isolated proxy verification

2026-10-31. Parent executed against the current S1 working tree before review. Fresh gateway build uses unmodified deploy/tablet/Dockerfile, nginx-main.conf and nginx.conf.template. Image `ibe160-password-gateway:s1` manifest `sha256:0963468d7dfd8a8115e5d4c1b50b02515f92aa6736ce0927ae7172b8b0d28dc2`.

Commands (repository root):

```powershell
docker build -f deploy/tablet/Dockerfile -t ibe160-password-gateway:s1 .
./scripts/verify-tablet-proxy.ps1 -PythonImage ibe160-v1followup-gate-tests:20261029-r1 -GatewayImage ibe160-password-gateway:s1
```

All passed: password-change POST with synthetic credential body is denied without admission, forwarded with valid synthetic admission, and no-store; synthetic password marker absent from gateway and probe-upstream logs. Existing five protected route classes ×24 missing/invalid token variants, cookie filtering, Origin/CSRF/header forwarding, Host/path restrictions, CSP/no-store and unavailable-admission fail-closed checks pass.

The script creates a unique internal Docker network and ephemeral non-root read-only containers, no published host ports, no database or volumes. It removes only those created containers/network in finally. No tablet, external issuer, real credential or production operation occurs. Gateway forwards to a synthetic HTTP probe, not the real password service: real API/PostgreSQL behavior is separately covered by S1 tests; combined deployment-style journey remains S4. No log contents or actual secret values are included in this evidence.

## Review loop 1

Rebuilt revised frontend through the same production-style Dockerfile as `ibe160-password-gateway:s1-r1`, manifest list `sha256:d1363947a0b09b5e634e35553d2d5ef7b62cadded4cba9e07c817faf1d9c23a9`. Reran the same script with that GatewayImage: all proxy/password-body/log-absence/admission-unavailable checks **PASS**. Same no-DB/no-host-port isolation and automatic scoped container/network removal. This supersedes the initial UI build for revised gateway-build evidence; neither test is a production deployment or owner/device acceptance.
