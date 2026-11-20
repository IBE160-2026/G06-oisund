# Road snapshot boundary

The historical public corpus records the Polaria to Flyplassvegen chain from 27 October 2026. It has 139 contiguous source segments, four source-bound roundabout arcs and recorded type 105 limits. The R4 arc-exit node is 218.448 m forward in the documented 200 m approach scenario. The registered 50 plate is approximately 25–26 m beyond the node. The decision and signing plan remain required to qualify the reporting point. [Exact decision record and field reference](../../../docs/evidence/v2-road-source-20261120.md#exact-decision-record-and-field-reference).

The dated 20 November recheck found 145 contiguous segments with the same span endpoints, changed interior references, and registered speed evidence for 144 of the 145 segments. It confirmed the distance to the R4 arc-exit node. The nine line 20 pilot patterns remain at least 2.4 km from the R4 exit. A compatible dated route for the road pilot must be qualified separately, together with bus turns, exact lanes, temporary regulations and physical GPS uncertainty. [Dated public evidence](../../../docs/evidence/v2-road-source-20261120.md).

The private route projection only returns a matching packaged `v2-approved.json` with the exact dated, frozen journey, occurrence range, versioned road packages and supporting direction, coverage, topology, source and error-model evidence. No such operational package is bundled. The technical controls use two explicitly synthetic manifests and the same runtime matcher. A simulated browser or a reachable NVDB endpoint cannot close the physical pilot gates.

## Local source refresh

From `backend`, run the explicit operator command with Python 3.13. This example reproduces the public 20 November scope in municipality `5501`.

```powershell
python -m app.road_evidence --municipality 5501 --sequence 1109517 1109722 1125918 1125938 1125949 1125950 1126027 1126028 1126029 1126030 1126487 1126506 1126527 1126588 1126914 3316796 3316797 3316798 --date 2026-11-20 --output ../tmp/nvdb-road-20261120.zip
```

The ZIP contains the raw response pages and `receipt.json` with the selected effective date, the observation and server times, page lengths and SHA-256 hashes, declared counts and any missing network sequences. A scoped road object may include extra placements in its raw page. The command fetches the segmented road network and object types 105, 573, 607, 616, 721, 856, 913, 977 and 979. It stops on incomplete pagination, inconsistent results or exhausted budgets. It allows at most 20 requests including at most two retries before the response body, 3 MB per body, 10 MB overall, 500 segments and 100 speed-limit objects. The tested Linux command has a 240-second acquisition deadline. The Python socket uses a 12-second timeout. A completed archive replaces the output atomically. The archive has research status and a separate file format from the runtime package. [Verified NVDB replay and source result](../../../docs/evidence/v2-road-source-20261120.md#repeatable-bounded-nvdb-collection).

## Offline corridor audit

From `backend`, pair the research ZIP with the ordered `source-bound-route.json` in the retained road plan. The example uses the retained dated archive and the default local plan worktree. Supply a different ZIP path after a new collection.

```powershell
$scope = 'D:/IBE160-plan-speed-limits/_bmad-output/experimental-extensions/speed-limits/qualification/2026-10-27/source-bound-route.json'
python -m app.road_corridor_audit --archive ../tmp/nvdb-collector-verification/road-live-20261120.zip --scope $scope
```

The command validates page hashes, scope and complete cursor chains before reconstructing the ordered network. It emits JSON with both input digests and the archive observation window, exact relative boundaries and source chainage, original geometries and direct type 105 records. `direct_gap` and `direct_conflict` identify segments with missing or inconsistent direct coverage. `direct_intervals` shows the exact ranges, where an empty value list marks a gap and multiple values mark a conflict. Each record retains its original placement bounds, its intersection with the segment and any field codes. `scope_intermediate_nodes` compares historical and archived node identities inside the matched spans. A null archive node means the refreshed segmentation has no boundary at that exact fraction. The output has research status. Parent-link translation, authorised turns, physical signing and route and GPS qualification have their own evidence. [Offline results](../../../docs/evidence/v2-road-source-20261120.md#offline-corridor-reconstruction).

- Source pilot specification and evidence are pinned on `codex/plan-speed-limits` at `5adc6fb2c0137a3a6519d4f7ba42dd57f0e02f1c`.
- [NVDB Les](https://nvdbapiles.atlas.vegvesen.no/) supplies public road topology and type 105 records under NLOD.
- Original sign evidence and licensing are stored in [the asset manifest](../../../frontend/public/assets/road-signs/source.json).
