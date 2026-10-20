# Development log

## 2026-09-21 – Project setup

### Work completed

- Cloned the assigned GitHub repository.
- Configured Git identity and verified the remote repository.
- Installed BMAD v6.12.0 according to Appendix B.
- Installed BMAD Core and BMad Method (BMM).
- Configured 29 BMAD skills for OpenAI Codex.
- Verified that the installation did not modify the existing README or `.gitignore`.
- Committed and pushed the setup to the `main` branch.

### AI use

OpenAI Codex was used to inspect Appendix B, run the BMAD installer, and verify the resulting files and Git status. All commands requiring changes were approved by the student.

### Verification

- BMAD installation completed without errors.
- Local branch was synchronized with `origin/main`.
- Working tree was clean after push.
- Setup commit: `23d620d`.

## 2026-09-21 – Product Brief

### Work completed

- Completed the BMAD Product Brief workflow for the bus-driver assistant.
- Defined the problem, users, MVP scope, success criteria, risks and broader vision.
- Separated the concise Product Brief from supporting evidence in an addendum.
- Sanitized supporting documentation before publication in the public repository.

### AI use

OpenAI Codex and the BMAD Product Brief workflow were used to facilitate structured discovery, inspect supplied course material and shift-report samples, draft the documents and perform editorial and privacy checks. Product decisions and scope priorities were approved by the student.

### Verification

- `brief.md` and `product-brief.md` were verified as identical.
- No code, PRD or architecture was created.
- Local paths and private operational identifiers were removed before publication.

## 2026-09-21 – Product Requirements Document

### Work completed

- Completed the guided BMAD Create PRD workflow for the bus-driver assistant.
- Defined and approved 25 functional requirements and four non-functional requirement groups.
- Clarified the course MVP, deferred capabilities and downstream technical validation.
- Reconciled the PRD with the Product Brief, source research and recorded decisions.
- Completed consistency, editorial and privacy reviews.
- Approved the PRD as final.

### AI use

OpenAI Codex with GPT-6 Astra and the BMAD PRD workflow facilitated requirements discovery, source research, drafting, adversarial review, reconciliation and privacy checks. Product decisions were reviewed and approved by the student.

### Time spent

Approximately 4.5 hours on guided PRD development and finalization.

## 2026-09-22 – UX design and validation

### Work completed

- Completed and approved the BMAD UX workflow using all five source documents, with the PRD and its addendum taking precedence over the briefs.
- Finalized English `DESIGN.md` and `EXPERIENCE.md`, five approved HTML references including a navigable 43-screen gallery, consolidated HTML/Markdown validation reports, reviewer reports, source reconciliation and decision history.
- Established landscape tablet layouts in Day A/Night C, vertical upcoming-first stops, current/next-stop emphasis, a persistent clock, relevant disruption headings and explicit data uncertainty.
- Confirmed PDF/image import, split working days with one summary, partial shift updates, persistent manual theme selection and an underlined active Auto control. Menu restrictions and the five-minute GPS-loss countdown remain explicit.
- Defined separate FADDER/INSTRUKTØR assignments, own driving and accompanied plans, explicit driver takeover, and accompanied-only summary/PDF evidence. Accompanied-person source files are deleted after import; necessary interpreted information remains in the mentor's working day.

### AI use

OpenAI Codex and the BMAD UX workflow supported iterative sketches, document drafting, source reconciliation and three user-selected validation lenses: document consistency/coverage, driver-position readability/interaction, and operational edge cases/role changes/data trust. The student reviewed the sketches, made product decisions and approved the completed UX and validation.

### Verification

- All 11 distinct validation findings were addressed; original reviewer reports and resolution records are preserved.
- Static checks verified token references, local/source links, paired component names and sketch navigation. Browser inspection checked clock placement and the active Auto underline.
- Mounted-device readability, touch, browser/sensor support and implemented behavior still require practical verification.
- Temporary browser profiles/caches, preview images and one-off working files are excluded from Git. Final documents, approved sketches, validation/reviewer reports, source tracing and the UX memlog are retained.
- No architecture or application implementation was started.

## 2026-09-23 – Step 4: Architecture completed

### Work completed

- Finalized the [Architecture Spine](../_bmad-output/planning-artifacts/architecture/architecture-IBE160-2026-09-23/ARCHITECTURE-SPINE.md) using the approved Product Brief, PRD and UX as authoritative inputs.
- The student approved architecture decisions AD-1–AD-14 through the interactive BMAD Architecture workflow.
- Defined the V1 boundaries, modular monolith, React/TypeScript client, Python/FastAPI backend, PostgreSQL, six conceptual contracts and local operational authority with offline synchronization.
- Recorded import, source uncertainty, notice lifecycle, access, writer transfer, retention and compatible-release rules, together with portable Docker Compose delivery on the Windows desktop, Cloudflare access and an isolated fictional demo.
- Retained the decision log, source reconciliation and independent review reports with the finalized architecture.

### AI use

OpenAI Codex and the BMAD Architecture workflow supported interactive decisions, official-source research, document drafting, source reconciliation and independent architecture reviews. The student approved the architecture decisions and their constraints.

### Verification and remaining pilot prerequisites

- Reconciled the architecture with Product Brief, PRD, DESIGN and EXPERIENCE. Addressed the independent reviewers' findings; the final document lint reported zero findings.
- Architecture approval does not establish pilot readiness. OCR on representative anonymized files, actual Entur/Svipper-origin coverage and relevance, Lenovo/Brave GPS and interaction behavior, offline recovery, synchronization/conflicts, deletion and release compatibility still require implementation tests.
- Cloudflare Access renewal/expiry, trusted HTTPS over mobile networks, private/demo isolation, Windows restart recovery and acceptable desktop resource use/noise must also be tested before real-shift pilot use.
- No application implementation, external service provisioning or deployment was performed in this step.

