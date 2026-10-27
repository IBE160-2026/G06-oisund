# Story 12.3 — accepted-main reconciliation

Story 12.1 and 12.2 are done/accepted by Jonas (27 October 2026). Story 12.3 remains review/pending. Full accepted main `74849ff21bee108fe9cff93d740a96a6c6d2d7c5` is merged into the existing `story/12-3-tablet-pc-accessibility` history; this is no merge of the story into main. The [original handoff](12-3-handoff.md) and all previous raw records remain historical checkpoints.

## Integration decisions

- The `FictionalAssessment.tsx` overlap combines accepted main's local live feedback, repeated-save announcement, readonly proposal during conflict/lost response, labelled current/proposed comparison with revision and Oslo dates, original receipt recovery and activity-status terminology with 12.3's shared allowlisted theme control, storage disclosure and preference-preserving reset. Neither side's entire product file replaced the other.
- Both scoped CSS additions remain: 58px controls, night fields, modal scrolling/spacing and checkbox sizing together with feedback/comparison palettes, readonly opacity and narrow comparison reflow. Existing actual text/boundary/focus thresholds, meaningful enlargement and deliberate negative probes remain unchanged.
- `PrivateAccess.tsx` keeps the accepted validated explicit `/private-api` priority, HTTPS Secure logout marker, server clock, no-store requests and owner/session/retention contracts. The only dedicated-entry adaptation is wrapping `tablet.tsx` in the existing ThemeProvider.
- Accepted main statuses and issue closures are combined with 12.3 E10-A4/E11-A4 technical closures; other open issues are preserved. 12.3 owner acceptance and physical/native/zoom/assistive-technology qualification remain open. 12.4 is backlog.

## Reproducible isolated commands

Run in `D:/IBE160/tmp/story-12-3` with Node on PATH and the installed Python executable. Root alone runs final full qualification, commits, session logging and authorized push.

```powershell
$py = 'C:/Users/Jonas/AppData/Local/Programs/Python/Python312/python.exe'
& $py scripts/verify-story123.py up
$env:VITE_PRIVATE_API_BASE='/private-api'
& $py scripts/verify-story123.py build
Remove-Item Env:VITE_PRIVATE_API_BASE
& $py scripts/verify-story123.py verify
& $py scripts/verify-story123.py browser tablet-pc.spec.ts tablet-pc-private.spec.ts tablet-pc-measurement-probes.spec.ts theme-clear.spec.ts
& $py scripts/verify-story123.py browser fictional-assessment.spec.ts fictional-day.spec.ts private-access.spec.ts
& $py scripts/verify-story123.py tablet-build
& $py scripts/verify-story123.py tablet-browser
& $py scripts/verify-story123.py backend-transport
& $py -X utf8 scripts/test_verify_story123.py
node --test scripts/test-prepare-story123-tests.mjs scripts/test-tablet-configuration.mjs
& $py scripts/verify-story123.py prepare
```

Standard build explicitly removes inherited `VITE_PRIVATE_API_BASE` and sets APIs 18323/18324. Separate tablet build uses production `deploy/tablet/index.html` and actual `src/tablet.tsx`, emits only `frontend/dist-story123-tablet`, and explicitly sets `/private-api` ahead of an unusable legacy HTTPS origin. It leaves `frontend/dist` intact. Dedicated browser mode always creates its own strict loopback preview on 18483 and refuses an occupied listener. The relative API is mocked; the dedicated test verifies actual palette change, reload/logout preference and absence of private browser storage, plus existing session suspension/clock expiry controls. Invalid-base checks execute the actual configuration prelude with allowed/rejected values.

The backend transport mode uses a disposable `--no-deps` container in `ibe160-story123-tests` and only `test_tablet_transport.py`, which mocks database access and does not start lifespan, migrate, provision or contact an account. It checks explicit exclusive transport modes, canonical HTTPS origin, CSRF, no-store and Secure cookies/logout. A running own test environment/image is prepared by `up`.

Both browser modes and tablet/backend commands use the existing durable executor: unique raw logs/report/bundle/index, before/after source hashes and separate normal/tablet build identity. Hashed source inputs now include deployment sources, `.dockerignore` and tablet compose. Fresh generated API records identify tested_story 12.3 / pending and dependencies 12.1/12.2 accepted; main's old verifier and old JSON are unchanged. Test copies and screenshots stay in owned disposable paths. When reusing the owned 15323 preview, set `STORY123_EXTERNAL_SERVER=1` for standard browser checks only. Dedicated tablet mode always owns its preview.

## Bounded implementation checks

- TypeScript source check: `frontend/node_modules/.bin/tsc.cmd --noEmit --project frontend/tsconfig.json`, passed.
- New build-environment unit checks: `python -m unittest scripts/test_verify_story123.py -k BuildEnvironmentTests`, 2/2 passed. Deliberately inherited tablet env is cleared for standard build and overridden explicitly for dedicated tablet build.
- Actual configuration prelude: `node --test scripts/test-tablet-configuration.mjs`, 1/1 passed, including six invalid explicit bases. Node reports its existing experimental type-stripping warning; no product exception occurred.
- Initial exploratory configuration-test attempt imported the removed TypeScript JavaScript compiler API and failed before tests; corrected to the installed Node type stripper, then passed. An initial root-directory npx TypeScript attempt was interrupted; the direct installed compiler command above passed. Neither is represented as a browser/product gate.

Root final API/browser/build/gateway/runtime results and exact fresh evidence belong below. No old pass is claimed as fresh, and bounded source/unit checks alone do not establish integrated runtime qualification.

## Qualification limits

No tunnel activation, DNS/access-policy change, ordinary/pilot-data mutation, rewrite of historical evidence, story-to-main merge, rebase or force push. Other containers, 15312 preview and existing manual plans are outside these commands. Prior physical pilot observations do not qualify this exact integrated version. Physical Lenovo/Android/Brave/mobile-network, native picker/marker pixels, actual OS/browser zoom and assistive technology remain separately unmeasured until explicitly recorded. Mocked tablet transport does not establish live HTTPS/Cloudflare access. No overall WCAG or complete 12.4 acceptance is inferred.

## Root final qualification

Pending root execution and evidence append.
