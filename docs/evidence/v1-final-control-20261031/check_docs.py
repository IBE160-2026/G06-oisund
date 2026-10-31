from pathlib import Path
import subprocess,re,json,urllib.parse
root=Path(__file__).resolve().parents[3]
files=subprocess.check_output(['git','diff','--name-only'],cwd=root,text=True).splitlines()+['docs/evidence/v1-final-control-20261031.md']
errors=[];count=0
def anchors(text):
 result=set()
 for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$',text,re.M):
  heading=re.sub(r'[`*_]','',heading).lower()
  result.add(re.sub(r'[^\w\- ]','',heading).replace(' ','-'))
 return result
for name in files:
 if not name.endswith('.md'):continue
 p=root/name
 for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target):continue
  target=target.strip('<>');path,_,anchor=target.partition('#');dest=(p.parent/urllib.parse.unquote(path)).resolve() if path else p
  count+=1
  if not dest.exists():errors.append([name,target,'missing target'])
  elif anchor and dest.suffix=='.md' and urllib.parse.unquote(anchor) not in anchors(dest.read_text(encoding='utf-8')):errors.append([name,target,'missing anchor'])
result={'files':len([f for f in files if f.endswith('.md')]),'links_checked':count,'errors':errors}
(root/'docs/evidence/v1-final-control-20261031/document-links.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));raise SystemExit(bool(errors))
