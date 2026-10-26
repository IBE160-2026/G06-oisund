"""Document-only checks. No services, product imports, tests or location access."""
from pathlib import Path
from datetime import datetime
import subprocess, re, json, sys

AREA = Path(__file__).resolve().parents[1]
ROOT = AREA.parents[2]
SPEC = AREA / "specs/spec-position-progression"
MARKER = "EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE"
errors = []
def check(value, name):
    if not value: errors.append(name)
def read(path): return path.read_text(encoding="utf-8")
def git(*args): return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True, encoding="utf-8").strip()

check(ROOT == Path("D:/IBE160-plan-position-progression").resolve(), "worktree root")
check(Path(git("rev-parse", "--show-toplevel")).resolve() == ROOT, "repository root")
check(git("branch", "--show-current") == "codex/plan-position-progression", "branch")
check("IBE160-2026/G06-oisund" in git("remote", "get-url", "origin"), "origin")
check(not git("diff", "--cached", "--name-only"), "index remains empty")
diff = subprocess.run(["git", "-C", str(ROOT), "diff", "--check"], capture_output=True, text=True)
check(diff.returncode == 0, "git diff --check: " + diff.stdout + diff.stderr)

raw = subprocess.check_output(["git", "-C", str(ROOT), "status", "--porcelain=v1", "-uall", "-z"], text=True, encoding="utf-8")
status_entries = [x for x in raw.split("\0") if x]
paths = [x[3:] for x in status_entries]
prefix = AREA.relative_to(ROOT).as_posix() + "/"
check(all(x.startswith(prefix) for x in paths), "changed paths restricted to extension")

mds = sorted(AREA.rglob("*.md"))
broken = []
for p in mds:
    text = read(p)
    for target in re.findall(r"\[[^\]]*\]\(([^)\n]+)\)", text):
        target = target.strip().strip("<>")
        if re.match(r"^[a-zA-Z]+://", target) or target.startswith("#"): continue
        target = target.split("#", 1)[0]
        if target and not (p.parent / target).exists():
            broken.append({"file": p.relative_to(AREA).as_posix(), "target": target})
check(not broken, "local Markdown links")

current = [AREA/"README.md", AREA/"scope.md", AREA/"source-map.md", AREA/"epics.md",
           *[SPEC/x for x in ["SPEC.md","behavior.md","route-interface.md","fictional-example.md","decisions.md","technical-addendum.md","validation.md"]]]
for p in current:
    check(MARKER in read(p), "experimental marker: " + p.name)
    check("{{" not in read(p), "no unresolved template: " + p.name)

kernel = read(SPEC/"SPEC.md")
caps = re.findall(r"^- \*\*(CAP-\d+)\*\*$", kernel, re.M)
check(caps == [f"CAP-{i}" for i in range(1,7)], "six stable capability IDs")
check(kernel.count("**intent:**") == 6 and kernel.count("**success:**") == 6, "intent/success pairs")
check("open_questions: []" in kernel and "assumptions: [A3]" in kernel, "settled Q1/Q2")
for p in [SPEC/"SPEC.md", AREA/"epics.md"]:
    fm=read(p).split("---",2)[1]
    for rel in re.findall(r"^  - ([^\n]+)$",fm,re.M):
        check((p.parent/rel).exists(), "frontmatter input/companion exists: " + rel)

epic = read(AREA/"epics.md")
check(re.findall(r"^## Epic (PP-E\d+):",epic,re.M)==["PP-E1"], "exactly one epic")
stories = re.split(r"^### Story ", epic, flags=re.M)[1:]
story_ids = [re.match(r"(PP-E1-S\d+):",x).group(1) for x in stories]
check(story_ids == [f"PP-E1-S{i}" for i in range(1,5)], "four ordered unique stories")
ac_ids = re.findall(r"\*\*(PP-S\d-AC\d+) — Given\*\*",epic)
check(len(ac_ids)==29 and len(set(ac_ids))==29, "29 unique acceptance criteria")
for i,section in enumerate(stories,1):
    for token in ["As a driver,", "I want", "So that", "**Scope and value:**", "**Dependencies:**", "**Requirements:**", "**Acceptance Criteria:**", "**Small qualification tasks:**"]:
        check(token in section, f"S{i} includes {token}")
    for ac in re.findall(r"^- \*\*PP-S\d-AC\d+.*$",section,re.M):
        check("**when**" in ac and "**then**" in ac and "**and**" in ac, f"S{i} Given/When/Then/And")
defined = re.findall(r"^- (PP-FR\d+) \(",epic,re.M)
check(defined == [f"PP-FR{i}" for i in range(1,9)], "eight unique FRs")
# Expand slash shorthand only in story requirement lines to check declared coverage.
covered=set()
for line in re.findall(r"^\*\*Requirements:\*\* (.*)$",epic,re.M):
    for group, nums in re.findall(r"PP-(FR|NFR|UX)(\d+(?:/\d+)*)",line):
        covered.update(f"PP-{group}{n}" for n in nums.split("/"))
