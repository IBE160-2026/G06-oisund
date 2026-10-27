from pathlib import Path
import subprocess,json,hashlib,urllib.request,re,sys
from datetime import datetime,timezone
root=Path.cwd(); out={"observed":datetime.now(timezone.utc).isoformat(),"revision":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),"checks":[],"owner_acceptance":"pending","dependency_acceptance":{"12.1":"accepted","12.2":"accepted"}}
def check(name,value):
 out["checks"].append({"name":name,"passed":bool(value)})
 if not value: print("FAILED",name)
def get(url):
 with urllib.request.urlopen(url,timeout=15) as r: return r.read()
def sha(b): return hashlib.sha256(b).hexdigest()
before=json.loads((root/"docs/evidence/12-3-main-sync-runtime-before.json").read_text())
fmt='{'+','.join('"'+key+'":{{json '+field+'}}' for key,field in [("id",".Id"),("name",".Name"),("image",".Image"),("started",".State.StartedAt"),("restarts",".RestartCount"),("labels",".Config.Labels")])+'}'
preserved=[]
for old in before["containers"]:
 if old.get("labels",{}).get("com.docker.compose.project")=="ibe160-story123-tests":continue
 current=json.loads(subprocess.check_output(["docker","inspect","--format",fmt,old["id"]],text=True))
 check("preserved container "+old["name"],current==old);preserved.append(current)
out["preserved_containers"]=preserved
current_ids=set(subprocess.check_output(["docker","ps","-aq","--no-trunc"],text=True).split())
expected_ids={c["id"] for c in preserved}|set(subprocess.check_output(["docker","ps","-aq","--no-trunc","--filter","label=com.docker.compose.project=ibe160-story123-tests"],text=True).split())
check("no leftover probe containers",current_ids==expected_ids)
oldassets=json.loads((root/"docs/evidence/12-3-main-sync-accepted-preview-before.json").read_text())
newassets={path:sha(get("http://127.0.0.1:15312"+path)) for path in oldassets}
check("accepted15312 all7 HTTP byte hashes unchanged",newassets==oldassets);out["accepted15312_sha256"]=newassets
assets={}
for entry,path in [("/","index.html"),("/demo","demo.html"),("/private","index.html")]:
 body=get("http://127.0.0.1:15323"+entry);check("own served "+entry,body==(root/"frontend/dist"/path).read_bytes());assets[entry]=sha(body)
 for asset in re.findall(rb'(?:src|href)="(/assets/[^"]+)"',body):
  asset=asset.decode();b=get("http://127.0.0.1:15323"+asset);check("own asset "+asset,b==(root/"frontend/dist"/asset.lstrip('/')).read_bytes());assets[asset]=sha(b)
out["served15323_sha256"]=assets
names=subprocess.check_output(["git","ls-files","backend"],text=True).splitlines()
expected={n.removeprefix("backend/"):sha((root/n).read_bytes()) for n in names if (root/n).is_file()}
out["backend_sha256"]=expected
out["own_containers"]=[]
for service in ["api","private-api","db","private-db"]:
 container="ibe160-story123-tests-"+service+"-1"
 meta=json.loads(subprocess.check_output(["docker","inspect","--format",fmt,container],text=True));out["own_containers"].append(meta)
 check("own project identity "+service,meta["labels"].get("com.docker.compose.project")=="ibe160-story123-tests")
 if service in ["api","private-api"]:
  code="from pathlib import Path;import json,sys,hashlib; names=json.load(sys.stdin);print(json.dumps({n:hashlib.sha256((Path('/app')/n).read_bytes()).hexdigest() for n in names}))"
  actual=json.loads(subprocess.check_output(["docker","exec","-i",container,"python","-c",code],input=json.dumps(list(expected)),text=True))
  check("running mounted backend bytes "+service,actual==expected)
