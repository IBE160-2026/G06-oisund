"""Transient, bounded text-PDF adapter. No oracle, HTTP, storage or fixture knowledge."""
from __future__ import annotations

import io
import json
import multiprocessing as mp
import os
import re
import time
from datetime import datetime, timedelta
from threading import Event
from typing import TypedDict
from zoneinfo import ZoneInfo

MAX_BYTES = 10 * 1024 * 1024
MAX_PAGES = 20
MAX_OUTPUT = 2 * 1024 * 1024
TIMEOUT = 30.0
CLOCK = r'\d{1,2}:\d{2}'
ZONE = ZoneInfo('Europe/Oslo')


class ImportDraft(TypedDict):
    """Adapter-only contract, independent of fictional Activity's positive-duration rule.

    Ordered source rows may have equal instants or nullable facts. Calendar instants,
    suffixes and pause groups are derived; owner interpretations never enter this result.
    """
    header: dict
    activities: list[dict]
    duties: list[dict]
    physical_bus: None
    timezone: str
    provenance: dict
    unresolved: list[dict]
    annotations: list[dict]
    pause_groups: list[dict]


class ImportFailure(Exception):
    """Safe public rejection code, never underlying PDF text or exception details."""


def clock(value):
    hour, minute = map(int, value.split(':'))
    if minute > 59 or hour > 47:
        raise ImportFailure('invalid_clock')
    return f'{hour:02}:{minute:02}'


