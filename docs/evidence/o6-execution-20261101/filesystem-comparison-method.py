import hashlib,json,subprocess,tarfile,uuid
from pathlib import Path
ROOT=Path.cwd();OUT=ROOT/'docs/evidence/o6-execution-20261101';TMP=ROOT/'tmp/o6-execution-20261101'

def run(args):return subprocess.run(args,capture_output=True,check=True).stdout

def inventory(ref):
 container='o6-artifact-'+uuid.uuid4().hex[:12];archive=TMP/(container+'.tar')
 try:
  run(['docker','create','--name',container,'--network','none','--entrypoint','true',ref])
  run(['docker','export','-o',str(archive),container])
  result={}
  with tarfile.open(archive)as tar:
   for entry in tar:
    name=entry.name.lstrip('./')
    if name in ['etc/hostname','etc/hosts','etc/resolv.conf']or name.startswith(('dev/','proc/','sys/')):continue
    if entry.isfile():
     f=tar.extractfile(entry);result[name]={'sha256':hashlib.file_digest(f,'sha256').hexdigest(),'mode':entry.mode,'uid':entry.uid,'gid':entry.gid}
    elif entry.issym()or entry.islnk():result[name]={'link':entry.linkname,'mode':entry.mode,'type':entry.type.decode()}
  return result
 finally:
  run(['docker','rm','-v',container])
  if archive.exists():archive.unlink()

refs={'api':'ibe160-o6-api:20261101-r1','access-gate':'ibe160-o6-gate:20261101-r1','postgres':'ibe160-o6-postgres:20261101-r2','gateway':'sha256:18f942c0107fa36b2fff8e11759d64ee08244fe115195e8e89bab03f4fc984c0'}
results={}
for role,ref in refs.items():
 before=inventory(ref);after=inventory('bussassistent-'+role+':5e521cbc658594a47c4568d352a50e46309573c4')
 differences={p:{'qualified':before.get(p),'staged':after.get(p)}for p in set(before)|set(after)if before.get(p)!=after.get(p)}
 results[role]={'qualified':ref,'staged':'bussassistent-'+role+':5e521cbc658594a47c4568d352a50e46309573c4','qualified_files':len(before),'staged_files':len(after),'differences':differences}
 print(role,len(differences),'differences',flush=True)
 (OUT/'staged-filesystem-comparison.json').write_text(json.dumps(results,indent=2)+'\n')

