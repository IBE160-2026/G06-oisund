# Story 12.4 — manual acceptance

**Current acceptance: approved by Jonas on28October2026.** He confirmed the tablet experience is satisfactory and the workflow much better, then explicitly approved Story12.4. [Acceptance record](evidence/12-4-owner-acceptance-2026-10-28.md). Pending/withheld statements below describe earlier checkpoints; executed test counts and limits are unchanged. No further mandatory personal retest remains.

Owner acceptance was **explicitly withheld** on28October2026 after all six guided manual checks passed. The owner requires a better overall shift-entry experience: fewer repeated detail reviews, optional editing for correct imports, dedicated bus-save actions and no jump to the page top after draft saves. [Follow-up specification](../_bmad-output/implementation-artifacts/spec-12-4-import-experience.md). The checks below qualify the earlier flow; new UI requires a focused retest and a new explicit owner decision.

This checklist concerns the isolated synthetic12.4 build, never the active website or owner's account. Automated desktop results and historical physical tests do not constitute acceptance.

## Open the isolated build

Worktree: `D:/IBE160/tmp/story-12-4`, branch `story/12-4-complete-user-flow`. The initial qualified implementation `5ca3f7df73f4cf49f5244dbc97a0a3ebb8de9891` / `main-CxykOOFA.js` is historical. The owner-directed UI correction builds `main-BRJ12oLt.js`; its exact executed source/build records and subsequent served-runtime qualification are in the [new evidence report](evidence/12-4-import-experience.md). Reload the page to replace the earlier in-memory application before retesting.

```powershell
$py = 'C:/Users/Jonas/AppData/Local/Programs/Python/Python312/python.exe'
& $py scripts/verify-story124.py up
& $py scripts/verify-story124.py prepare
& $py scripts/verify-story124.py serve
```

Use a separate private browser window to keep these loopback session cookies separate from other local app ports. Open <http://127.0.0.1:15324/private>. For the new four-point retest, read the fresh synthetic credentials locally from `.private-runtime/story124-experience-manual.json` (the earlier `.private-runtime/story124-manual-credentials.json` is historical and retained); do not paste credentials into evidence. The separate demo is <http://127.0.0.1:15324/demo>. Actual APIs use loopback18325/18326; own Compose project is `ibe160-story124-tests`. This is separate from `app.bussassistent.com` and its existing operational database/tunnel. No public12.4 route is configured.

`serve` builds before starting a verified loopback listener and refuses an occupied port. Before automated browser tests, run `stop-preview` to release only its own preview. `prepare` is additive and does not reset existing manual work. Browser regression fixtures must never use the manual account.

## Focused retest for the owner-directed correction

The technical parts below have now also passed automated checks on the actual Lenovo/Brave; see the [new physical report](evidence/12-4-import-experience-device-2026-10-28.md), including its failed-attempt limits. Personal comfort/overall experience and explicit owner acceptance remain pending. Repeating every technical check by hand is not a prerequisite; use the steps to assess the experience and report discrepancies. The tablet currently shows a separate new physical automation account with two unstarted plans; the fresh manual account below remains unused.


The earlier guided six-test series passed but did not earn acceptance. Use a fresh dedicated synthetic account for this retest so repeated fixture imports do not create confusing duplicate date/version labels among earlier records. Preserve both previous device accounts and their records. Credentials belong only in ignored local runtime state; they must not be copied into this document or screenshots.