### Next step

**Step 5: Epics & Stories**, based on the approved Product Brief, PRD, UX and Architecture Spine. Step 4 is complete. Neither BMAD Spec nor Epics & Stories is started in this session.

## 2026-09-23 – Step 5: Requirements and formal epics approved

- Used approved Brief, PRD, UX and AD-1–AD-14 to extract 25 FRs, four NFR groups and 44 in-scope UX requirements plus a deferred-scope marker into [epics.md](../_bmad-output/planning-artifacts/epics.md). Recorded supersessions, responsibility boundaries, dependencies and early source/OCR/device qualification.
- The owner approved workflow steps 1 and 2: eight formal epics, each responsible for its own access, persistence, error handling and privacy. E8-D (demonstrable delivery), E8-P (pre-pilot permission) and E8-E (field evaluation) remain separate.
- Corrected capacity assumptions: more than 40 hours is guaranteed, but no reliable remaining budget or delivery date exists. Neither 40 nor 160 hours is an available fixed budget; deferring a requirement needs a separate decision.
- Stopped before stories at the owner's request. The owner requested saving and GitHub publication for this session; that request is historical, not evidence that later local work is published.

## 2026-09-25 – E1–E3 story planning

| Epic | Approved stories | Main decisions and traceable details |
|---|---|---|
| E1 Private access and drafts | 1.1–1.4 (4) | Immediate private lock even with missing logout response; persistent pending revocation and fail-closed recovery; fixed AD-12 expiry; only a matching immutable-batch receipt establishes server confirmation. |
| E2 Prepare and revise a day | 2.1–2.12 (12) | Representative OCR/source investigations; Tide service date/extended hours versus calendar display time; explicit reviewed-revision confirmation; transient PDF/image originals, preserved corrections and partial coverage; combined-day split work/additions and scoped stale revision proposals. |
| E3 Actual trip and interaction | 3.1–3.15 (15) | Qualified separate position/speed, visible startup/five-minute exceptions, no network-only GPS fallback; independent passage/departure reference for 100 m; manual provenance, repeated-stop identity and visible gaps; distinct return start, uncertain physical outcomes, bus-change times, persistent manual theme and measured wake support. |

- Reviewed each story interactively and retained the owner's clarifications in its acceptance criteria and approval record. E3 coverage approval included focus/closure tests in 3.2 and meaningful announcement tests in 3.5.
- Recovered after a tool interruption by inspecting actual files: 3.5 approval was missing and 3.6 had not been saved. Recreated the agreed 3.6, registered both approvals once and verified canonical copies before continuing. This was a documentation repair, not tested application recovery.
- Closed E3 planning and paused before E4 at the owner's request. The owner requested commit/push for this checkpoint; Git outcomes are separate from approval and do not establish publication of subsequent work.

## 2026-09-26 – E4–E7 story planning

| Epic | Approved stories | Main decisions and traceable details |
|---|---|---|
| E4 Source-backed notices | 4.1–4.8 (8) | Actual source coverage versus metadata/fetch failure; evidence-based identity/version/closure and repeated-stop relevance; seen only after actual exact-version display; visible additional notices; acknowledgement changes only driver state; one eligible new-notice chime, no old-audio replay. |
| E5 Offline continuity | 5.1–5.13 (13) | Concrete active-day grant, coherent assets/reopen, independent Access/app/source/receipt states; explicit conflicts and planned/emergency transfer; preserved former-device work; retained-client compatibility; accepted update versus staging; terminal settlement/fences and all-copy expiry. **5.4 timing proof remains open.** |
| E6 Mentor roles and contexts | 6.1–6.10 (10) | Mentor confirms their copy, not the other person's confirmation; revision-specific links, separate A–B–A periods and activity contexts; immediate driver restrictions despite failed storage; manual takeover; active revision preserved; unknown actual role after recovery stays restricted. |
| E7 Closing and summary | 7.1–7.6 (6) | Explicit terminal ending and first-review completion, interrupted review continuation; honest summary and revision-bound local PDF; day-scoped retained access/expiry; factual varied greeting without permanent history. **7.1 unverified end time cannot extend the earliest binding deadline.** |

- The owner approved each story and the E4–E7 coverage summaries, retaining V1 and AD-1–AD-14. E8 was opened with a separate unapproved first draft; no operational gate was passed.
- Detailed clarification wording and test cases remain in [canonical epics and stories](../_bmad-output/planning-artifacts/epics.md) and [individual story files](../_bmad-output/planning-artifacts/story-drafts/).

## 2026-09-27 – E8 story planning and epic approval

| Stories | Approved responsibility |
|---|---|
| 8.1–8.2 | Isolated fictional PC demo, shared rules, independent failure scenarios and reset without old-run effects. |
| 8.3 | Actual client/FastAPI/PostgreSQL lifecycle evidence, separate from static demo and source/device qualification. |
| 8.4–8.5 | Portable protected runtime, Windows restart downtime, verified Access and provider handling before real files. |
| 8.6 | Assessable delivery/evidence/AI-reflection package and separate E8-D decision record. |
| 8.7–8.8 | Actual representative import/source and mounted Lenovo/Brave qualification; independent 100-m reference and honest measured/synthetic/untested distinctions. |
| 8.9–8.10 | Real-duration whole-day continuity, access/transfer/settlement/expiry, measured host downtime/resources/noise and a concrete old/new release preserving active/pending work. |
| 8.11 | Later dated owner E8-P decision requiring mandatory passes and resolved blockers, including 5.4/7.1. Story approval is not pilot permission. |
| 8.12 | Protocol agreed before first shift, three actual assigned days after positive E8-P, negative/interrupted days retained, planned/unobserved/measured behavior separated and independent E8-E outcome. |

