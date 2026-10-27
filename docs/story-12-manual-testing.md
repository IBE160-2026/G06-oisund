# Story 12.1 and 12.2 — Jonas' manual test checklist

Jonas har ikke gjennomført manuell/fysisk akseptansetest av Story 12.1 eller Story 12.2. Teknisk integrasjon og automatiske tester innebærer ikke brukeraksept. Begge avventer Jonas sin testing.

Both stories remain `review` / `in-review`, with owner acceptance pending. Local integration is authorized independently of acceptance. See [integration results](evidence/12-integrated-handoff.md) for the current automated results and commit references.

## Start the integrated local application

Use PowerShell in `D:\IBE160`, on local `main`, with Docker Desktop running. The following commands use a dedicated synthetic project. Ordinary services on 5173/8000/8001 and the old story environments are separate.

```powershell
$py = 'C:/Users/Jonas/AppData/Local/Programs/Python/Python312/python.exe'
& $py scripts/verify-story12-integration.py up
& $py scripts/verify-story12-checks.py build
& $py scripts/verify-story12-integration.py prepare
& $py scripts/verify-story12-checks.py serve
```

If the verified preview is already running, use it directly. To rebuild later, stop only that preview with `& $py scripts/verify-story12-checks.py stop-preview`, rebuild and serve again. An occupied port is deliberately refused; do not stop an unidentified listener.

- Simulation: <http://127.0.0.1:15312/demo> (also `/demo.html`), no backend/login required by the simulation.
- Actual fictional PostgreSQL assessment: <http://127.0.0.1:15312/>.
- Actual private application with synthetic data: <http://127.0.0.1:15312/private>.
- Isolated APIs: fictional 18312, private 18313. Migration 014 runs automatically when the private API starts.
- Open a new InPrivate window. Credentials are stored only in ignored `.private-runtime/story12-manual-credentials.json`; read that local file, never put its contents in screenshots, evidence, commits or chat.
- Preparation provides two synthetic line-20 plans for 2 and 3 January 2031, with separate source drafts. The dates are intentional, so expiry cannot invalidate the manual fixture before testing. Use only fictional files from `Eksempelfiler/`.
- To repeat after deleting one plan, rerun `prepare`: it adds only missing requested dates and preserves the surviving plan and edits. It refuses unexpected dates, duplicate plans or changed line scope. It does not reset your account or overwrite existing plans.

These are loopback addresses on this PC. Physical tablet/network testing needs separately configured access to this integrated build. The existing tablet environment is a separate deployment and does not establish that this build was tested there.

## 12.2: repeatable simulation

- [ ] Open `/demo`. `Fiktive demodata` and simulated storage remain clear on every screen. No login is needed.
- [ ] Choose partial import. Uncertain source facts stay visibly uncertain. Edit duty/bus, save explicitly, review the simulated receipt and confirm the plan.
- [ ] Select and inspect an activity before Start. Selection must not start the day or register completion. Check previous/next boundaries.
- [ ] Cancel Start once, then confirm it. Propose and save one outcome; leave another unregistered.
- [ ] Try the next-save fault controls: unavailable preserves the proposal; stale revision shows comparison; lost acknowledgement stays unresolved until receipt lookup. Failed lookup must not claim success.
- [ ] Read and maintain a notice with missing source/start information. Unknown stays unknown. Try empty/filtered/unavailable reader examples. A new notice requires a valid ending.
- [ ] Cancel end/abort, then confirm one. The recap is read-only, shows saved counts and preserves unregistered outcomes as unknown. Independently maintained notices remain available after closure.
- [ ] Cancel reset, then confirm reset and repeat the journey. Reset clears only this simulation instance. Reload also resets volatile simulation state.
- [ ] Try unsupported input and the labelled manual fallback. It edits duty/bus within a fixed three-activity sample; it is not actual PDF extraction or full activity authoring.
- [ ] Check keyboard focus, narrow layout and both manual themes. The illustrative legacy notice without ending is excluded from active reading and has no completion action in this simulation. Theme persistence and broader physical device qualification belong to later stories.

## Actual fictional database path

- [ ] Open `/`. Wait for `Ikke lagret`. Save with `Lagre fiktiv dag`: expect `Lagret og bekreftet av tjenesten.`
- [ ] Reload the saved URL: expect the original stored day and `Lagret eksempel er hentet fra tjenesten.` Overnight calendar dates and unknown bus remain explicit.
- [ ] Open `/demo` and reset it. Return to the saved URL: the actual stored day must still be readable. The simulation reset does not reset PostgreSQL or private data.

## 12.1 and 12.2: actual private notice integration

- [ ] Sign in at `/private` using the synthetic credentials. Open the 2 January plan and `Manuelt vedlikeholdte avvik` → `Registrer avvik`.
- [ ] Enter a fictional SMS description, title and line 20, leave source URL/update/start unknown, and set `Gyldig tildato` to 4 January 2031. Save: expect an actual saved receipt, no invented source check and one notice.
- [ ] Open the 3 January plan and `Les avvik for linjer og datoer`. The same incident appears once. Edit its title in maintenance: both days show the same updated incident.
- [ ] Delete only the 2 January confirmed plan. Open 3 January: the independent account notice remains. The separate source draft can remain until its own retention deadline.
- [ ] Explicitly choose `Kontrollerte kilden nå`, then `Avslutt avvik manuelt`. Active reading excludes the ended notice; maintenance retains read-only history. Editing, checking and ending remain distinct facts. Ending is not proof that a road is clear.
- [ ] Create another notice ending 1–2 minutes in the future. In account maintenance, after ending it is marked expired and cannot be extended; retained history lasts until its separate storage deadline. This current-date notice will not overlap the 2031 plans in the filtered day reader; inspect its status in maintenance.
- [ ] Import a supplied fictional PDF, review/cancel it and verify the retained plan survives. No raw original or filename should persist in browser stores.
- [ ] Log out, use Back and reload. Private fields remain unavailable until a new login. No private localStorage/sessionStorage/service-worker data is expected; private API replies use `Cache-Control: no-store`.

Actual lost-response and replay behavior is exercised by automatic transport fault tests against the real API/PostgreSQL, separately from the simulation. A manual visual session does not itself prove seven-day purge, late transaction races or original-command immutability; see the named automatic checks in the integration report.

## Record your outcome

For each story record pass/fail, device/browser/build, steps and observed differences. Do not mark either story accepted until Jonas explicitly confirms it. Physical testing and user acceptance remain separate from all automated desktop results.
