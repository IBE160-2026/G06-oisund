"""One-time mechanical transcription of the approved Markdown, before extraction."""
import hashlib
import json
import re
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]
source = root / 'Eksempelfiler/README.md'
text = source.read_text(encoding='utf-8')
fixtures = []
overview = re.findall(r'^\| \[(\d)\].*?\| (9000000\d) \| (2030-\d\d-\d\d) \| (\w+) \| (\d) \| (.*?) \| (.*?) \| (.*?) \| (\d+) \| (\d+) \|$', text, re.M)
duties = [['960300','960300','960301'],['960146','960146'],['960127'],['960090','960090'],['960006'],['960078','960109','960109'],['960077','960077','960077','960110']]
duty_positions = [[1,16,26],[1,10],[1],[1,8],[1],[1,10,13],[1,10,13,17]]
# Independent row membership from the approved activity tables, in pause-table order.
pause_memberships = {'1':[[15],[25]],'2':[[8,9]],'4':[[7]],'6':[[9]],'7':[[8,9],[13],[17]]}
pause_table = text.split('## Pauser i assistenten')[1].split('## Vognløp')[0]
for n, shift, date, weekday, pages, times, work, span, trips, deadheads in overview:
    section = text.split(f'## Eksempel {n}:')[1].split('\n## ')[0]
    rows = []
    for page, time, label, places in re.findall(r'^\| ([1-4](?:–[1-4])?) \| (.*?) \| (.*?) \| (.*?) \|$', section, re.M):
        start, end = re.findall(r'\d\d:\d\d', time)
        line = trip = origin = destination = None
        if ' / ' in label:
            line, trip = label.split(' / ')
            kind = 'deadhead' if line == 'tom' else 'trip'
        else:
            kind = 'deadhead' if label.startswith('Travel to (') else label
        if ' → ' in places:
            origin, destination = places.replace('UNN', 'Universitetssykehuset Nord-Norge').split(' → ')
        owner = label.startswith('Travel to (')
        source_label = 'Travel to' if owner else (line if trip else label)
        rows.append(dict(pages=list(range(int(page[0]),int(page[-1])+1)), start=start, end=end,
                         label=source_label, kind=kind, line=None if line=='tom' else line,
                         trip_id=trip, origin=origin, destination=destination,
                         end_day=1 if '(+1)' in time else 0,
                         start_day=1 if '(+1)' in time and start != '23:50' else 0,
                         owner_fields=['kind','start','origin','destination'] if owner else []))
    filename=f'Eksempel-{n}-anonymisert.pdf'
    pause_groups=[]
    approved_pauses=re.findall(r'^\| '+n+r' \| (.*?) \| (.*?) \|$',pause_table,re.M)
    for (source_pause,display),members in zip(approved_pauses,pause_memberships.get(n,[])):
        pause_times=re.findall(r'\d\d:\d\d',display)
        day=1 if 'neste dag' in display else 0
        instants=[(datetime.fromisoformat(date+'T'+value)+timedelta(days=day)).replace(tzinfo=ZoneInfo('Europe/Oslo')).isoformat() for value in pause_times]
        kind='meal' if display.startswith('Matpause') else 'coffee' if display.startswith('Kaffepause') else 'split'
        pause_groups.append(dict(rows=members,start=instants[0],end=instants[1],kind=kind,
                                 labels=[rows[index-1]['label'] for index in members]))
    assert len(approved_pauses)==len(pause_memberships.get(n,[]))
    fixtures.append(dict(file=filename, sha256=hashlib.sha256((root/'Eksempelfiler'/filename).read_bytes()).hexdigest(),
        header=dict(shift_id=shift, service_date=date, weekday=weekday, pages=int(pages),
                    start=re.findall(r'\d\d:\d\d',times)[0],end=re.findall(r'\d\d:\d\d',times)[1],
                    end_day=1 if '(+1)' in times else 0,work=work,span=span,
                    employer='Tide Buss',department='Tromsø',driver='Testsjåfør (00000)',
                    origin='Garasje Gimle',destination='Garasje Gimle',
                    supplements=['25,00% '+('1h10' if n=='6' else '1h11' if n=='7' else '0h00')]+(['40,00% 0h00'] if n in ['1','4'] else [])),
        duties=duties[int(n)-1],duty_after_activities=duty_positions[int(n)-1],activities=rows,pause_groups=pause_groups, expected_counts=dict(trips=int(trips),deadheads=int(deadheads)),
        owner_notes=['08:29–08:51 paid free time; not a PDF activity'] if n=='5' else []))
assert [len(x['activities']) for x in fixtures]==[33,16,6,16,5,16,21]
out=dict(approval={'owner':'Jonas Øisund','date':'2026-10-20','source':'Eksempelfiler/README.md',
                   'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
                   'transcription':'Independent approved Markdown tables transcribed before parser execution; source pages are field provenance.'},fixtures=fixtures)
target=root/'backend/tests/fixtures/import_expected.json'
target.parent.mkdir(parents=True,exist_ok=True)
target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print([len(x['activities']) for x in fixtures])
