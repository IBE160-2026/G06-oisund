# Story12.4 — accepted main integration,28October2026

Jonas explicitly authorized source integration and main push after [owner acceptance](12-4-owner-acceptance-2026-10-28.md), preserving existing data/access/environments and excluding deployment/12.5. He subsequently authorized deleting the fully integrated12.3/12.4 remote/local branches after main is checked and pushed, preserving private worktrees/data.

## Actual merge and accepted-content identity

Fresh `git fetch origin --prune` found local/origin main both `c3e5d66a7d9faa9af19a58c6002538610c163352`; there were no newer main changes. Local/origin12.4 both `4e38e240917b29450e68f817b85411185ef5eac3`. Both main and12.4 checkouts were clean. All required commits were ancestors of the accepted branch: UX/product5ee35ef, physical evidence2671ef7, acceptance4198b1a and log4e38e24, plus mobile correctionc0e809f. The [preflight](12-4-main-preflight.json) retains branch/worktree/container identities.

Merge `b0b2a6246b329ad0efa85b570c3f9a0d7a932c33` follows previous project practice: `git merge --no-ff`, message Merge accepted Story12.4 complete user flow, parents c3e5d66 and4e38e24. It completed without conflicts or product edits. The entire committed merge tree is exactly the accepted branch tree: `9a3a080188411d02d3ba81f45859e4c8fdef8ebc`. Thus all code, tests, UX changes, physical evidence, acceptance, documentation and history are retained.

All frontend/backend/scripts/fixtures/integration configuration has zero committed diff from accepted product `5ee35efb3753bed10bafc21a53a88fec3d93b287`. Main's98 tested frontend/backend source files equal the exact tested worktree after Git LF/CRLF normalization;49 differ only in those checkout line endings. Tested worktree bytes still match their recorded hashes. Mobile PrivateAccess.tsx, pdfUpload.ts, playwright.tablet.config.ts and mobile specification/evidence blobs equal c0e809f exactly; PrivateImport's accepted UX changes remain alongside the preserved upload behavior. No conflict resolution altered mobile logic.

## Fresh checks after merge

| Executed on merged main | Result |
|---|---|
| TypeScript `node frontend/node_modules/typescript/bin/tsc --noEmit --project frontend/tsconfig.json` |Passed; [log](12-4-main-typescript.txt), no assets emitted/rebuilt. |
| `python -m unittest scripts/test_verify_story124.py` |12/12 passed; [log](12-4-main-python.txt). The printed FAIL is the deliberately injected audit-exception test, followed by unittest OK; it is not an actual runtime-audit failure. |
| `node --test scripts/test-prepare-story124-tests.mjs scripts/test-tablet-configuration.mjs` |6/6 passed; [log](12-4-main-node.txt). Windows junction refusal exercised where file-symlink privilege was unavailable; no skipped tests. Existing Node experimental warning only. |
| Read-only integration audit |215/215 checks passed; [record](12-4-main-integration.json), [method](12-4-main-audit-method.py). Includes exact trees/product/mobile identity,98 source checks and the preservation checks below. |
| Final desktop/mobile/physical evidence archives |All3 archive hashes and172 individual member hashes verified:93+47+32. These preserve final64-case desktop,32-case mobile and revised physical device bytes. |
| Existing runtime |All27 container IDs/images/ports/start times/restart counts/source-mount sets unchanged. Four loopback HTTP200 responses have identical body hashes; bare18081 root remains RemoteDisconnected before/after, so this does not claim authenticated remote health. No container/tunnel/rebuild/deploy command was issued. |

Product content is identical, so approved **64/64 actual API/PostgreSQL/browser**, **32/32 controlled mobile boundary** and actual Lenovo checks are reused rather than rerun. Revised physical raw attempts remain13 passed/4 failed exploratory records, with all relevant scenarios subsequently passing; the owner's later explicit decision grants acceptance. Historical broad317/5/4 is not relabelled326/326. No fresh functional/API/database/physical run is claimed by this integration.

## Audit attempts and limits

The first preflight assumed all existing unauthenticated loopback roots returned HTTP responses;18081 closed the connection. The guard stopped before merge. [Initial preflight](12-4-main-preflight-initial.json) and [method](12-4-main-preflight-initial-method.py) are retained. The corrected method records response/transport categories per port without changing services; the same18081 category remained after merge.

The first whole-record container comparison failed. An immediate independent reread found no field differences ([reread](12-4-main-runtime-reread-difference.json)). The initial after-snapshot was not retained, so its root cause is unproven. The final method sorts semantically unordered mount lists while requiring exact identity/image/ports/start/restarts/mount membership, and retained before/after values passed. [Initial audit](12-4-main-audit-initial.json), [method](12-4-main-audit-initial-method.py). No runtime mutation or weakened identity requirement was used to obtain the pass.

## Publication and cleanup

This report records checked local integration before main publication; the session log records the actual push receipt and subsequent branch cleanup.12.4 stays done/accepted and12.5 stays backlog. No deployment or active-site/data/access change is included. Test environments are retained; any private/active worktrees will be preserved at their exact original commits rather than recursively deleted. The older tablet-remote-access worktree had16 pre-existing changed/untracked entries and is outside this task; it remains untouched.
