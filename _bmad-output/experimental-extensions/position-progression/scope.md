# Scope and current planning decisions

**EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

V1.3.0 planning draft, updated 2026-10-26. User clarifications U1–U5 and [PP-D1–D4](specs/spec-position-progression/decisions.md) supersede contrary proposals in the original research-era scope. They are direction for planning, not approval of implemented behavior. The current contract is [SPEC and companions](specs/spec-position-progression/SPEC.md); [research](research/technical-position-progression-2026-10-26/research.md) retains the external evidence and untested platform questions.

## User clarifications

- **U1 — Start:** choose the first stop of the trip/range actually driven. Mid-trip start and resume permit another relevant occurrence; full-pattern index1 is not mandatory.
- **U2 — Recovery:** desired automatic reacquisition can relocate the estimate across several missed stops when fresh measurements and route context are clear. It never records those stops as observed. Manual post-gap selection is now required for the first delivery (PP-D1).
- **U3 — Advisory manual anchor:** a new manual choice gets protection against immediate GPS replacement. Later coherent reliable measurements can outweigh an older anchor; age alone is never evidence that GPS is right.
- **U4 — Saved stop:** retain the latest stop identity, trip/occurrence context, evidence time and manual/GPS provenance for a next-trip proposal. Remap identity into the new pattern/range; do not carry sequence numbers or assume a shared origin. Preserve existing access/deletion deadlines.
- **U5 — Coordinates:** propose Entur NSR as authoritative for Quay/StopPlace coordinates. Preserve ID mapping, source, version, validity and parent/platform distinction. Describe the additions locally; the route plan is unchanged.

## First-delivery planning boundary

The first delivery plans foreground, opt-in assistance on one manually selected, user-confirmed dated trip. Start from an explicitly chosen/accepted occurrence; use qualified measurements for ordinary progression and later reassessment of that advisory anchor. A manual correction resets evidence and briefly protects the choice; explicit Pause remains a separate control.

After interruption, first delivery requests manual occurrence choice and fresh acquisition. Qualified automatic multi-stop relocation is deferred by PP-D1. The user's manual choice can jump directly to the relevant occurrence without catch-up steps. PP-D2 permits reuse within the same workday/shift identity, including across midnight, never merely the same calendar date. PP-T1 proposes one online, workday-owned last-stop record, available for the next selected trip. Different workdays require manual start; reuse cannot extend access/deletion deadlines. This replaces the original session-only-anchor proposal without introducing a full GPS history.

A3: all numerical gates are experiment seeds, not validated limits. Threshold expiry never overrides freshness, coherence, plausible movement or ambiguity checks. No reliability/cadence claim exists for the Lenovo; identify model/SKU and qualify Brave/Chrome separately later. See [behavior](specs/spec-position-progression/behavior.md).

## Dependencies and boundaries

The latest available route plan at 7cada9d2e66af9806358f582bc8ea459321a6563 is draft P1 line20 association in draft review with frozen workday carry-forward. Require the compatible dated journey, unique selected occurrence range, source direction/headsign, explicit service/calendar times and ordered repeated occurrences. A confirmed unverified reference stays labelled unverified; hard contradictions prevent assistance. Neither a line/trip number/privateCode nor nearest time proves identity.

The proposed [handoff](specs/spec-position-progression/route-interface.md) adds qualified NSR coordinates/version mappings and separate route-health versus measurement-health states. Geometry is optional. Missing coordinates keep the affected portion manual; an accurate fix does not repair missing data. Pattern/source refresh cannot overwrite frozen references or manual route facts. No enrichment of an active plan is authorized.

Keep estimated stop, manual assertion and confirmed route distinct. Position/time cannot select another activity, mark performed/skipped/interrupted outcomes, start/end/abort work or infer a return trip. A last-stop suggestion requires explicit next-trip selection and acceptance. Existing ownership, revision/retry recovery, fixed expiry, online authority, transient originals, private/demo isolation and readable Day/Night/focus behavior remain.

Trusted HTTPS and actual tablet access must be qualified separately; the current loopback runtime is not a tablet deployment. Raw measurements remain in a bounded transient buffer; clear them on pause, switch, access loss or closure. No coordinate history, analytics payload, public position query or private persistent browser cache. Browser/OS location providers may still use network services.

Implementation waits for completed/tested V1, required route functionality and separate authorization. No automatic-notice, live-vehicle or complete-regional-catalogue dependency. Line20 is the initial pilot proposal; research-era dates do not guarantee future coverage. This round creates [one extension epic with four stories](epics.md), and executes no product tests, location collection, services, commits or publication.

## Settled decisions and remaining qualification

Q1/Q2 are closed by PP-D1/PP-D2: manual recovery first and same-workday anchor reuse across midnight. No material product choice remains open for this bounded epic. These are planning decisions, not acceptance of implementation. The manual anchor stays advisory over time; continuous qualified GPS progression does not require a confirmation at each stop. Explicit Pause/Off remains binding.

Accuracy thresholds, coordinate qualification, trusted tablet access and hardware suitability are evidence gaps assigned as small tasks in the affected stories. The [fictional example](specs/spec-position-progression/fictional-example.md) demonstrates the boundary and the separate future recovery branch, with no GPS test evidence.

Later possibilities include qualified automatic reacquisition, geometry-assisted ambiguity handling, wider route coverage, optional screen-wake support and verified Entur vehicle supplementation. Background/native behavior requires separate investigation.
