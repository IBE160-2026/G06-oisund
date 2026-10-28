# Story 12.5 — accepted main integration, 28 October 2026

Jonas authorized integration, main publication and deletion of the fully merged story branch, preserving all environments and data. Story 12.5 remains done/accepted; Epic 12 remains open for its retrospective. No deployment, release/tag, learning-platform submission or extension work is included.

## Source and version identity

Fresh fetch found main/origin main at `99c272b09abaa5ffecf3286b406fbf065a445c7c` and local/origin story at `330d5a21bc38decc95bbd5332edee2acf08e4faa`. All 12 registered worktrees were clean before integration. Merge `dbdbd1813e29c02913b72e15a24f0a3321565d95` uses `git merge --no-ff`; its parents are those two commits. There were no conflicts. Its complete tree is exactly the accepted story tree `c8cad236b865df2e62ba0016b9e949a8eb4f127d`: all accepted code, tests, fixtures, evidence, acceptance/status and session history are retained, including `12c8475` and `330d5a2`.

The reproducible source/evidence snapshot remains `c067fdbb20150219c041588ed4e990e7b0ef6b94`, reachable through main. Executable source, fixtures, tests and configuration have no differences from that snapshot. Historical evidence keeps its original source references, including the post-review `8d50684` runs. Acceptance and integration are later documentation, not retroactive changes to the tested snapshot.

The current README now clones **main** before detaching at the same immutable snapshot. This is necessary because the approved story branch is being deleted. The immutable snapshot's own historical README still names the former branch; the current README explicitly explains which clone command to use. No tag/release or new runtime version is introduced.

## Fresh integration checks

Executed on Windows, Node v24.19.0, npm 11.17.0, Docker 29.7.2, Compose v5.5.1. Commands run from `D:/IBE160` unless specified.

| Check | Actual result |
|---|---|
| `node --test scripts/test-submission.mjs` | 6 passed, zero skips; [Windows log](12-5-main-node-windows.txt). |
| Pinned Node 24.19.0 Alpine container, `--rm --network none`, read-only scripts mount, same Node test command | 6 passed, zero skips; [Linux log](12-5-main-node-linux.txt). |
| Pinned Python 3.13-slim container, `--rm --network none`, read-only deploy/submission mount, `python -m unittest -v test_fictional` | 3 passed; [wrapper log](12-5-main-wrapper.txt). |
| Fresh `git archive --format=tar --output=tmp/integration-125-fresh-frontend/source.tar dbdbd1813e29c02913b72e15a24f0a3321565d95 frontend`, then `tar -xf ... -C tmp/integration-125-fresh-frontend`; `npm.cmd ci` in exported frontend | New node_modules, 26 packages installed, audit reported zero vulnerabilities; [install log](12-5-main-npm-ci.txt). No existing dependencies/assets reused. |
| In exported frontend: set `VITE_PRIVATE_API=http://127.0.0.1:18328`, `VITE_FICTIONAL_API=http://127.0.0.1:18327`; `npm.cmd run build` | TypeScript and Vite passed; [build log](12-5-main-frontend-build.txt). Exported build was not deployed. |
| Read-only existing demo status and served asset identity | Five healthy services, existing synthetic account verified; all three served asset hashes equal both original review evidence and the newly built assets. [Status](12-5-main-status.txt), [identity](12-5-main-verification.json). No login secrets recorded. |
| Complete ancestry/tree, executable blob identity, documentation links/line bounds and runtime/worktree preservation | 358 local links and 111 source-line bounds checked in the current README, submission documents, reproduction, owner acceptance and this report. [Verification](12-5-main-verification.json), [method](12-5-main-verification-method.mjs); [before/after preservation](12-5-main-preservation.json), [method](12-5-main-preservation-method.mjs). |

PowerShell's execution policy blocked the first bare `npm` invocation before installation. `npm.cmd` succeeded without changing policy. An initial successful build used unrelated environment variable names and therefore default API addresses; it was repeated with the actual demonstration variables above. Only the correctly configured build is the final retained build log. These are integration-command corrections, not product changes.

Two audit setup attempts were corrected before the successful recorded checks: a relative method-copy command was issued from the demo checkout rather than main (no file or runtime change), and the first link check required its own not-yet-generated result. The final method allows only its own output to be generated after successful checks; all other linked files must already exist.

The full actual API/PostgreSQL/backend/browser/reset/restart reproduction is **reused at its original source versions**, not rerun or relabelled: [reproduction and original failures](12-5-reproduction.md), [owner's ten-part acceptance](12-5-owner-acceptance-2026-10-28.md). Exact executable tree identity makes those results applicable to this conflict-free merge. No new fullstack, parser, physical-device, seven-day soak or operational benefit claim is made. Repeating a reset against the retained review environment would discard user data and is deliberately excluded.

## Preservation, publication and cleanup

The read-only preflight recorded all 35 existing containers and 16 volumes, plus all 12 registered worktrees. No existing service was stopped, restarted, rebuilt, replaced or reset. Production, tunnel/access, accounts/passwords and private files are outside the commands used here. Ephemeral network-disabled unit-test containers were removed normally.

Main push succeeded from `99c272b` to `2b91f0a55fbf3117b39c2cecaf5e5091b9cfbfd9`, containing merge dbdbd18, integration documentation 7aac8a2 and separate session log. Fresh fetch confirmed main/origin equality. `git rev-list --count story/12-5-reproducible-submission --not origin/main` returned **0**, and the local/remote story tips both equalled accepted330d5a2 before deletion.

Only then, `git -C tmp/story-12-5 switch --detach 330d5a21bc38decc95bbd5332edee2acf08e4faa`, `git push origin --delete story/12-5-reproducible-submission` and `git branch -d story/12-5-reproducible-submission` succeeded. Both refs are confirmed absent; no force flags or directory deletion. [Cleanup record](12-5-main-cleanup.json), [method](12-5-main-cleanup-method.mjs).

The story worktree remains clean at its exact accepted commit, retaining its directory and ignored local files. The independent demonstration clone remains clean/detached at c067fdb with its private generated runtime files; its local origin directory still exists. The demo remains available at http://127.0.0.1:15325/private. All other registered worktree HEADs/statuses and all35 containers/16 volumes were checked unchanged again after branch deletion. Exact runtime identity and served assets still pass. No secrets were read for this integration or included in the new files. Further commits record this completed cleanup/session only; they do not change executable source or the pinned delivery.
