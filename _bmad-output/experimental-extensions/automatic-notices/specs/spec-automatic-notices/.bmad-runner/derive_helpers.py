from pathlib import Path
import subprocess,sys
root=Path('D:/IBE160-plan-automatic-notices'); spec=root/'_bmad-output/experimental-extensions/automatic-notices/specs/spec-automatic-notices'; mem=root/'_bmad/scripts/memlog.py'
def log(kind,text):
    r=subprocess.run([sys.executable,str(mem),'append','--workspace',str(spec),'--type',kind,'--text',text],capture_output=True,text=True)
    if r.returncode: raise RuntimeError(r.stderr+r.stdout)
def derive(name,content,kind='decision'):
    for block in content.strip().split('\n\n'):
        if not block.startswith(('#','>','---')): log(kind,'Derivation '+name+': '+block)
    (spec/name).write_text(content,encoding='utf-8')
