"""Host lifecycle is mocked; never mounts Docker socket or host production data."""
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch, Mock
from contextlib import ExitStack

spec = importlib.util.spec_from_file_location('restore_ops', Path(__file__).with_name('bussassistentctl.py'))
ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ops)
SHA = 'a' * 40


class RestoreOperations(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.maintenance = self.root / 'maintenance'
        self.maintenance.mkdir()
        self.path = self.root / 'releases' / SHA
        self.path.mkdir(parents=True)
        self.operation = 'b' * 32
        self.directory = self.root / 'restore' / self.operation
        self.directory.mkdir(parents=True)
        (self.directory / 'replacement.sql').write_text('BEGIN; COMMIT;')
        self.state = dict(operation=self.operation, release=SHA, stage='closed', attempts=0,
            source_fingerprint='source', prior_fingerprint='prior', expected={'schema':15,'business':{}},
            retained={}, authority_fingerprint='quarantined')
        for key, value in [('ROOT',self.root),('MAINTENANCE',self.maintenance),('BACKUPS',self.root/'backups')]:
            p = patch.object(ops,key,value); p.start(); self.addCleanup(p.stop)

    def test_pending_blocks_every_normal_mutation(self):
        (self.maintenance/'pending.json').write_text('{}')
        for action in ['start','deploy','rollback','enable','reboot','gateway-switch',
                       'prepare-db','restore-initial','install-tools','backup','recovery-issue']:
            with self.subTest(action=action), patch.object(sys,'argv',['ctl',action]), patch.object(ops,'run') as run:
                with self.assertRaisesRegex(ValueError,'inhibited'):
                    ops.main()
                run.assert_not_called()
        with self.assertRaisesRegex(ValueError,'inhibited'):
            ops.start(self.path)

    def test_wrong_source_and_release_reject_before_close(self):
        with patch.object(ops,'close_restore') as close, patch.object(ops,'release',return_value=self.path):
            for name, digest in [('../source.dump','0'*64),('source.dump','0'*64),('20260101T000000Z-'+SHA+'.dump','bad')]:
                with self.assertRaises(ValueError):
                    ops.begin_restore(name,digest,SHA)
            close.assert_not_called()
        with patch.object(ops,'release',side_effect=[self.path,self.root/'other']), patch.object(ops,'verify_release_images') as images:
            with self.assertRaisesRegex(ValueError,'mismatch'):
                ops.begin_restore('20260101T000000Z-'+SHA+'.dump','0'*64,SHA)
            images.assert_not_called()

    def source(self):
        ops.BACKUPS.mkdir()
        name='20260101T000000Z-'+SHA+'.dump'
        path=ops.BACKUPS/name
        path.write_bytes(b'synthetic trusted archive')
        path.chmod(0o640)
        return name,path,hashlib.sha256(path.read_bytes()).hexdigest()

    def beginning(self):
        stack=ExitStack()
        for name in ['verify_release_images','restore_guards','resume_restore']:
            stack.enter_context(patch.object(ops,name))
        stack.enter_context(patch.object(ops,'release',return_value=self.path))
        stack.enter_context(patch.object(ops,'preflight_restore',return_value={
            'schema':15,'business':{},'database_fingerprint':'source'}))
        return stack

    def test_begin_snapshots_same_bytes_and_retains_source(self):
        name,path,digest=self.source()
        with self.beginning():ops.begin_restore(name,digest,SHA)
        state=json.loads((self.maintenance/'pending.json').read_text())
        snapshot=self.root/'restore'/state['operation']/'source.dump'
        self.assertEqual(snapshot.read_bytes(),path.read_bytes())
        self.assertEqual(state['sha256'],digest)
        self.assertEqual(state['stage'],'prepared')

    def test_tamper_symlink_and_writable_source_fail_before_pending(self):
        name,path,digest=self.source()
        with self.beginning(), self.assertRaisesRegex(ValueError,'digest mismatch'):
            ops.begin_restore(name,'0'*64,SHA)
        self.assertFalse((self.maintenance/'pending.json').exists())
        path.chmod(0o666)
        with self.beginning(), self.assertRaisesRegex(ValueError,'Unsafe'):
            ops.begin_restore(name,digest,SHA)
        path.unlink()
        target=self.root/'archive';target.write_bytes(b'synthetic trusted archive')
        path.symlink_to(target)
        with self.beginning(), self.assertRaises(OSError):ops.begin_restore(name,digest,SHA)
        self.assertFalse((self.maintenance/'pending.json').exists())

    def test_wrong_source_owner_fails_before_pending(self):
        name,path,digest=self.source()
        info=path.stat()
        with self.beginning(), patch.object(ops.os,'fstat',return_value=Mock(st_mode=info.st_mode,st_uid=10001,st_nlink=1)), \
             self.assertRaisesRegex(ValueError,'Unsafe'):
            ops.begin_restore(name,digest,SHA)
        self.assertFalse((self.maintenance/'pending.json').exists())

    def test_durable_stage_and_no_reopen_after_unverified(self):
        ops.save_restore(self.state,'replacing')
        self.assertEqual(json.loads((self.maintenance/'pending.json').read_text())['stage'],'replacing')
        self.assertFalse((self.maintenance/'pending.new').exists())
        with patch.object(ops,'restore_state',return_value=self.state), patch.object(ops,'start') as start:
            with self.assertRaisesRegex(ValueError,'not ready'):
                ops.reopen_restore()
            start.assert_not_called()

    def run_resume(self, stage, fingerprint='source', fail=False):
        self.state['stage']=stage
        def offline(path,action):
            return {'business':{},'schema':15,'authority_fingerprint':'quarantined'}
        with patch.object(ops,'restore_state',return_value=self.state), patch.object(ops,'release',return_value=self.path), \
             patch.object(ops,'close_restore'), patch.object(ops,'database_fingerprint',return_value=Mock(stdout=fingerprint)), \
             patch.object(ops,'offline',side_effect=offline), patch.object(ops.subprocess,'run'), patch.object(ops,'compose') as compose:
            if fail:
                compose.side_effect=subprocess.CalledProcessError(1,'synthetic')
            if fail:
                with self.assertRaises(subprocess.CalledProcessError):ops.resume_restore()
            else:ops.resume_restore()
            return compose.call_args_list

    def test_ambiguous_success_never_repeats_replacement(self):
        calls=self.run_resume('replacing','source')
        self.assertFalse(any('psql' in call.args for call in calls))
        self.assertEqual(self.state['stage'],'verified')

    def test_proven_rollback_retries_once_and_failure_stays_replacing(self):
        calls=self.run_resume('replacing','prior',True)
        self.assertEqual(self.state['stage'],'replacing')
        self.assertEqual(self.state['attempts'],1)
        self.assertEqual(sum(any('exec psql' in str(arg) for arg in call.args) for call in calls),1)
        self.assertTrue((self.maintenance/'pending.json').exists())

    def test_unknown_or_exhausted_replacement_stays_closed(self):
        for fingerprint, attempts in [('unknown',0),('prior',3)]:
            self.state['attempts']=attempts
            with self.assertRaisesRegex(ValueError,'investigation'):
                self.run_resume('replacing',fingerprint)

    def test_verified_resume_cannot_reset_credentials(self):
        self.state['stage']='verified'
        with patch.object(ops,'restore_state',return_value=self.state), patch.object(ops,'release',return_value=self.path), patch.object(ops,'offline') as offline:
            with self.assertRaisesRegex(ValueError,'already verified'):
                ops.resume_restore()
            offline.assert_not_called()

    def test_interrupted_retention_never_replaces_or_requarantines(self):
        calls=self.run_resume('retaining')
        self.assertFalse(any('psql' in call.args for call in calls))
        self.assertEqual(self.state['stage'],'verified')

    def test_reopening_requires_same_authority_and_business(self):
        self.state['stage']='verified'
        ops.save_restore(self.state,'verified')
        for check in [{'business':{'changed':True},'authority_fingerprint':'quarantined'},
                      {'business':{},'authority_fingerprint':'old-hashes'}]:
            with patch.object(ops,'restore_state',return_value=self.state), patch.object(ops,'release',return_value=self.path), \
                 patch.object(ops,'close_restore'), patch.object(ops,'offline',return_value=check), patch.object(ops,'start') as start:
                with self.assertRaisesRegex(ValueError,'verification failed'):ops.reopen_restore()
                start.assert_not_called()

    def test_precommit_crash_stays_opening_then_retry_tolerates_retention(self):
        ops.save_restore(self.state,'verified')
        with patch.object(ops,'restore_state',return_value=self.state), patch.object(ops,'release',return_value=self.path), \
             patch.object(ops,'close_restore') as close, patch.object(ops,'offline',return_value={
                 'business':{},'authority_fingerprint':'quarantined'}), patch.object(ops,'compose'), \
             patch.object(ops,'ready',side_effect=KeyboardInterrupt), patch.object(ops,'run') as run:
            with self.assertRaises(KeyboardInterrupt):ops.reopen_restore()
            self.assertEqual(close.call_count,2)
            self.assertEqual(json.loads((self.maintenance/'pending.json').read_text())['stage'],'opening')
            run.assert_not_called()
        self.opening_mocks({'business':{'retention-changed':True},'authority_fingerprint':'quarantined'})
        self.assertFalse((self.maintenance/'pending.json').exists())

    def opening_mocks(self, checked, late_failure=False):
        with patch.object(ops,'restore_state',return_value=self.state), patch.object(ops,'release',return_value=self.path), \
             patch.object(ops,'close_restore'), patch.object(ops,'offline',return_value=checked) as offline, \
             patch.object(ops,'compose'), patch.object(ops,'ready'), patch.object(ops,'run'), \
             patch.object(ops,'start'), patch.object(ops,'wait_tunnel') as wait:
            if late_failure:wait.side_effect=ValueError('Accepted traffic then connectivity failed')
            if late_failure:
                with self.assertRaises(ValueError):ops.reopen_restore()
            else:ops.reopen_restore()
            return offline.call_count

    def test_late_failure_never_reinstates_stale_fingerprints(self):
        ops.save_restore(self.state,'verified')
        self.opening_mocks({'business':{},'authority_fingerprint':'quarantined'},True)
        self.assertFalse((self.maintenance/'pending.json').exists())
        self.assertEqual(self.state['stage'],'ingress-committed')
        self.assertEqual(self.opening_mocks({'business':{'new-work':True},'authority_fingerprint':'fresh-passwords'}),0)

    def test_crash_at_ingress_commit_does_not_reverify_credentials(self):
        ops.save_restore(self.state,'ingress-committed')
        self.assertEqual(self.opening_mocks({'business':{},'authority_fingerprint':'changed'}),0)

    def test_stop_does_not_reenter_systemd_helper_lock(self):
        def compose(path,*args,**kwargs):
            return Mock(stdout='private-db\n' if args[0]=='ps' else '0\n')
        with patch.object(ops,'compose',side_effect=compose) as dc, patch.object(ops,'run') as run, \
             patch.object(ops.subprocess,'run',return_value=Mock(returncode=3)):
            ops.close_restore(self.path)
        self.assertEqual(run.call_args.args[0],['systemctl','stop','cloudflared'])
        self.assertTrue(any(c.args[1]=='up' and c.args[-1]=='private-db' for c in dc.call_args_list))

    def test_guard_definitions_fail_closed_and_keep_restrictions(self):
        root=Path(__file__).parent
        for unit in ['bussassistent.service','cloudflared.service']:
            self.assertIn('ConditionPathExists=!/etc/bussassistent/maintenance/pending.json',(root/unit).read_text())
        compose=(root/'compose.yaml').read_text()
        self.assertEqual(compose.count('test -r /maintenance; test -x /maintenance'),3)
        self.assertEqual(compose.count('/etc/bussassistent/maintenance:/maintenance:ro'),3)
        self.assertEqual(compose.count('cap_drop: [ALL]'),4)
        self.assertEqual(compose.count('read_only: true'),4)

    def test_offline_timeout_removes_only_its_named_container(self):
        with patch.object(ops,'compose',side_effect=subprocess.TimeoutExpired('synthetic',180)) as compose, \
             patch.object(ops.subprocess,'run') as run:
            with self.assertRaises(subprocess.TimeoutExpired):ops.offline(self.path,'migrate')
        args=compose.call_args.args
        name=args[args.index('--name')+1]
        self.assertTrue(name.startswith('bussassistent-restore-offline-'))
        self.assertIn('PGOPTIONS=-c lock_timeout=5s -c statement_timeout=120s -c transaction_timeout=120s',args)
        self.assertEqual(run.call_args.args[0],['docker','rm','-f',name])

    def test_sql_prefix_precedes_real_subprocess_descriptor_writes(self):
        archive=self.directory/'source.dump';archive.write_bytes(b'synthetic archive')
        target=self.directory/'assembled.sql'
        def transport(path,*args,**kwargs):
            if '--list' in args:return Mock(stdout=b'; synthetic TOC\n')
            return subprocess.run([sys.executable,'-c',"import sys;sys.stdout.write('SET statement_timeout = 0;\\nSET lock_timeout = 0;\\nSET transaction_timeout = 0;\\n-- Name: restored\\nCREATE TABLE restored(id integer);\\n')"],
                                  stdout=kwargs['stdout'],check=True)
        with patch.object(ops,'compose',side_effect=transport):ops.restore_sql(self.path,archive,target)
        content=target.read_text()
        self.assertTrue(content.startswith('BEGIN;\n'))
        self.assertLess(content.index('DROP SCHEMA'),content.index('CREATE TABLE restored'))
        self.assertTrue(content.endswith('COMMIT;\n'))
        self.assertNotIn('timeout = 0',content)
        for name,value in [('lock_timeout','5s'),('statement_timeout','120s'),('transaction_timeout','120s')]:
            self.assertIn("SET LOCAL "+name+"='"+value+"';",content)

    def test_fifo_rejected_without_blocking_and_failed_copies_removed(self):
        ops.BACKUPS.mkdir()
        name='20260101T000000Z-'+SHA+'.dump'
        os.mkfifo(ops.BACKUPS/name)
        with self.beginning(), self.assertRaisesRegex(ValueError,'Unsafe'):
            ops.begin_restore(name,'0'*64,SHA)
        self.assertEqual(list((self.root/'restore').iterdir()),[self.directory])

    def test_completed_copies_expire_but_pending_material_survives(self):
        import time
        (self.directory/'source.dump').write_bytes(b'synthetic-sensitive')
        receipt=self.directory/'completed.json';receipt.write_text('{}')
        old=time.time()-172801;os.utime(receipt,(old,old))
        ops.save_restore(self.state,'verified')
        with patch.object(ops,'restore_state',return_value=self.state):ops.prune_restore_copies()
        self.assertTrue((self.directory/'source.dump').exists())
        (self.maintenance/'pending.json').unlink()
        ops.prune_restore_copies()
        self.assertFalse((self.directory/'source.dump').exists())
        self.assertTrue(receipt.exists())

    def test_status_is_safe_metadata_only(self):
        import contextlib,io
        ops.save_restore(self.state,'opening')
        output=io.StringIO()
        with patch.object(ops,'restore_state',return_value=self.state),contextlib.redirect_stdout(output):ops.restore_status()
        result=json.loads(output.getvalue())
        self.assertEqual(result['next_action'],'restore-reopen')
        self.assertNotIn('authority_fingerprint',output.getvalue())

    def test_preflight_timeout_removes_named_check_and_database(self):
        calls=[]
        def run(args,**kwargs):
            calls.append(args)
            if 'app.manage' in args:raise subprocess.TimeoutExpired('synthetic',180)
            return Mock(stdout='')
        config={'services':{'private-db':{'image':'synthetic-db'},'private-api':{'image':'synthetic-api'}}}
        with patch.object(ops,'compose',return_value=Mock(stdout=json.dumps(config))), \
             patch.object(ops,'restore_sql'),patch.object(ops,'run',side_effect=run), \
             patch.object(ops.subprocess,'run',return_value=Mock(returncode=0)) as direct:
            with self.assertRaises(subprocess.TimeoutExpired):ops.preflight_restore(self.path,self.directory/'source.dump',self.directory)
        checks=[c for c in calls if 'app.manage' in c]
        name=checks[0][checks[0].index('--name')+1]
        self.assertTrue(name.startswith('bussassistent-restore-check-'))
        self.assertIn(['docker','rm','-f',name],[c.args[0] for c in direct.call_args_list])
        self.assertTrue(any(c[:4]==['docker','rm','-f','-v'] for c in calls))

    def test_initial_confirmation_requires_quarantine_receipt(self):
        with patch.object(sys,'argv',['ctl','confirm-data',SHA]),patch.object(ops,'release',return_value=self.path), \
             patch.object(ops,'CONFIG',self.root/'server.env'),patch.object(ops,'database_summary') as summary:
            with self.assertRaises(FileNotFoundError):ops.main()
            summary.assert_not_called()

    def test_legacy_data_ready_cannot_bypass_initial_quarantine(self):
        marker=self.root/'data-ready';marker.write_text(SHA)
        with patch.object(sys,'argv',['ctl','deploy',SHA]),patch.object(ops,'release',return_value=self.path), \
             patch.object(ops,'CONFIG',self.root/'server.env'),patch.object(ops,'DATA_READY',marker), \
             patch.object(ops,'verify_release_images') as images:
            with self.assertRaises(FileNotFoundError):ops.main()
            images.assert_not_called()

    def initial_import(self, fail_quarantine=False):
        uploads=self.root/'uploads';uploads.mkdir()
        archive=uploads/'initial.dump';archive.write_bytes(b'synthetic initial archive')
        digest=hashlib.sha256(archive.read_bytes()).hexdigest()
        marker=self.root/'data-ready'
        events=[]
        checked={'business':{'accounts':{'rows':2}},'authority_fingerprint':'quarantined'}
        def compose(path,*args,**kwargs):
            if 'pg_restore' in args:
                self.assertIn('--single-transaction',args)
                self.assertEqual(kwargs['stdin'].read(),archive.read_bytes())
                events.append('import')
            return Mock(stdout='0\n')
        def offline(path,action):
            events.append(action)
            if action=='restore-quarantine' and fail_quarantine:
                raise ValueError('synthetic quarantine transaction failure')
            return checked
        with patch.object(ops,'UPLOADS',uploads),patch.object(ops,'DATA_READY',marker), \
             patch.object(ops,'CONFIG',self.root/'server.env'),patch.object(ops,'release',return_value=self.path), \
             patch.object(ops,'compose',side_effect=compose),patch.object(ops,'offline',side_effect=offline), \
             patch.object(ops,'database_summary') as summary,patch.object(ops,'start') as start:
            if fail_quarantine:
                with self.assertRaisesRegex(ValueError,'quarantine transaction failure'):ops.restore_initial(SHA,digest)
                self.assertFalse((self.root/'initial-quarantined.json').exists())
                with patch.object(sys,'argv',['ctl','confirm-data',SHA]),self.assertRaises(FileNotFoundError):ops.main()
                self.assertFalse(marker.exists())
                summary.assert_not_called()
            else:
                ops.restore_initial(SHA,digest)
                self.assertEqual(events,['import','restore-inspect','migrate','restore-inspect','restore-quarantine','restore-verify'])
                self.assertEqual(json.loads((self.root/'initial-quarantined.json').read_text()),
                                 {'release':SHA,'authority_fingerprint':'quarantined'})
                self.assertFalse(marker.exists())
                with patch.object(sys,'argv',['ctl','confirm-data',SHA]):ops.main()
                self.assertEqual(events[-1],'restore-verify')
                self.assertEqual(marker.read_text(),SHA+'\n')
                summary.assert_called_once_with(self.path)
            start.assert_not_called()

    def test_initial_import_quarantine_receipt_and_confirmation(self):
        self.initial_import()

    def test_initial_quarantine_failure_blocks_confirmation(self):
        self.initial_import(fail_quarantine=True)


if __name__=='__main__':unittest.main()
