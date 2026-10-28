# Story12.4 — physical test of the revised import experience

**Current acceptance: approved by Jonas on28October2026.** He confirmed the tablet experience is satisfactory and the workflow much better, then explicitly approved Story12.4. [Acceptance record](12-4-owner-acceptance-2026-10-28.md). Pending/withheld statements below describe earlier checkpoints; executed test counts and limits are unchanged. No further mandatory personal retest remains.

On28October2026 the new owner-directed UI was tested on the actual USB-connected Lenovo TB361FU / Android16 / Brave1.97.59 / Chromium155.0.8059.85. The relevant technical scenarios subsequently passed after the harness corrections below. No new product defect was established and no product source changed. **Story12.4 remains explicitly not approved; personal assessment/acceptance is still pending.**

## Identity and method

Product commit `5ee35efb3753bed10bafc21a53a88fec3d93b287`; testing HEAD `e655c02eefbb60032974f35a189f49009ae014f5`. The device actually loaded `/assets/main-BRJ12oLt.js`; device-side fetch SHA256 matched `86df9a48bc01673b421f5f925ac6335793468a966e54df19ff93cdb88ea784b3`. Exact [preflight](12-4-experience-device-20261028/preflight.json), [summary/source hashes](12-4-experience-device-20261028/summary.json) and [raw attempts](12-4-experience-device-20261028/checks.ndjson) are retained. This qualifies the revised UI, unlike the earlier physical report for5ca3f7d/main-CxykOOFA.js.

Actual landscape1280×605 and portrait800×1085 CSS pixels, DPR2. Android system rotation was temporarily locked to portrait through ADB, then original accelerometer_rotation=1/user_rotation=1 were restored and landscape checked again. This is actual device rotation, not CDP metrics emulation. Native file-picker controls used observed Android UI hierarchy and ADB input; app actions used CDP touch plus DOM fill/keyboard/select. These are automated actions on a real device, not human finger comfort assessment. No lifecycle/visibility events were injected and no API endpoints mocked.

Only compose project `ibe160-story124-tests`, frontend15324 and actual APIs18325/18326/PostgreSQL were used. A new dedicated synthetic automation account was additively provisioned. Old accounts/records were not reset or edited; the browser profile now uses the new synthetic session. The separate fresh owner-retest account remains unused. Prior Brave target IDs/URL hashes were preserved; no unrelated tab contents/file names were logged or operated. No private original PDF, active site, operational database or tunnel was used.

Pre-device runtime audit [152258267860Z](12-4-runtime-20261028T152258267860Z.json) and post-device audit [153936825486Z](12-4-runtime-20261028T153936825486Z.json) both passed38/38, including exact served source/API settings, backend identity and preservation of all23 pre-existing container IDs/images/ports. No earlier backend/desktop gate is presented as newly rerun here.

## Expected and observed results

| Physical scenario | Independent expected result | Observed |
|---|---|---|
| Native picker cancellation | Return to unchanged empty workspace, no adoption/write | Passed; no review and0 drafts. |
| Native A return | Exact synthetic PDF bytes, restored access, compact independent identity, no automatic save | Passed: HTTP200,45330 bytes, SHA256700b459a3552012ae2ccd493078c6b597b837379804ebdf386143cb38e4f14c1. Summary97000001/4February2030/06:50–08:50; optional full source,0 drafts. Native hidden/visible transitions observed. |
| Correct-as-is A | Explicit save directly reaches separate approval, no mandatory editor; saved facts match independent Fasit-testskift oracle | Passed: exactly1 draft/revision1; all activity dates/times/trips/endpoints/duty checked independently; unknown decisions unchecked and confirmation disabled until explicit choices. |
| Confirmation | Only explicit required decisions/confirmation create a plan; no automatic Start | Passed:1 plan and lifecycle confirmed, Start remains an explicit action. |
| Confirmed bus | Adjacent dedicated action saves independent bus only, durable after reload | Passed for A and C: physical bus revision1 retained; source draft unchanged. A button gap from field measured8px. |
| C overnight identity and edit choice | Separate97000003/service8February, source8→9February/22:10–03:50; editing chosen explicitly | Passed against all independent C oracle activity facts; importing/editing left only A saved until explicit C save. C used file-input payload on the actual device, not a native C-picker claim. |
| C correction/save position | Corrected destination saved beside intact source; viewport/focus retained with nearby approval | Passed revision1: scroll36898→36939.5, delta41.5px against unchanged<100 bound; save focus retained and Continue to approval in viewport. |
| Draft bus scope | Bus-only action changes only bus; unrelated proposals must not silently persist | Passed: clean bus-only revision2 preserved all activities; dirty bus+destination refused separate save, both proposals retained and stored revision2 unchanged; explicit whole-draft save produced revision3. |
| C reload/current approval | Exact saved revision3/correction/bus/source survives reload; current compact approval retains explicit unknown decisions | Passed; optional full facts remained collapsed, required acknowledgements remained unchecked. |
| Independent documents | C confirmation uses C revision3; A and both source drafts remain independent | Passed:2 plans; A source/bus unchanged, C independent current physical bus survives reload beside unchanged C source draft. Both remain unstarted. |
| Consultation and notice access | Planned-start fact remains above existing450px bound; notice reader and return reachable | Passed in actual portrait and landscape: top406.5625px; reader/return works; no Start from selection/navigation. |
| Cleanup/isolation | Restore rotation, preserve old tabs and avoid persistent private browser storage | Passed; only theme localStorage, empty sessionStorage and0 IndexedDB/caches/Service Workers. Own temporary UI dump removed; earlier synthetic Download PDF retained. |

