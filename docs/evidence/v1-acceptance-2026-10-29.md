# D1–D3 candidate verification and owner walkthrough

Product/test/tooling snapshot: `3c2287ed68d0cbb1923439fc6ee00254395072a4` (C1). Owner acceptance of the complete candidate is **pending**. Later documentation/evidence commits do not change C1 product behavior. Historical `c067fdbb20150219c041588ed4e990e7b0ef6b94` remains unchanged.

## Authority and scope

Jonas requested completion of available verification and a stepwise personal assessment. After his **explicit candidate approval** and satisfaction of actual D1–D3 criteria, he authorizes recording acceptance, merging updated main, integration checks/push, Epic12/V1 closure and non-forced deletion of the fully integrated follow-up branch. No additional merge confirmation is required. Until that approval, Epic12 remains open. This supersedes the earlier blanket no-merge wording only under those conditions.

Server setup is separate bonus work, excluded from this delivery and its prerequisites; possible future v1.0.1 evaluation is not implementation authorization. No production deploy, account/data/access-rule change, server move, tag/release, coursework or extension is included.

## Actual source and device

The isolated review UI is `http://127.0.0.1:15326/private`, fictional API18329, private API18330, project `ibe160-v1followup-tests`. [Fresh source proof](v1-followup-source-proof-20261029T175511.json) verifies own image files and served assets, including `main-Ce6IpVYI.js`. Dedicated synthetic personal-review credentials are local only: `D:/IBE160/tmp/v1-remediation/.private-runtime/v1-acceptance-manual-credentials.json`; no credential value is published.

Actual USB-connected Lenovo TB361FU, Android16, Brave/Chromium155.0.8059.85, native800×1085 CSS portrait/DPR2. Playwright connects to the device browser in separate contexts with `viewport:null`; no device-metrics emulation. Prior private tabs/cookies are preserved. Only new loopback USB reverse mappings15326/18329/18330 and an owned DevTools forward were added.

[Physical-browser gate](v1-followup-device-browser-20261029T180012285199Z-4df76182.json): **22/22 passed** (17D1 +5D2) in3.2min, retaining original assertions, exact adapter/config/build inputs and raw output in its indexed archive. Browser actions execute on actual hardware; controlled HTTP faults are test doubles, and the API/PostgreSQL journeys use the isolated synthetic runtime. This is neither personal finger testing nor comprehensive OS/accessibility certification. Previous desktop, backend and bounded gate/proxy evidence remains applicable to unchanged C1; overlapping counts are not summed.

## Personal controls

Each answer below is actual owner feedback, separate from automated/passive observations and from whole-candidate approval.

| Control | Actual owner answer | Evidence / remaining work |
|---|---|---|
| 1. Known selection rejection, unavailable current facts, repeated access check, cancel remains reachable | “Bestått og forståelig” | [Control1 metadata](v1-acceptance-device/personal-control-1.json); passive screenshot/guard observation. Canonical429 and current503 are controlled faults; no selection write reaches the API. |
| 2. Start→confirm, known rejection/current unavailable, refresh, cancel rejected Start | “Bestått og forståelig” | Captured `rejection/start` observation: one intercepted dispatch, navigation guard released; “Avvist skiftstart er avbrutt. Lagret skiftstatus er uendret.” No Start write reaches the API. |
| 3. Accepted selection with lost reply, permanent parent disappearance, deliberate cancel/confirm abandonment | Pending | Must distinguish no acknowledged saving from actual stored result; no resend and notice registry retained. |
| 4. Both Oslo02:30 occurrences | Pending | Inspect explicit UTC+02:00 and UTC+01:00 source/validity facts on actual device. |
| 5. Independent synthetic A7 sources and practical flow | Pending | SMS/noURL and long shared-link/all-lines, unknown facts, scrolling/readability/finger comfort. |
| Whole candidate decision | Pending | Subset passes and early design direction do not approve the candidate. |

The live manual driver controls only its own synthetic context/account/plans. A first non-interactive helper could not receive stdin; it was replaced by an owned TTY process. Control1 capture assertions completed before an extra closed-context teardown iteration failed. Neither helper issue is relabelled a product failure or hidden as a passing helper execution. Subsequent controls use the corrected TTY driver.

## D3 available access and proof boundaries

Jonas reports only one active Access token and one other administered account **not assigned to the app**, already verified denied. There is no available saved genuine expired token and no other assigned member account. Therefore genuine expired-token replay and another assigned member/MFA-policy control remain **unperformed**. Non-member denial is not substituted for either. No rule/account change or candidate deployment is made to manufacture access.

Candidate B6–B10 evidence remains the actual isolated signed-JWT/Nginx/API/PostgreSQL, preparation parity, concurrency/deadline/cooldown/cache/recovery and cookie controls in the [qualification ledger](../submission/v1-followup-qualification.md). External observations concern the older running production version, not C1. WAN/IPv6/full OS/supply-chain and pathological pre-socket DNS cancellation remain precisely unqualified. These are preserved operational proof limits, not approved postponements or newly required local SCOPE-02 gates.

## Fresh delivery reproduction

A separate detached C1 checkout at `D:/IBE160/tmp/v1-delivery-candidate` preserves the existing `ibe160-submission` instance and all server work. [Exact config-only instance record](v1-acceptance-reproduction-instance.json) records four literal namespace/port substitutions: `ibe160-submission`→`ibe160-v1-delivery`,15325→15327,18327→18331,18328→18332. Application sources are unchanged; bonus server files are absent. This is a qualified isolated configuration of C1, not a claim that its configuration bytes are a pristine checkout.

The original guarded `submission.mjs init` recipe completed with exit0 after fresh uncached image/dependency build, five healthy services, migrations, synthetic account verification and fictional seed. The initial tool output was truncated; only the [retained completion tail](v1-acceptance-init-completion-tail.txt) is available, not a claimed complete raw initialization log.

The [runtime result](v1-acceptance-reproduction/submission-runtime-check.json) passed: ordinary-account reset refusal leaves both databases identical; populated private/fictional tables and deadlines survive stop/start/repeated initialization and restart; synthetic reset preserves generated secrets/migration/security settings and reseeds exactly one fictional day/account. All39 other container IDs/images/start times/states/mount relationships and18 other volume identities/creation times were identical at that measurement. This baseline includes already-running review/test services; it does not describe a global Docker startup.

The [browser report](v1-acceptance-reproduction/submission-browser-report.json) records **3/3 passed in48.3s**, exit0: independent A import/save/confirm/manual-use/ended/restart/reopen; C corrected midnight flow/aborted/reopen; B correct import/direct distinct approval. These use actual newly built frontend/API/PostgreSQL in desktop Chromium, not the tablet or in-memory demo. Locked host npm installation completed with0 reported vulnerabilities; this is not a supply-chain certification. Existing fixed-argument shell and color-environment warnings remain recorded without product-failure attribution.

[All actual API Python files and served frontend asset hashes](v1-acceptance-reproduction/source-proof.json) match the own fresh images; health including private cleanup is OK. API source is C1 with checkout newline normalization only. Frontend artifacts reflect the documented API-port configuration and therefore have their own hashes, separate from the15326 manual-review build. [Indexed logs/methods](v1-acceptance-reproduction/index.json) preserve exact preparation, device adapter and source-proof methods. The temporary device config was copied into evidence and removed from the frontend only after equality with its executed hash was proved. No product change was needed.
