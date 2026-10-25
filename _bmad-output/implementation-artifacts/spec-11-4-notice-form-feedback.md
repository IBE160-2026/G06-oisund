---
title: '11.4 — Explain notice requirements and blocked saving'
type: fix
route: oneshot
created: 2026-10-25
baseline_commit: cdcf2816b86772e559f33ded5807e8cb5a4473bc
story: '11.4'
status: done
---

## Intent

The owner could not save an “Omkjøring” notice with `svipper.no` as its source and optional fictional times. Explain which source-backed traffic notices belong here, distinguish title from line identifiers, and show required fields and reasons saving is blocked beside the save control. Preserve proposals, navigation, source checks and manual closure. Keep existing API validation and optional unknown times; no categories, automatic URL inference, filtering, commit or push.

## Implementation Notes

The authorized, uncommitted 11.4 delivery is the baseline. The source URL requires an explicit HTTP(S) scheme; validation previously appeared only at the top, far from saving, while unresolved optional clocks disabled saving. Limit changes to notice editor guidance, validation feedback, focused browser tests and documentation. Use isolated synthetic runtime data and restore ordinary services after verification. Story remains in review pending owner acceptance.

Implemented source-backed traffic notice examples, title/line guidance, required-versus-optional help, a live requirements region beside saving and editor status next to the save control. Existing date relation, conflicts, pending-operation recovery and read-only reasons remain distinct. Input values are neither inferred nor discarded. No backend, schema or source-check/closure changes.

## Review Triage Log

- Medium — patch: rejected field validation persisted after correcting the URL. Recompute validation feedback from current fields after a rejected attempt; test both correction and navigation.
- Low — patch: unresolved-clock summary omitted resolver outage and nonexistent-clock recovery. Explain the existing retry, alternative-clock, occurrence and clear actions, referring to the precise message beside the affected timestamp. No resolver-state/API change required.
- Low — patch: URL guidance omitted whitespace, backslash, control characters and length rejection. Include the existing 2048-character bound and prohibited characters; test an invalid already-prefixed URL.

Only the Blind Hunter layer runs in this oneshot route. All three findings were verified against surrounding code and patched; none deferred. Sprint remains review because owner acceptance of 11.4 is pending. User instruction overrides automatic commit/push steps.

Verification: production build passed; 46 notice browser tests passed before final review corrections (3.8m), followed by six focused final-version tests (34.9s). The final feedback render was visually inspected. Original evidence restored byte-for-byte. Ordinary services healthy; all 23 table fingerprints, original database and secret preserved, except three expired login-throttle rows removed by existing startup cleanup. Served HTML/assets equal final dist (`index-BeADbJ3f.js`, `index-BElU2L01.css`). No backend/schema changes or Git recording. See [evidence](../../docs/evidence/11-4-manual-notices.md).
