# Story 11.2 — Selected activity and separate screens

## Scope and authority

Owner authorized implementation on 2026-10-24, including separate upload, interpretation control/editing, day and activity screens. Baseline: `5160feeba20bb2d5730d37aa96b130a6fd23e86c`. See the [approved specification](../../_bmad-output/implementation-artifacts/spec-11-2-understand-the-selected-activity.md) and current sprint status. Jonas explicitly accepted 11.2 on 2026-10-25 and subsequently authorized commit/push; the next story remains unstarted.

The selected view shows the exact acknowledged member, confirmed type, relevant identifiers, explicit planned start/end dates and Oslo times, known/unknown endpoints, current uncertainty and associated neutral source markers. It preserves manual selection and the existing explicit shift start. No stops, automatic progression, outcomes, notices or closure functionality are introduced. Future notices and closure/recap destinations are recorded in UX planning, not presented as delivered controls. The limited working demo remains unchanged.

## Verification record

Independent review and final technical verification are complete. Jonas explicitly accepted 11.2 on 2026-10-25, reporting that it works well and is much clearer. Results below are executed 11.2 evidence, separate from historical 11.1 results. Acceptance does not imply every offered manual/device check was performed.

- Root isolated verifier-control tests: 5 passed in 0.146s; expected mocked failure output exercises restoration paths, without service/data operations.
- Independent browser-control attempt: CUA inventory returned no browsers; opening IAB returned `Browser is not available: iab`. No interactive CUA pass is claimed. Automated rendered-browser coverage and screenshot inspection are tracked separately.
- Actual iPad/Safari, hardware touch and assistive technology: not run. These remain separate 12.3/12.4 obligations.
- Worker pre-review selected-activity suite: **20 passed (1.3m)** on the compact layout. Covers actual upload/edit/save/review/confirm/day/detail/back/reload, exact member/calendar facts, opposite direction/identical identities, grouped pauses, unknown non-passenger places/identifiers, confirmed classifications, current versus historical/neutral/unlocated source information, retained draft/time input, lost Start recovery, terminal draft recovery and held selection/bus, upload/editor and parent-read/editor races.
- Reviewed selected suite: **27 passed (1.7m)**, followed by **5 refined cases passed (23.1s)**. Adds independent literal midnight/autumn-offset expectations, passenger unknown identifiers, held Next/Back intent, focus preservation, row-local Open/group return, independent old-plan/new-confirmation expiry and delayed denial/failure recovery.
- Root actual PostgreSQL/API: **302 passed (353.71s)**; exact populated restart/repeated-migration/state preservation and production build passed. API/database/verifier code is unchanged by subsequent frontend corrections.
- Root first complete browser gate: **272 passed / 12 failed (20.9m)**. One expired-plan read needed immediate busy/read release; ten old assertions needed navigation to their separate visible screen; one old pause toggle closed a group already opened by Back. Original failed log: ignored `tmp/11-2-root-final.log`; contexts: `tmp/11-2-first-broad-errors`. This is a failed gate, not a passing result.
- All **13 affected cases passed (1.3m)** after these corrections, retaining the original data/security/late-response assertions and including independent pending-confirmation expiry. Final root complete browser run: **284 passed (18.1m)**, one worker, no retries, exit 0; log `tmp/11-2-root-browser-final.log`. This supersedes the failed browser gate; the API/restart result remains valid on unchanged backend code.
- All three independent BMAD reviewers re-inspected retained fixes; original edge reviewer additionally inspected the scoped expired-plan read correction. No concrete remaining defect in those scopes; no retained finding deferred. Individual findings and rejected candidates are recorded in the specification.
- Intermediate broader runs are retained in ignored `tmp/11-2-worker-*.log`; one stopped at 58 passed / 15 failed / 201 unrun, later reruns were deliberately interrupted for fixes. These are not complete passing gates. Final root results must supersede them.
- Root visually inspected new normal 1024×768 Day and 768×1100 Night viewports and earlier enlarged detail renders. The compact layout brings selected facts above the fold in landscape; endpoints fit the tested 1024×768 case. Long/enlarged content remains scrollable; no clipped facts were observed. This is viewport emulation, not actual tablet evidence.
- Six current `11-2-contrast-{width}-{day,night}.json` records measure selected detail text/boundaries at 14.387:1 Day / 12.855:1 Night; keyboard focus is 3px, at 21:1 Day / 11.450:1 Night. Each width/theme case asserts no horizontal overflow, control height ≥58px and keyboard operation. Other UI surfaces retain separate existing regression checks.