- The owner approved all twelve E8 stories individually, then approved the coverage summary and closed E8 on the planning level. Totals: E1 4, E2 12, E3 15, E4 8, E5 13, E6 10, E7 6, E8 12 = **80 story plans across eight approved epics**.
- Coverage review found no missing E8 responsibility or need for a thirteenth story; declared dependencies exist and point backward. Controlled demo/fullstack, actual environment qualification and gate decisions retain different evidentiary roles. Early investigations are not deferred until E8.
- Dense qualification can require several observation sessions; the three-day trial is inherently multi-day. Story count is not a capacity estimate. No requirements or architecture choices were removed.

### Open risks and next step

- **OPEN — timing basis in [5.4](../_bmad-output/planning-artifacts/story-drafts/story-5.4.md) / [7.1](../_bmad-output/planning-artifacts/story-drafts/story-7.1.md):** a client timestamp alone cannot justify delayed server acceptance of offline activation after login expiry. An unverifiable end time cannot extend access/retention; enforce the earliest applicable limit. A separate solution decision plus necessary implementation/retest evidence is required before positive E8-P. Planning approval does not resolve this.
- Actual source/OCR coverage, mounted sensing/100-m/usability/Auto/wake/audio, full-day recovery, unknown-role restrictions, provider handling, host/noise and compatible releases remain unexecuted qualification obligations. Negative findings need explicit solutions, not silent scope reduction.
- Assessment dates/browser, evaluation protocol/scheduling, capacity and delivery time remain unresolved. Existing accepted limits (Windows sign-in before Docker, possible permanent loss without historical private backups) do not waive qualification.
- **Next substantive work: project step 6 / readiness control in a separate new chat.** Story creation, epic planning and internal step-5 final document validation are complete; readiness has not started or passed. E8-D, E8-P and E8-E are not execution approvals. Actual shifts still require the later positive dated E8-P decision.

### AI use, verification and log maintenance

OpenAI Codex used the BMAD Create Epics and Stories workflow to read actual planning documents, draft one story at a time, incorporate owner decisions and maintain traceability/coverage. The owner reviewed all 80 stories and epic boundaries; AI output did not substitute for approval or practical evidence.

At the owner's request on 2026-09-27, condensed repetitive story-by-story progress entries into the dated summaries above. The canonical story bodies, individual approval records and epic coverage/decision records remain in epics.md and all 80 story files. Earlier setup/Brief/PRD/UX/architecture log entries are preserved.

Document checks verified unique canonical story counts, saved approvals, dependency identifiers, resume state and whitespace. These are document checks, not application, sensor, source, database or pilot tests. No application implementation, actual qualification/field data collection, provisioning, deployment or BMAD Spec occurred in this planning stage. The condensation/approval update was initially saved locally; the subsequent authorized publication checkpoint is recorded below.

## 2026-09-27 – Step 5 closed; publication checkpoint

- At the owner's request, completed the internal epics/stories final document checks; [validation record](../_bmad-output/planning-artifacts/epics-final-validation.md) maps FR-1–25, UX/quality coverage, architecture, scope and dependency checks. All eight epics and 80 stories remain approved plans; no acceptance criteria were changed.
- The generic setup-only first-story instruction yields to the approved first vertical slice: 1.1 includes repeatable setup and private access. E1's equivalent scope headings are present; multi-session qualification is not falsely treated as a one-session coding promise. Adopted architecture and V1 scope are preserved.
- Checked canonical/individual acceptance text, counts, approvals, saved state, references and Git diff scope. Reviewed changed/new Markdown for accidental edits, credential/private-key/token patterns and operational identifiers; publication contains planning documents and the log, not application data or credentials. These are document checks, not executed product tests.
- The owner authorized committing and pushing these documents to the current branch. Publication outcome and commit hash are reported separately after Git verification; this record does not preclaim push success.
- Exact continuation: project step 6 in a separate chat using bmad-sprint-planning for readiness, with epics.md, the final-validation record, approved PRD/UX/Architecture Spine and this log. The completion hook is empty; no automatic next workflow was run. **5.4/7.1 remains OPEN.** No readiness, implementation, E8-D acceptance, actual pilot permission, provisioning or deployment occurred.

## 2026-09-27 – BMAD steps 1–6 closed: implementation readiness

