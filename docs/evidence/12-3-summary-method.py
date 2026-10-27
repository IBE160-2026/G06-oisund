from pathlib import Path
import json,sys
root=Path.cwd()
record=Path(sys.argv[1]); d=json.loads(record.read_text(encoding="utf-8"))
rows=json.loads((root/d["measurements"]).read_text(encoding="utf-8"))
positive=[r for r in rows if r["test"].startswith(("real private surfaces ","rendered demo states ","rendered API assessment "))]
states=[r["values"] for r in positive if isinstance(r["values"],dict) and "environment" in r["values"]]
texts=[v for s in states for v in s["text"]]; boundaries=[v for s in states for v in s["boundaries"]]
focus=[r["values"] for r in positive if r["state"].endswith("-focus") and isinstance(r["values"],dict)]
stops=[v for f in focus for v in f["results"]]; pairs=[v for f in focus for v in f["pixelResults"]]
native=[v for r in positive if r["state"].endswith("-native-indicators") for v in r["values"]]
result={"source_record":record.as_posix(),"run":record.stem.removeprefix("12-3-browser-"),"scope":"positive actual product states only; deliberate negative helper probes excluded", "state_measurements":len(states),"text_measurements":len(texts),"minimum_text_ratio":min(v["ratio"] for v in texts),"boundary_measurements":len(boundaries),"minimum_boundary_ratio":min(v["ratio"] for v in boundaries),"keyboard_stops":len(stops),"minimum_focus_adjacent_ratio":min(v["ratio"] for v in stops),"minimum_focus_width":min(v["width"] for v in stops),"focus_hosts_with_unfocused_signature_checked":len(pairs),"actual_same_pixel_pairs":sum(not p["cacheHit"] for p in pairs),"representative_cache_results":sum(p["cacheHit"] for p in pairs),"minimum_same_pixel_changed_area_to_required_area":min(p["changedArea"]/p["requiredArea"] for p in pairs),"native_states":len(native),"minimum_native_edge_ratio":min(min(v["edgeRatios"]) for v in native),"checked_glyph_samples":sum(v["checked"] for v in native),"minimum_checked_glyph_component_area":min(v["glyph"]["area"] for v in native if v["checked"]),"glyph_pixel_contrast_threshold":3,"unmeasured_product_layers":[v for s in states for v in s["unmeasured"]],"critical_clipping":[v for s in states for v in s["clipping"]],"user_agents":sorted({s["environment"]["userAgent"] for s in states}),"root_font_sizes":sorted({s["environment"]["rootFontSize"] for s in states}),"unmeasured":["native calendar/time-picker icons/popups","native select-arrow and disclosure-marker pixels","physical Lenovo Pad / Android / Brave","OS/browser chrome zoom","assistive technology"],"owner_acceptance":"pending"}
print(json.dumps(result,indent=2))
