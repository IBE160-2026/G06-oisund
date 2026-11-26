# Cross-source and lifecycle verification

> EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE

Accessed 2026-10-26 by lead, independently reading sources already identified by researcher.

1. Svipper article https://svipper.no/nyheter/stengte-plattformer-pa-giaverbukta-terminal-fra-mandag-26-oktober.6992.aspx published 2026-10-23 16:07, modified 16:26. Direct web page retrieved: asphalt work 26-29 October; normal service planned 30 October; platforms 1/2 moved to3. Table includes 24 airport vs Skjelnan; 28 Solligarden vs Hamna; 42 both directions. This corroborates the actual Entur situation TRO:SituationNumber:426 linked to this URL (see entur-r1.md). Different presentation fields: stop-level SX versus article line/direction table. Corroboration of this one event, not independent validation of complete feed or latency. Dates have no displayed timezone; do not fabricate machine validity from article dates.

2. Entur https://entur.atlassian.net/wiki/spaces/PUBLIC/pages/637370694/SIRI-SX+-+Validity+of+a+message (updated 2019-03-19): directly read. Same ID update with Progress closed; closure EndTime >=5 hours ahead; closed suppressed from journey search but retained in stream to EndTime. This is documented profile semantics, not a TRO closed-message observation. No disappearance==resolved rule established.

3. Entur https://developer.entur.no/terms-of-service (modified 2026-09-28): directly read. ET-Client-Name required; NLOD reuse subject to attribution/license and modifications statement, no endorsement. No accuracy/completeness/availability guarantee. No source-specific application cache-retention permission inferred from HTTP cache headers.

Spot-check outcome: corroborated example and lifecycle statements match sources. Independent publishers Svipper/Entur support Giaverbukta event linkage; the Entur record may originate from the same upstream operator, so this is cross-channel consistency, not independent reporting of event truth. Mark provider-specific assertions unverified under BMAD independent-publisher ledger rule. No opposing evidence found to justify replacing missing direction with guessed direction.
