# Story 12.2 — independent-scope handoff

The repeatable fictional demo is technically verified and ready for manual review. Overall acceptance is pending: final actual notice creation/retry/lost-response integration must wait for the stable, integrated 12.1 contract. No owner acceptance is recorded.

## Checkout and integration boundary

- Branch: `story/12-2-fictional-assessment`.
- Worktree: `C:/Users/Jonas/.codex/.chatgpt-projects/g-p-6ab6b4c1c6888191a96d3242fab912b4/story-12-2`.
- Recorded base and unchanged HEAD: `0bae54833f38dc3dbf041d54c324c220618c21da`; local and published main matched at initial verification.
- Shared changes are the small demo import/link/dispatch in `frontend/src/main.tsx`, a Vite multi-entry configuration/alias, and a README guide link. No backend/private controller/migration edits. Other additions are demo-specific UI/model/style, tests, isolated Compose/runners, specifications and evidence. Reconcile main-entry/config hunks when integrating 12.1; do not replace its API environment settings.
- Read-only 12.1 contract documentation was inspected again after its integration report appeared. It still reports final runtime verification/review pending. New notices require server-issued `POST /notice-operations` admission, then the original ID on `POST /notices`. Lost issuance must not dispatch creation; once creation may have dispatched, retain that ID and use receipt lookup before retry. Unknown/deleted/expired IDs cannot recreate incidents. No unfinished 12.1 code was imported.
- Account notices retain their own lifetime, independent of original-day ending/deletion/expiry. This branch does not take over 12.1 retention/deletion work.

## Delivered behavior

Dedicated `/demo` and `/demo.html` entries load the network-free simulation, with distinct import, proposal editor, saved-plan review, day, selected activity, notice reader/editor, Start/end/abort confirmation and terminal recap screens. Import uncertainty and unsupported scanned PDF are labelled simulations. Unsaved proposals, uncertain replies and confirmed simulated receipts remain distinct. Stable selected-member outcomes, explicit Start, frozen plan, confirmation/cancel and unknown terminal outcomes preserve the accepted manual semantics.

Unavailable, conflict and lost-response saves are controlled examples. Failed receipt lookup never sends a second mutation. Reader examples distinguish no stored data, empty filtering and unavailable/unknown contents. Confirmed reset affects only the current fictional memory instance; it does not clear browser stores, cookies or any server data. Notices remain independently editable after shift closure. No GPS, external source, credential or browser persistence is needed.

## Verification and review

- Final root frontend run: [production build and 14 Edge passes](12-2-frontend-20261026T220411706929Z-a5bf80782560.json), exit 0 for both commands. Covers repeated reset, normal/failure flows, exact saved outcomes, known-start boundaries, unknowns, proposals, keyboard return, native dialogs, 360px layout and rendered Day/Night comparison/dialog contrast. Monitoring starts before navigation and permits only expected static demo assets; fetch/XHR/GPS attempts and page errors remain zero.
- Actual isolated API/PostgreSQL: [executed run](12-2-real-20261026T215053Z.json), 18 existing assessment tests plus save/read/replay/conflicting replay/restart/reset/reseed and unauthenticated private denial passed. Populated synthetic private account and sentinel fingerprints were identical across fictional reset. Caller-discarded acknowledgement followed by same-operation replay is precisely qualified; this is not an injected transport failure or a private notice recovery pass.
- [Final audit](12-2-final-audit.json): frontend source and bundle hashes match the final root run; 62 backend app/test/migration/build files in the tested container match the worktree byte for byte; prior actual app hashes match; backend tracked diff and untracked list are empty. All 414 historical non-12.2 evidence files match their before hashes. Git index is empty.
- Audit SHA256: `6573f7a71c562bdacdd0236f3a695c3ba417a5a0b797a309d960a8f5df9da712`.
- All three independent review layers returned and reinspected the retained corrections. Sixteen findings were individually triaged in the story spec: fifteen bounded corrections/verification gaps resolved; one low-priority legacy-completion expansion rejected with an explicit limitation. No unresolved concrete regression remains in the independent scope. Original failures and earlier checkpoints retain their historical status.

## Start and inspect

The task preview is currently running only on `127.0.0.1:15222` (PID 36492; execution session 23736). `/demo` returned HTTP 200. Its own synthetic Compose services remain on fictional API 18222 and private API 18223, with project `ibe160-story122-tests` and separate `story122_fictional`/`story122_private` volumes. Ordinary and parallel services were not stopped or reset.

For a later manual launch, from this worktree's `frontend` directory:

```powershell
npm.cmd ci
npm.cmd run build
npm.cmd run start -- --port 15222 --host 127.0.0.1
```

Open `http://127.0.0.1:15222/demo`. Try partial import, save, confirm plan, select before Start, confirm/cancel Start, save an outcome, cancel then confirm end/abort, maintain a notice after closure, and confirm/cancel reset. Use the next-save fault and reader-example controls to inspect failures.

From the worktree root, `python scripts/verify-story122-frontend.py` reruns the build/browser gate; stop only this task's existing preview first because the verifier refuses port reuse. `python scripts/verify-story122.py` is the separate real API/PostgreSQL verifier and deliberately refuses existing task containers/volumes. Its [guide](../fictional-assessment.md) explains the exact project-only fresh-run cleanup; no ordinary cleanup command is needed for manual demo use.

## Limits and retained state

The demo edits duty/bus within a fixed three-activity sample; it is not an actual PDF parser or full activity authoring UI. The legacy missing-ending example is illustrative/excluded, with no completion command. Actual private notice admission/retry/lost-response verification, physical tablet observations and broader 12.3 theme persistence remain unperformed here. Simulated saves never prove PostgreSQL behavior.

Environment preparation and exact successful renderer command are in [the environment record](12-2-environment.md). Only ignored worktree-local TOML/TEMP/cache settings were used; no global environment or security changes. Existing branch/worktree/log history is preserved. No merge, staging, commit/push, external deployment, next story or acceptance registration occurred.
