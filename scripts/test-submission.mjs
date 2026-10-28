import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validateConfig, validateContainer, validateOwnership, PROJECT } from './submission.mjs';
const config = () => ({ name: PROJECT, services: {
  frontend: { ports: [{host_ip:'127.0.0.1', published:'15325'}] },
  api: { ports: [{host_ip:'127.0.0.1', published:'18327'}] },
  'private-api': { ports: [{host_ip:'127.0.0.1', published:'18328'}], environment: {SUBMISSION_PROJECT:PROJECT, PRIVATE_DATABASE_URL:'postgresql://private_work@private-db/private_work', PRIVATE_DATABASE_PASSWORD_FILE:'/run/secrets/submission_password', PRIVATE_ORIGIN:'http://127.0.0.1:15325', PRIVATE_TEST_PROJECT:'ibe160-private-tests'} },
  db: { volumes:[{type:'volume',source:'submission_fictional'}] },
  'private-db': { volumes:[{type:'volume',source:'submission_private'}] },
}, volumes: { submission_fictional:{name:PROJECT+'_submission_fictional'},submission_private:{name:PROJECT+'_submission_private'} } });
test('configuration refuses wrong project, published host, storage, API and test marker', () => {
  validateConfig(config());
  for (const change of [c=>c.name='ordinary', c=>c.services.frontend.ports[0].host_ip='0.0.0.0', c=>c.services.db.volumes[0].type='bind', c=>c.volumes.submission_private.external=true, c=>c.volumes.submission_private.name='ordinary_pg', c=>c.services['private-api'].environment.PRIVATE_DATABASE_URL='postgresql://private_work@localhost/private_work', c=>c.services['private-api'].environment.PRIVATE_TEST_PROJECT='ordinary']) {
    const value = config(); change(value); assert.throws(()=>validateConfig(value));
  }
});
test('running container refuses foreign project, network, or volume before reset', () => {
  const make=()=>({Config:{Labels:{'com.docker.compose.project':PROJECT,'com.docker.compose.service':'private-db'}},NetworkSettings:{Networks:{[PROJECT+'_default']:{}}},Mounts:[{Destination:'/var/lib/postgresql/data',Type:'volume',Name:PROJECT+'_submission_private'}]});
  validateContainer(make(),'private-db','submission_private');
  for (const change of [c=>c.Config.Labels['com.docker.compose.project']='ordinary',c=>c.NetworkSettings.Networks.ordinary={},c=>c.Mounts[0].Name='ordinary_private_pg',c=>c.Mounts[0].Type='bind']) { const value=make();change(value); assert.throws(()=>validateContainer(value,'private-db','submission_private')); }
});
test('same project from another checkout/config refuses before lifecycle changes', () => {
  const make=()=>({Config:{Labels:{'com.docker.compose.project':PROJECT,'com.docker.compose.project.working_dir':'D:/clean','com.docker.compose.project.config_files':'D:/clean/compose.submission.yaml'}}});
  validateOwnership(make(),'D:/clean');
  for(const label of ['com.docker.compose.project.working_dir','com.docker.compose.project.config_files']) { const value=make();value.Config.Labels[label]='D:/ordinary';assert.throws(()=>validateOwnership(value,'D:/clean')); }
});
