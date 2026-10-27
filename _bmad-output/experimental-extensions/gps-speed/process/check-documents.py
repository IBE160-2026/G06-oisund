"""Documentation-only checks; no product import, tests, network or GPS."""
from pathlib import Path
import json
import re
import subprocess

root = Path(__file__).resolve().parents[1]
repo = root.parents[2]
scope = "EXPERIMENTAL EXTENSION — OUTSIDE APPROVED V1 SCOPE"
errors = []
files = sorted(p for p in root.rglob("*") if p.is_file())
links = 0
for p in files:
    raw = p.read_bytes()
    try:
        txt = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        errors.append(f"Invalid UTF-8: {p.relative_to(root)}")
        continue
    if p.suffix == ".json":
        try:
            json.loads(txt)
        except ValueError:
            errors.append(f"Invalid JSON: {p.relative_to(root)}")
    if p.suffix != ".md":
        continue
    if p.name != ".memlog.md" and scope not in txt:
        errors.append(f"Missing scope: {p.relative_to(root)}")
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", txt):
        if target.startswith(("https://", "http://", "#")):
            continue
        links += 1
        if not (p.parent / target.split("#")[0]).resolve().exists():
            errors.append(f"Broken link: {p.relative_to(root)} -> {target}")
spec = root / "specs/spec-gps-speed/SPEC.md"
epic = root / "planning/epics.md"
for p, key in [(spec, "companions"), (epic, "inputDocuments")]:
    txt = p.read_text(encoding="utf-8")
    block = re.search(rf"(?m)^{key}:\n((?:  - .*\n)+)", txt)
    if not block:
        errors.append(f"Missing {key}")
    else:
        for target in re.findall(r"  - (.+)", block[1]):
            links += 1
            if not (p.parent / target).resolve().is_file():
                errors.append(f"Missing {key} target: {target}")
spec_text = spec.read_text(encoding="utf-8")
epic_text = epic.read_text(encoding="utf-8")
caps = re.findall(r"\*\*(CAP-\d+)\*\*", spec_text)
stories = re.findall(r"^### Story (GS-E1-S\d+):", epic_text, re.M)
ac_lines = [line for line in epic_text.splitlines() if re.match(r"- \*\*S\d-AC\d", line)]
ac_ids = [re.search(r"S\d-AC\d+", line)[0] for line in ac_lines]
if len(caps) != 4 or len(set(caps)) != 4:
    errors.append("Expected four unique CAPs")
if len(stories) != 4 or len(set(stories)) != 4:
    errors.append("Expected four unique stories")
if len(ac_ids) != 20 or len(set(ac_ids)) != 20:
    errors.append("Expected twenty unique ACs")
for line in ac_lines:
    if not all(marker in line for marker in ["Given**", "**When**", "**Then**"]):
        errors.append("Incomplete Given/When/Then")
for heading in ["Why", "Capabilities", "Constraints", "Non-goals", "Success signal"]:
    if f"## {heading}" not in spec_text:
        errors.append(f"Missing spec kernel field: {heading}")
git = ["git", "-c", f"safe.directory={repo.as_posix()}", "-C", str(repo)]
changed = subprocess.check_output(git + ["diff", "--name-only", "5adc6fb2c0137a3a6519d4f7ba42dd57f0e02f1c"], text=True).splitlines()
untracked = subprocess.check_output(git + ["ls-files", "--others", "--exclude-standard"], text=True).splitlines()
prefix = "_bmad-output/experimental-extensions/gps-speed/"
outside = [p for p in changed + untracked if not p.startswith(prefix)]
if outside:
    errors.append("Changes outside GPS document root")
# High-signal patterns only. Semantic inspection is separately required.
patterns = [r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", r"gh[pousr]_[A-Za-z0-9]{20,}", r"AKIA[0-9A-Z]{16}", r"eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{15,}\."]
secret_files = []
for p in files:
    if p.suffix not in (".md", ".json"):
        continue
    txt = p.read_text(encoding="utf-8-sig")
    if any(re.search(pattern, txt) for pattern in patterns):
        secret_files.append(str(p.relative_to(root)))
if secret_files:
    errors.append("Potential secret pattern; inspect named files without printing value")
result = {
    "kind": "documentation-only",
    "scope": scope,
    "base_commit": "5adc6fb2c0137a3a6519d4f7ba42dd57f0e02f1c",
    "files_examined": len(files),
    "local_links_and_manifest_paths": links,
    "capabilities": len(caps),
    "epics": len(re.findall(r"^## Epic GS-E1:", epic_text, re.M)),
    "stories": len(stories),
    "given_when_then_criteria": len(ac_ids),
    "changes_outside_document_root": outside,
    "potential_secret_files": secret_files,
    "errors": errors,
    "passed": not errors,
    "product_tests_run": False,
    "physical_gps_run": False,
    "external_commit_links_http_checked": False
}
(root / "process/document-checks.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=True))
raise SystemExit(1 if errors else 0)
