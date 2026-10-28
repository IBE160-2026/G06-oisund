# Story 12.4 — manual acceptance

Owner acceptance is pending. This checklist concerns the isolated synthetic12.4 build, never the active website or owner's account. Automated desktop results and historical physical tests do not constitute this acceptance.

## Open the isolated build

Worktree: `D:/IBE160/tmp/story-12-4`, branch `story/12-4-complete-user-flow`. Qualified implementation commit: `5ca3f7df73f4cf49f5244dbc97a0a3ebb8de9891`; subsequent evidence/log commits preserve the same product bytes. Final served main asset: `main-CxykOOFA.js`; see the linked post-commit runtime audit in the handoff.

```powershell
$py = 'C:/Users/Jonas/AppData/Local/Programs/Python/Python312/python.exe'
& $py scripts/verify-story124.py up
& $py scripts/verify-story124.py prepare
& $py scripts/verify-story124.py serve
```

Use a separate private browser window to keep these loopback session cookies separate from other local app ports. Open <http://127.0.0.1:15324/private>. Read the synthetic credentials locally from `.private-runtime/story124-manual-credentials.json`; do not paste credentials into evidence. The separate demo is <http://127.0.0.1:15324/demo>. Actual APIs use loopback18325/18326; own Compose project is `ibe160-story124-tests`. This is separate from `app.bussassistent.com` and its existing operational database/tunnel. No public12.4 route is configured.

`serve` builds before starting a verified loopback listener and refuses an occupied port. Before automated browser tests, run `stop-preview` to release only its own preview. `prepare` is additive and does not reset existing manual work. Browser regression fixtures must never use the manual account.

## Acceptance checklist

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
