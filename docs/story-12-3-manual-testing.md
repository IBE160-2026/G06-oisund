# Story 12.3 — Jonas' manual checklist

> Publication follow-up,27 October2026: Jonas has now explicitly authorized committing/pushing the completed documentation and evidence, then merging12.3 into main after identity/final checks and pushing main. Earlier no-commit/no-push/no-merge statements describe the previous checkpoint.12.4 remains backlog.


**Story 12.3: done/accepted,27 October2026.** Jonas approved personal Lenovo/Brave readability and touch comfort, and granted conditional overall acceptance. The remaining required device checks passed, making that approval effective; see [final decision and evidence](evidence/12-3-device-acceptance-2026-10-27.md). No further mandatory owner action.12.1/12.2 remain accepted;12.4 backlog. Latest instruction prohibits commit/push; no merge was performed.

## Physical Lenovo result — 27 October2026

Physical TB361FU / Android16 / Brave1.97.59 USB testing is now recorded in the [device report](evidence/12-3-device-testing-2026-10-27.md). Covered device checks, native controls, actual2x pinch, selected focus pixels and theme/privacy lifecycle passed after bounded adapter corrections. Jonas separately confirmed finger theme activation and physical portrait keeping Night/visible controls. That report is the earlier partial checkpoint; the [final private-flow/glyph/focus follow-up](evidence/12-3-device-acceptance-2026-10-27.md) now completes the required scope and records owner acceptance.

Do not repeat completed checks. Private review/confirmation, ended/aborted private recap, native glyph pixels in both themes, actual keyboard focus and final logout/privacy now passed on the same8ca318b product. TalkBack/hardware keyboard/OS magnification/Brave text-size settings remain untested compatibility coverage, not extra prerequisites under the actual story criteria. Earlier pending/hardware limits below describe prior checkpoints; only specifically evidenced coverage is superseded. USB reverse15323/18323/18324 accesses this build independently of the old remote pilot. No ordinary HTTPS/mobile-network deployment qualification is inferred.

For optional later inspection: log in to the existing synthetic account in `/private`; open5January2031 for ended recap (one completed/one unregistered) or6January2031 for aborted recap (both unregistered), switch Day/Night and reload/reopen. Expect the same server facts, read-only controls and theme. These additive device fixtures leave2/3January manual plans intact. Credentials remain in the ignored local file described below; do not put them in reports.

## Start this isolated build

Use PowerShell in `D:/IBE160/tmp/story-12-3`, with Docker Desktop running:

```powershell
$py = 'C:/Users/Jonas/AppData/Local/Programs/Python/Python312/python.exe'
& $py scripts/verify-story123.py up
& $py scripts/verify-story123.py prepare
& $py scripts/verify-story123.py build
& $py scripts/verify-story123.py serve
```

If the verified preview is already running, use it directly. For a later rebuild, stop only this task's verified preview with `& $py scripts/verify-story123.py stop-preview`, rebuild and serve again. An occupied port is refused; never stop an unidentified listener.

- Open <http://127.0.0.1:15323/demo> for the isolated in-memory simulation, or <http://127.0.0.1:15323/private> for the actual private application with synthetic data. The actual fictional database assessment is at <http://127.0.0.1:15323/>.
- Read credentials locally from ignored `.private-runtime/story123-manual-credentials.json`. Never put the password in screenshots, commits or chat.
- Preparation adds synthetic line 20 plans for 2 and 3 January 2031 without overwriting existing plans/edits. Use only fictional data and the repository's `Eksempelfiler/` if testing import.
- This environment uses Compose `ibe160-story123-tests`, APIs 18323/18324 and its own volumes/secrets. The 12.1/12.2 preview 15312 and APIs 18312/18313 are separate and must remain untouched.
- These addresses are loopback on this PC. Physical tablet access requires a separately verified route to **this build**. The existing tablet deployment is not evidence for 12.3; no new external route is activated here.

## Reusable replay checklist (not outstanding acceptance work)

The unchecked boxes below are a blank template for a future independent replay. They do not supersede the completed scope/evidence above and are not a request for Jonas to repeat it.

- [ ] In a fresh browser context, open `/private`: expect Day and an unpressed `Nattmodus` control. Toggle it: expect `Visning: Natt` and pressed state. Reload, open `/demo`, reset the simulation and return: the chosen theme remains.
- [ ] Log in using the synthetic account. Open the 2 January plan, day overview, selected activity, bus field and notice reader/maintenance. Switch themes on each type of screen. Text, unknown facts, links, disabled boundaries and current selection must remain distinguishable and readable.
- [ ] In `/demo`, open the partial example, enter a long Norwegian duty/bus value, save, confirm plan and inspect a selected activity before Start. Selection must not start work. Use the next-save fault controls for unavailable/conflict: proposal and comparison stay readable, and failure never claims saved.
- [ ] Use keyboard Tab/Shift+Tab in access, editor and maintenance. Open Start/end/reset confirmation; cancel or Escape where offered. Expect a visible focus ring, no keyboard escape from the native reset modal and return to the visible invoking control. Open notice maintenance from preparation both with and without an open plan, then return: focus returns to that preparation button.
- [ ] Use 200% text and long Norwegian values at narrow/wide PC sizes, then portrait/landscape on the actual tablet when access is available. All content and actions remain reachable without horizontal page scrolling or clipped critical information. Check native field/checkbox indicators and touch targets on the actual device.
- [ ] Explicitly Start the simulation, save one activity status and leave another unregistered, then cancel and confirm ending. Expect a read-only recap, the saved activity status and unknown/unregistered remainder. Theme changes never record an activity status. Reset removes simulated content while preserving the theme.
- [ ] Log out of `/private`, use Back and reload. Private content stays unavailable until login; theme remains. Application localStorage contains only `ibe160-theme=day|night` after an explicit theme choice, and no private fields; unrelated preexisting keys are not deleted.