## Attempts, corrections and counting limits

There are **17 grouped exploratory records:13 passed and4 failed attempts**, not17/17 or a unique-case count. All relevant scenarios above subsequently passed; original failures remain in checks.ndjson:

1. Initial CDP login touch did not submit; no successful login was inferred. Keyboard Enter from the same dedicated account form produced actual200 and empty lists. No product change.
2. Two native A attempts timed out waiting for an upload response while the picker remained open. A separate background DevTools reconnect timed out30seconds outside the17 grouped records; ADB still showed an awake connected device/Brave. Cancel returned to the app with Importen er avbrutt. The successful attempt required a fresh compressed UI dump and tapped the nearest observed clickable row rather than text-node coordinates. Both helper changes were made together, so no claim isolates stale XML as the sole cause. It then selected the same known synthetic file and proved exact request bytes/HTTP200. No upload defect was established from the uncompleted picker attempts.
3. The first consultation test reached the reader but asserted a nonexistent region name. Reading the actual component established Avvik for linjer og datoer. The corrected full consultation/reader/return check passed at unchanged geometry thresholds. No product change.

Executed helper snapshots include the initial driver and corrected driver. Other sources are their final executed versions; intermediate native-selection metadata files retain the final successful observation, not a reconstructed history of every attempt. Failed assertions/timestamps remain unchanged in the raw journal. Credentials, cookies and full UI dumps are excluded.

## Visual evidence and remaining acceptance

Natural viewport screenshots were visually inspected: [native A summary](12-4-experience-device-20261028/native-A-summary-viewport.png), [A approval](12-4-experience-device-20261028/A-approval-viewport.png), [confirmed bus](12-4-experience-device-20261028/A-confirmed-bus-viewport.png), [C retained save position](12-4-experience-device-20261028/C-saved-position-portrait.png), [C bus scope](12-4-experience-device-20261028/C-bus-scope-portrait.png), [portrait consultation](12-4-experience-device-20261028/C-selected-portrait-viewport.png), [landscape consultation](12-4-experience-device-20261028/C-selected-landscape-viewport.png). No tiled full-page composite is used. This does not certify every theme/zoom/accessibility combination or personal comfort.

The tablet is left on its own new synthetic account at `http://127.0.0.1:15324/private`, preparation/lists, with two unstarted plans. Credentials remain only in ignored `.private-runtime/story124-experience-device.json`. For a clean personal retest, the unused `.private-runtime/story124-experience-manual.json` account remains available. Existing USB reverse/DevTools forward are retained; no public route/tunnel was started.

The technical parts of the four-point follow-up checklist are now also exercised on actual hardware. Jonas still needs to assess the overall experience/scrolling/readability and explicitly decide acceptance. Earlier six personal checks remain historical. Do not infer acceptance or start12.5. [Exact-byte bundle](12-4-experience-device-20261028.tar.gz) and [per-entry index](12-4-experience-device-20261028.index.json) preserve source/artifact bytes across Git newline normalization.
