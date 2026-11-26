import json,urllib.request,urllib.parse,datetime,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parent
ALLOWED=('https://ws.geonorge.no/','https://nvdbapiles.atlas.vegvesen.no/','https://register.geonorge.no/')
def get(name,url):
    assert url.startswith(ALLOWED)
    logpath=BASE/'requests.jsonl'
    logs=logpath.read_text(encoding='utf-8').splitlines() if logpath.exists() else []
    assert len(logs)<45, 'Request budget exhausted'
    entry={'name':name,'url':url,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request=urllib.request.Request(url,headers={'X-Client':'IBE160-speed-planning','User-Agent':'IBE160-speed-planning'})
        with urllib.request.urlopen(request,timeout=35) as response:
            data=response.read(3000001)
            assert len(data)<=3000000,'Response over budget'
            entry.update(status=response.status,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
        (BASE/(name+'.json')).write_bytes(data)
        result=json.loads(data) if data.lstrip().startswith((b'{',b'[')) else data.decode('utf-8')
    except Exception as error:
        entry['error']=str(error); result=None
    with logpath.open('a',encoding='utf-8') as f: f.write(json.dumps(entry,ensure_ascii=False)+'\n')
    return result
if __name__=='__main__':
    import sys
    if sys.argv[1]=='initial':
        config=get('swagger-config','https://nvdbapiles.atlas.vegvesen.no/v3/api-docs/swagger-config')
        print(json.dumps(config,ensure_ascii=False)[:3500])
        for label,query in [('polaria','Strandvegen 2'),('south','Kvaloyvegen 1'),('langnes','Kvaloyvegen 300'),('airport','Flyplassvegen 1')]:
            query=query.replace('Kvaloy','Kval\u00f8y')
            url='https://ws.geonorge.no/adresser/v1/sok?'+urllib.parse.urlencode({'sok':query,'kommunenummer':'5501','treffPerSide':1,'utkoordsys':'25833'})
            result=get('address-'+label,url)
            print(label,json.dumps(result,ensure_ascii=False)[:2600])