- Completed the BMAD step-6 [implementation readiness check](../_bmad-output/planning-artifacts/implementation-readiness.md) against the approved PRD, UX, Architecture Spine and eight epics/80 stories. Checked artifact inventory, forward/backward traceability, story dependencies and bounded completion, architecture/UX decisions, inter-artifact conflicts and practical implementability/evidence. The planning gate is **PASS with status «betinget implementeringsklar»**: bounded implementation and early investigations can start in declared dependency order. This is not a pilot or release approval.
- **TIME-01 — product-owner decision adopted:** First durable server acceptance of a day activation must occur strictly before the fixed 14-day sign-in deadline E. Original server-issued Tg conservatively bounds retention after an unverifiable offline ending. Offline restart with uncertain time keeps the local copy locked until trusted control, deleting expired data before display. Approved, unknown and rejected local results have distinct access/export behavior. The pilot requires device custody, reconnect/hand-in, supervised wipe and incident response for a missing device. [PRD](../_bmad-output/planning-artifacts/prds/prd-IBE160-2026-09-21/prd.md), UX, architecture AD-10/12, relevant stories and the [change proposal](../_bmad-output/planning-artifacts/sprint-change-proposal-2026-09-27.md) record the supersession of older 5.4/7.1 wording. Implementation and tests remain open.
- **IR-01 — product-owner decision adopted:** V1 project acceptance requires at least 4.5:1 for all informative text, 3:1 for necessary non-text information, and the specified keyboard-focus area and 3:1 contrast checks across Day, Night, both Auto outcomes and relevant states. Color alone cannot convey state. The yellow sun's bare fill is calculated at 1.59:1 against white; the accepted static SVG has a dark outline/under-stroke, but implemented rendering needs measurement. Rendered PDF needs separate page-level contrast checks. These are project criteria, not a claim of overall WCAG AAA conformance. The [UX validation record](../_bmad-output/planning-artifacts/ux-designs/ux-IBE160-2026-09-22/validation-report.md) corrects its earlier R2 completion claim. Decision closed; measurements open.
- **Open implementation and later gates:** Execute TIME-01 activation/expiry/recovery/deletion tests and IR-01 rendered UI, semantic-icon, focus and PDF measurements. Representative anonymized import cases, actual Entur/Svipper coverage, mounted Lenovo/Brave sensing/readability/Auto/wake/audio, whole-day recovery, provider/access/host handling and release compatibility need actual evidence. E8-D demonstrable delivery, E8-P pre-pilot permission and E8-E three-day field evaluation remain separate and unpassed. No planned test is counted as passed; actual shifts require a later dated positive E8-P decision. Assessment dates/browser, field protocol and reliable capacity/delivery estimate are still unresolved.
- **Next BMAD workflow:** Run `bmad-sprint-planning` with **sprint-planning** intent to recheck the planning gate and generate the implementation tracking file (`sprint-status.yaml`) from canonical `epics.md`. This readiness-only step did not generate sprint tracking or start implementation. The first bounded implementation slice remains Story 1.1, alongside independent early investigations 2.1, 2.2, 3.1 and 4.1.

## 2026-10-19 – Correct-course proposal following instructor feedback

- Jonas requested `bmad-correct-course` after reading the instructor's 6 October feedback and selected one consolidated proposal. He estimates 60–80 remaining work hours, including a holiday week potentially allowing about 40 hours. The submission is expected in December; the exact date remains unconfirmed.
- Created [SCOPE-02: minimal assessable V1](../_bmad-output/planning-artifacts/sprint-change-proposal-2026-10-19.md), covering brief, PRD, architecture, UX, all eight old epics and all 80 stories. The proposed replacement has four epics and 20 bounded stories: supported text-PDF import with correction, saved day overview, manual navigation, manually maintained source-linked notices and a local fullstack demo. Offline execution, automatic source/GPS behavior, mentor roles, advanced revisions, PDF export and operational field evaluation move to later scope only if the owner approves.
- The proposal explicitly identifies changes to earlier owner decisions, especially mandatory automatic notices and TIME-01's offline mechanisms. Speed limits were already optional downstream; aligning the older brief does not remove a current backlog story. The September readiness PASS is not a pass for the proposed replacement plan.
- Verified that all 80 old story IDs are mapped exactly once, all 20 new story dependencies exist and point backward, and proposal links resolve. These are document checks; no application implementation, extraction test, integration qualification or field trial occurred.
- **Pending:** explicit owner approval of the concrete proposal. Current approved planning sources remain unchanged. After adoption, synchronize the source documents and active backlog, check readiness, generate tracking, and start the timeboxed PDF investigation and first persisted fictional fullstack slice. No old requirement is silently deferred, no agent handoff has been executed, and no pilot use is authorized by this proposal.

### Owner adoption and coordinated handoff — 2026-10-19

- Jonas explicitly approved the complete SCOPE-02 proposal after the batch review. This resolves the pending approval above and adopts S02-A–G, including manual notices/navigation, online-only saved state and deferral of the previously mandatory automatic/offline/mentor/reporting scope. The change is classified as a major replan.
- Applied the decision to both identical brief copies, PRD, Architecture Spine, DESIGN, EXPERIENCE and canonical epics. Nine original primary documents were copied byte-for-byte and hash-checked before replacement; the [historical index](../_bmad-output/planning-artifacts/archive/pre-scope-02-2026-10-19/README.md) explains the raw snapshots. Historical addenda/reconciliation/review documents carry precedence notices. All 80 old individual stories are marked superseded; their earlier approval evidence is preserved.
- Published 20 current planning story copies with matching canonical acceptance blocks. Stable aliases V1-01–V1-20 map to fresh numeric IDs 9.1–12.5; four epics 9–12 alias V1-E1–V1-E4. Fresh numbering satisfies the installed BMAD parser without reusing old identifiers. It does not change the approved scope.
- The new [readiness check](../_bmad-output/planning-artifacts/implementation-readiness.md) is PASS for bounded implementation. It records the unexecuted fixture, software-version, privacy/UI and delivery checks and the still-unconfirmed December deadline. Historical readiness/mockup approval is not treated as current product evidence.
- Generated [sprint-status.yaml](../_bmad-output/implementation-artifacts/sprint-status.yaml) using the installed BMAD parser: four epics and 20 stories, all backlog; four optional retrospectives; no warnings, dropped orphans or statuses upgraded from planning copies. Verified active local links, identical briefs, unique IDs, backward dependencies, exact canonical/planning-story acceptance text and the 80 historical dispositions.
- **Handoff completed at planning level:** product/backlog, architecture and UX responsibilities are reflected in the current documents; the developer receives the new backlog and tracking file. Begin V1-01 / 9.1 with the 3–4-hour anonymized-PDF/fasit investigation, or independent V1-02 / 9.2 with the persisted fictional fullstack slice. Preserve at least 12 hours of the estimated 60–80-hour remaining capacity for correction/delivery and reassess effort after 8–10 hours and around 30 hours.
- This turn updates plans and tracking only. No application implementation, extraction/integration/device test, public deployment or field trial has been performed or marked passed. No commit or push was requested or performed.
- Final checks passed: BMAD sprint validation returned `valid: true` with no problems; all 32 current document links/encoding checks passed; all 20 canonical/planning-story blocks match; all 80 historical IDs are mapped exactly once; Git whitespace checking passed after removing trailing spaces. The temporary update payload was removed. Changes are confined to planning/tracking, README and this log.

