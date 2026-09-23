# Architecture evidence review

Date: 2026-09-23. Scope: current `ARCHITECTURE-SPINE.md` and its decision log; official-source spot verification of stack, starter defaults, Cloudflare admission and Service Worker lifecycle. This review does not constitute application, provider, device or pilot testing.

## Verdict

**PASS — no blocking or corrective findings from the evidence lens.** The committed technology choices exist at the stated versions, the starter is described accurately, and the access/update design distinguishes documented mechanisms from unproven target behavior. User policy choices are identified as choices rather than vendor guarantees.

## Version and starter verification

| Claim | Evidence checked | Result |
| --- | --- | --- |
| React 19.3.0 | [Official versions](https://react.dev/versions) lists the September 9, 2026 release. | Matches. |
| Vite 8.3.0 / TypeScript 6.0.2 seed from create-vite 9.2.1 | [Tagged React/TypeScript template](https://raw.githubusercontent.com/vitejs/vite/create-vite@9.2.1/packages/create-vite/template-react-ts/package.json) declares `^8.3.0` / `~6.0.2`; its React range is `^19.2.8`. | Matches the seed description. The spine does not claim React 19.3.0 is the tagged template's literal default, or that ranges are installed lockfile versions. |
| Node 24.21.0 LTS | [Official release index](https://nodejs.org/en/blog/release) lists this LTS on September 9. | Matches; distinct from newer Current releases. |
| Python 3.14 / FastAPI 0.141.1 | [Template pyproject](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/backend/pyproject.toml) requires Python `>=3.14,<4.0` and FastAPI `>=0.141.1,<1.0.0`; [FastAPI release](https://github.com/fastapi/fastapi/releases/tag/0.141.1) exists. | Matches. Python is correctly a baseline, not an invented patch pin. |
| Full Stack FastAPI template is only a selective reference | [Current README](https://raw.githubusercontent.com/fastapi/full-stack-fastapi-template/master/README.md) and pyproject expose substantial bundled application/authentication/deployment scope. | The spine appropriately excludes inherited application features and does not silently adopt its SQLModel/Alembic/JWT stack. |
| PostgreSQL 18.6 | [Official version policy](https://www.postgresql.org/support/versioning/) lists 18.6. | Matches the supported seed. |
| cloudflared 2026.9.1 | [Official release](https://github.com/cloudflare/cloudflared/releases/tag/2026.9.1) dated September 11. | Matches. |
| OCR candidates 0.11.10 / 5.5.3 | Official [pdfplumber release](https://github.com/jsvine/pdfplumber/releases/tag/v0.11.10) and [Tesseract release](https://github.com/tesseract-ocr/tesseract/releases/tag/5.5.3). | Exist; their product suitability remains explicitly conditional, as it should. |

The document requires actual dependency/image locks at bootstrap. It does not pretend the candidate combination has been installed or tested.

## Load-bearing feasibility checks

**AD-13 and AD-10:** Cloudflare documents separate application/policy and global session lifetimes, including one-month configuration. Its model supports the spine's independent outer gate; the actual app session and bounded day authority remain application responsibilities. The preflight is explicitly limited to credential expiry and does not guarantee connectivity. [Session management](https://developers.cloudflare.com/cloudflare-one/access-controls/access-settings/session-management/).

The signed application token exposes expiry and application audience. Comparing the verified token's expiry with the authorized day allowance is feasible; it requires the validation already stated in the spine. [Application token](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/application-token/).

Cloudflare explicitly recommends creating Access protection before the published route, and supports token validation in cloudflared through Protect with Access. This supports the selected private ingress boundary; the fictional route must remain separately configured. [Self-hosted application setup](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/).

The source also documents an optional AJAX `X-Requested-With: XMLHttpRequest` convention for an expired-session 401. This is an implementation opportunity, not a required architecture correction: the current conservative treatment of redirects, unexpected content and failed requests is valid and should remain. [Session management, AJAX](https://developers.cloudflare.com/cloudflare-one/access-controls/access-settings/session-management/#ajax).

**AD-14:** waiting workers may activate after all controlled clients close; `skipWaiting` can mix a new worker with an old page. Therefore, merely declining a reload would not satisfy the user's requirement. The spine correctly specifies persistent active-build selection, complete versioned assets and non-destructive failure rather than claiming the browser's waiting state enforces workday boundaries. The exact boot implementation is still a story and test obligation. [Service Worker lifecycle](https://web.dev/articles/service-worker-lifecycle).

**AD-7:** Journey Planner v3 is a GraphQL service whose point-to-point result is optimized. The spine correctly avoids treating optimized journeys as a complete catalogue and requires qualification of targeted whole-day queries. [Entur Journey Planner](https://developer.entur.no/docs/open-services/journey-planner). The log records the separately researched SX/TRO candidate and protocol caveats; this review's direct realtime-page fetch returned an internal browser error, so it does not claim a fresh independent coverage verification. The spine makes no unsupported full-Svipper-coverage assertion.

**AD-13 operations:** Docker restart policies support restarting eligible containers after daemon restart and differ from application health/reconnect. The document preserves the Windows sign-in limitation and demands actual restart/noise evidence. [Docker restart policy](https://docs.docker.com/engine/containers/start-containers-automatically/).

## Coverage and evidence limits

- AD-1 through AD-5 primarily bind ownership and project contracts; they make no unsupported product-capability claims. IndexedDB, validated APIs and PostgreSQL transactions are established mechanisms, while reliable implementation remains to be tested.
- AD-6 through AD-9 retain import/source/GPS uncertainty and target-device gates instead of converting documentation into success claims.
- AD-10 through AD-12 specify local policy and standard session, locking and retention mechanisms. Browser storage is not called durable or encrypted, closed-browser deletion is not promised, and logical deletion is distinguished from forensic erasure.
- AD-13 and AD-14 make their provider/device/recovery tests explicit. No successful tunnel, HTTPS, migration, cold restart or application compatibility test is claimed.

No additional architecture decision or user approval is needed from this lens. Preserve the stated qualification gates during Epics & Stories; none should be weakened by interpreting this document review as pilot acceptance.