1. **Correct import:** import synthetic `Testskift-A.pdf`. Check compact shift97000001,4February2030,06:50–08:50, source places and unknown bus. Open full source details only if desired. Choose **Alt stemmer – lagre og fortsett**. The waiting state and final approval must remain compact without entering the editor. Make only the displayed necessary unknown/type decisions, then confirm. The day opens without automatically starting the shift.
2. **Explicit correction:** import a separate synthetic `Testskift-C.pdf`, shift97000003. Check service date8February,22:10–03:50 and explicit8→9February source calendar dates. Choose **Rett eller legg til opplysninger** and change a destination to a clearly synthetic manual value. Scroll to **Lagre utkast** once and save. Verify focus/scroll stays at that save action and saved feedback is visible there. Use the adjacent **Fortsett til godkjenning** without scrolling through all fields again; return to editing without confirming yet.
3. **Both bus-save locations:** in the already saved C draft, change only **Buss/vogn** and use **Lagre buss/vogn**. When unrelated changes also exist, the explanatory text must require **Lagre hele utkastet med buss**, with no hidden persistence/loss of other proposals. Continue and confirm the saved C version. On its day, change **Fysisk buss** with the adjacent **Lagre fysisk buss** action. Reload/reopen the C plan: the independent current bus must survive. The earlier A plan remains separate.
4. **Overall assessment:** judge the number of steps, repeated information, scrolling, readability and save feedback on the actual tablet. State discrepancies or an explicit Story12.4 acceptance decision. None of these steps grants acceptance automatically; do not repeat all six older checks solely because they are listed below.

## Original broader acceptance checklist (historical reference)

- [ ] Sign in with the synthetic account. Import `Eksempelfiler/Testskift-A.pdf`; compare the review with independently authored `Eksempelfiler/Fasit-testskift.json` caseA. Check source shift identity, line/trip/duty distinctions and unknown bus/direction. Importing must not save anything.
- [ ] Adopt the review, change one destination/time, enter a manual physical bus and explicitly save. Reload/reopen: corrected facts remain alongside original source facts and uncertainty. Confirm only after explicitly resolving or acknowledging the displayed requirements.
- [ ] Import caseC separately. Verify service date8February2030 and calendar rollover to9February against the oracle. It must create separate work and preserve the first plan. A bad/blank PDF or cancelled import must leave confirmed work intact.
- [ ] Open a saved plan, select a trip and use previous/next. Selection must remain manual; it must neither Start nor register completion. Enter one multi-line account notice with an ending date and unknown source-update/start. Confirm the reader labels partial validity and matches the explicitly entered lines/dates.
- [ ] Start creating/editing a notice, type multiline text, switch to another browser tab, then return. Wait for access restoration; the proposal must remain editable and unsaved. Continue and explicitly save once. Navigate to reader/day and back; check selected activity and saved notice persist.
- [ ] In two windows of the synthetic account, create competing bus or activity selections. After the first conflict, save another change in the other window. “Last inn lagret” must fetch that newest value without saving another change; a failed read must retain the local proposal and offer retry.
- [ ] Explicitly Start, register one activity as completed manually, leave the others unregistered, and inspect end confirmation. Cancel first, then explicitly end. Reload/open recap: exactly that activity is completed manually; others stay unknown/unregistered. The recap is read-only, and there is no resume.
- [ ] On separate synthetic work, explicitly abort. Inspect interrupted/unregistered outcomes and reload the fixed recap. Account notices must remain independently available after day closure.
- [ ] Log out; use Back and reload. Private content must remain hidden. Another isolated account must not see the first account's saved work. The demo must remain visibly fictional and never reveal private records.
- [ ] Review the [executed evidence and failure matrix](evidence/12-4-handoff.md), especially actual stale/lost-response recovery and deterministic expiry tests. Do not wait seven days or alter the operational clock/database for acceptance.
- [ ] Record device/browser, exact branch commit/build, observed discrepancies and the owner's explicit acceptance decision. Do not infer approval from checked automated tests.

At the initial desktop checkpoint the tablet was unavailable. The later [physical Lenovo follow-up](evidence/12-4-device-testing-2026-10-28.md) covers native PDF selection/cancellation, complete actual flows, native notice tab switching/HOME, concurrency and account/logout boundaries over isolated USB. These automated device actions do not grant owner acceptance. Instrumented notice tab/HOME emitted no hidden/visible, although the native picker did; preserve that evidence limit. The tablet is left logged into a separate dedicated synthetic account at15324/private; its credentials are only in ignored `.private-runtime/story124-device.json`. The original manual account above remains unchanged. No tunnel or active-site replacement was used.
