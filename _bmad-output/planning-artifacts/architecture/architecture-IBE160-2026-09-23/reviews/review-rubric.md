# Architecture reviewer gate — rubric walker

Reviewed: 2026-09-23. Artifact: `ARCHITECTURE-SPINE.md`, draft after input reconciliation and deterministic lint. This is a document review; no implementation, deployment or device behavior was tested.

## Verdict

PASS. The spine is suitable for Epics & Stories. Both clarification findings below were fixed and the specific AD-11/AD-14 edits were verified on 2026-09-23. It covers the initiative's structural dimensions and preserves the adopted V1 boundary. Neither fix required a new product choice or another user approval: both make consequences of already adopted decisions enforceable across independently implemented parts.

## Findings

### R-1 — Preserve the active client's complete required API contract, not only its outgoing event format

**Priority:** high. **Location:** AD-14, third paragraph; release gate. **Disposition:** resolved. AD-14 now expressly preserves required requests, responses/errors, recovery/day data, notice updates and access/logout operations through the affected data's expiry.

AD-14 explicitly requires a new backend to support immutable event formats through the relevant data expiry. It also pins an active client's build. That client still needs other contracts while it remains active: notice/source responses, session/day-grant checks, logout, recovery and the synchronization receipt/error shapes. A backend could obey the narrower event-format rule yet change one of these response shapes or endpoints and make the retained client unable to update notices, process a receipt or settle a queued logout.

State that backend compatibility covers the full API surface required by each retained active build, including request, response and error contracts, through that build's applicable data lifetime. It can be implemented with minimal version adapters; no generic API-versioning platform is implied. Extend the existing old-client/new-backend release test accordingly. This follows directly from the adopted coherent-build and active-day-continuation promises.

### R-2 — Make day-grant rebinding part of the writer-transfer contract

**Priority:** medium. **Location:** AD-10 client-bound grant; AD-11 transfer. **Disposition:** resolved. AD-11 now atomically rebinds the grant to the new authenticated client/session and retires the former grant, preserving deadlines, for planned and emergency transfer.

AD-10 binds a day grant to a client. AD-11 atomically transfers writer ownership to a new client but does not state how that client-bound authorization follows the transfer. Independent access and takeover implementations could therefore produce a successfully transferred epoch that the new client cannot use after ordinary access expires, or copy a grant in a way that leaves the old client authorized to submit writes.

Specify that transfer reconciles the new client's authorized day scope with the new writer epoch before it can take control, under the authenticated same-owner transfer operation. Rebinding does not extend the original permitted day or retention deadlines, and cannot give the former writer permission to submit old events. The old device's retained local work remains available only through the adopted explicit conflict/recovery process. Concrete token/session storage remains story-level detail.

## Good-spine checklist

| Check | Assessment |
| --- | --- |
| Real divergence points at initiative altitude | Strong: authority, local transactions, synchronization, source certainty, lifecycle, writer transfer, access, retention and release continuity are binding. R-1 and R-2 close remaining contract seams. |
| Enforceable decisions | Every AD has Binds/Prevents/Rule and an identifiable outcome. Most rules are directly testable; field and source qualification are correctly distinguished from proven behavior. |
| Safe deferrals | DTO details, schema tools, OCR selection, numeric GPS thresholds and provisioning can remain downstream subject to the recorded boundaries. Failed coverage or capability qualification returns to an explicit decision. No request to prebuild speculative adapters is needed. |
| Scope and source coverage | Approved sources are identified with precedence, and detailed UX remains authoritative rather than copied wholesale. V1, fictional demo, linked-plan contexts, pilot configuration and excluded integrations are explicit. Prior input reconciliation is acknowledged, not rerun in full by this review. |
| Technical currency | Stack has versions and primary-source evidence. Conditional OCR choices are distinguished from adoption. A dedicated parallel currency reviewer owns fresh source verification. |
| Brownfield/inheritance | No existing implementation or inherited parent spine is represented as constraining this new project. |
| Deployment/environment | Windows-first Compose, separate private/demo origins, Cloudflare gate, no published database/API, restart limits, later portable host, secure-context development and secret placement are covered. |
| Operations and loss | Polling/cleanup recovery, resource/noise limits, working storage, explicit absence of historical private backups, observable offline/freshness status and expiry guards are covered. |
| Test/acceptance envelope | Concrete future gates cover PostgreSQL integration, offline durability, external source completeness, actual Lenovo/Brave behavior, access clocks, restart and update recovery. No simulated or researched result is falsely presented as a passed pilot test. |
| Simplicity and altitude | Fourteen adopted decisions account for the document's length. Lower-level files, fields and libraries remain deferred. Diagrams explain ownership, local-before-remote persistence and deployment without prescribing a speculative framework. |

No outstanding finding from this review. The follow-up verified only the two requested edits; other reviewers' dispositions remain independent.