## 2026-10-19 - Story 9.2: persisted fictional local day

- Implemented the first executable SCOPE-02 slice: React/TypeScript, FastAPI and actual PostgreSQL, isolated under the fictional-assessment Compose project and persistent volume. Published ports bind only to 127.0.0.1; database has no published port. The Norwegian screen labels fictional/planned/unknown facts and explicit overnight calendar dates.
- Only the fixed fictional fixture is accepted. UUIDs and the fictional owner are server assigned. A server-issued operation UUID exists before save; concurrent identical retries return one stable record, changed accepted payloads conflict. Day retention is exactly seven days from first server creation; retry/read never extend it. Expiry denies access immediately, and startup/hourly cleanup removes associated day/operation state; unknown/purged operation IDs cannot resurrect data. Seed/reset use only the guarded fictional database and repeat known payload values.
- Actual registry/container versions resolved and executed: Docker29.7.2, Python3.13.16, PostgreSQL17.11, Node24.19.0/npm11.17.0, FastAPI0.149.0, uvicorn0.54.0, psycopg3.3.6, React19.3.1, TypeScript7.0.2, Vite8.3.4 and Playwright1.64.1. Base images are digest pinned, Python dependencies fully version locked and npm dependencies integrity locked. Initial older pins were replaced after current registry verification; the initial Vite audit finding was resolved. Final npm audit: zero vulnerabilities; pip check: no broken requirements.
- Executed `docker compose config --quiet`, `docker compose up -d --build --wait`, explicit migrate, fictional-only reset and repeated seed successfully. Final production frontend build/typecheck passed after correcting the initial missing Vite CSS module types.
- Executed `docker compose exec -T api python -m pytest -q`: **12 passed** (0.85s) against actual HTTP/PostgreSQL, covering equality, stable/concurrent replay, changed-payload conflict, malformed/extra/non-fictional requests without day mutation, server owner, exact retention, expiry/purge/no resurrection, invalid origin and non-assessment configuration denial.
- Executed `scripts/verify-persistence.ps1`: actual PostgreSQL/API service restart retained the entire acknowledged record `5b874fbc-6c61-403e-bf4d-c569375e8842` and repeated-save identity. Executed `scripts/verify-unavailable.ps1`: actual database stop returned503, explicit retry recovered, stopped API could not return a day, and all services recovered healthy.
- Executed `npx.cmd playwright test`: **4 passed** (4.1s) in installed headless Edge. Real keyboard save/reload at1440/768px, visible focus, no horizontal overflow, no localStorage, synthetic fetch failure with retained example/explicit retry and failed reopen, and HTML/malformed response rejection all passed. Screenshots saved as `Docs/evidence/9-2-1440.png` and `9-2-768.png`; root inspected both as readable with no overflow. The browser connector exposed no browser surface, so these are development automation observations. Actual tablet hardware, assistive technology and a complete accessibility audit remain unqualified.
- README documents exact setup, migrations, seed/reset, tests, service restart, outage and teardown commands plus limits. Spec and only story9.2 tracking move to **review**, pending the independent review workflow. Other stories remain unchanged. Git whitespace check passed. Services remain running for review; no commit or push performed.

### Story 9.2 review corrections - 2026-10-19

- Tightened database URL validation to reject query overrides, fragments and unsupported schemes before psycopg connects. Regression spies prove host/user/database overrides never reach the connector. Strictly reject numeric/non-boolean fictional markers before Pydantic coercion while preserving date parsing. Corrected the README: bootstrap credentials are a superuser in a dedicated fictional-only cluster; private data must never share it.
- Frontend rejects invalid or impossible timestamps, future creation, reversed/expired deadlines and mismatched reopen identity. A 410 or known expiry clears the day, footer, operation and URL identifier and offers a fresh example. Transport failures retain still-valid acknowledged presentation. Browser regressions now discard a real committed save acknowledgement and verify unchanged operation/record/result on retry, assert Oslo overnight rendering before/after reload, and cover response rejection and automatic expiry cleanup.
- All HTTP calls in both PowerShell verification scripts now have explicit timeouts. Parsed both scripts successfully and inspected every HTTP call; full restart/outage reruns are left to root's full verification. Restored the original blank line after this log's title and corrected README sprint status wording.
- Targeted verification only: edited API boundary tests `pytest -q -k 'invalid_no_mutation or database_overrides or origins_and_non_assessment_denial'`: **13 passed, 5 deselected** (0.49s). Edited browser spec: **12 passed** (6.6s). Rebuilt edited frontend/API; production typecheck/build passed. Story remains **review**; root owns final full verification and completion status.

