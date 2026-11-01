"""UUID-scoped local probes; never reads production data or touches existing stacks."""
import json
from pathlib import Path
import secrets
import sys
import time
from uuid import uuid4
import native_reachability as n

refs=json.loads((n.OUT/'images.json').read_text())
prefix=sys.argv[2] if len(sys.argv)>2 else ''
def mount(source,target,readonly=True):
    return ['--mount',f'type=bind,source={source},target={target}'+(',readonly' if readonly else '')]
def command(label,image,tail,network='none',extra=None,forbid=True):
    directory=n.TMP/label;directory.mkdir(exist_ok=False)
    args=['docker','run','--rm','--network',network,'--read-only','--cap-drop','ALL','--security-opt','no-new-privileges:true',
          '--user','10001:10001','--tmpfs','/tmp:rw,nosuid,nodev,size=256m,mode=1777',
          *mount(n.ROOT/'scripts/operations-followup','/probe'),*mount(n.TMP,'/analysis'),*mount(directory,'/trace',False),
          '-e','LD_AUDIT=/analysis/native_audit.so','-e','O6_NATIVE_LOG=/trace/native.jsonl',
          '-e','O6_PYTHON_LOG=/trace/python.jsonl','-e','PYTHONDONTWRITEBYTECODE=1',
          '-e','PYTHONPATH=/app:/app/tests:/gate:/probe/native_site']
    if forbid:args+=['-e','O6_FORBID_SQLITE=1']
    return args+(extra or [])+[image,*tail]
def collect(label):
    directory=n.TMP/label;summary={}
    for filename in ['native.jsonl','python.jsonl']:
        files=sorted(directory.glob(filename+'*'))
        assert files,filename
        data=b''.join(p.read_bytes()for p in files)
        (n.OUT/(label+'-'+filename)).write_bytes(data)
        rows=[json.loads(line)for line in data.splitlines()]
        if filename=='native.jsonl':
            assert any(r['kind']=='audit_ready'for r in rows)
            summary['native_pids']=sorted({r['pid']for r in rows if r['kind']=='audit_ready'})
            summary['target_objects']=[r for r in rows if r['kind']=='object'and('sqlite' in r['name'].lower()or'libacl' in r['name'])]
            summary['target_bindings']=[r for r in rows if r['kind']=='binding']
            summary['object_count']=sum(r['kind']=='object'for r in rows)
        else:
            assert any(r['event']=='audit_ready'for r in rows)
            summary['python_pids']=sorted({r['pid']for r in rows if r['event']=='audit_ready'})
            summary['sqlite_events']=[r for r in rows if r['event'].startswith('sqlite3.')]
    n.save(label+'-audit-summary.json',summary)
    return summary

def main():
    if sys.argv[1]=='library-and-unit':
        for role in ['api-old','gate-old']:
            n.capture('r2-static-'+role,['docker','run','--rm','--network','none','--read-only','--cap-drop','ALL','--user','10001:10001',
              *mount(n.ROOT/'scripts/operations-followup','/probe'),*mount(n.TMP,'/analysis'),refs[role],'python','-B','/probe/native_static.py'])
            label='positive-'+role
            n.capture(label,command(label,refs[role],['python','-B','/probe/native_positive.py'],forbid=False))
            summary=collect(label)
            assert summary['sqlite_events'] and len(summary['target_objects'])>=2
            names={r['name']for r in summary['target_bindings']}
            assert {'acl_get_file','acl_set_file','acl_extended_file','acl_delete_def_file','sqlite3_open_v2'}<=names
    if sys.argv[1] in ['library-and-unit','app']:
        label=prefix+'pdf-regression'
        n.capture(label,command(label,refs['api-old'],['python','-m','pytest','-q','-p','no:cacheprovider','tests/test_pdf_import.py','tests/test_private_import.py'],
          extra=mount(n.ROOT/'Eksempelfiler','/fixtures')))
        summary=collect(label);assert not(summary['target_objects']or summary['target_bindings']or summary['sqlite_events'])
        label=prefix+'gate-jwt'
        n.capture(label,command(label,refs['gate-old'],['python','-B','/probe/native_gate_probe.py'],extra=mount(n.ROOT/'deploy/tablet/access_gate','/gate-tests')))
        summary=collect(label);assert not(summary['target_objects']or summary['target_bindings']or summary['sqlite_events'])
    elif sys.argv[1] in ['http','http-pdf']:
        suffix=uuid4().hex[:12];network='o6-native-'+suffix;db='o6-native-db-'+suffix
        password=n.TMP/('password-'+suffix);password.write_text(secrets.token_urlsafe(48))
        created_network=False;created_db=False
        try:
            n.run(['docker','network','create','--internal',network]);created_network=True
            n.run(['docker','run','-d','--name',db,'--network',network,'--network-alias','private-db','--read-only',
              '--tmpfs','/var/lib/postgresql/data:rw,nosuid,nodev,size=512m,mode=0700,uid=999,gid=999',
              '--tmpfs','/var/run/postgresql:rw,nosuid,nodev,mode=0777','--tmpfs','/tmp:rw,nosuid,nodev,mode=1777',
              '-e','POSTGRES_USER=tablet_bootstrap','-e','POSTGRES_DB=private_work','-e','POSTGRES_PASSWORD_FILE=/run/secrets/tablet_postgres_password',
              *mount(password,'/run/secrets/tablet_postgres_password'),
              *mount(n.ROOT/'deploy/tablet/init-private-role.sql','/docker-entrypoint-initdb.d/10-role.sql'),refs['db-old']]);created_db=True
            for _ in range(100):
                p=n.run(['docker','exec',db,'pg_isready','-h','127.0.0.1','-U','tablet_bootstrap','-d','private_work'],check=False)
                if p.returncode==0:break
                time.sleep(.2)
            else:raise RuntimeError('Own tmpfs database not ready')
            extra=['-e','OPERATIONS_DISPOSABLE=1','-e','APP_MODE=private-local','-e','PRIVATE_LOOPBACK_DEVELOPMENT=1',
              '-e','PRIVATE_DATABASE_URL=postgresql://private_work@private-db/private_work',
              '-e','PRIVATE_DATABASE_PASSWORD_FILE=/run/secrets/tablet_postgres_password',*mount(password,'/run/secrets/tablet_postgres_password')]
            # Run mutation families first: that harness explicitly requires an empty account table.
            if sys.argv[1]=='http':
                label=prefix+'http-families'
                n.capture(label,command(label,refs['api-old'],['python','-B','/probe/native_http_loss.py'],network,
                  extra+['-e','PRIVATE_ORIGIN=http://127.0.0.1:18000']))
                summary=collect(label);assert not(summary['target_objects']or summary['target_bindings']or summary['sqlite_events'])
            label=prefix+'http-pdf'
            n.capture(label,command(label,refs['api-old'],['python','-B','/probe/native_http_pdf.py'],network,
              extra+['-e','PRIVATE_ORIGIN=http://127.0.0.1:8000',*mount(n.ROOT/'Eksempelfiler','/fixtures')]))
            summary=collect(label);assert not(summary['target_objects']or summary['target_bindings']or summary['sqlite_events'])
        finally:
            if created_db:n.run(['docker','rm','-f',db])
            if created_network:n.run(['docker','network','rm',network])
            password.unlink()
            n.save(prefix+'http-fixture-cleanup.json',dict(network=network,container=db,password_removed=not password.exists(),existing_volumes_used=False))
    else:raise SystemExit('Unknown phase')


if __name__=='__main__':main()
