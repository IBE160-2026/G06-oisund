# Line 20 dated route reference

The pilot covers Troms line `TRO:Line:1_20` for the operating dates **23–29 November 2026**. The verified public archive contains 15 line patterns, with nine active across the pilot and both directions running each day. Independent membership counts from the source evidence are 136 / 136 / 136 / 136 / 143 / 109 / 64. The parser produced these counts for all seven days. `Complete` refers to the dates, line, and contents of this pinned export. The review panel shows archive age separately from data coverage.

The source is Entur's [Troms NeTEx export](https://storage.googleapis.com/marduk-production/outbound/netex/rb_tro-aggregated-netex.zip), generation `1795129398375617`, ETag `5d5e931e207e5ccfc8b6dd2cae6314f8`, SHA-256 `03662d51c1438514d1695e632c598a7ea589d5384a19804658212fc4af0af8b9`. The locally verified copy was acquired at approximately 01:14 UTC on 20 November. Its line and shared XML contain publication clocks, preserved without an invented offset or provider freshness timestamp.

Use the owner sandbox's existing launch script with the verified archive at `.private-runtime/route/troms-netex-1795129398375617.zip`. The loader works offline from that local file at startup. Missing or rejected input leaves the draft route source unavailable. Run this offline control from `backend/` in the project's Python environment.

```sh
python -m app.route_source /reference/troms-netex-1795129398375617.zip --observed-at 2026-11-20T01:13:54Z
```

For explicit owner-only reacquisition, use the same command with `--download` against an unused output path, `APP_MODE=private-local`, and `V2_ROUTE_SOURCE_REFRESH=owner` with the actual observation timestamp. Acquisition uses the fixed public export and sends no account, workday, draft, location, or activity facts. Keep the pinned archive in local runtime storage.

An exact comparison uses the saved operating date, literal normalized place names, and planned clocks. A saved turn number, provider private code, and clock proximity do not establish an identity. A checked absence refers to this exact comparison within available and closed evidence. Explicit selections preserve the direction, destination display, full pattern, and inclusive occurrence range separately from original and edited draft facts. When the source cannot be checked or the source facts differ, the prior selection remains visible. An archive without the former journey supports a missing-reference status, with no realtime cancellation inference. The reference transaction remains usable with unavailable source data.

## Qualification limits

- The October/November casebook remains historical in the planning worktree. The synthetic time controls replay the two October/November night conversions along with extended clocks and unresolved DST cases. They do not widen the current date manifest.
- The real archive verifies date membership, both directions, actual source order, destination display and exact NSR Quay identifiers. This archive maps each scheduled point to a Quay and lacks a direct parent StopPlace link for these calls. The API returns that parent as unknown.
- Synthetic draft pairs cover exact inbound and outbound comparisons, alternatives including repeated Quays, bounded absence, variants, incompatible choices, stale and unavailable sources, operation replay, review races, expiry, and frozen evidence. No actual-date private shift pairs or independent real-shift matching oracle were used. Positive automatic matching and imported turn-number equivalence remain unqualified.
- Live refresh and realtime cancellation are outside this pinned launch. The version comparison is covered with controlled changed and missing public facts. A later source archive requires explicit verification and a revised pin.