### Story 9.2 final root verification and handoff — 2026-10-19

- Used bmad-build with current SCOPE-02 sources. No repository AGENTS.md exists. Selected independent 9.2 because 9.1 lacks representative anonymized PDFs and independent expected facts, as explicitly permitted by the current backlog. Prepared the implementation spec before code. Independent review covered blind defects, edge cases and verification gaps; all 13 findings have individual triage evidence in the spec. Direct corrections were applied; no retained blocker or deferred implementation task for this story remains.
- Final root checks: Compose configuration passed; **18 HTTP/PostgreSQL tests passed (0.90s)**; production frontend build/typecheck passed; **13 headless Edge tests passed (6.7s)**. Browser tests now verify a committed save with its acknowledgement deliberately dropped, unchanged operation/record identity on retry, explicit Oslo overnight dates, malformed/expired/wrong-record responses and known expiry cleanup.
- Root reran both real-service scripts: DB/API restart preserved identical record `8caae39b-59a6-449e-982c-3d596e976579`; real database stop returned503, explicit retry recovered, stopped API failed honestly and all services returned healthy. Two targeted browser checks overlapped the deliberate outage and failed transiently; the serialized final full browser run passed with no skipped case. Root inspected both 1440/768px screenshots. Actual tablet/assistive-technology/exhaustive accessibility qualification is not claimed.
- Spec status is done; sprint status remains review under bmad-build's final sync rule, epic 9 in-progress, every other story backlog. The original planning-story copy remains its approved backlog definition. Startup/reset/tests/teardown and limits are documented in README. Services remain running on loopback for owner review. User instruction overrides the workflow's local-commit step: no commit, push or next story.

### Owner check and publication authorization — 2026-10-19

- Jonas reported that the local slice appears to work as documented, then explicitly requested commit and push. This is owner-reported local verification; no additional device or accessibility qualification is inferred. Sprint story remains review.
- Authorized publication scope is the completed story 9.2 implementation, tests, evidence, setup instructions and tracking/log updates. No next change or story starts in this session. Publication success is verified separately after Git execution.

## 2026-10-20 — Story 9.2 closed and tracking reconciled

- At Jonas's request, reconciled story 9.2 from review to done in sprint tracking. The implementation spec was already done. Closure relies on the recorded final 18 API/PostgreSQL tests, 13 browser tests, production build/typecheck, real restart/outage checks, independent review with no retained blocker, and the owner's successful local use reported on 19 October.
- README now reports the completed story; the spec includes a dated closure entry that supersedes its earlier review handoff. Epic 9 stays in-progress and every other story stays backlog. Approved planning definitions remain intact; live implementation status is tracked separately.
- Confirmed the 19 October implementation publication: commit `040170eed4e043ecb899e39547270e0de6acf82a` was pushed to origin/main. Today's reconciliation is documentation/tracking only. No application code changed or application tests rerun; no next story, new commit or push.

## 2026-10-20 — Owner-approved PDF fixtures and import handoff

- Jonas Øisund explicitly approved the [fasit](../Eksempelfiler/README.md) for all seven [anonymized example PDFs](../Eksempelfiler/), ten pages in total. Recorded his dated approval in the fasit. Codex transcribed the source activities using text extraction and visual inspection of all pages, then incorporated the owner's domain explanations. The approved baseline has 46 route trips, 31 deadheads (including the clarified Travel to) and 113 explicit source activity rows.
- Owner clarifications govern implementation: `Vogn` is a vehicle duty (vognløp), a collection of trips, not a physical bus. Preserve `960xxx` and use the final three digits, including leading zeros such as `006` and `090`, for the realtime screen. Physical bus does not occur anywhere in these PDFs; obtain it externally and enter it manually. A vehicle-duty change alone is not evidence of a physical bus change. This records data meaning, not a new automatic/live integration requirement.
- Adjacent pause types may be displayed as one pause. If MealBreak is included, label the entire interval matpause; Coffee alone is kaffepause; Split break is split break/deltskiftpause. Preserve underlying source rows/provenance for comparison. Concrete combined meal breaks are example 2, 12:01–12:43, and example 7, 08:52–09:28.
- Example 5 ends paid time at 08:51 although the last Sign-off ends at 08:29: the owner explained 22 minutes of paid free time to meet the two-hour minimum. Example 6 Travel to is continuous deadheading Skoglyst → Breivika 15:33–16:00, 27 minutes without waiting; its completed interpretation comes from adjacent trips plus the owner, not additional PDF fields.
- Linked the baseline and implementation obligations into canonical stories 9.1 / V1-01, 10.1 / V1-05, 10.4 / V1-08 and 10.5 / V1-09, their matching planning copies and Epic 9 context. Fixture availability is now established. Extraction classification, supported-envelope decision and application acceptance remain unexecuted; story 9.1 and downstream stories remain backlog. No application code changed or application tests rerun.
- Jonas authorized diff inspection, commit and push of the example PDFs, fasit and related documentation. Publication outcome is checked separately after Git execution; this entry does not preclaim push success.

## 2026-10-20 — Story 9.1: bounded text-PDF extraction qualification

