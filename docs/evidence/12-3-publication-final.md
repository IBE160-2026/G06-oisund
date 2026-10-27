# Story12.3 — accepted main integration and final checks

Jonas explicitly authorized documentation/evidence commit and push, followed by story-to-main integration, unchanged-test-basis checks and main push on27October2026. This supersedes the previous checkpoint's no-commit/no-push restriction. Story12.3 remains **done/accepted** under the [recorded owner decision and actual device evidence](12-3-device-acceptance-2026-10-27.md).12.4 remains backlog and was not started.

## Recorded commits and integration

- Documentation/acceptance/final device evidence: `ea7764d` (217 files). All202 newly staged raw blobs matched the recorded SHA256 index before commit.
- Separate session log/issues commit: `1ac729c16b28ae19a0c9509022c92cffe3298aa7`. Story push succeeded from remote `d0369b3` to this commit, preserving the earlier local physical-test/log commits.
- Clean local/origin main before integration: `74849ff21bee108fe9cff93d740a96a6c6d2d7c5`. Fetch found no new incoming product changes.
- Merge: `cd8b4405a1ef5752440e719c3f8abf1253584e11`, parents accepted main74849ff and story1ac729c. No conflicts.
- Entire committed merge tree equals the pushed accepted story tree: `ad97c9465d4e2ce0e26f91cce11297753e97e77f`. Product paths have zero committed diff from tested product/tool revision `8ca318b55b98eb34de54f29ecab038322e3ccab6`. Subsequent publication changes concern only this evidence/documentation and session logging.

This report and final checks are committed before main publication. The [continued session log](../../.logs/jonas-oisund/996-2026-10-27-11-07-12-story-12-3-nettbrett-og-pc.md) records the actual main-push outcome and final publication check after that step; a report prepared before push is not itself a push receipt.

## Fresh final checks on merged main

| Check actually run | Result / evidence |
|---|---|
| Installed TypeScript `--noEmit --project frontend/tsconfig.json` | Passed; [log](12-3-publication-typescript.txt). No rebuilt assets or runtime restart. |
| `python -m unittest scripts/test_verify_story123.py -k BuildEnvironmentTests` |4/4 passed; [log](12-3-publication-python.txt). |
| `node --test scripts/test-prepare-story123-tests.mjs scripts/test-tablet-configuration.mjs` |2/2 passed; [log](12-3-publication-node.txt). Existing Node experimental type-stripping warning. |
| Exact test-worktree source/build manifest |41/41 source and6/6 built hashes unchanged. Main's committed tree is identical; main checkout content is identical after CRLF/LF normalization, as detailed below. |
| Archived and Git-committed device evidence |All339 raw blobs (137 earlier +202 final), working files and both archives match SHA256 indices; no historical failures/results rewritten. |
| Preserved runtime |All26 containers retain exact ID/image/start/restart/labels. Seven15312 and seven15323 HTTP byte hashes unchanged; both own API health endpoints200 with correct modes. |
| Actual Lenovo Brave target |All four target ID/title/URL triples unchanged, including three other tabs. Read-only evaluation confirms own Night demo, no private recap, and actual device fetch of main JS SHA256 `e06eae81214d031fddf7ee98d2f44871f4a538ea0781e2391bf8f022cfe11021`. No input/navigation/focus command, ordinary-tab action or browser-close operation. |
| Status/scope |12.3 done/accepted;12.1/12.2 remain accepted;12.4 backlog. No deployment or next story. |

Machine-readable [final audit](12-3-publication-final.json), [runtime observations](12-3-publication-runtime.json), [audit method](12-3-publication-audit-method.py) and [runtime method](12-3-publication-runtime-method.cjs) retain the exact identities, paths and results. The runtime method requires installed dependencies and the existing isolated USB target; it is a read-only audit, not a replacement for the earlier functional journeys.

## Initial audit mismatch and correction

The first publication audit exited1 at `frontend/index.html` because it assumed raw byte identity between separate Windows working directories. Twenty source files have only Git-checkout CRLF/LF differences;21 match raw bytes. All41 have identical normalized content, and the **entire committed merge/story trees are exactly equal**. The exact tested-worktree41 source/6 build hashes also remain unchanged. No product source was edited to conceal the difference, no rebuild occurred, and the first failure is not reported as a passed attempt. See [initial failure](12-3-publication-audit-initial.json) and [initial method](12-3-publication-audit-initial-method.py); the final audit enumerates every affected path and independently checks normalized content, committed tree, exact test-runtime hashes and raw evidence bytes.

The earlier accepted story/current-main suites and physical-device evidence apply to the same product content. This publication performs bounded final checks, **not a fresh complete browser/backend run**. The earlier19 grouped device attempts/17 passes/2 adapter failures, preceding physical57/39/18 and historical12.1/12.2 **477/479** remain unchanged. No overall WCAG, TalkBack/hardware-keyboard/OS-magnifier, ordinary HTTPS/mobile-network or complete12.4 qualification is inferred.

The ordinary runtime and separate15312 test service were preserved; merging source into main does not deploy/rebuild them. The isolated15323 environment still serves the accepted12.3 build. Existing deployment/security/operations follow-ups and inherited B6–B10 remain open in issues.md. The [manual checklist](../story-12-3-manual-testing.md) and accepted decision require no repeated owner testing for unchanged12.3.