After the final gate, frontend source hashes match its starting snapshot. The local `/private` entry and served JS/CSS are byte-equal to tested production output (`index-C-vlN3zD.js`, `index-Btibde1U.css`). Private health returns 200; ordinary API/database are healthy and test API/database are stopped. All monitored original business/source/policy/selection/lifecycle/receipt/session/security/secret digests and database identity are preserved. The only initial-baseline change is three expired login-throttle rows removed by unchanged startup cleanup; subsequent snapshots match the restored post-worker baseline exactly. No ordinary account/record was an automated test target, no volume/secret reset, and no historical image changed. Root inspected final normal 1024×768 Night and enlarged 768 Day renders, alongside earlier Day/Night viewport checks. No product code changed after the final run.

## Matrix coverage

| Specification scenario | Executable coverage |
|---|---|
| 20/24, opposite directions, identical identity | `private-selection.spec.ts`; selected exact-member and identical-ordinal cases |
| Midnight / source extended hours | selected exact-member dates; existing day/source-clock cases |
| Individual grouped pause | selected exact-member navigation; existing selection/day projections |
| Null/blank facts, no inherited places | selected missing deadhead/CAR/Travel to/Sign-on cases; existing passenger/day unknown cases |
| Corrected classification and source distinctions | selected classification and located/unlocated marker cases; uploaded corrected-place flow |
| First/last/single boundaries | selected exact-member and single missing-fact cases; existing single-member selection case |
| Failed/stale/denied/expired/account change | existing selection/start/identity cases plus new expired-draft and held-reply flows |
| Full separate-screen journey | selected uploaded-document case and normal/enlarged viewport cases |
| Unsaved/unresolved navigation | selected memory/Start case and three held-response race cases |

Review additions directly cover passenger missing line/trip/direction, explicit Back during held Next, focus-preserving failures, read-only selected-row opening/grouped return and independent expiry of an old retained plan versus a different new confirmation.

## Owner walkthrough

Use `http://127.0.0.1:5173/private` with your existing account:

1. In **Forberedelse og planlister**, choose **Velg tekst-PDF**. Inspect the separate interpretation screen, then **Bruk som separat nytt utkast**.
2. Correct fields in the editor. **Lagre utkast** → **Gjennomgå lagret utkast** → resolve the actual classifications/acknowledgements → **Bekreft gjennomgått plan**. The day opens separately.
3. In the day, use **Velg aktivitet N**. After acknowledgement, only that member opens with **Tilbake til dagen**, previous/next, planned dates/times, relevant identifiers, places and unknown/uncertainty labels.
4. Return to the day: focus returns to the selected member, including its pause group. Open it using **Åpne aktivitet N** at that row or **Åpne valgt aktivitet** above the list. Reload, reopen the saved plan and open the saved choice again. These read-only Open actions do not write; navigation alone must leave the shift unstarted.
5. Separately register bus and use the existing explicit **Start skift** from the day. Repeat navigation; verify these registrations remain. Preparation/editor can be revisited without losing unsaved input, while unresolved writes keep their recovery reachable.
6. Check a missing endpoint, an overnight member and a grouped pause member. Switch **Nattmodus**, enlarge text and use Tab/Enter. Detail permits scrolling for long/enlarged information.

Future notices receive a secondary day-linked screen in 11.4/11.5; outcomes/end/abort/recap belong in day/shift navigation in 11.3. They have no working placeholder actions here. Intermediate stops remain post-V1; demo expansion remains later planned work. Record device results and owner acceptance explicitly.
