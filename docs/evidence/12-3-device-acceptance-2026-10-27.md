# Story 12.3 — final Lenovo checks and conditional owner acceptance

> Main integration,27October2026: accepted12.3 was merged without conflicts; the entire committed merge tree equals the accepted story tree. [Final checks and publication record](12-3-publication-final.md) supersede earlier no-merge/no-push checkpoint statements.12.4 remains backlog.


> Publication follow-up,27 October2026: Jonas has now explicitly authorized committing/pushing the completed documentation and evidence, then merging12.3 into main after identity/final checks and pushing main. Earlier no-commit/no-push/no-merge statements describe the previous checkpoint.12.4 remains backlog.


**Outcome: done / accepted, 27 October 2026.** Jonas explicitly approved readability and touch/target comfort on Lenovo/Brave, based on observing and personally trying the application during and immediately after testing. His latest message grants overall acceptance once the remaining required checks pass, no unresolved defect prevents acceptance and no further manual assessment is needed. The checks below fulfil those conditions. No additional owner action is required for Story12.3.

The same message ends **“Ikke Commit eller push.”** This later restriction governs: documentation/evidence/log changes remain uncommitted; no push or story-to-main merge was performed. Product code stayed stable. Story12.4 was not started. Acceptance of this story does not deploy it or accept the complete12.4 flow.

## Exact basis and methods

- Worktree `D:/IBE160/tmp/story-12-3`, branch `story/12-3-tablet-pc-accessibility`, HEAD before/after testing `e87049b9541e6881c4af71f02fdeb8acdf6e7537`.
- Product/tool source remains `8ca318b55b98eb34de54f29ecab038322e3ccab6`; subsequent commits concern evidence/logging. All41 source and6 build hashes match `.private-runtime/story123-build.json`, SHA256 `b57c1053a88b4d66467e7296c5f53663e9f7e309b375a5f72f88193d6ce04ea6`.
- Local and origin main both remain `74849ff21bee108fe9cff93d740a96a6c6d2d7c5`, clean locally and an ancestor of the tested branch. This includes remote access and accepted12.1/12.2. Main itself has not acquired12.3; a later merge must recheck these identities before relying on this qualification.
- Physical Lenovo TB361FU / serial HA2BN9HR / Android16 / Brave1.97.59 / Chromium155.0.8059.85. Reduced web UA's Android10 is not the actual OS version. Actual portrait viewport800×1085 CSS pixels, DPR2; no device-metric emulation.
- Existing Brave target `98DC3098B039D88F7BC83957BBD8AC4C`, frontend15323, private API18324, fictional API18323, Compose `ibe160-story123-tests`. Existing USB reverse links and DevTools forward50894 retained. The first action was a small real-device login/observed-workspace smoke before the remaining journeys.
- DOM fill supplied credentials; DOM `selectOption` selected classification/status. CDP injected touch operated buttons/acknowledgements in the real Brave tab. CDP keyboard events exercised focus/navigation; PNGs captured actual browser pixels. These are automated device actions, not human finger actions. Jonas' earlier finger/physical-rotation confirmations and latest subjective assessment are separate human evidence.
- Credentialed fetch **from the device** added only synthetic drafts/plans for5/6January2031, using the current local synthetic account. Existing2/3January manual fixtures were never advanced, overwritten or reset. Their four list rows retain exact metadata; no full pre-run database-byte snapshot is claimed. New5January plan ended with one completed/one unregistered activity;6January plan aborted with both unregistered. These added fixtures remain inspectable after login until their retention deadlines. No credentials or CSRF/cookie values are included here.

## New executed results

