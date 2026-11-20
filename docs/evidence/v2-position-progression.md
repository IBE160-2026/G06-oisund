# V2 stop progression evidence

On 2026-11-20 at 01:19:58 UTC, three exact line 20 Quays from the frozen Troms archive were checked with the Entur NSR Read API. Each Quay and its StopPlace were read by public ID. The catalogue retains the selected source fields, versions, explicit validity fields and fetch time. The Quay coordinates themselves were copied without adjustment. [Entur Read API](https://developer.entur.org/stop-places-v1-read/) · [Source terms](https://developer.entur.no/terms-of-service) · [NLOD 2.0](https://data.norge.no/nlod/en/2.0)

| Scheduled Quay | Quay version | Parent StopPlace | StopPlace version | Dated GPS eligibility |
| --- | --- | --- | --- | --- |
| NSR:Quay:90847 | 3 | NSR:StopPlace:53331 | 3 | Manual, Quay validity missing |
| NSR:Quay:89699 | 3 | NSR:StopPlace:52717 | 3 | Manual, Quay validity missing |
| NSR:Quay:95924 | 2 | NSR:StopPlace:56013 | 2 | Manual, Quay validity missing |

The parent responses supplied only a validity start. The Quay responses omitted validity entirely. Fetch time and modification time describe observation and change. Eligibility requires positive validity evidence for the dated call from both exact objects. The three records remain manual for the 2026-11-23–29 pilot. The frozen route digest is `03662d51c1438514d1695e632c598a7ea589d5384a19804658212fc4af0af8b9`, and the coordinate release is `nsr-line20-2026-11-20-v1`. [Coordinate sidecar](../../backend/app/nsr_position_sidecar.json)

The deterministic controls use fictional dated trips and simulated fixes. They cover ordered repeated stops, a protected manual assertion, an interrupted 3→6 manual choice, exact-Quay overnight handoff, access, conflicting revisions, and anchor expiry. The estimator uses a 20-second manual protection period, a maximum of six samples over 30 seconds, distinct evidence over at least six seconds, and a 30 m accuracy cap. The shared watch cuts off after a 10-second raw-fix gap. The storage boundary allows one anchor and up to 256 compact receipts per workday. Only public Quay coordinates are served with the route projection. The save path receives occurrence identity, origin and evidence time, and inherits the parent deadline.

Before using ordinary GPS progression on the pilot, establish Quay and StopPlace validity for the exact call dates, then qualify the actual Lenovo model and Android build on Brave and Chrome separately. Record foreground permission results, trusted HTTPS, screen-lock and power-saving interruption behavior, repeat/nearby Quay discrimination, device accuracy against independent known positions, and narrow/enlarged Day/Night keyboard and tablet readability. The source probe and fictional controls leave those checks open.