for port in [18323,18324]:check("own API health "+str(port),json.loads(get("http://127.0.0.1:"+str(port)+"/health"))["status"]=="ok")
for mode,folder in [("","dist"),("tablet-","dist-story123-tablet")]:
 identity=json.loads((root/(".private-runtime/story123-"+mode+"build.json")).read_text());built={str(p.relative_to(root)):sha(p.read_bytes()) for p in (root/"frontend"/folder).rglob('*') if p.is_file()};check(mode+"build bytes match identity",built==identity["built"])
 import importlib.util
 s=importlib.util.spec_from_file_location("r",root/"scripts/verify-story123.py");r=importlib.util.module_from_spec(s);s.loader.exec_module(r)
 check(mode+"source matches build identity",identity["source"]=={k:v for k,v in r.manifest().items() if k.startswith('frontend/src/') or k in ['frontend/package.json','frontend/package-lock.json','frontend/vite.config.ts','frontend/tsconfig.json','frontend/index.html','frontend/demo.html','frontend/vite.story123-tablet.config.ts','deploy/tablet/index.html','deploy/tablet/Dockerfile','.dockerignore','compose.tablet.yaml']})
 check(mode+"effective API identity",identity["effective_api_settings"]==r.effective_api_settings(r.build_environment(bool(mode))))
check("accepted main is ancestor",subprocess.run(["git","merge-base","--is-ancestor","origin/main","HEAD"]).returncode==0)
check("main unchanged74849ff",subprocess.check_output(["git","-C","D:/IBE160","rev-parse","HEAD"],text=True).strip()=="74849ff21bee108fe9cff93d740a96a6c6d2d7c5")
check("main worktree clean",not subprocess.check_output(["git","-C","D:/IBE160","status","--porcelain"],text=True).strip())
check("backend deployment equal accepted main",not subprocess.check_output(["git","diff","origin/main","--","backend","deploy","compose.tablet.yaml",".dockerignore"],text=True).strip())
import io,tarfile
image="ibe160-story123-gateway:main-sync-74849ff"
out["gateway_image_id"]=subprocess.check_output(["docker","image","inspect","--format","{{.Id}}",image],text=True).strip()
raw=subprocess.check_output(["docker","run","--rm","--network","none","--read-only","--entrypoint","tar",image,"-C","/usr/share/nginx/html","-cf","-","."])
with tarfile.open(fileobj=io.BytesIO(raw)) as t:files={m.name:t.extractfile(m).read() for m in t.getmembers() if m.isfile()}
out["gateway_asset_sha256"]={n:sha(b) for n,b in files.items()}
check("gateway private-only three-file asset set",len(files)==3 and set(n for n in files if n.endswith(".html"))=={"./index.html"})
js=b"".join(b for n,b in files.items() if n.endswith(".js"))
check("gateway contains theme and relative private API",b"ibe160-theme" in js and b"/private-api" in js)
check("gateway excludes demo/fictional API","PrÃƒÆ’Ã‚Â¸v en fiktiv arbeidsdag".encode() not in js and b"18323" not in js and b"legacy.invalid" not in js)
import importlib.util,socket
spec=importlib.util.spec_from_file_location("preview_audit",root/"scripts/verify-retained-data.py");preview=importlib.util.module_from_spec(spec);spec.loader.exec_module(preview);preview.PREVIEW_PORT=15323
record=json.loads((root/"tmp/story123-preview/frontend-server.json").read_text())
out["preview"]=record
check("owned preview identity and listener",preview.owned_preview(record,preview.process_identity(record["identity"]["pid"])) and preview.preview_listener(record["identity"]["pid"]))
for port in [18481,18483]:
 try:
  with socket.socket() as sock:sock.bind(("127.0.0.1",port))
  check("test preview released "+str(port),True)
 except OSError:check("test preview released "+str(port),False)
check("manual credentials present",(root/".private-runtime/story123-manual-credentials.json").is_file())
out["database_limit"]="No pre-run database byte fingerprint was captured. Preservation claims cover target isolation, container metadata and served HTTP bytes only."
Path("docs/evidence/12-3-main-sync-runtime.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(sum(c["passed"] for c in out["checks"]),"/",len(out["checks"]))
sys.exit(0 if all(c["passed"] for c in out["checks"]) else 1)