| Check | Actual result |
|---|---|
| Private long Norwegian draft, Day/Night | Readable wrapped text, actual text/boundary/layout assertions passed. |
| Private review and decisions | Confirmation initially disabled; required unknown-type classification and acknowledgement controls visible. Explicit manual classification and checked acknowledgements enabled confirmation. Actual server confirmation opened the day without starting work. Both themes measured. |
| Private acknowledgement indicators | Non-empty census: four checked/unchecked samples across both themes; minimum edge11.085:1; two actual checked glyphs detected. |
| Start confirmation | Both themes measured; actual focus pixel pairs passed; cancel returned focus to Start and retained not-started. Explicit confirmation produced actual server start receipt. |
| Manual activity | Selection did not complete work. Explicit completed choice plus Save changed only activity1; server receipt observed. Remaining activity stayed unregistered. |
| End confirmation | Actual counts/remainder disclosed in both themes; cancellation returned focus. Explicit confirmation ended the synthetic plan. |
| Private terminal recap | Both themes passed. Actual planned times remain separate from server start/end; unknown bus, one completed and one unregistered remain explicit. Exact visible text survived reload/reopening. Independent server recap verifies outcomes, manual classification, ended state and seven-day deadline from actual ending. |
| Terminal read-only behavior | Day/selected activity expose no Start/end/status editor; recap contains no status combobox. No inferred physical driving/completion. |
| Aborted variant | Separate actual private plan; cancellation/review in both themes, then explicit abort. Server state aborted; both outcomes remain unregistered. Day/Night recap measured. |
| Native date/time/select/disclosure glyphs |14 qualified actual pixel crops, both themes; closed/open disclosure in historical-details and closure surfaces. Minimum representative glyph/background6.415:1. Core colors selected by frequency/channel difference without using the passing contrast threshold; glyph identity visually inspected in the isolated crop. This closes the earlier unmeasured application-affordance gap. It is not a numeric audit of every Android system-picker pixel. |
| Keyboard/focus | Four Start/end confirmation pixel pairs and two complete private-recap keyboard censuses:20 observations,18 additional pixel pairs. Minimum changed/required perimeter area1.555; minimum census adjacent contrast11.450:1; all reachable census controls visited, visible and unobscured. The viewport adapter only supplied the actual800×1085 clipping bounds; it never changed layout. |
| Logout/privacy | Actual logout, reload and cross-entry navigation retain Night. Private UI hidden; localStorage exactly the allowlisted theme, empty sessionStorage/IndexedDB/CacheStorage, zero Service Workers. Own tab restored to logged-out Night demo. |

Fresh rendering totals: **16 states,1,960 text observations (minimum6.126:1),484 boundaries (minimum4.781:1), zero critical clipping, zero horizontal page overflow and zero unsupported product layers.** These are this follow-up's totals, not a new broad PC run.

