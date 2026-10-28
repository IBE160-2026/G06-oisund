# Story 12.4 — physical Lenovo follow-up, 28 October 2026

**Outcome:** available complete flows and targeted boundaries passed on the actual USB-connected tablet after documented harness corrections. No new product defect or product change was required. Story12.4 remains **review / owner acceptance pending**. Automated device actions do not constitute a human finger assessment or acceptance.

## Identity, methods and isolation

Implementation `5ca3f7df73f4cf49f5244dbc97a0a3ebb8de9891`; HEAD during testing `80aea192e7918762f41fd4784e2cfafac1a7b75f` (later documentation/logs only). Actual Lenovo TB361FU / Android16 / Brave1.97.59 / Chromium155.0.8059.85, portrait800×1085 CSS pixels, DPR2. Reduced web UA Android10 is not the actual OS. No device-metric or visibility lifecycle emulation.

The unchanged `main-CxykOOFA.js` is served by original owned preview44564 on15324, with actual APIs18325/18326 and PostgreSQL in `ibe160-story124-tests`. A [fresh build](12-4-build-20261028T111917198656Z-3377c5a3.json) passed; `serve` refused the occupied port. Its existing listener was identified and reused after identity audit. [Isolated startup](12-4-up-20261028T111824850662Z-c198a1de.json), [pre-device audit](12-4-runtime-20261028T111950271385Z.json) and [post-device audit](12-4-runtime-20261028T114551360673Z.json) preserve exact inputs. Both audits passed38/38; served files/API source match recorded bytes and all23 pre-existing container IDs/images/ports are preserved.

Only new dedicated synthetic accounts/records were used. Existing manual12.4 account, operational data, active website and tunnel were not used or changed. No cloudflared process was present at final check; no tunnel was started. USB reverse15324/18325/18326 and own DevTools forward50924 remain for inspection. Four prior Brave targets retain IDs/URL hashes; their contents were not operated or captured. Owned extra demo tabs were closed. No private original PDFs or identifying metadata were read or committed.

Native Android picker/tab controls used observed UI nodes and ADB input. Login, confirmation and several app buttons used CDP touch; remaining app navigation, fields and selects used DOM/keyboard/selectOption in the actual device browser. These are automated actions, not human fingers. Unique temporary titles identified only owned tabs in native tab UI, then were restored. No unrelated file listing/tab title was logged.

## Executed outcomes

| Check | Independent expected result | Actual result |
|---|---|---|
| Native picker cancellation | No import adoption/save | Original workspace restored, zero drafts, no adopted review. |
| Native PDF return | Exact synthetic A bytes, restored access, no auto-save | Actual Downloads selection; HTTP200;45330 bytes, SHA256700b459a3552012ae2ccd493078c6b597b837379804ebdf386143cb38e4f14c1; genuine native hidden/visible events; review shown; draft list empty. |
| Independent A/C facts and saved correction | Fasit-testskift oracle, exact dates/trips/lines/duty, February UTC+01:00, separate identities, preserved source/manual/unknown distinctions | Passed; C rolls to9February2030 while service date stays8February. Manual destination/source note and SYN-124 survive explicit save/reopen/confirmation beside unchanged source metadata. C used file-input payload automation on the real tablet, not a native C-picker claim. |
| Native notice tab switch | Proposal retained, zero automatic notice writes, resumed editing works | Native UI selected only own demo and returned; foreground demo URL verified. Title/multiline body unchanged,0 POSTs, stored notice list unchanged; added third line and explicitly saved once. |
| Native HOME/return | Original session and unsaved proposal retained | Session object unchanged; fields and stored list unchanged before explicit Save. Four successful session responses include explicit checks; do not label all four as lifecycle-triggered. |
| Second concurrent bus change | Fresh C replaces cached comparison B only after authorized read | Actual separate API commands saved B then C in same dedicated session. Local proposal retained; Load saved made exactly1 GET/0 POSTs and adopted SYN-current-device124 at revision+2. No API mocks. |
| A terminal flow | Manual selection does not Start/complete; explicit Start/completed/end;1 completed/4 unregistered | Passed, including actual own database/API restart, identical recap/selection, browser reload/reopen and read-only result. |
| C terminal flow | Explicit Start/interrupted/abort;1 interrupted/14 unregistered | Passed; exact recap and manually changed bus survive reload/reopen; no Start/resume. |
| Logout/history/reload | After confirmed logout, private UI hidden and API401 | Passed after authoritative Du er logget ut.; no private resurrection. |
| Account switch | Second account empty; foreign record denied; original records preserved | Passed: empty draft/plan lists, foreign plan404, original two records/recaps identical after re-login. |
| Private browser storage | No persistent private data | Only theme localStorage allowed; sessionStorage empty; IndexedDB/caches/Service Workers zero. |

