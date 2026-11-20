---
title: 'Verify navigation protection through adoption of current saved values'
type: 'chore'
created: '2026-11-20'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem**. Two broad Edge cases saw the correct current bus value and sampled the window navigation guard before it released. A single input assertion does not establish that the outer workspace has finished applying the adoption.

**Approach**. Verify the failed read and a controlled pending retry with the local proposal and navigation protection intact. After an authorized retry restores current data, verify the outer controls and browser navigation guard release. Preserve request counts and confirm the saved value directly.

</frozen-after-approval>

## Implementation Notes

The tests exercise bus and activity selection against isolated PostgreSQL via `frontend/tests/private-current-adoption.spec.ts`. `PrivateBus` publishes its value and invokes the parent lock callback. `PrivateConfirmation` forwards the lock in an effect, and `PrivateDrafts` updates the window listener in another effect. The established path is present on local main and V2. Compare that transition on both builds. Keep the stable test inputs and scopes, and change runtime code only if the guard can remain incorrect after the corresponding outer controls settle.

The original broad Edge report failed `bus: unavailable fresh adoption never replaces local proposal with cached comparison` and `bus: changed-equal-revision fresh adoption never replaces local proposal with cached comparison` at the final immediate `beforeUnload` assertion. The field value had already passed its assertion in both cases. A narrow run of those two cases repeated three times per build caught the intermediate guard once on local main. The next probe 10 ms after starting to sample already observed the guard released. All six narrow V2 samples had released at the first probe. The runtime revisions were local main `df3fc940a7f97bd632e230ddb38c2fa45e8d2bfb` and V2 `8af7bae8694cfb6998f373e000c1333a92730571`. All 35 archived main frontend input blobs matched Git.

The comparison used the `ibe160-v2-regression` project with notices refresh off, localhost UI origin `19671`, private API `19673`, and the existing isolated regression database. Both frontend previews were built against that API. The temporary Playwright configuration is `frontend/test-results/v2-adoption-test/config.ts`. Reports under `tmp/v2-adoption-original-*.json` retain the original probe, and `tmp/v2-adoption-reviewed-*.json` retain the first strengthened pass. For the repository V2 runner, regenerate `frontend/.v2-tests` with `node scripts/prepare-v2-tests.mjs` from the root, start `scripts/v2-local.ps1 -Mode Test -ApisOnly`, build the frontend to `dist-ibe160-v2-tests` using API ports `19652` and `19653`, then run `playwright test --config playwright.v2.config.ts private-current-adoption.spec.ts` from `frontend` with `COMPOSE_PROJECT_NAME=ibe160-v2-tests`.

A diagnostic observed the browser guard from the exact input update in both originally failing variants. The guard was active at this update and was released at the later sample in all four runs, two per build. All 20 final comparison cases passed on each build. The final tests require the failed-read message and original proposal, a confirmed held retry with active navigation protection, release after the actual response, correct saved data, no writes, and usable navigation. Runtime code was unchanged. [Earlier lifecycle assertion distinction](spec-v2-lifecycle-regression-contract.md). The exact update probe and final runs are retained locally in `tmp/v2-adoption-commit-probe-*.json` and `tmp/v2-adoption-final-*.json`.

## Review Triage Log

- Medium, patched. The held request now matches the method and confirms that the exact GET has entered the route handler. The retry button must be disabled before sampling the guard.
- Medium, patched. Recovery removes the comparison and the selection proposal. The test opens preparation after verifying the authoritative saved value and guard release.
- Low, patched. After 401, the login view must have replaced the private section and cleared its window listener. Read and write counts are checked after that transition.
- Low, patched. The comparison revisions, fixture setup, original case names and standard V2 generator are recorded above.
- Low, scoped out. Concurrent independent resource drafts would require a separate scenario. Existing bus-only leave-guard cases cover the resource's dirty and unresolved states. This regression tests the release following adoption of the current resource.
