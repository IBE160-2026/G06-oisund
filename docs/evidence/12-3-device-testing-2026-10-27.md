# Story 12.3 — physical Lenovo / Brave verification, 27 October 2026

> Later final decision,27 October2026: [remaining required device checks passed and conditional owner approval became effective](12-3-device-acceptance-2026-10-27.md).12.3 is done/accepted. Pending/unperformed statements below describe this earlier checkpoint; original results/failures remain unchanged. No commit/push/main merge in the final follow-up.


The covered device checks passed after bounded test-adapter corrections. **No confirmed product defect was found. Story12.3 remains review/pending owner acceptance.** Jonas confirmed the finger theme change and physical portrait rotation separately; neither answer is treated as acceptance of the whole story.12.1/12.2 remain done/accepted. No12.4 work, product correction, main merge, deployment or push was performed.

## Device, build and isolation

Lenovo TB361FU, serial HA2BN9HR, Android16; Brave com.brave.browser1.97.59 / Chromium155.0.8059.85. Its reduced web user-agent reports Android10/K; OS version comes from ADB, not that reduced string. Actual layout viewports were1280x605 landscape and800x1085 portrait, DPR2. No viewport emulation or CSS font enlargement was used for these physical tests.

Existing worktree `D:/IBE160/tmp/story-12-3`, branch `story/12-3-tablet-pc-accessibility`, start HEAD78ea4d780bc06a1d57c98059ae44d06db34d0061. Product/tool sources still equal8ca318b55b98eb34de54f29ecab038322e3ccab6; accepted main74849ff remains integrated. All41 source and6 built-file hashes match [build identity](12-3-device-20261027T200011Z/build-identity.json), manifest SHA256b57c1053a88b4d66467e7296c5f53663e9f7e309b375a5f72f88193d6ce04ea6. JavaScript fetched by the actual tablet was main-mjCyzRo6.js, SHA256e06eae81214d031fddf7ee98d2f44871f4a538ea0781e2391bf8f022cfe11021.

Only target98DC3098B039D88F7BC83957BBD8AC4C was operated. DevTools forward50894 and existing device reverse15323/18323/18324 were reused. Both actual API health responses were200, expected fictional-assessment/private-local, from the device. Credentials were read locally into memory; no password/cookie/token values were recorded. Existing synthetic2/3January2031 data was used. The private plan's selected-activity acknowledgement changed; no private shift was started, no private bus/notice content saved, and no manual plan was ended, deleted or overwritten. The separate fictional API example was saved/reopened; demo lifecycle/status/reset are memory-only simulations.

[Postflight](12-3-device-20261027T200011Z/postflight.json) rechecks build/source, target and restored OS settings. [Runtime preservation](12-3-device-20261027T200011Z/preserved-runtime.json) confirms all26 container ID/image/start/restart/label sets and all7 accepted15312 HTTP byte hashes unchanged. Three other Brave targets retain their IDs/titles/URLs; no input, refresh or navigation was sent to them. The ordinary remote app is still the separate pilot version, not qualified as12.3 by this test. Free rotation, saved rotation1 and automatic rotation1 were restored exactly. The owned temporary UI-hierarchy dump was removed. USB routes remain for continued testing. The synthetic private session is logged out; the owned tab is left at `/demo`, Night.

## Completed checks and input provenance

