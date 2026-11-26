import json, hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
load=lambda n:json.loads((root/'imports'/n).read_text(encoding='utf-8-sig'))
journeys=load('api-line20-journeys.json')['body']['data']['line']['serviceJourneys']
active=[j for j in journeys if '2026-10-26' in j['activeDates']]
from collections import Counter
variants=Counter((j['directionType'],j['quays'][0]['name'],j['lastQuay'][0]['name']) for j in active)
dates=sorted({d for j in journeys for d in j['activeDates']})
samples=load('api-selected-journeys.json')['body']['data']
summary={'access_date':'2026-10-26','line':'TRO:Line:1_20','templates':len(journeys),'active_on_2026_10_26':len(active),'observed_date_min':dates[0],'observed_date_max':dates[-1],'variants':[{'direction':k[0],'from':k[1],'to':k[2],'count':v} for k,v in variants.items()],'samples':[]}
for key,j in samples.items():
 c=j['estimatedCalls']; repeats={q:n for q,n in Counter(x['scheduledQuay']['id'] for x in c).items() if n>1}
 summary['samples'].append({'name':key,'id':j['id'],'privateCode':j['privateCode'],'direction':j['directionType'],'pattern':j['journeyPattern'],'count':len(c),'first':c[0],'last':c[-1],'destinations':list(dict.fromkeys(x['destinationDisplay']['frontText'] for x in c if x['destinationDisplay'])),'repeated_quays':repeats})
(root/'imports'/'api-observation-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
manifest=[]
for p in sorted((root/'imports').iterdir()):
 if p.is_file() and p.name!='sha256-manifest.json': manifest.append({'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(root/'imports'/'sha256-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