def parse_document(data: bytes) -> ImportDraft:
    import pdfplumber
    header = None
    activities, duties, unresolved, annotations, source_rows = [], [], [], [], []
    header_evidence = {}
    current = None
    with io.BytesIO(data) as stream, pdfplumber.open(stream) as pdf:
        if pdf.doc.encryption:
            raise ImportFailure('encrypted')
        if not 0 < len(pdf.pages) <= MAX_PAGES:
            raise ImportFailure('page_limit')
        for number, page in enumerate(pdf.pages, 1):
            if not page.chars:
                raise ImportFailure('image_only_or_empty')
            head = page.crop((0, 0, page.width, 110)).extract_text() or ''
            identity = re.search(r'Skift:\s*(\S+)', head)
            date = re.search(r'Date:\s*(\d{2}/\d{2}/\d{4})\s+(\w+)\s+(.+)', head)
            start = re.search(r'Skift start:\s*('+CLOCK+r')\s+(.+?)\s+Arb.tid:\s*(\d+h\d+)\s+Utstrekk:\s*(\d+h\d+)', head)
            end = re.search(r'Skift slutt:\s*('+CLOCK+r')\s+(.+?)\s+Tillegg:', head)
            employer = re.search(r'^(.+?) - ', head)
            division = re.search(r'Division:\s*(.+)', head)
            if not all([identity,date,start,end,employer,division]):
                raise ImportFailure('unsupported_header')
            facts = dict(shift_id=identity[1], service_date=datetime.strptime(date[1],'%d/%m/%Y').date().isoformat(),
                         weekday=date[2],driver=date[3],employer=employer[1],department=division[1],
                         start=clock(start[1]),origin=start[2],work=start[3],span=start[4],
                         end=clock(end[1]),destination=end[2],
                         supplements=[f'{p} {v}' for p,v in re.findall(r'(\d+,\d+%)\s*(\d+h\d+)',head)])
            if header is None:
                header = facts
            elif header != facts:
                raise ImportFailure('conflicting_headers')
            header_evidence[str(number)] = dict(facts)
            # Qualified HASTUS layout: full-width header, two body columns.
            for column in (0, 1):
                body = page.crop((column*page.width/2,110,(column+1)*page.width/2,790))
                for line_no, line in enumerate((body.extract_text() or '').splitlines(),1):
                    provenance = dict(page=number,column=column+1,line=line_no)
                    marker=re.search(r'(?<=[0-9])\s+([A-Za-z])$',line)
                    if marker:
                        annotations.append(dict(value=marker[1],meaning=None,provenance=provenance))
                        line=line[:marker.start()]
                    if re.fullmatch(r'[A-Za-z]',line):
                        annotations.append(dict(value=line,meaning=None,provenance=provenance))
                        continue
                    duty = re.fullmatch(r'Vogn\s+(CAR\s*-\s*[1-4]|\S+)',line)
                    trip = re.fullmatch(r'(\S+)\s*/\s*(\S+)\s+(.+?)\s+('+CLOCK+r')',line)
                    activity = re.fullmatch(r'(Sign-on|Sign-off|Split break|Coffee|MealBreak|Paid meal before|Paid meal after|Travel to|Travel from|Fadder|Instruktør)\s+('+CLOCK+r')(?:\s+('+CLOCK+r'))?',line)
                    stop = re.fullmatch(r'(?:\d+\.\d+\s+)?(.+?)\s+('+CLOCK+r')',line)
                    if duty:
                        source_rows.append(dict(location=provenance,fields={'duty':duty[1]}))
                        suffix = re.search(r'([0-9]{3})$', duty[1])
                        if not suffix and not re.fullmatch(r'CAR(?:\s*-\s*[1-4])?', duty[1]):
                            unresolved.append(dict(code='unrecognized_source_line',provenance=provenance))
                        duties.append(dict(value=duty[1],suffix=suffix[1] if suffix else None,after_activity=len(activities),provenance=provenance))
                        current = None
                    elif trip or activity:
                        if trip:
                            label, trip_id, origin, start_clock = trip.groups()
                            car = bool(duties and re.fullmatch(r'CAR(?:\s*-\s*[1-4])?', duties[-1]['value']))
                            kind = 'deadhead_car' if label == 'tom' and car else 'deadhead' if label == 'tom' else 'CAR' if label == 'CAR' else 'trip'
                            item=dict(label=label,kind=kind,line=None if label in ('tom', 'CAR') else label,
                                      trip_id=trip_id,origin=origin,destination=None,start=clock(start_clock),end=None)
                        else:
                            label, a, b = activity.groups()
                            item=dict(label=label,kind=label,line=None,trip_id=None,origin=None,destination=None,
                                      start=clock(a) if b else None,end=clock(b or a))
                        item.update(pages=[number],provenance={key:[provenance] for key in item},source_order=len(activities)+1)
                        source_rows.append(dict(location=provenance,fields={key:value for key,value in item.items() if key not in ('provenance','pages','source_order','kind')}))
                        activities.append(item)
                        current = item if trip else None
                    elif stop and current is not None:
                        source_rows.append(dict(location=provenance,fields={'destination':stop[1],'end':clock(stop[2])}))
                        current['destination'], current['end'] = stop[1],clock(stop[2])
                        if number not in current['pages']:
                            current['pages'].append(number)
                        current['provenance']['destination']=[provenance]
                        current['provenance']['end']=[provenance]
                    elif line not in ('Notes:',) and not line.startswith(('HASTUS','Page:')):
                        unresolved.append(dict(code='unrecognized_source_line',provenance=provenance))
            page.close()
        header['pages']=len(pdf.pages)
    # Calendar assignment is proved by service date + start + stated span, never clock ordering.
    base=datetime.fromisoformat(header['service_date']+'T'+header['start']).replace(tzinfo=ZONE)
    hours,minutes=map(int,header['span'].split('h'))
    finish=base+timedelta(hours=hours,minutes=minutes)
    if finish.strftime('%H:%M') != header['end'] or finish-base >= timedelta(days=1):
        unresolved.append(dict(code='unproven_calendar_interval'))
        finish=None
    header['end_day']=(finish.date()-base.date()).days if finish else None
    header['start_instant']=base.isoformat()
    header['end_instant']=finish.isoformat() if finish else None
    for item in activities:
        for field in ('start','end'):
            candidates=[]
            if finish and item[field]:
                h,m=map(int,item[field].split(':'))
                for day in (0,1):
                    candidate=base.replace(hour=h%24,minute=m)+timedelta(days=day+h//24)
                    if base <= candidate <= finish:
                        candidates.append(candidate)
            instant=candidates[0] if len(candidates)==1 else None
            item[field+'_instant']=instant.isoformat() if instant else None
            item[field+'_day']=(instant.date()-base.date()).days if instant else None
            for suffix in ('_instant','_day'):
                item['provenance'][field+suffix]=calendar_provenance(f'activities.{item["source_order"]}.{field}')
            if item[field] is None or instant is None:
                unresolved.append(dict(code='unresolved_time',activity=item['source_order'],field=field))
        if item['kind'] in ('trip','deadhead','deadhead_car','CAR') and item['destination'] is None:
            unresolved.append(dict(code='missing_endpoint',activity=item['source_order']))
        if item['start_instant'] and item['end_instant'] and item['end_instant']<item['start_instant']:
            unresolved.append(dict(code='reversed_activity_time',activity=item['source_order']))
    return dict(header=header,activities=activities,duties=duties,physical_bus=None,timezone='Europe/Oslo',
                provenance={'header':{key:calendar_provenance('header.'+('end' if key in ('end_day','end_instant') else 'start')) if key in ('start_instant','end_instant','end_day') else {'derived_from':['document.pages']} if key=='pages' else {'page':1,'region':'header','field':key} for key in header},
                            'header_evidence':header_evidence,'source_rows':source_rows,'calendar':'derived from service date, header start and stated Utstrekk',
                            'duty_suffix':'derived final three numeric characters when present; owner-approved meaning'},
                unresolved=unresolved,annotations=annotations,pause_groups=group_pauses(activities))


def calendar_provenance(clock_path):
    return {'derived_from':[clock_path,'header.service_date','header.start','header.span','header.end','timezone'],
            'rule':'unique instant in header interval'}


def group_pauses(activities):
    groups=[]
    labels={'MealBreak','Paid meal before','Paid meal after','Coffee','Split break'}
    for row in activities:
        if row['label'] not in labels:
            continue
        previous=groups[-1] if groups else None
        if (previous and previous['rows'][-1]+1==row['source_order']
                and previous['start'] is not None and previous['end'] is not None
                and row['start_instant'] is not None and row['end_instant'] is not None
                and previous['end']==row['start_instant']):
            previous['rows'].append(row['source_order']); previous['end']=row['end_instant']; previous['labels'].append(row['label'])
        else:
            groups.append(dict(rows=[row['source_order']],start=row['start_instant'],end=row['end_instant'],labels=[row['label']]))
    for group in groups:
        group['kind']='meal' if 'MealBreak' in group['labels'] else 'split' if 'Split break' in group['labels'] else 'coffee' if set(group['labels'])=={'Coffee'} else 'paid_meal'
    return groups


def _worker(data, connection):
    # Third-party errors/warnings must never emit raw payloads to application logs.
    with open(os.devnull,'w') as sink:
        os.dup2(sink.fileno(),1); os.dup2(sink.fileno(),2)
        try:
            result={'ok':parse_document(data)}
        except ImportFailure as exc:
            result={'error':str(exc)}
        except Exception as exc:
            from pdfminer.pdfdocument import PDFPasswordIncorrect, PDFEncryptionError
            encrypted=any(isinstance(error,(PDFPasswordIncorrect,PDFEncryptionError)) for error in (exc,exc.__cause__,exc.__context__))
            result={'error':'encrypted' if encrypted else 'corrupt_or_unsupported'}
        try:
            payload=json.dumps(result,ensure_ascii=False).encode()
            connection.send_bytes(payload if len(payload)<=MAX_OUTPUT else b'{"error":"output_limit"}')
        finally:
            connection.close()


def extract_pdf(data: bytes, *, filename='input.pdf', cancel: Event | None=None, timeout=TIMEOUT) -> ImportDraft:
    if not isinstance(data,bytes) or not filename.lower().endswith('.pdf') or not data.startswith(b'%PDF-'):
        raise ImportFailure('wrong_type')
    if len(data)>MAX_BYTES:
        raise ImportFailure('size_limit')
    context=mp.get_context('spawn')
    receive,send=context.Pipe(duplex=False)
    process=context.Process(target=_worker,args=(data,send),daemon=True)
    deadline=time.monotonic()+min(timeout,TIMEOUT)
    try:
        if cancel is not None and cancel.is_set():
            raise ImportFailure('cancelled')
        process.start(); send.close()
        while True:
            if cancel is not None and cancel.is_set():
                raise ImportFailure('cancelled')
            if time.monotonic()>=deadline:
                raise ImportFailure('timeout')
            if receive.poll(0.02):
                try:
                    result=json.loads(receive.recv_bytes(MAX_OUTPUT))
                except (EOFError,OSError,ValueError):
                    raise ImportFailure('worker_failed') from None
                if 'error' in result:
                    raise ImportFailure(result['error'])
                return result['ok']
            if not process.is_alive():
                raise ImportFailure('worker_failed')
    finally:
        if process.pid:
            if process.is_alive():
                process.terminate()
            process.join(1)
            if process.is_alive():
                process.kill(); process.join()
            process.close()
        receive.close(); send.close()
