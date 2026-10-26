# Existing behavior and extension boundaries

> **EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE**

## Baseline and evidence authority

The draft uses committed baseline aa0fcfb48904c7e0bdd6c68280e5db2d21f478ed. SCOPE-02 remains V1 authority; manual web/SMS notices are accepted 11.4 behavior. Main-workspace uncommitted 11.5/11.6 and preliminary Epic 11 retrospective are background, not adopted acceptance. Reconcile any later accepted committed baseline before implementation; do not silently import local changes. Earlier scope.md left provider selection open; the current user asks for Entur TRO as proposed source, not approved implementation.

Research project-context evidence: nullable exact line, printed trip/direction, places and explicit Oslo planned times; no guaranteed canonical line/journey/stop IDs, sequence or geometry. A small reviewed binding set plus honest review is therefore sufficient to evaluate a line/time slice; usefulness remains to be measured.

## Manual and automatic information

P: Source content, computed relevance and user additions remain separately identifiable. Preserve manual web/SMS text, optional URL/source description, original source clocks, entered/edited/checked times and manual end. Collection cannot overwrite/delete notes, mark checked, remove corrections or reopen manually ended records. Source changes are not edits attributed to the user.

P: A correction is a labelled local interpretation with original evidence available. Changed source content retains the correction, explains the change and requests reassessment where relevant rather than silently applying it to a different revision. Linking manual records is explicit/reversible. Manual navigation and planned-versus-actual facts remain independent.

P: Preserve server-authoritative ownership/revisions, private/demo separation, expiry and access denial. Do not send private plans, SMS, associations or notes to providers or add a private persistent browser cache. Dataset/geographic collection does not need private trip requests. Polling, reading, retry and association must not extend existing seven-day private-plan retention; expired/deleted/unauthorized plans cannot expose private linkage. Public source-history retention is Q-5; this spec grants no database/schema change or indefinite storage.

## Simple future mapping interface

P: A conceptual read-only lookup accepts provider/codespace, exact public line and date, optionally a typed stop/direction/journey hint. It returns resolved/ambiguous/unavailable, candidate canonical IDs, provenance, mapping version and applicability dates. Ambiguous/unavailable never becomes an invented match. This is desired behavior, not an API, schema or architecture choice.

P: Initially a reviewed small mapping set suffices. Later the separately planned network extension may provide versioned LineRef, NSR StopPlace/Quay, route-pattern/direction, dated journey, stop-order and geometry through this boundary. Notice behavior owns source lifecycle/relevance explanations; mapping data owns identity/topology. Complete routes/GPS/progression are not prerequisites. Precise route/stop/direction matching waits for its necessary verified bindings.

## Source limits

Research recommends structured Entur TRO SX with Svipper local reference. SX is passenger-facing, without complete cancellation or internal-driver-order coverage established; TRO GTFS alerts are unverified. Svipper has useful local detail but no supported automatic ingestion contract established. Manual reference checks do not require automated access or blanket provider contact. Vegvesen needs authenticated current evidence and corridor bindings; it is deferred with ET/VM, GTFS alerts and automatic Svipper enrichment.
