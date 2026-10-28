import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validateConfig, validateContainer, validateRuntime, validateOwnership, PROJECT } from './submission.mjs';
const privateEnv = () => ({APP_MODE:'private-local', PRIVATE_LOOPBACK_DEVELOPMENT:'1', SUBMISSION_PROJECT:PROJECT, PRIVATE_DATABASE_URL:'postgresql://private_work@private-db/private_work', PRIVATE_DATABASE_PASSWORD_FILE:'/run/secrets/submission_password', PRIVATE_ORIGIN:'http://127.0.0.1:15325', PRIVATE_TEST_PROJECT:'ibe160-private-tests', PRIVATE_TEST_API:'http://private-api:8000', PRIVATE_TEST_ORIGIN:'http://127.0.0.1:15325'});
const ports = {frontend:[15325,15325],api:[8000,18327],'private-api':[8000,18328]};
const volumes = {db:'submission_fictional','private-db':'submission_private'};
const config = () => ({name:PROJECT,services:{
  ...Object.fromEntries(Object.entries(ports).map(([service,[target,published]])=>[service,{ports:[{host_ip:'127.0.0.1',target,published:String(published),protocol:'tcp'}],...(service==='private-api'?{environment:privateEnv()}:{})}])),
  ...Object.fromEntries(Object.entries(volumes).map(([service,source])=>[service,{volumes:[{type:'volume',source,target:'/var/lib/postgresql/data'}]}])),
},volumes:Object.fromEntries(Object.values(volumes).map(volume=>[volume,{name:PROJECT+'_'+volume}]))});
function container(service) {
  const mapping=ports[service];
  return {
    Config:{Labels:{'com.docker.compose.project':PROJECT,'com.docker.compose.service':service},Env:service==='private-api'?Object.entries(privateEnv()).map(([key,value])=>key+'='+value):[]},
    State:{Running:true,Status:'running',Health:{Status:'healthy'}},
    NetworkSettings:{Networks:{[PROJECT+'_default']:{}},Ports:mapping?{[mapping[0]+'/tcp']:[{HostIp:'127.0.0.1',HostPort:String(mapping[1])}]}:{'5432/tcp':null}},
    Mounts:volumes[service]?[{Destination:'/var/lib/postgresql/data',Type:'volume',Name:PROJECT+'_'+volumes[service]}]:[],
  };
}
const runtime = () => ['frontend','api','private-api','db','private-db'].map(container);

test('configuration refuses wrong project, ports, storage source/target and test guard', () => {
  validateConfig(config());
  for (const change of [c=>c.name='ordinary',c=>c.services.frontend.ports[0].host_ip='0.0.0.0',c=>c.services.api.ports[0].published='8000',c=>c.services.api.ports[0].target=9000,c=>c.services.frontend.ports[0].protocol='udp',c=>c.services.db.ports=[{host_ip:'127.0.0.1',published:'5432',target:5432,protocol:'tcp'}],c=>c.services.db.volumes[0].type='bind',c=>c.services['private-db'].volumes[0].target='/other-data',c=>c.volumes.submission_private.external=true,c=>c.volumes.submission_private.name='ordinary_pg']) {
    const value=config();change(value);assert.throws(()=>validateConfig(value));
  }
});
test('desired and running private API must use matching guarded storage, endpoints and origins', () => {
  for(const key of Object.keys(privateEnv())) {
    const desired=config();desired.services['private-api'].environment[key]='wrong';assert.throws(()=>validateConfig(desired),key);
    const running=container('private-api');running.Config.Env=running.Config.Env.map(value=>value.startsWith(key+'=')?key+'=wrong':value);assert.throws(()=>validateContainer(running,'private-api'),key);
  }
});
test('every service needs healthy running state; missing/duplicate frontend refuses', () => {
  validateRuntime(runtime());
  assert.throws(()=>validateRuntime(runtime().filter(value=>value.Config.Labels['com.docker.compose.service']!=='frontend')));
  const duplicate=runtime();duplicate[0]=container('api');assert.throws(()=>validateRuntime(duplicate));
  for(const service of ['frontend','api','private-api','db','private-db']) {
    for(const change of [c=>c.State.Running=false,c=>c.State.Status='exited',c=>c.State.Health.Status='unhealthy',c=>c.State.Health.Status='starting',c=>delete c.State.Health]) {
      const values=runtime();change(values.find(c=>c.Config.Labels['com.docker.compose.service']===service));assert.throws(()=>validateRuntime(values),service);
    }
  }
});
test('actual published bindings must be exact loopback ports and databases unpublished', () => {
  for(const service of ['frontend','api','private-api']) {
    const [target]=ports[service];
    for(const change of [c=>c.NetworkSettings.Ports[target+'/tcp'][0].HostIp='0.0.0.0',c=>c.NetworkSettings.Ports[target+'/tcp'][0].HostPort='9999',c=>c.NetworkSettings.Ports[target+'/tcp'].push({HostIp:'::',HostPort:'9999'}),c=>c.NetworkSettings.Ports={'9999/tcp':[{HostIp:'127.0.0.1',HostPort:String(ports[service][1])}]},c=>c.NetworkSettings.Ports[target+'/tcp']=null]) {
      const value=container(service);change(value);assert.throws(()=>validateContainer(value,service),service);
    }
  }
  for(const service of Object.keys(volumes)) {
    const value=container(service);value.NetworkSettings.Ports['5432/tcp']=[{HostIp:'127.0.0.1',HostPort:'5432'}];assert.throws(()=>validateContainer(value,service,volumes[service]));
  }
});
test('running container refuses foreign project/network/volume before reset', () => {
  validateContainer(container('private-db'),'private-db','submission_private');
  for(const change of [c=>c.Config.Labels['com.docker.compose.project']='ordinary',c=>c.NetworkSettings.Networks.ordinary={},c=>c.Mounts[0].Name='ordinary_private_pg',c=>c.Mounts[0].Type='bind',c=>c.Mounts[0].Destination='/other-data']) {
    const value=container('private-db');change(value);assert.throws(()=>validateContainer(value,'private-db','submission_private'));
  }
});
test('same project from another checkout/config refuses lifecycle changes; case follows native platform', () => {
  const make=()=>({Config:{Labels:{'com.docker.compose.project':PROJECT,'com.docker.compose.project.working_dir':'/clean/Submission','com.docker.compose.project.config_files':'/clean/Submission/compose.submission.yaml'}}});
  validateOwnership(make(),'/clean/Submission');
  for(const label of ['com.docker.compose.project.working_dir','com.docker.compose.project.config_files']) {
    const value=make();value.Config.Labels[label]='/ordinary';assert.throws(()=>validateOwnership(value,'/clean/Submission'));
    const caseOnly=make();caseOnly.Config.Labels[label]=caseOnly.Config.Labels[label].replace('Submission','submission');
    if(process.platform==='win32') assert.doesNotThrow(()=>validateOwnership(caseOnly,'/clean/Submission'));
    else assert.throws(()=>validateOwnership(caseOnly,'/clean/Submission'));
  }
});
