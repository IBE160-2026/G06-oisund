---
title: 'Preserve PDF bytes during mobile upload'
type: bugfix
created: 2026-10-27
status: done
route: oneshot
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Mobile upload of the owner's three ordinary shift PDFs fails with an undifferentiated parsing message. The assistant must accept these everyday inputs and present their interpreted activities for review.

**Approach:** Preserve the selected PDF bytes in bounded, cancellable browser memory before sending them; retain the file-input reference until processing completes. Distinguish local file reading, transport, server rejection and invalid response errors. Verify the real files transiently and add synthetic regressions. Preserve the original files unchanged, exclude attachments from Git/builds, and keep their personal information out of source, fixtures, documentation and logs. No automatic save, publication, migration or operational data mutation.

</frozen-after-approval>

## Implementation Notes

- Small reversible frontend fix; no intent gaps or irreversible actions. Original attachments are the only pre-existing untracked content. User authorizes investigation/fix and requires private originals to remain intact. Only session log files will be committed, per project instructions.
- Existing parser, subprocess limits, typed mapping, HTTP response and frontend validators all accept the three attached inputs. The production-equivalent hardened image produces successful responses in an isolated networkless test with synthetic authorization and no database.
- Primary upstream evidence: https://bugs.webkit.org/show_bug.cgi?id=319985 documents disk-backed File bodies arriving empty on iOS, including file-provider/sandbox cases; reading into memory avoids this networking-process failure. This is a supported hypothesis for the reported device, not a captured request from that device.
- Footprint: `frontend/src/PrivateAccess.tsx`, `frontend/src/PrivateImport.tsx`, a bounded PDF byte-reading helper, synthetic tablet browser regressions, and `.gitignore`. Reuse the authenticated workspace lock, CSRF, cancellation and no-store transport. Do not alter parser facts, authentication policy or persistence.
- Check original byte hashes before/after without publishing identifying metadata. Remove temporary text/JSON/render artifacts at completion. Run production build, synthetic transport/cancellation/error regressions, original fixture parser regressions, and transient browser review of all three private inputs without saving them.
- Owner identified Pixel/Android and immediate failure after selection; the earlier iOS-specific hypothesis is not the device diagnosis. A synthetic native-picker hide/show reproduction fails before upload when the file change arrives during session restoration. Preserve memory transport as file-provider hardening, and wait for the in-flight restoration before the existing workspace identity/cancellation check. This does not relax authorization or resume a cancelled upload. Chromium also documents native provider upload failures at https://issues.chromium.org/issues/40123366; that separate engine failure has not been captured on this device.
- Implemented a 10-second bounded, cancellable access wait covering either picker/visibility event order. Original session identity, logout lock, visibility and restored access must all pass before workspace validates the session and rotates CSRF. File reading is independently bounded to 10 MiB/10 seconds and cancelled on abort/unmount. Network transport receives an ArrayBuffer, never the provider-backed File.
- Verification: 119 existing backend import tests; 31-test tablet browser suite; three focused final decoding/transport tests including a new stalled-response-body timeout case; production TypeScript/Vite and Docker builds. All three private inputs also passed transient local narrow-viewport review/adoption with exact uploaded-byte comparison and no save request. These tests used mocked authentication/network response transport and real isolated parser/HTTP results, not the operational account or database.
- All three originals were verified byte-for-byte unchanged; attachments are Git-ignored and excluded by Docker's existing build allowlist. Temporary extracts, page render, response JSON and private browser-test files/results were deleted. No private input content is in the persistent fixtures, report, logs or built image.
- Independent Blind Hunter review ran; dispatch-only edge-case and verification-gap layers were not used for this oneshot fix. All six findings below were patched; none deferred.
- Automatic approval review initially rejected replacing the shared gateway. The owner subsequently explicitly approved updating app.bussassistent.com; only the gateway was replaced successfully. Active image `ibe160-tablet-gateway:pdf-upload-20261027`, manifest `sha256:980c6b662cb29b04e7305d1fa9b0912979651aaf8d1edfb02c10340c99956352`; rollback image remains `ibe160-tablet-gateway:main-2dd1b11`. Nginx configuration, matching built JS asset, loopback-only port and unauthenticated 403/no-store were verified. Every other running container ID/image remained unchanged. Physical Pixel retest remains pending. See `docs/evidence/mobile-pdf-upload.md`.
- Owner acceptance, 2026-10-27: the owner confirmed that the files now upload as intended on mobile, approved the correction and explicitly authorized push. This supersedes the earlier pending physical-retest and log-only commit restrictions for this completed correction. Original private files remain excluded from publication. No product code changed after the tested deployment.

## Review Triage Log

| Finding | Verdict and resolution |
| --- | --- |
| Picker may return before restoration starts | Medium, patched: bounded access wait handles either ordering; both event-order browser regressions pass. |
| Restoration wait retains bytes after cancellation | Medium, patched: abort-aware wait settles immediately; test holds session response while checking input cleanup. |
| Malformed JSON is mislabeled as network failure | Medium, patched: SyntaxError tagged as unusable response; regression passes. |
| No committed successful-review regression | Medium, patched: entirely synthetic parser-generated fixture reaches review/adoption, with no automatic save. |
| Browser config can serve stale output | Medium, patched: test server builds its dedicated tablet entry before starting preview. |
| Decode catch also masks response-body timeouts | Medium, patched: only SyntaxError is reclassified; body TimeoutError is preserved and regression passes. |
