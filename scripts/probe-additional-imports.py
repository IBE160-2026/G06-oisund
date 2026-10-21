"""Read-only exploratory probe; expected rows come from the independent source table."""
import hashlib
import json
import re
from pathlib import Path
from app.pdf_import import extract_pdf
from app.private_import import interpret
from app.draft_domain import DraftContent


def run():
    readme = Path('/fixtures/README.md').read_text(encoding='utf-8-sig')
    results = []
    for number in (8, 9):
        section = readme.split(f'## Eksempel {number}:', 1)[1].split('\n## ', 1)[0]
        expected = []
        for line in section.splitlines():
            if not re.match(r'\| 1 \| \d', line):
                continue
            _, page, clocks, activity, places, _ = [x.strip() for x in line.split('|')]
            start, end = clocks.split('–')
            label = activity.split(' (')[0]
            origin, destination = (None, None) if places == 'Ikke oppgitt' else places.split(' → ')
            line_code, trip = label.split(' / ') if ' / ' in label else (None, None)
            expected.append(dict(start=start, end=end, label=line_code or label,
                                 line=None if line_code in ('tom', 'CAR') else line_code, trip_id=trip,
                                 origin=origin, destination=destination, pages=[int(page)]))
        assert len(expected) == {8: 23, 9: 8}[number]
        path = Path(f'/fixtures/Eksempel-{number}-anonymisert.pdf')
        source = extract_pdf(path.read_bytes())
        content = interpret(source).model_dump(mode='json')
        actual = [{key: row[key] for key in expected[0]} for row in source['activities']]
        missing = [row for row in expected if row not in actual]
        extra = [row for row in actual if row not in expected]
        order_matches = actual == [row for row in expected if row in actual]
        reloaded = DraftContent.model_validate_json(json.dumps(content)).model_dump(mode='json')
        assert reloaded == content
        result = dict(example=number, pdf_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                      expected_rows=len(expected), actual_rows=len(actual), missing=missing, extra=extra,
                      retained_rows_in_expected_order=order_matches,
                      qualification=content['import_metadata']['qualification'],
                      header=content['import_metadata']['header'], duties=source['duties'],
                      duty_changes=content.get('vehicle_duty_changes'),
                      change_activity_numbers=[next(i for i, row in enumerate(content['activities'], 1)
                                                    if row['id'] == c['from_activity_id'])
                                               for c in content.get('vehicle_duty_changes', [])],
                      unresolved=source['unresolved'], pause_groups=source['pause_groups'],
                      activities=content['activities'], model_json_roundtrip=True)
        results.append(result)
    Path('/render/probe-result.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
    for result in results:
        print(json.dumps({key: value for key, value in result.items() if key not in ('activities', 'duties')}, ensure_ascii=False))


if __name__ == '__main__':
    run()
