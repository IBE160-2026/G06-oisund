- source_spec: `_bmad-output/implementation-artifacts/spec-11-5-cross-day-notice-register.md`
  status: resolved 2026-10-27 under E11-A11; retained as historical evidence, not open work.
  summary: Clamp the existing private-session timeout when a device clock is more than about eleven days behind the server.
  historical_evidence: At the 11.5 checkpoint, `frontend/src/PrivateAccess.tsx:226` passed the full session lease plus device skew to setTimeout; the investigation encountered immediate expiry under fourteen-day backward skew.
  resolution: Current `frontend/src/PrivateAccess.tsx:250–255` schedules at most1000ms before rechecking the original deadline with shared server/monotonic time. `frontend/tests/private-retention.spec.ts` and `docs/evidence/12-1-retained-data.md` record qualification; E11-A11 is already done. No new lease or clock policy is introduced by this documentation correction.

Current V1 closure classification and remaining work are consolidated in [the closeout assessment](../../docs/submission/v1-closeout.md). The B6–B10 entries below remain open; their V1 deferral has not been approved by that assessment.

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