| Scope | Result | Input / observation |
|---|---|---|
| First small probe | Passed before broader testing | CDP touch changed actual palette and pressed state; actual pointerdown/touchstart observed. [Smoke](12-3-device-20261027T200011Z/smoke.json). |
| Private access / themes | Passed | DOM-filled local synthetic credentials; CDP touch submits/toggles. Login, preparation, day, selected activity, bus proposal, notices and editor render on actual Brave. |
| Preference lifecycle / privacy | Passed | Scripted same-tab navigation, actual logout200, Android BACK, reload. Night retained; only ibe160-theme in localStorage, empty sessionStorage/IndexedDB/CacheStorage and zero Service Workers. [Android Back](12-3-device-20261027T200011Z/private-after-native-back-verified.png). |
| Real orientation | Passed in bounded scope | ADB OS rotation, not browser viewport emulation: portrait/landscape retained plan/unsaved notice fields/theme. Original settings restored. Jonas then physically rotated to portrait and confirmed Night and visible controls. |
| Long Norwegian text and reachability | Passed | DOM fill into actual bus/notice/demo inputs. Host clipping/overflow checks, reachable actions and cancelling the private proposal. No content write to private bus/notices. |
| Android keyboard | Open/hide/reopen passed | CDP touch opened actual Android IME; bounded mInputShown metadata and direct framebuffer. ADB BACK dismissed it. Text entry used DOM fill, not manual IME typing. [Keyboard](12-3-device-20261027T200011Z/native-keyboard-portrait.png). |
| Native calendar/time/select | Passed | CDP touches actual icons/select; native UI hierarchy identifies controls; ADB OS taps choose28October, hour22 and Alle linjer. Actual form values2026-10-28 /22:07:00 /all observed. No notice saved. [Calendar](12-3-device-20261027T200011Z/native-date-picker-icon.png), [time](12-3-device-20261027T200011Z/native-time.png). |
| Actual browser pinch and scrolling | Passed | CDP synthesized touch pinch raised visualViewport.scale from1 to approximately2, while CSS root remained16px. Native scroll moved pageTop125 to473.5 at2x. Restored approximately1. **Not CSS text enlargement and not OS magnification.** [Direct2x framebuffer](12-3-device-20261027T200011Z/actual-zoom-2x-direct-framebuffer.png), [after scroll](12-3-device-20261027T200011Z/actual-zoom-2x-after-scroll.png). |
| Demo feedback / failure / conflict / recovery | Passed | Existing simulation controls selected by script; actual device rendering. Long proposal retained, readonly comparison, unavailable message, stale-version handling and original receipt recovery. These are simulated outcomes, not network/PostgreSQL failure qualification. |
| Demo lifecycle | Passed | Selection does not Start. Start cancellation/focus, explicit Start, saved manual status, closure cancellation, readonly recap with unknown remainder, reset/reload preserving Day. Actual private Start was opened/cancelled without starting its plan. |
| Native HTML reset modal | Passed | CDP keyboard traversal completed cycle on actual Brave; focus remains in modal. Escape/cancel returns to invoking control. Actual focus-pixel change measured for2 hosts,3 keyboard observations; smallest changed/required area1.491. No hardware keyboard or TalkBack claim. |
| Actual checkbox rendering | Passed | Existing PNG edge/fill/glyph assertions, one actual checkbox, both checked states; minimum edge ratio10.131:1 and a measured checked glyph. Empty census from earlier wrong scenario is excluded. |
| Actual fictional API entry | Passed | Day/Night, actual synthetic save confirmation and reload/genuine stored-example message; theme retained. Separate from memory-only demo and private data. |
| Private reader / existing draft editor | Passed for presentation | Explicitly **DOM element.click navigation**, after waiting for enabled controls. Actual Night portrait text/boundary/clipping checks. No touch claim for these last navigation actions and no private save. |
| Human finger / physical rotation | Passed as user observations | Jonas explicitly answered yes to finger theme activation and physical portrait keeping Night/visible controls. Passive observation confirms Night/portrait. [Finger](12-3-device-20261027T200011Z/manual-finger-confirmed.json), [physical observation](12-3-device-20261027T200011Z/final.json). |

The read-only viewportSize adapter for the existing focus-pixel helper returns actual innerWidth/innerHeight solely for screenshot clipping. It does not call setViewportSize, device-metric emulation or change browser layout. Native date/time/select screenshots demonstrate rendering and usable choices; they do not establish numeric contrast for every individual native glyph.

## Measurements and original failures

[Summary](12-3-device-20261027T200011Z/summary.json), [original chronological grouped checks](12-3-device-20261027T200011Z/checks.ndjson). There are57 grouped exploratory attempts:39 passed and18 adapter/flow-precondition failures, preserved verbatim with their corrections. Separate initial smoke and two user controls are recorded independently. **This is not a57/57 suite and not a new PC broad-run result.**

