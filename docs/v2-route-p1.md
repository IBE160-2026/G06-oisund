# Line 20 dated route reference

The pilot covers Troms line `TRO:Line:1_20` for the operating dates **23–29 November 2026**. The verified public archive contains 15 line patterns, with nine active across the pilot and both directions running each day. Independent membership counts from the source evidence are 136 / 136 / 136 / 136 / 143 / 109 / 64. The parser produced these counts for all seven days. `Complete` refers to the dates, line, and contents of this pinned export. The review panel shows archive age separately from data coverage.

The source is Entur's [Troms NeTEx export](https://storage.googleapis.com/marduk-production/outbound/netex/rb_tro-aggregated-netex.zip), generation `1795129398375617`, ETag `5d5e931e207e5ccfc8b6dd2cae6314f8`, SHA-256 `03662d51c1438514d1695e632c598a7ea589d5384a19804658212fc4af0af8b9`. The locally verified copy was acquired at approximately 01:14 UTC on 20 November. Its line and shared XML contain publication clocks, preserved without an invented offset or provider freshness timestamp.

At 02:43:18 UTC on 20 November, one HTTP HEAD on the public unversioned URL still reported that generation, the same ETag and 7,225,724 bytes. This metadata check confirms that the archived bytes were still the current release at that time. The runtime's recorded archive observation remains 01:13:54 UTC. [Entur timetable publication](https://developer.entur.no/open-data/timetable).

Keep the verified original archive at `.private-runtime/route/troms-netex-1795129398375617.zip`. Owner startup reads the original and any retained recheck offline. If the original pin is missing or invalid, the draft route source is unavailable. Run this offline control from `backend/` in the project's Python environment.

```sh
python -m app.route_source /reference/troms-netex-1795129398375617.zip --observed-at 2026-11-20T01:13:54Z
```

In PowerShell 7, start the preview with an explicit current-source check. The same switch works with `-ApisOnly`.

```powershell
pwsh -NoProfile -File scripts/v2-local.ps1 -Mode Owner -RecheckRouteSource
```

The isolated check requests the fixed public export once over HTTPS and sends only public request headers. It requires HTTP 200, a strong ETag, the provider generation, a bounded size, and a valid HTTP date. Redirects, responses with a reported cache age above one hour, and invalid transport are rejected. All seven dates must be complete and their dated departures, pattern versions, calendar facts, ordered calls, clocks and coverage must match the original. An equivalent archive may have a different SHA-256. New selections then use the returned SHA-256 and can pin the v2 manual stop mapping. Previously saved selections and receipts keep their original archive and mapping.

The check stores the archive and its receipt atomically at `.private-runtime/route/recheck/current-line20.bundle`. The receipt records SHA-256, size, generation, ETag, local UTC check time, HTTP Date and cache age. The local check time is measured when response headers arrive. The 24-hour clock starts from the earlier of HTTP Date and local check time minus reported cache age. The NeTEx publication clocks remain separate. A second check cannot overwrite a newer observation. A failed check reports the reason, leaves the retained bundle intact, and aborts that launch. A later ordinary Owner start rehashes retained evidence and rechecks all seven dated facts locally. With invalid or missing retained evidence, it uses the original observation. Test mode rejects the switch. Route lookup uses the startup evidence.

The original observation expires on 21 November at 01:13:54 UTC. On 20 November, the Owner command finished checking at 03:18:08.537204 UTC and found the same generation, ETag, size and SHA-256. The response reported `Age: 208` and HTTP Date `03:14:38 UTC`, which gave an effective observation of 03:14:38 UTC and expiry at that time on 21 November. Both observations expire before the operating dates. Run the explicit check during the trial to qualify whichever public archive is current then.

An exact comparison uses the saved operating date, literal normalized place names, and planned clocks. A saved turn number, provider private code, and clock proximity do not establish an identity. A checked absence refers to this exact comparison within available and closed evidence. Explicit selections preserve the direction, destination display, full pattern, and inclusive occurrence range separately from original and edited draft facts. When the source cannot be checked or the source facts differ, the prior selection remains visible. An archive without the former journey supports a missing-reference status, with no realtime cancellation inference. The reference transaction remains usable with unavailable source data.

## Qualification limits

- The October/November casebook remains historical in the planning worktree. The synthetic time controls replay the two October/November night conversions along with extended clocks and unresolved DST cases. They do not widen the current date manifest.
- The real archive verifies date membership, both directions, actual source order, destination display and exact NSR Quay identifiers. The timetable archive maps each scheduled point to a Quay. The manual position projection adds the exact parent StopPlace from the versioned NSR extract for new decisions that pin it. The public timetable projection still carries the original fields. [Manual mapping and qualification](evidence/v2-position-progression.md).
- A disposable owner-sandbox plan exercised the actual pinned outbound `TRO:ServiceJourney:20_260918101387157_1133` on the 23 November operating day. The private API found occurrences 1–80 from `NSR:Quay:90847` at 23:05 to `NSR:Quay:92496` at 00:14 on 24 November and froze the reviewed reference. This used a synthetic workday and real planned public facts. The private coordinate and road projections kept their insufficient evidence unavailable.
- Synthetic draft pairs cover exact inbound and outbound comparisons, alternatives including repeated Quays, bounded absence, variants, incompatible choices, stale and unavailable sources, operation replay, review races, expiry, and frozen evidence. No actual-date private shift pairs or independent real-shift matching oracle were used. Positive automatic matching and imported turn-number equivalence remain unqualified.
- The explicit Owner check is for equivalent dated facts from the current static export. Changed facts or incomplete coverage require a separately reviewed pin. Realtime cancellation is outside this source.
