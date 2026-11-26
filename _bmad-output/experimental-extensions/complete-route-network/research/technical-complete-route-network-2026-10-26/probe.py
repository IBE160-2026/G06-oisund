"""Bounded read-only research probe; all files stay beside this script."""
import json, sys, urllib.request, urllib.error, datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CLIENT='ibe160-complete-route-network-research'
def request(label, query=None, url=None):
    url=url or 'https://api.entur.io/journey-planner/v3/graphql'
    body=json.dumps({'query':query}).encode() if query else None
    req=urllib.request.Request(url,data=body,headers={'ET-Client-Name':CLIENT,'User-Agent':CLIENT,'Content-Type':'application/json'})
    record={'accessed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':url,'method':'POST' if body else 'GET','query':query,'client':CLIENT}
    try:
        with urllib.request.urlopen(req,timeout=35) as r:
            raw=r.read(1500001)
            if len(raw)>1500000: raise ValueError('Bounded response exceeded 1.5MB')
            record.update(status=r.status,headers=dict(r.headers),body=json.loads(raw))
    except urllib.error.HTTPError as e:
        record.update(status=e.code,error=e.read(12000).decode(errors='replace'))
    except Exception as e: record.update(error=str(e))
    (ROOT/'imports'/f'api-{label}.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(record,ensure_ascii=False,indent=2))
if __name__=='__main__':
    label=sys.argv[1]
    query=Path(sys.argv[2]).read_text(encoding='utf-8-sig') if len(sys.argv)>2 else None
    if label=='geocode': request(label,url='https://api.entur.io/geocoder/v3/autocomplete?text=Troms%C3%B8%20sentrum&size=4&layers=venue')
    else: request(label,query)
