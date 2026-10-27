import json,hashlib,datetime
from pathlib import Path
P=Path(__file__).resolve().parent
def read(n): return json.loads((P/(n+'.json')).read_text(encoding='utf-8-sig'))
def rows(n):
 d=read(n)
 return d if isinstance(d,list) else d.get('objekter',d.get('vegnettsrutesegmenter',[]))
def select(n,lid,lo=0,hi=1):
 return [(n,s) for s in sorted(rows(n),key=lambda s:s['startposisjon']) if s['veglenkesekvensid']==lid and s['startposisjon']>=lo-1e-8 and s['sluttposisjon']<=hi+1e-8]
chain=[]
chain+=select('pilot-named-roads',1109722)
chain+=select('pilot-named-roads',1109517,0,.9902808)
for lid in [1126588,1126029,1126527,1126027]: chain+=select('surface-r1-r2',lid)
chain+=select('pilot-north-roads',1126030,.88033387,1)+select('pilot-north-roads',1126030,0,.62975708)
chain+=select('surface-r2-r3',1126028)
chain+=select('pilot-north-roads',1125949,.65287709,1)+select('pilot-north-roads',1125949,0,.35105026)
chain+=select('surface-r3-circle',1125918)
chain+=select('airport-circle',1125950,.87462251,1)+select('airport-circle',1125950,0,.05053167)
chain+=select('surface-circle-exit',1126506)
gaps=[]; out=[]; distance=0
for i,(src,s) in enumerate(chain):
 if i and chain[i-1][1].get('sluttnode')!=s.get('startnode'): gaps.append({'before':i,'from':chain[i-1][1].get('sluttnode'),'to':s.get('startnode')})
 out.append(dict(occurrence=i+1,source=src+'.json',reference=s['referanse'],link=s['veglenkesekvensid'],start=s['startposisjon'],end=s['sluttposisjon'],from_node=s.get('startnode'),to_node=s.get('sluttnode'),source_length_m=s['lengde'],chainage_m=round(distance,3),fields=s.get('feltoversikt'),geometry_srid=s['geometri']['srid'],geometry=s['geometri']['wkt'],metadata=s.get('metadata')))
 distance+=s['lengde']
logs=[json.loads(x) for x in (P/'requests.jsonl').read_text().splitlines()]
hash_errors=[x['name'] for x in logs if 'sha256' in x and hashlib.sha256((P/(x['name']+'.json')).read_bytes()).hexdigest()!=x['sha256']]
assert not gaps and not hash_errors
ring_lengths={str(lid):round(sum(s['source_length_m'] for s in out if s['link']==lid),3) for lid in [1126029,1126030,1125949,1125950]}
summary={'scope':'source-document audit; not product test or physical validation','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_requests':len(logs),'downloaded_bytes':sum(x.get('bytes',0) for x in logs),'hash_errors':hash_errors,'candidate_segments':len(out),'node_gaps':gaps,'candidate_length_m':round(distance,3),'start_node':out[0]['from_node'],'end_node':out[-1]['to_node'],'roundabout_lengths_m':ring_lengths,'r2_to_r3_corrected_m':round(ring_lengths['1126030']+242.984,3),'r4_change_node':'3251245','r4_to_end_m':round(sum(s['source_length_m'] for s in out if s['link']==1126506),3),'not_qualified':['all turn restrictions and vehicle access','physical signs and temporary/variable regulation','GPS confidence and geometric error model','operational source freshness','final icon bytes/license manifest']}
(P/'source-bound-route.json').write_text(json.dumps({'status':'planning candidate; all increasing positions; not driving authorization','summary':summary,'segments':out},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(P/'local-audit.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