28 qualified rendered-state observations include1,410 text observations (minimum6.126:1),398 control boundaries (minimum4.781:1), zero critical clipping, zero unsupported product layers and zero horizontal page overflow at the natural unzoomed viewports. Measurements reuse the existing source helpers; original TS and executed stripped MJS snapshots are in the run folder. This is bounded state evidence, not an all-views/all-zoom WCAG certification.

The18 failed grouped attempts are classified as follows:

| Count | Actual cause | Correction / bounded evidence |
|---|---|---|
|1 | Expected Dagsoversikt instead of actual Dagen din | Actual heading/status checked; day measurements passed. |
|2 | Fysisk buss label matched region and textbox | Explicit textbox role used. |
|1 | Expected Valgt aktivitet region instead of actual selected-activity surface | Existing selected-activity locator used; pre-Start and Start cancellation passed. |
|2 | ADB metadata exceeded Node's default buffer | Output filtered to mInputShown; bounded output and larger buffer only for screenshots. Native keyboard show/hide/reopen passed. |
|1 | Exact floating-point equality for zoom1 versus1.000000238 | Appropriate0.001 tolerance;2x native pinch and restoration independently observed. |
|2 | Touch attempts did not establish the logout click after scrolling | Diagnostic proves correct hit, trusted click and logout200; paint settling/touch duration added. Later actual logout/Android Back/reload passed. |
|1 | Adapter wrongly expected a native confirmation from explicit Forkast | Source has direct discard, not window.confirm. No new discard requirement or product fix invented. |
|1 | Back reached demo but load-event wait timed out | Android BACK with actual URL/DOM assertions used; private login-only restoration and Night verified. |
|1 | Lost-response scenario still had an unresolved stale-revision comparison | Followed existing test prerequisite: adopt current, then new lost response. Actual pending region asserted; original lookup passed. Initial empty-checkbox output is not counted. |
|1 | Exact activity select label included child option text | Existing non-exact selector used; lifecycle passed. |
|1 | Existing PC focus helper assumed non-null Playwright viewportSize | Read-only actual-viewport adapter, then full modal focus/pixel assertions passed. |
|2+2 | Additional reader actions occurred while its control was still disabled; dependent editor steps then lacked a reader Back control | Wait for intended enabled/ready state, then DOM navigation. Reader/editor presentation passed. Not an enabled-control product defect. |

Preparatory JavaScript syntax/shell-quoting corrections happened before those commands could operate on the device/runtime and are not product passes. Some exploratory image filenames name the intended scenario; only linked asserted-state evidence qualifies it. In particular `004-demo-pending-night-demo-pending-night.json` was actually a stale conflict and is excluded from qualified measurements. The first post-browser-capture pinch framebuffer is not used as2x proof; the direct framebuffers above are captured before any Playwright screenshot with scale independently observed. No raw failing result is rewritten or relabelled.

Phase scripts are audit snapshots of the actions actually used, not an unattended reusable suite: several resume an observed state. Earlier phases used driver-before-touch-settle.cjs; later phases used the settled driver.cjs, and final extra views explicitly wait for enabled controls. Restore the original tmp/story123-device layout and reverify target/build/device before attempting reproduction. Credentials are intentionally absent from the evidence.

## Remaining owner checks and limits

- Assess personal reading/touch comfort on the forms during ordinary use. The two simple finger/rotation controls are already confirmed and need no repetition.
- If relevant to use: TalkBack/assistive technology, hardware keyboard, OS magnification or Brave's text-size setting. None was enabled or claimed tested here. Pinch zoom was tested separately.
- Private draft review/confirmation and terminal private recap were not advanced on-device; existing manual seed plans were retained. Their demo counterparts and prior PC evidence remain separate. No complete PDF-through-closure12.4 qualification or ordinary HTTPS/Cloudflare/mobile-network qualification is claimed.
- Individual native date/time/select/disclosure glyph pixel contrast remains unmeasured beyond observed screenshots/functionality; checkbox glyphs were measured.
- Jonas' explicit overall Story12.3 acceptance remains pending. No code fix is awaiting approval because no product defect was confirmed.