The A continuation reuses the actual previously captured native response, compared with independent oracle facts; it substitutes no network response. Device API reads use credentialed fetch from the device page. After a helper race, the saved checkpoint was verified and resumed without resetting or replaying earlier writes.

## Raw attempts and corrections

[Checks](12-4-device-20261028/checks.ndjson), [summary/source hashes](12-4-device-20261028/summary.json), [journey adaptation](12-4-device-20261028/journey-adaptation.json) and final source snapshots under `12-4-device-20261028/executed-sources/` preserve actual methods. There are **23 nested/grouped exploratory records:15 passed and8 failed attempts**, not23/23 or a clean unique-case suite. Original failures remain:

- Recents-only native search missed the newly pushed file; no upload. Cancellation was checked; actual Downloads selection then passed.
- A typestripped signature was missed by the adapter, leaving invalid relative `/private` navigation without baseURL. Both nested failure rows remain. Correcting the adapter preserved the native review.
- Simplified Open selected helper raced completed auto-opening. Saved selection was verified in actual UI/API; continuation completed without re-importing.
- Two strict native-tab attempts required hidden/visible events that were absent even with focus emulation disabled. Real switch/return and retained input completed. Qualified checks record actual behavior and empty arrays; no visibility events were injected.
- C helper used the wrong internal unstarted enum `not_started`. Established lifecycle contract is `confirmed`, visible as Ikke startet. No Start occurred before correction; the continuation explicitly started/aborted once.
- Initial API401 assertion ran while logout was pending and UI already locked;200 preceded revocation. Corrected check waited for authoritative logout before history/reload/API denial. No authorization bypass is established.

[Additional connection/port observations](12-4-device-20261028/connection-observations.json) document a background DevTools timeout, exact-target refusal after ordering changed and safe occupied-port refusal, outside the23 grouped rows. No product source changed for these corrections.

## Visual evidence and limits

Qualified natural viewport captures: [A recap](12-4-device-20261028/physical-recap-A-viewport.png), [C recap](12-4-device-20261028/physical-recap-C-viewport.png), [C interrupted member](12-4-device-20261028/physical-recap-C-selected-viewport.png), [native import](12-4-device-20261028/native-import-review.png), [resumed notice](12-4-device-20261028/native-notice-resumed.png). They were visually inspected. Android fullPage composites repeated viewport tiles; originals remain explicitly **unqualified** in [capture limitations](12-4-device-20261028/capture-limitations.json). No all-view/all-zoom/accessibility certification follows.

Native picker return produced genuine hidden/visible. Native tab/HOME switching in this instrumented session did not. Unsaved-state preservation, actual return and session checks passed; visibility-triggered dirty-notice restoration cannot be inferred from empty event arrays. Uninstrumented human finger/tab/background observation remains an optional concrete follow-up, not a demonstrated product bug. All mobile event-order/account/expiry combinations were not physically repeated; the separate32-case boundary suite retains that scope.

Jonas has not given12.4 acceptance. Earlier12.3 comfort/rotation and historical mobile approval remain historical. No merge, deployment or12.5 work occurred.

## Current manual inspection

Tablet: own Brave tab at **http://127.0.0.1:15324/private**, logged into the dedicated synthetic account on preparation/lists. A/C terminal plans and two notices remain inspectable. Original manual account is unchanged. Dedicated credentials, if needed, remain only in ignored `.private-runtime/story124-device.json`; never publish it.

Synthetic `Download/ibe160-story124-synthetic-A.pdf` remains for manual native selection. The owned temporary UI-hierarchy dump was removed. USB routing requires connection and creates no public route/tunnel. Use the [manual checklist](../story-12-4-manual-testing.md), optionally try notice tab switching with your own finger, and record owner acceptance separately.

[Exact-byte device bundle](12-4-device-20261028.tar.gz) and [member/hash index](12-4-device-20261028.index.json) preserve raw final-source and artifact bytes across Git newline normalization. Credential-literal scanning passed; ignored account state, cookies, UI hierarchy dumps and private originals are excluded. Source snapshots are the final executed versions, not reconstructed originals of every exploratory revision.
