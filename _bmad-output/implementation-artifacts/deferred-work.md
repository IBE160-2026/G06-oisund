- source_spec: `_bmad-output/implementation-artifacts/spec-11-5-cross-day-notice-register.md`
  summary: Clamp the existing private-session timeout when a device clock is more than about eleven days behind the server.
  evidence: `frontend/src/PrivateAccess.tsx:226` passes the full remaining fourteen-day session lease plus device skew to setTimeout without a 2,147,483,647 ms clamp; the corrective browser investigation encountered immediate expiry under fourteen-day backward skew. This access controller is unchanged from the preserved initial tree. Notice expiry itself now uses server timestamps plus monotonic elapsed time and is tested with two-hour initial skew and a one-day backward clock jump; broader access-clock behavior remains separate.

- source_spec: `_bmad-output/implementation-artifacts/spec-12-3-current-main-sync.md`
  summary: Align tablet preparation team-name validation with the gate (B6).
  evidence: Accepted main preparation accepts uppercase/trailing-hyphen/overlong teams while Admission rejects them; fail-closed setup mismatch, unchanged by12.3.

- source_spec: `_bmad-output/implementation-artifacts/spec-12-3-current-main-sync.md`
  summary: Align tablet preparation owner-email ASCII validation with the gate (B7).
  evidence: Accepted main preparation accepts non-ASCII email while Admission requires ASCII; unchanged operator-input mismatch.

- source_spec: `_bmad-output/implementation-artifacts/spec-12-3-current-main-sync.md`
  summary: Evaluate bounded concurrency for admission during slow JWKS lookup (B8).
  evidence: Accepted main uses single-threaded HTTPServer with3s network timeout; slow lookup serializes other admissions. No bypass claim.

- source_spec: `_bmad-output/implementation-artifacts/spec-12-3-current-main-sync.md`
  summary: Bound unknown-kid JWKS refresh attempts before ordinary deployment (B9).
  evidence: Accepted main PyJWKClient refreshes unknown keys; repeated lookup path visible in source, external exploitability behind Cloudflare not demonstrated.

- source_spec: `_bmad-output/implementation-artifacts/spec-12-3-current-main-sync.md`
  summary: Minimize outer Access cookies forwarded to private API (B10).
  evidence: Accepted nginx configuration forwards original Cookie while removing assertion header; filter outer Access credentials while preserving app session/CSRF cookies and test proxy behavior. No actual disclosure observed.