- Loaded the implementation spec and both context files before implementation. Transcribed the independent approved README into `backend/tests/fixtures/import_expected.json` before inspecting PDF extraction; retained approval, README/PDF SHA-256 values, all 113 ordered rows and the seven counts 33/16/6/16/5/16/21. Duty occurrence positions were added from the same approved descriptions. The parser cannot read this oracle or use fixture-specific answers.
- Added a separate `ImportDraft` adapter and qualification CLI, without changing the fictional domain, API, UI, storage or migrations. In-memory spawned workers enforce 10 MiB, 20 pages, 30 seconds and 2 MiB output, with explicit safe rejections and termination/join/pipe cleanup. Originals are read-only fixture mounts outside the image. Unknown annotations, zero-minute rows, repeated trip identifiers, continuation pages, duty occurrences/suffixes and source pause rows survive extraction. Calendar instants are derived from service date/start/stated span, never clock order alone; actual bus stays null.
- Executed all seven PDFs / ten pages. Examples 1–5 and 7 are supported for the independently qualified source facts; example 6 remains partial. Every required source comparison matches: 113 activities, 46 route trips and 30 numbered deadheads extracted. Owner-assisted Travel to is the 31st deadhead; its six assistance gaps remain separate and cannot count as automatic completeness. Paid free time in example 5 is an attributed explanation, not an invented row. Intermediate stops, other layouts, DST and production integration remain unqualified.
- Preserved negative evidence: initial parsing missed a row adjacent to a `t` annotation; preserving unknown `t`/`N` markers corrected the layout handling without changing the fasit. Encrypted rejection initially hit a wrapped library exception; corrected the safe mapping. The final qualification command exits 1 because example 6 remains partial, as required. Missing/changed/unapproved files remain untested. Detailed field comparisons, versions, hashes, timing, failures and downstream recommendation are in [JSON](evidence/9-1-import-qualification.json) and [the evidence report](evidence/9-1-import-qualification.md).
- Registry/official-document verification and actual installation pinned pdfplumber 0.11.10 and its complete dependency set. `docker compose build api` passed; import suite **22 passed** (2.63s); existing actual HTTP/PostgreSQL suite **18 passed** (0.99s); `pip check` found no broken requirements. Tests cover oracle integrity/counts, every expected source field, calendar/owner distinctions, deliberate missing/changed facts, invalid/encrypted/image/page/size inputs, timeout/cancel worker cleanup and output limits. The experiment and evidence completed well within four hours, with no omitted fixture. README includes reproducible commands and explicit downstream limits.
- No commit or push. Only this story is handed to the parent build workflow for independent review and status synchronization; no later feature starts here.

### Story 9.1 final root verification and handoff — 2026-10-20

- Completed three independent review layers and recorded every finding separately in the spec. Corrected individual field provenance validation, calendar derivation links, approved pause-group comparison, exported source-order validation, explicit fact-origin attribution, unresolved-pause grouping and independent synthetic annotation coverage. The approved README/PDF baseline is unchanged; pause expectations were transcribed from its existing approved table. No findings deferred or retained blocker.
- Rebuilt API image; final root runs passed **76 import tests (3.17s)**, **18 actual HTTP/PostgreSQL tests (0.89s)** and `pip check`. Regenerated all seven fixture results at 12:52:49 UTC: 113 source rows, zero required source-fact mismatches, six supported and example 6 partial with six owner-assisted gaps. CLI exit 1 is intentional. Checked final implementation/oracle hashes against the report. The full execution/review cycle remains within four hours.
- Spec status is done; sprint story 9.1 moves to review under build's terminal synchronization rule. Story 9.2 remains done, epic 9 in-progress and all other stories backlog. README documents the qualified envelope and reproducible CLI. Production PDF review/import remains story 10.1. The approved spec prohibits commit/push, overriding the workflow's local-commit instruction; neither was performed. No next story started.

### Story 9.1 owner acceptance and closure — 2026-10-20

- Jonas completed bmad-walkthrough and approved the change with "Klar til godkjenning, ser bra ut." Closed sprint story 9.1 from review to done and synchronized README, the implementation spec and evidence report. This dated closure supersedes earlier review handoff statements. Story 9.2 remains done, epic 9 remains in-progress and all other stories remain backlog.
- Acceptance relies on the recorded independent reviews, 76 passing import tests, 18 passing real HTTP/PostgreSQL tests and the qualified-envelope evidence. Six examples remain supported and example 6 partial with separately attributed owner facts. Approval does not establish production import support or imply the optional manual commands were executed by the owner.
- Documentation/tracking only; no application code changed or application tests rerun. No commit, push or next story started. Walkthrough completion customization resolved to empty.

### Story 9.1 publication authorization — 2026-10-20

- After accepting story 9.1, Jonas explicitly requested commit, push and an updated development log. This supersedes the earlier no-commit/no-push boundary for the completed story. Publication includes the adapter/CLI, independent oracle/transcription script, pinned dependencies, tests, evidence, owner acceptance and synchronized documentation/tracking.
- No application code changed after the recorded final verification: 76 import tests and 18 actual HTTP/PostgreSQL tests passed. This publication step checks the full staged diff and whitespace; no new test execution is claimed. No next story starts. Commit/push outcome will be recorded after Git confirms publication.

### Story 9.1 publication confirmed — 2026-10-20

- Created commit `6a9979d568d93793a7495565832b7f450430a249` (`feat: qualify supported PDF imports for story 9.1`) and successfully pushed it to `origin/main` at `https://github.com/IBE160-2026/G06-oisund.git`. Git reported `e8c0cf2..6a9979d main -> main`; local HEAD and the updated origin/main reference matched, and the working tree was clean immediately after publication.
- The commit contains all 14 intended files, including the independent transcription script and owner closure. Staged whitespace checks passed. This confirmation is a documentation-only follow-up; no new code, test run or next story. Its own push is verified separately after committing this log entry.

