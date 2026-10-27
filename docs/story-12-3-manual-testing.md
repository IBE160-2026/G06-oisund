# Story 12.3 — Jonas' manual checklist

**Owner acceptance: pending.** Jonas has not performed manual/physical acceptance of 12.1 or 12.2; both remain in review. 12.3 also remains in review until his explicit approval. Automated desktop results do not qualify physical Lenovo Pad / Android / Brave use.

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

## Short checklist

- [ ] In a fresh browser context, open `/private`: expect Day and an unpressed `Nattmodus` control. Toggle it: expect `Visning: Natt` and pressed state. Reload, open `/demo`, reset the simulation and return: the chosen theme remains.
- [ ] Log in using the synthetic account. Open the 2 January plan, day overview, selected activity, bus field and notice reader/maintenance. Switch themes on each type of screen. Text, unknown facts, links, disabled boundaries and current selection must remain distinguishable and readable.
- [ ] In `/demo`, open the partial example, enter a long Norwegian duty/bus value, save, confirm plan and inspect a selected activity before Start. Selection must not start work. Use the next-save fault controls for unavailable/conflict: proposal and comparison stay readable, and failure never claims saved.
- [ ] Use keyboard Tab/Shift+Tab in access, editor and maintenance. Open Start/end/reset confirmation; cancel or Escape where offered. Expect a visible focus ring, no keyboard escape from the native reset modal and return to the visible invoking control. Open notice maintenance from preparation both with and without an open plan, then return: focus returns to that preparation button.
- [ ] Use 200% text and long Norwegian values at narrow/wide PC sizes, then portrait/landscape on the actual tablet when access is available. All content and actions remain reachable without horizontal page scrolling or clipped critical information. Check native field/checkbox indicators and touch targets on the actual device.
- [ ] Explicitly Start the simulation, save one outcome and leave another unregistered, then cancel and confirm ending. Expect a read-only recap, the saved outcome and unknown/unregistered remainder. Theme changes never record an outcome. Reset removes simulated content while preserving the theme.
- [ ] Log out of `/private`, use Back and reload. Private content stays unavailable until login; theme remains. Application localStorage contains only `ibe160-theme=day|night` after an explicit theme choice, and no private fields; unrelated preexisting keys are not deleted.

Record pass/fail with build, device/browser version, orientation, zoom/text settings, steps and observed differences. Record Jonas' explicit approval separately. Manual acceptance of 12.1/12.2 still uses [their own checklist](story-12-manual-testing.md).

## Requirement-to-evidence map

| Story criterion | Concrete behavior and check |
|---|---|
| Both manual themes, labelled controls, keyboard/dialog focus | Shared preference on all entries; keyboard traversal and actual rendered text/control/focus measurements on access, editor, review, day, activity, notices, conflict/error, closure and recap. Native reset focus is trapped and cancellation returns to invoker. |
| Long Norwegian text/enlargement/tablet/PC layout | Explicit 100%/200% text cases at 800/1440px in both themes, literal long synthetic values, actual overflow and focus visibility checks. Physical target qualification remains separate. |
| Persist theme without private data | Exact allowlisted storage assertions across reset/reload/routes/logout; invalid/denied storage tests; existing demo no-network/GPS/private-persistence regression. |
| Preserve current contracts and scope | Actual private API/PostgreSQL fixtures, independent expected behaviors and regression checks; no backend/schema/parser/retention changes, Auto, wake, GPS or 12.4 work. |
| Meaningful executed evidence and limitations | [Execution and review report](evidence/12-3-handoff.md) and unique `12-3-*` manifests/measurements; original failures retained. Historical 477/479 is unchanged, not a fresh complete broad pass. |

## Repeat automated checks

```powershell
& $py scripts/verify-story123.py verify
& $py scripts/verify-story123.py browser tablet-pc.spec.ts tablet-pc-private.spec.ts tablet-pc-measurement-probes.spec.ts theme-clear.spec.ts
& $py scripts/verify-story123.py browser fictional-assessment.spec.ts fictional-day.spec.ts private-access.spec.ts
```

Browser mode starts its own strict-port preview if none is explicitly managed. When using the verified `serve` preview above, set `$env:STORY123_EXTERNAL_SERVER='1'` for browser checks. Clear this process-scoped value afterward. The runner preserves source/test/build hashes, command exits, raw UTF-8 logs, per-state measurements and original failures. Consult the execution report for the exact final regression files actually run.

Native checkbox boundaries/checkmarks are measured from actual Edge PNGs. Individual native calendar/time-picker, select-arrow and disclosure-marker pixels, OS/browser zoom, assistive technology and actual hardware remain unmeasured and require the manual record. Computed text/control measurements do not establish those passes.
