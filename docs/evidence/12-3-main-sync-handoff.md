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
& $py scripts/verify-story123.py tablet-browser --port 18481
& $py scripts/verify-story123.py backend-transport
& $py scripts/verify-story123.py browser private-access.spec.ts private-retention.spec.ts private-recovery.spec.ts private-notice-recovery-integration.spec.ts private-crossday-notices.spec.ts private-notice-reader.spec.ts
& $py -X utf8 scripts/test_verify_story123.py
node --test scripts/test-prepare-story123-tests.mjs scripts/test-tablet-configuration.mjs
& $py scripts/verify-story123.py prepare
```

Standard build explicitly removes inherited `VITE_PRIVATE_API_BASE` and sets APIs 18323/18324. Separate tablet build uses production `deploy/tablet/index.html` and actual `src/tablet.tsx`, emits only `frontend/dist-story123-tablet`, and explicitly sets `/private-api` ahead of an unusable legacy HTTPS origin. It leaves `frontend/dist` intact. Dedicated browser mode always creates its own strict loopback preview on 18483 and refuses an occupied listener. The relative API is mocked; the dedicated test verifies actual palette change, reload/logout preference and absence of private browser storage, plus existing session suspension/clock expiry controls. Invalid-base checks execute the actual configuration prelude with allowed/rejected values.

The backend transport mode uses a disposable `--no-deps` container in `ibe160-story123-tests` and only `test_tablet_transport.py`, which mocks database access and does not start lifespan, migrate, provision or contact an account. It checks explicit exclusive transport modes, canonical HTTPS origin, CSRF, no-store and Secure cookies/logout. A running own test environment/image is prepared by `up`.

Both browser modes and tablet/backend commands use the existing durable executor: unique raw logs/report/bundle/index, before/after source hashes and separate normal/tablet build identity. Identity also includes only the three allowlisted effective API build settings; arbitrary environment values are never serialized. Browser gates compare those settings with the expected mode. Hashed source inputs now include deployment sources, `.dockerignore` and tablet compose. Fresh generated API records identify tested_story 12.3 / pending and dependencies 12.1/12.2 accepted; main's old verifier and old JSON are unchanged. Test copies and screenshots stay in owned disposable paths. When reusing the owned 15323 preview, set `STORY123_EXTERNAL_SERVER=1` for standard browser checks only. Dedicated tablet mode always owns its preview, default18483; optional18481 verifies compatibility with the retained original tablet fixture configuration.

## Bounded implementation checks

- TypeScript source check: `frontend/node_modules/.bin/tsc.cmd --noEmit --project frontend/tsconfig.json`, passed.
- New build-environment unit checks: `python -m unittest scripts/test_verify_story123.py -k BuildEnvironmentTests`, 2/2 passed. Deliberately inherited tablet env is cleared for standard build and overridden explicitly for dedicated tablet build.
- Actual configuration prelude: `node --test scripts/test-tablet-configuration.mjs`, 1/1 passed, including six invalid explicit bases. Node reports its existing experimental type-stripping warning; no product exception occurred.
- Initial exploratory configuration-test attempt imported the removed TypeScript JavaScript compiler API and failed before tests; corrected to the installed Node type stripper, then passed. An initial root-directory npx TypeScript attempt was interrupted; the direct installed compiler command above passed. Neither is represented as a browser/product gate.

Root final API/browser/build/gateway/runtime results and exact fresh evidence belong below. No old pass is claimed as fresh, and bounded source/unit checks alone do not establish integrated runtime qualification.

## Qualification limits

No tunnel activation, DNS/access-policy change, ordinary/pilot-data mutation, rewrite of historical evidence, story-to-main merge, rebase or force push. Other containers, 15312 preview and existing manual plans are outside these commands. Prior physical pilot observations do not qualify this exact integrated version. Physical Lenovo/Android/Brave/mobile-network, native picker/marker pixels, actual OS/browser zoom and assistive technology remain separately unmeasured until explicitly recorded. Mocked tablet transport does not establish live HTTPS/Cloudflare access. No overall WCAG or complete 12.4 acceptance is inferred.

## Root final qualification

Final gates ran at `8ca318b55b98eb34de54f29ecab038322e3ccab6`, after merge `1197a1fd02aacd99ce27dd561db6990d84d054f4` (parents original story `df84065` and accepted main `74849ff`). Root fetched origin again; main is still exactly74849ff and its working copy is clean. No story-to-main merge. Source/build files remain unchanged after qualification; later commits record documentation/evidence/session only. Machine-readable aggregation: [qualification](12-3-main-sync-qualification.json).

| Final scope | Result | Unique raw manifest |
|---|---|---|
| Checked standard build, inherited tablet base cleared | passed | [12-3-build-20261027T190059396568Z-2259b324.json](12-3-build-20261027T190059396568Z-2259b324.json) |
| Actual API/PostgreSQL | 74/74 | [12-3-verify-20261027T190102042205Z-0fef7b07.json](12-3-verify-20261027T190102042205Z-0fef7b07.json) |
| Accepted demo and actual fictional assessment | 37/37 | [12-3-browser-20261027T190135888667Z-54ce7f61.json](12-3-browser-20261027T190135888667Z-54ce7f61.json) |
| Checked dedicated tablet build | passed | [12-3-tablet-build-20261027T190217469866Z-5d574672.json](12-3-tablet-build-20261027T190217469866Z-5d574672.json) |
| Dedicated tablet browser18483 | 5/5 | [12-3-tablet-browser-20261027T190219960924Z-ede9b007.json](12-3-tablet-browser-20261027T190219960924Z-ede9b007.json) |
| Dedicated tablet browser18481 compatibility | 5/5 | [12-3-tablet-browser-20261027T190237489569Z-9d3c7b69.json](12-3-tablet-browser-20261027T190237489569Z-9d3c7b69.json) |
| Backend transport | 14/14 | [12-3-backend-transport-20261027T190254406174Z-c878589c.json](12-3-backend-transport-20261027T190254406174Z-c878589c.json) |
| Complete12.3 matrix, negative probes and cross-tab clear | 34/34 | [12-3-browser-20261027T190258982753Z-1bffeae3.json](12-3-browser-20261027T190258982753Z-1bffeae3.json) |
| Selected private regression suites | 86/86 | [12-3-browser-20261027T191324534402Z-c1c3772d.json](12-3-browser-20261027T191324534402Z-c1c3772d.json) |
| Actual private gateway image build | passed | [12-3-gateway-build-20261027T190111954909Z-8022f7a7.json](12-3-gateway-build-20261027T190111954909Z-8022f7a7.json) |
| Access gate with current mounted source | 13/13 | [12-3-gate-check-20261027T190143642963Z-7ec999a8.json](12-3-gate-check-20261027T190143642963Z-7ec999a8.json) |
| Tablet Compose configuration, no services started | passed | [12-3-gateway-config-20261027T190148035587Z-a044943a.json](12-3-gateway-config-20261027T190148035587Z-a044943a.json) |
| Gateway/proxy negative and admitted requests | 120 rejected plus valid/fail-closed checks | [12-3-gateway-proxy-20261027T190151212433Z-bdf41816.json](12-3-gateway-proxy-20261027T190151212433Z-bdf41816.json) |
| Additive manual fixture preparation | 17/17 | [12-3-prepare-20261027T192251010882Z-adfce32f.json](12-3-prepare-20261027T192251010882Z-adfce32f.json) |

All final browser manifests have zero skipped, unexpected or flaky cases, unchanged source/executed inputs, correct built assets and matching allowlisted API settings. The34-case matrix took616.056s. Python tooling7/7 passed, including expected real failed-command and timeout/parent-exit probes; Node generator/configuration2/2 passed. Logs: [Python](12-3-main-sync-tooling.txt), [Node](12-3-main-sync-node.txt). Known warnings are the installed Node experimental type-stripper, Playwright color settings and backend TestClient deprecation; no gate failed on them.

Fresh positive-product measurements:312 states,25,112 text observations (minimum6.126:1),6,584 control boundaries (minimum4.781:1),5,912 keyboard observations and5,632 unfocused signatures. There are1,940 actual before/after pixel pairs and3,692 explicitly identified representative cache results; minimum changed/required focus area1.291.80 distinct native checkbox states include40 checked glyph samples. No unsupported product layers or critical clipping were recorded. These are Edge156 at800/1440px and16/32px root text, not physical/OS-zoom/assistive-technology passes. See [fresh measurement summary and hashed provenance](12-3-main-sync-measurement-summary.json); old measurement JSON remains unchanged.

The accepted-main semantic review covered relative-API priority, HTTPS/logout/clock contracts, private-only gateway packaging, and the accepted save/repeated-event/readonly/conflict/recovery/activity feedback changes, even where Git did not conflict. Actual API/gateway sources remain byte-identical to accepted main. Four textual conflicts (assessment, scoped CSS, sprint status and issues) were integrated preserving both sides. The dedicated tablet provider and test selector/configuration adaptations were necessary; taking either entire assessment file would discard one side's behavior. Other incoming changes are primarily accepted-status, pilot/test documentation and session history. Current tracking now also closes the already delivered remote-access setup, while ordinary deployment remains separate.

Three review layers and their reinspection retained no newly introduced issue. Fixed B1–B4 and E1/V1; B5 rejected with specific counterevidence. Five inherited transport follow-ups (preparation team/email validation alignment, serial JWKS lookup, unknown-key refresh bounds and outer-cookie minimization) are recorded separately in [triage](../../_bmad-output/implementation-artifacts/spec-12-3-current-main-sync.md) and [deferred work](../../_bmad-output/implementation-artifacts/deferred-work.md). They are unchanged from accepted main and do not revoke12.1/12.2 acceptance. No demonstrated authentication bypass, credential disclosure or external denial-of-service claim is made.

Earlier same-session checks at1197 passed build/API74/demo37/tablet4/backend14; the34-case attempt was deliberately interrupted before review corrections and remains exit1 (`12-3-browser-20261027T185055155765Z-2e19f0f8.json`). The implementation agent's first restricted preview startup also remains exit1 (`12-3-tablet-browser-20261027T185700217739Z-6588456d.json`), with verified owned children cleaned before the successful escalated suite. Root's first auxiliary gate command mounted source at/app while the image works in/gate: no tests found, exit4 (`12-3-gate-check-20261027T190117937529Z-62cd0d24.json`). The corrected actual command mounted/gate and passed13/13. All raw failed/interrupted records and snapshots remain; none is relabelled a pass. Historical477/479 and later successful affected12.1/12.2 checks remain historical. No new complete broad browser/backend run is claimed.

Own runtime was updated by `up` at1197; subsequent patches affect only verification tooling/tests. Final mounted backend-byte and served-asset audits independently qualify the running source. Additive prepare retains existing manual edits/plans and provides synthetic line20 plans2/3January2031. The owned preview serves this version on15323. Password remains only in ignored `.private-runtime/story123-manual-credentials.json`. Use [Jonas' updated checklist](../story-12-3-manual-testing.md).12.1/12.2 are accepted;12.3 stays review/in-review pending explicit manual acceptance and12.4 stays backlog.


### Final runtime and artifact audit

[Final runtime](12-3-main-sync-runtime.json):61/61 checks passed. All22 non-story containers retain exact ID/image/start/restart/labels; all seven captured15312 HTTP hashes are identical. Main remains clean74849ff, is an ancestor of this story, and backend/deploy/transport files equal accepted main. Both running API mounts match every tracked backend file. The standard/dedicated assets, source identity and effective API settings match their build records. All transient test previews/probe containers are gone; owned preview PID54432 serves current assets on15323. There is no pre-run database-byte fingerprint, so byte equality of old database contents is not claimed.

The first audit was60/61 because its expected gateway file set incorrectly excluded the inherited Nginx50x.html. Preserve [initial raw result](12-3-main-sync-runtime-initial.json) and [initial method](12-3-main-sync-runtime-method-initial.py). The extra file's SHA256 is876766b4e80133fd490603e073d3567425b88794828a9292104244c9e40875ed, independently checked against the exact pinned nginx1.28-alpine base digest. The [final method](12-3-main-sync-runtime-method.py) permits exactly the three qualified private app files plus that unchanged base error page. No product change or lowered contrast/focus threshold was involved. Initial and final source methods and before snapshots are retained.

Artifact verification is recorded in `12-3-main-sync-artifact-audit.json`: new JSON/archive readability and hashes, preserved historical12.3 raw bytes, local document links, whitespace and scoped secret scan against only the own synthetic manual/database passwords. No tunnel-token contents were read. Technical qualification is complete; manual12.3 acceptance remains pending.