## 2026-10-20 — Story 9.3: private access implementation handoff

- Read the approved spec and its full Epic 9 context before implementation. Added a separate private Compose project/cluster/volume and loopback API on 8001; preserved fictional demo storage/reset on 8000 and the default frontend. Private migrations run in ordered transactions under an advisory lock. Accounts, hashed opaque sessions, bounded persistent login metadata and startup/hourly cleanup belong only to private PostgreSQL.
- Provisioning uses hidden `getpass` input twice and refuses terminals that would echo. No account/default account password is seeded. Salted stdlib scrypt (N=32768/r=8/p=3) uses the pinned Python/OpenSSL runtime; official Python/OWASP docs and executable hashing were checked, with no added dependency or lock change. `initialize-private.ps1` generates/preserves a Git-ignored Docker database secret. A generated-secret transition initially failed safely until the existing synthetic database role was updated; clean startup generates the file before creating PostgreSQL. Never replace this secret while preserving an existing volume.
- Session tokens are random, hashed in storage and expire exactly 14 days after original server sign-in. HttpOnly host-only SameSite cookies, exact origin checks and signed CSRF proof protect login/logout. Public configuration is unsupported and fails closed; insecure cookies require the explicit loopback flag. Private resources return no-store, derive ownership from sessions and distinguish 401 renewal from safe foreign-profile 404. Generic validation/credential errors and disabled access logging avoid secret/private payload echoes. Limits are 10/name, 20/IP and 100 global per 15 minutes, at most 201 persisted buckets; global admission serializes concurrent attempts.
- Added Norwegian `/private` form/empty workspace. Presentation/credentials remain in memory and clear on expiry/logout/history/visibility transitions; late responses cannot restore it. A security-only pending cookie preserves the logout lock across reload until acknowledged revocation; it stores no account or private content. BroadcastChannel sends only logout state so other open tabs clear immediately. No private work uses browser stores or offline grants. Draft CRUD/retention and application PDF integration remain later stories.
- Both Docker projects built and became healthy; private Compose validation and `pip check` passed. Private actual HTTP/PostgreSQL tests: **8 passed (19.02s)**, including synthetic two-owner isolation, origin/CSRF, hashed fixed-deadline sessions, revocation/expiry/cleanup, concurrent bounded throttling and CLI PTY no-echo. Existing assessment: **18 passed (0.97s)**. Fixture-mounted import regressions: **76 passed (3.22s)**; six supported examples and example 6 partial remain unchanged. `npm.cmd run build` and Docker frontend typecheck/build passed.
- Final full Playwright run: **21 passed (23.8s)**, 13 demo and eight private tests. Checked 768/1440px keyboard/focus/wrapping, no local/session storage, reload/back, fixed deadline/server expiry, unconfirmed logout, lost acknowledgement and retry settlement, another open tab and stale responses. Added [768px](evidence/9-3-768.png) and [1440px](evidence/9-3-1440.png) screenshots; inspected the rendered 768px image. Restored regression-generated story 9.2 screenshots to their committed baseline.
- `uv run --no-project scripts/verify-private-access.py` passed sequential private PostgreSQL/API restart, unchanged session/deadline and throttle metadata, twice-reapplied migrations, cleanup, isolated fictional reset, crossed identifier denial and logout. This script deliberately resets only demo data. Windows Store Python was unavailable, so the documented uv command was used. An overlapping intermediate restart/browser run caused a container-exec interruption and throttle snapshot mismatch; the final sequential runs both passed. Logs contained no credentials/private payloads. `git check-ignore` confirms the local secret is excluded.
- Setup/provisioning/test/teardown and the generated-secret lifetime are documented in README. Authentication protocol cookies/security lock are distinct from private saved work. Safe CSRF-cookie rotation conflicts can require retry in concurrent tabs. No public deployment, real-device/assistive-technology audit or draft acceptance is claimed. Implementation is handed to the parent for independent diff/matrix review and final status synchronization; no commit/push or next story.

### Story 9.3 final root verification and review handoff — 2026-10-20

- Three independent review layers and root audit produced fifteen individually triaged findings. Fixed late-login/logout ordering with cross-tab Web Locks, persistent logout lock, common throttle windows, non-ASCII/signed/aged CSRF rejection tests, synthetic-only verification safety, post-render focus, unfinished input preservation, threaded CSRF checks and streamed request-size bounds. No finding was deferred; the dedicated local bootstrap-superuser finding was rejected as hypothetical privilege hardening under the workflow's low-finding rule.
- Root read the full diff and inspected both screenshots. Final root verification: private HTTP/PostgreSQL 14 passed (27.33s), existing assessment 18 passed (1.03s), approved import 76 passed (3.22s), full Playwright 23 passed (23.3s), frontend production build/typecheck passed. Actual private DB/API restart, unchanged deadlines/security metadata, migration replay, cleanup, isolated demo reset and revocation passed sequentially. Both Compose configs and pip check passed; all spec matrix rows have executed coverage. Sandbox permission failures were retried successfully with escalation.
- Restored only regression-generated 9.2 screenshots; retained 9.3 images. Spec is done, sprint 9.3 is review and epic 9 remains in-progress. Stories 9.1/9.2 remain done; 9.4 remains backlog. No retained blocker, draft/PDF integration or next story. Local commit follows this entry per BMAD; no push. README documents setup and synthetic-only testing after real account provisioning.
