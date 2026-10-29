from pathlib import Path
import importlib.util
import json
import os
import subprocess
import sys
root=Path(__file__).resolve().parents[1]
subprocess.run(['node','scripts/prepare-v1followup-tests.mjs'],cwd=root,check=True)
subprocess.run(['node','tmp/prepare-device-suite.cjs'],cwd=root,check=True)
spec=importlib.util.spec_from_file_location('followup',root/'scripts/verify-v1followup.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
sys.argv=[__file__,'device-browser']
runner=module.load_runner()
module.load_guard()['guard_runtime']()
state=json.loads((root/'.private-runtime/v1-acceptance-device.json').read_text(encoding='utf-8'))
env=dict(os.environ,V1_DEVICE_ENDPOINT=state['endpoint'],COMPOSE_PROJECT_NAME='ibe160-v1followup-tests',V1FOLLOWUP_REPORT=str(runner['RUN']/'report.json'),V1FOLLOWUP_OUTPUT_DIR=str(runner['RUN']/'results'))
inputs=[Path(__file__),root/'tmp/prepare-device-suite.cjs',root/'frontend/playwright.v1-device-temp.config.ts',*(root/'frontend/.v1followup-tests').glob('*.ts'),*(root/'frontend/dist').rglob('*')]
runner['execute'](['npx.cmd','playwright','test','--config=playwright.v1-device-temp.config.ts','private-d1-remediation.spec.ts','private-d2-qualification.spec.ts'],root/'frontend',env,inputs,timeout=1800)
