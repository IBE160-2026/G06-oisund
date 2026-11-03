"""Scope/stop/rollback boundaries without production data, Docker or services."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('gateway_ops',Path(__file__).with_name('bussassistentctl.py'))
ops=importlib.util.module_from_spec(spec);spec.loader.exec_module(ops)
IMAGE='sha256:'+'e'*64


class GatewayMaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.old=Path(self.tmp.name)/('a'*40);self.new=Path(self.tmp.name)/('b'*40)
        for root in [self.old,self.new]:
            for name in ['backend/Dockerfile','frontend/source.ts','deploy/tablet/access_gate/gate.py',
                         'deploy/tablet/nginx-main.conf','deploy/tablet/nginx.conf.template']:
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('same')
        self.initial={k:dict(id=k,image='sha256:'+'c'*64,pid=10,started='original',restarts=0)
                      for k in ['private-api','access-gate','private-db','gateway']}
        self.initial.update(tunnel='unchanged',boot_id='original')
        self.final=copy.deepcopy(self.initial);self.final['gateway'].update(id='new',image=IMAGE,pid=20)

    def config(self,root,db='postgres:fixed'):
        return subprocess.CompletedProcess([],0,stdout=json.dumps(dict(source=str(root),
             services={'private-api':{'image':'api:'+root.name},'private-db':{'image':db}})))

    def test_scope_allows_only_release_alias_difference(self):
        with patch.object(ops,'compose',side_effect=lambda root,*a,**kw:self.config(root)):
            ops.gateway_source_guard(self.old,self.new)

    def test_scope_rejects_application_or_database_changes(self):
        (self.new/'frontend/source.ts').write_text('password feature')
        with self.assertRaisesRegex(ValueError,'frontend'):
            ops.gateway_source_guard(self.old,self.new)
        (self.new/'frontend/source.ts').write_text('same')
        with patch.object(ops,'compose',side_effect=lambda root,*a,**kw:self.config(root,'postgres:new' if root==self.new else 'postgres:fixed')):
            with self.assertRaisesRegex(ValueError,'Compose'):
                ops.gateway_source_guard(self.old,self.new)

    def invoke(self, mode='ok',actual=IMAGE):
        calls=[]
        def run(args,**kw):
            calls.append(args)
            return subprocess.CompletedProcess(args,0,stdout=json.dumps([{'Id':actual}]))
        def compose(root,*args,**kw):
            calls.append((root,args))
            if mode=='failure' and root==self.new and args[0]=='up':
                raise subprocess.CalledProcessError(1,args)
        snapshots=[self.initial,self.final] if mode=='ok' else [self.initial,self.initial]
        if mode=='lifecycle':
            changed=copy.deepcopy(self.final);changed['private-api']['pid']=999
            snapshots=[self.initial,changed,self.initial]
        with patch.object(ops,'release',side_effect=lambda value=None:self.old if value is None else self.new), \
             patch.object(ops,'gateway_source_guard'),patch.object(ops,'run',side_effect=run), \
             patch.object(ops,'compose',side_effect=compose),patch.object(ops,'gateway_snapshot',side_effect=snapshots), \
             patch.object(ops,'ready'),patch.object(ops,'wait_tunnel'),patch.object(ops,'backup') as backup,patch.object(ops,'link') as link:
            try:
                ops.gateway_switch(self.new.name,IMAGE,self.old.name)
            except (ValueError,subprocess.CalledProcessError):
                self.assertFalse(link.called)
                if actual!=IMAGE:self.assertFalse(backup.called)
                raise
        return calls

    def test_switch_never_requests_other_service_or_tunnel_restart(self):
        calls=self.invoke()
        mutations=[args for row in calls if isinstance(row,tuple) for args in [row[1]] if args[0]=='up']
        self.assertEqual(mutations,[('up','-d','--no-deps','--no-build','--pull','never','gateway')])
        self.assertFalse(any(isinstance(row,list) and row[0]=='systemctl' for row in calls))
        self.assertEqual(json.loads((self.new/'gateway-maintenance.json').read_text())['after']['private-db'],self.initial['private-db'])

    def test_wrong_image_stops_before_backup_or_restart(self):
        with self.assertRaisesRegex(ValueError,'qualified artifact'):
            self.invoke(actual='sha256:'+'f'*64)

    def test_gateway_failure_restores_only_gateway(self):
        with self.assertRaises(subprocess.CalledProcessError):self.invoke('failure')

    def test_unrelated_lifecycle_change_rejects_switch_and_recovers(self):
        with self.assertRaisesRegex(ValueError,'lifecycle'):
            self.invoke('lifecycle')


if __name__=='__main__':unittest.main()