Record pass/fail with build, device/browser version, orientation, zoom/text settings, steps and observed differences. Record Jonas' explicit approval separately. 12.1/12.2 are accepted; [their own checklist](story-12-manual-testing.md) remains historical evidence.

## Requirement-to-evidence map

| Story criterion | Concrete behavior and check |
|---|---|
| Both manual themes, labelled controls, keyboard/dialog focus | Shared preference on all entries; keyboard traversal and actual rendered text/control/focus measurements on access, editor, review, day, activity, notices, conflict/error, closure and recap. Native reset focus is trapped and cancellation returns to invoker. |
| Long Norwegian text/enlargement/tablet/PC layout | Explicit 100%/200% text cases at 800/1440px in both themes, literal long synthetic values, actual overflow and focus visibility checks. Physical target qualification remains separate. |
| Persist theme without private data | Exact allowlisted storage assertions across reset/reload/routes/logout; invalid/denied storage tests; existing demo no-network/GPS/private-persistence regression. |
| Preserve current contracts and scope | Actual private API/PostgreSQL fixtures, independent expected behaviors and regression checks; no backend/schema/parser/retention changes, Auto, wake, GPS or 12.4 work. |
| Meaningful executed evidence and limitations | [Current-main integration report](evidence/12-3-main-sync-handoff.md) and unique `12-3-*` manifests/measurements; original failures retained. Historical 477/479 is unchanged, not a fresh complete broad pass. |

## Repeat automated checks

```powershell
& $py scripts/verify-story123.py verify
& $py scripts/verify-story123.py browser tablet-pc.spec.ts tablet-pc-private.spec.ts tablet-pc-measurement-probes.spec.ts theme-clear.spec.ts
& $py scripts/verify-story123.py browser fictional-assessment.spec.ts fictional-day.spec.ts private-access.spec.ts
```

Browser mode starts its own strict-port preview if none is explicitly managed. When using the verified `serve` preview above, set `$env:STORY123_EXTERNAL_SERVER='1'` for browser checks. Clear this process-scoped value afterward. The runner preserves source/test/build hashes, command exits, raw UTF-8 logs, per-state measurements and original failures. Consult the execution report for the exact final regression files actually run.

Native checkbox boundaries/checkmarks are measured from actual Edge PNGs. Individual native calendar/time-picker, select-arrow and disclosure-marker pixels, OS/browser zoom, assistive technology and actual hardware remain unmeasured and require the manual record. Computed text/control measurements do not establish those passes.


## Accepted-main feedback and dedicated tablet entry

Use a fresh hard reload of the current build. Historical 12.3 test results precede this integration and do not qualify the new version.

- [ ] In the demo editor, save twice and verify that each confirmation is visible beside the form. Exercise unavailable, conflict and lost acknowledgement: values remain readable in the same readonly form while locked; compare labelled current/proposed fields and revision, then recover the original receipt. Controls use `Simulert lagringsresultat` and `Manuell aktivitetsstatus`.
- [ ] For the dedicated private tablet entry, run the separate checks below. They build `deploy/tablet/index.html`/`src/tablet.tsx` into `frontend/dist-story123-tablet` and own a strict loopback listener on 18483 during the check. Verify the actual theme changes, reload/logout persistence and no private browser storage. The relative `/private-api` transport is mocked in these browser checks; this is not a live proxy, HTTPS or physical-device pass.

```powershell
& $py scripts/verify-story123.py tablet-build
& $py scripts/verify-story123.py tablet-browser
& $py scripts/verify-story123.py tablet-browser --port 18481
& $py scripts/verify-story123.py backend-transport
node --test scripts/test-tablet-configuration.mjs
```

The standard `build` mode clears inherited `VITE_PRIVATE_API_BASE`; it still targets its own private API 18324. The dedicated build runs TypeScript checks and explicitly sets `/private-api` and an intentionally unusable legacy base to prove relative-base priority. Port 18481 is an additional compatibility check for the retained original tablet configuration; both ports are strict loopback listeners owned only for each check. Tests include failed logout, persistent locking across reload, successful retry and retained theme, with empty private storage/cache/service-worker assertions. Invalid explicit-base checks evaluate the actual configuration prelude and fail closed. The separately built tablet output leaves the standard demo/private output intact. Current gateway/HTTPS transport checks and fresh full matrix outcomes are recorded separately in the integration report.