The [qualified summary](12-3-device-final-20261027T205355Z/qualified-summary.json) contains the exact counts and exclusions. The prior [physical report](12-3-device-testing-2026-10-27.md) retains its57 attempts/39 passes/18 adapter failures, actual native pickers/IME, actual2× pinch/scroll, rotation, feedback/conflict/recovery, theme lifecycle and human finger/rotation evidence. Those results have not been rewritten as fresh successes. The [accepted-main qualification](12-3-main-sync-handoff.md#root-final-qualification) retains the executed34/34 story matrix,86/86 selected private regressions,37/37 demo/fictional checks,74/74 API/PostgreSQL and build/transport/gateway/runtime results. Its312 measured states include PC16/32px text and800/1440px layouts. None of those suites was rerun here because product bytes remained unchanged. Historical12.1/12.2 **477/479** remains historical, followed by the separately documented successful affected checks.

## Failures, corrections and raw provenance

The new grouped log contains **19 attempts:17 pass,2 preserved adapter failures**. It is not19/19. One further initial glyph probe failed outside the grouped log. No product defect was established; no product fix was applied.

1. `icons.cjs` expected a select in the draft editor, where none exists. Its original timeout remains in `icons-error.txt`. Real select glyphs were measured in private review instead.
2. The first reload comparison incorrectly parsed a plain UTF-8 `innerText` export as JSON. The original error remains. Reopening itself had succeeded.
3. The next comparison mixed `innerText` and `textContent` whitespace. Comparing actual `innerText` with the saved `innerText` passed, followed by independent server-state/outcome/deadline assertions. The original mismatch remains.
4. Initial closure marker crops included the border and clipped the glyph. Their `closure-*-disclosure-pixels.json` files are explicitly **excluded**. Corrected regions use actual computed padding/borders/first-line coordinates; all eight `verified-details-*`/`verified-closure-*` marker crops were visually inspected, then independently asserted at >=3:1. No border was counted as glyph evidence.

202 raw files are retained in the2,216,800-byte archive (SHA256 `7e041bbb737ed665aa1b76ea58006820eeac0168c2d7d5ca17b5eabe2c8ae75c`). The [final artifact audit](12-3-device-final-artifact-audit.json) verifies every archive/disk entry, all137 earlier raw files and archive unchanged,30 local document links, the scoped password scan and unchanged source/build/main/index state.

Executed probes are preserved under [raw evidence](12-3-device-final-20261027T205355Z/), with [archive](12-3-device-final-20261027T205355Z.tar.gz) and [SHA256 index](12-3-device-final-20261027T205355Z.index.json). Scripts are phase snapshots resuming observed device states, not an unattended suite. For reproduction restore the original `tmp/story123-completion` directory depth, installed dependencies, credentials, exact target and fixtures; reverify ownership/build before input. Never run existing destructive test setup against the manual account. Two text exports (`private-recap-text.json`, `review-decided-text.json`) are plain UTF-8 despite their original suffix; preserve their bytes and read as text. Node reports its installed experimental type-stripping warning.

## Requirement assessment and remaining limits

| Governing requirement | Acceptance assessment |
|---|---|
| AC1 / AC-10 / NFR1 / IR-01: included foreground/background/necessary icons/focus, themes, keyboard, long text, enlargement, disabled boundaries, layouts and non-private preference | Satisfied by unchanged-current-main PC matrix plus earlier actual-device controls/2× pinch/rotation/lifecycle and this private review/recap/native-glyph/focus follow-up. Jonas explicitly approves personal readability and touch comfort. Disabled-state necessary information/boundaries are in the matrix; actual real-device review initially blocked confirmation. CSS32px text is PC enlargement evidence; actual earlier device pinch is browser zoom evidence. They are not interchangeable. |
| AC2: current contracts, owner/private/demo/manual/unknown distinctions; no deferred prerequisites | Satisfied within12.3. Actual private server confirmation/start/manual status/end/abort/recap demonstrate the distinctions; unknown remainder stays unknown. Existing owner/session/privacy regressions remain applicable to identical code. No Auto/wake/GPS/audio/offline/PDF qualification or12.4 acceptance inferred. |
| AC3: meaningful executed evidence/failures/limits | Satisfied by raw attempts, original errors, qualified/excluded measurements, observed device/browser/build and historical/new separation. |

**Not tested:** TalkBack/other assistive technology, hardware keyboard, OS magnifier and Brave text-size setting. Current NFR1 requires keyboard operation, enlargement and actual tablet/PC observations, not qualification of every such technology; actual keyboard events, PC text enlargement, real-device pinch and Jonas' physical assessment supply those requirements. These technologies remain unclaimed compatibility coverage, not silently passed tests or new acceptance prerequisites. No overall WCAG conformance is claimed.

**Separate deployment/security work:** this build's ordinary HTTPS/Cloudflare/mobile-network route is unqualified here. The older pilot is not12.3. Existing deployment/drift/operations follow-ups and inherited main B6–B10 remain open under their existing records; this slice changes none of that code, and no demonstrated bypass/leak/external denial of service is asserted. They do not invalidate the included-view acceptance or reopen accepted12.1/12.2. Full PDF-through-closure/system qualification remains12.4, which is still backlog.

Final [postflight](12-3-device-final-20261027T205355Z/postflight.json): all26 containers have unchanged ID/image/start/restart/labels; seven accepted15312 HTTP hashes match; three other Brave tabs retain exact ID/title/URL and received no control actions. Original remote access is preserved. Source/build identity, main identity/ancestry and clean main worktree passed. Rotation remains free/auto enabled; no OS setting was changed by this follow-up. No further mandatory physical action or subjective judgement is outstanding for12.3.

## Owner decision recorded

Jonas' latest message in this chat,27October2026, is the decision source: subjective readability/touch comfort approved; overall acceptance conditional on satisfactory remaining required checks and no unresolved acceptance-blocking defect. Those conditions are now satisfied by the evidence above. **Register12.3 as done/accepted**; keep12.1/12.2 accepted and12.4 backlog. The final no-commit/no-push restriction leaves this documentation and logging as local working-copy changes. No merge or publication is included.

The [manual checklist](../story-12-3-manual-testing.md) now records this result. Its reusable steps remain available for later reproduction; Jonas need not repeat already completed checks.
