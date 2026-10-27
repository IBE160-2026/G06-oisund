# Mobile PDF upload correction

## Diagnosis and scope

The reported immediate failure occurred on Android after returning from the native file picker. All three privately supplied inputs passed the existing parser, isolated subprocess, typed mapping, HTTP response and frontend validators. Their contents and identifying metadata are deliberately absent from this report and the test fixtures.

A synthetic browser reproduction demonstrated that the picker can deliver its selection while visibility restoration is still checking the session. The previous upload entered the authenticated workspace too early and rejected the still-suspended access state; its generic catch incorrectly described this as a PDF parsing failure. The regression failed before the correction and passed afterward. A physical reproduction on the owner's device remains necessary to establish that this was its exact failure path.

The upload now waits, within a fixed deadline and with cancellation, for restored access to the original session. It also reads the selected file into bounded browser memory before sending bytes, and retains the picker reference until processing settles. Cancellation, logout, changed account, expired session and failed access checks still prevent upload. Error messages distinguish file reading, access, transport, parser rejection and invalid responses.

## Verification

- 119 existing backend import/qualification/boundary tests passed in a networkless disposable container.
- 31 tablet browser tests passed, including both selection/visibility event orders, restored/expired/changed/unavailable sessions, cancellation, logout, byte integrity and synthetic review/adoption without saving.
- Final focused malformed-JSON, network-failure and response-body-timeout tests: 3 passed. The last test was added after the full suite; the other two were repeated after the decoding correction.
- Three transient private-input browser checks passed at a 390-pixel viewport: exact uploaded bytes, rendered review rows, explicit adoption, no save requests and no browser persistence. Responses came from the real isolated HTTP parser result; authentication and browser endpoint transport were local test doubles.
- Production TypeScript/Vite builds and final local Docker build passed. Isolated gateway tests passed 120 missing/invalid identity variants, valid request forwarding, no-store/CSP, and admission-service-unavailable rejection. No gateway configuration changed afterward.
- Original files were hash-compared locally and remained byte-for-byte unchanged. Temporary extracts, render, response JSON, hash manifest and private browser-test artifacts were deleted. Original attachments remain local, Git-ignored, untracked and excluded from build contexts. Persistent regression data is generated solely from the existing synthetic PDF helper.

## Runtime handoff

Source baseline: `2dd1b1122dfa8093df156277dae4bb90da059588`, plus this correction. The owner approved the correction and authorized commit/push after the successful physical mobile test on 2026-10-27.

Prepared image: `ibe160-tablet-gateway:pdf-upload-20261027`, manifest `sha256:980c6b662cb29b04e7305d1fa9b0912979651aaf8d1edfb02c10340c99956352`. Local ignored override: `.private-runtime/mobile-pdf-upload.yaml`. Existing rollback image: `ibe160-tablet-gateway:main-2dd1b11`.

Automatic approval review initially rejected replacing the shared gateway because the user's bug-fix instruction was not considered explicit deployment authorization. The owner then explicitly approved updating app.bussassistent.com. Only the gateway was replaced, using the existing deployment files plus the ignored local override, with `--no-deps --no-build --pull never`.

Post-deployment checks passed: Nginx configuration valid; running image matches the approved build; HTML references final asset `index-BTlu6rnO.js`; only loopback port 18081 is published; unauthenticated access remains 403 with no-store. Every other running container retained its ID and image. The API, database, access gate and source PDFs were not modified.

## Owner acceptance — 2026-10-27

The owner confirmed that the supplied files now upload as intended on the mobile device, explicitly accepted the correction and authorized pushing it. This closes the physical Pixel retest. The successful retest establishes the intended behavior after the correction; it does not retrospectively capture the exact failed network request. Private originals remain excluded from Git and publication.
