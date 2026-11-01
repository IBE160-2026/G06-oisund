"""Conservative Python imports and all ELF dependencies/symbols in a local image."""
import ast
from collections import deque
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0,'/analysis/pyelftools.whl')
from elftools.elf.elffile import ELFFile

roots=['/usr/local/lib','/usr/lib/x86_64-linux-gnu','/usr/local/bin','/usr/bin','/usr/sbin','/app/app','/gate']
elves={};pyfiles={};allfiles=set()
for root in roots:
    for path in Path(root).rglob('*'):
        if not path.is_file() or path.is_symlink() or path in allfiles:continue
        allfiles.add(path)
        if path.suffix=='.py':pyfiles[path]=path.read_text(errors='replace')
        with path.open('rb') as stream:
            if stream.read(4)!=b'\x7fELF':continue
            stream.seek(0);elf=ELFFile(stream);needed=[];soname=None;rpaths=[]
            for segment in elf.iter_segments():
                if segment.header.p_type=='PT_DYNAMIC':
                    for tag in segment.iter_tags():
                        if tag.entry.d_tag=='DT_NEEDED':needed.append(tag.needed)
                        if tag.entry.d_tag=='DT_SONAME':soname=tag.soname
                        if tag.entry.d_tag in ('DT_RPATH','DT_RUNPATH'):rpaths.append(getattr(tag,'rpath',getattr(tag,'runpath','')))
            references=[]
            for section in elf.iter_sections():
                if section.header.sh_type in ('SHT_DYNSYM','SHT_SYMTAB'):
                    for symbol in section.iter_symbols():
                        if symbol.name.startswith(('sqlite3_','acl_','fts5')):
                            references.append(dict(name=symbol.name,undefined=symbol['st_shndx']=='SHN_UNDEF'))
            data=path.read_bytes()
            markers=sorted(set(x.decode() for x in re.findall(rb'(?:sqlite3_[A-Za-z0-9_]+|fts5[A-Za-z0-9_]+|acl_(?:get|set|extended|delete)_[A-Za-z0-9_]+)',data)))
            elves[str(path)]=dict(sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),needed=needed,soname=soname,rpaths=rpaths,
                                  relevant_symbols=references,sqlite_acl_markers=markers[:1000],marker_count=len(markers))

# Map pure Python and binary module names. Package parents are included. All
# conditional imports are included, overapproximating the configured service.
modulepaths={};packages=set()
def modname(path):
    name=str(path)
    for base in ['/usr/local/lib/python3.13/site-packages/','/usr/local/lib/python3.13/lib-dynload/','/usr/local/lib/python3.13/','/app/','/gate/']:
        if name.startswith(base):
            value=name[len(base):]
            if value.endswith('.py'):
                value=value[:-3].replace('/','.')
                if value.endswith('.__init__'):value=value[:-9];packages.add(value)
                return value
            if '.so' in value:
                value=value.split('.cpython-')[0].split('.abi3')[0]
                if value.endswith('.so'):value=value[:-3]
                return value.replace('/','.')
    return None
for path in list(pyfiles)+[Path(p)for p in elves]:
    name=modname(path)
    if name:modulepaths.setdefault(name,[]).append(str(path))
graph={};parse_errors=[];dynamic=[]
for path,text in pyfiles.items():
    name=modname(path)
    if not name:continue
    try:tree=ast.parse(text)
    except SyntaxError:parse_errors.append(str(path));continue
    imports=set();parent=name if name in packages else name.rpartition('.')[0]
    for node in ast.walk(tree):
        if isinstance(node,ast.Import):imports.update(a.name for a in node.names)
        elif isinstance(node,ast.ImportFrom):
            base=node.module or ''
            if node.level:
                parts=parent.split('.')
                base='.'.join(parts[:len(parts)-node.level+1]+([base]if base else []))
            imports.add(base)
            imports.update(base+'.'+a.name for a in node.names if a.name!='*')
        elif isinstance(node,ast.Call):
            func=node.func
            if (isinstance(func,ast.Name)and func.id in ['__import__','eval','exec'])or(isinstance(func,ast.Attribute)and func.attr in ['import_module','CDLL','LoadLibrary','dlopen']):
                dynamic.append(dict(module=name,line=node.lineno,function=ast.unparse(func),constant_first_argument=ast.literal_eval(node.args[0]) if node.args and isinstance(node.args[0],ast.Constant) else None))
    graph[name]=sorted(imports)
entry='app.run' if 'app.run' in modulepaths else 'gate'
entries=[entry,'app.private_main'] if entry=='app.run' else [entry]
queue=deque(entries);reachable=set()
while queue:
    name=queue.popleft()
    if name in reachable or name not in modulepaths:continue
    reachable.add(name)
    for i in range(1,len(name.split('.'))):queue.append('.'.join(name.split('.')[:i]))
    queue.extend(graph.get(name,[]))

# Resolve all matching SONAMEs conservatively, not just the first load path.
byname={}
for path,record in elves.items():
    for key in [Path(path).name,record['soname']]:
        if key:byname.setdefault(key,set()).add(path)
roots_native={p for p in elves if '/site-packages/' in p}
roots_native.update(p for p in elves if p.startswith('/usr/local/bin/python'))
roots_native.update(p for m in reachable for p in modulepaths.get(m,[])if p in elves)
native=set();queue=deque(roots_native)
while queue:
    name=queue.popleft()
    if name in native:continue
    native.add(name)
    for dep in elves[name]['needed']:queue.extend(byname.get(dep,[]))
result=dict(entry_module=entry,explicit_entries=entries,python_modules_total=len(modulepaths),reachable_python_modules=sorted(reachable),
    reachable_target_python=[m for m in reachable if 'sqlite' in m.lower() or m.lower().startswith('acl')],
    reachable_dynamic_import_load_sites=[r for r in dynamic if r['module'] in reachable],parse_errors=parse_errors,
    native_roots=sorted(roots_native),native_closure=sorted(native),
    native_closure_target_evidence={p:r for p,r in elves.items()if p in native and(r['relevant_symbols']or r['sqlite_acl_markers']or 'sqlite' in p or '/libacl' in p)},
    all_elf=elves,
    target_binary_users={p:r['needed'] for p,r in elves.items()if any('libacl' in n or 'libsqlite' in n for n in r['needed'])},
    assumptions='Python conditional imports included; all third-party native extensions included; dynamic names not assumed safe solely from import closure. Symbol/string search cannot exclude arbitrary obfuscated/static code or independent code execution.')
print(json.dumps(result,sort_keys=True))