check(set(defined)<=covered, "FR story coverage")
check({f"PP-NFR{i}" for i in range(1,6)}<=covered, "NFR story coverage")
check({f"PP-UX{i}" for i in range(1,4)}<=covered, "UX story coverage")

example=read(SPEC/"fictional-example.md")
calls=re.findall(r"^\| (A-o\d+) \| (\d+) \| (FIX:Q:\w+) \| (\d\d:\d\d) \|$",example,re.M)
check(len(calls)==8 and len({c[0] for c in calls})==8, "eight unique A occurrences")
check([c[1] for c in calls]==list(map(str,range(1,9))), "ordered A sequence")
check([c[0] for c in calls if c[2]=="FIX:Q:B"]==["A-o2","A-o5"], "repeated Quay retains occurrences")
coords = re.findall(r"^\| (FIX:SP:\w+) \| (FIX:Q:\w+) \| ([\d.]+) \| ([\d.]+) \|$",example,re.M)
check(len(coords)==7 and all(-90<=float(c[2])<=90 and -180<=float(c[3])<=180 for c in coords), "synthetic coordinate catalogue")
check(set(c[2] for c in calls)<={c[1] for c in coords}, "A calls resolve coordinate references")
bpattern=re.search(r"Full pattern \*\*([^*]+)\*\*, occurrence keys B-o1",example).group(1).split(",")
check(bpattern[2]=="G" and calls[-1][2]=="FIX:Q:G", "A8 maps by Quay to B3")
check("2026-11-03,00:00:00+01:00" in example and "dayOffset=0" in example, "B dated journey context")
before=datetime.fromisoformat("2026-11-02T23:48:00+01:00")
after=datetime.fromisoformat("2026-11-03T00:08:00+01:00")
check((after-before).total_seconds()==1200 and "age20min" in example, "overnight age twenty minutes")
end=datetime.fromisoformat("2026-11-03T00:20:00+01:00")
expiry=datetime.fromisoformat("2026-11-10T00:20:00+01:00")
check((expiry-end).days==7 and end.isoformat() in example and expiry.isoformat() in example, "fixed maximum parent deadline")
check("FICTIONAL ONLY" in example and "unqualified-synthetic" in example, "example not test evidence")

runner=AREA/".bmad-runner"
config=json.loads(read(runner/"resolved-epics-config.json"))
check(Path(config["core"]["output_folder"]).resolve()==AREA, "output root")
check(Path(config["modules"]["bmm"]["planning_artifacts"]).resolve()==AREA, "epic output root")
yaml=read(runner/"_bmad/bmm/config.yaml")
for key in ["output_folder","planning_artifacts"]:
    value=re.search(r"^"+key+r': "([^"]+)"$',yaml,re.M).group(1)
    check(Path(value).resolve()==AREA, "actual YAML route: "+key)
routing=json.loads(read(runner/"epics-routing.json"))
for key in ["runner_root","output","spec_workspace","memory","step_config"]:
    check(Path(routing[key]).resolve().is_relative_to(AREA), "routing destination: "+key)
workflow=json.loads(read(runner/"resolved-epics-workflow.json"))["workflow"]
check(not workflow["activation_steps_prepend"] and not workflow["activation_steps_append"] and not workflow["on_complete"], "no writing hooks")
report={
"kind":"document validation only","date":"2026-10-26",
"result":"pass-as-planning-draft" if not errors else "fail",
"errors":errors,"broken_links":broken,"markdown_files_checked":len(mds),
"capabilities":caps,"epic":"PP-E1","stories":story_ids,"acceptance_criteria":len(ac_ids),
"requirements":{"FR":8,"NFR":5,"UX":3,"coverage":"pass" if set(defined)<=covered else "fail"},
"fictional_A_occurrences":len(calls),"fictional_quay_coordinates":len(coords),
"overnight_example":{"workday":"W1","from":before.isoformat(),"to":after.isoformat(),"age_seconds":1200,"old_occurrence":"A-o8","new_occurrence":"B-o3"},
"routing_inside_extension":True,"changed_paths_inside_extension":all(x.startswith(prefix) for x in paths),
"changed_paths":paths,"index_empty":not git("diff","--cached","--name-only"),
"head":git("rev-parse","HEAD"),"product_tests_run":False,"real_positions_collected":False,
"gps_suitability_demonstrated":False,"implementation_authorized":False,
"semantic_review":"See validation.md for manual preservation/dependency checks; lexical checks alone do not prove semantics."
}
(SPEC/"validation.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({k:report[k] for k in ["result","errors","markdown_files_checked","acceptance_criteria","index_empty","changed_paths_inside_extension"]},ensure_ascii=False))
sys.exit(bool(errors))
