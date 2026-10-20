"""Independent comparator and CLI. Only this module reads the approved oracle."""
import argparse
import hashlib
import importlib.metadata
import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path

from app.pdf_import import ImportFailure, extract_pdf

ORACLE=Path(__file__).resolve().parents[1]/'tests/fixtures/import_expected.json'


def field_origin(path):
    if path=='timezone':
        return 'owner-approved'
    if path in {'activity_count','duties','duty_suffixes','duty_occurrences','duty_provenance','pause_groups','physical_bus'}:
        return 'extracted' if path=='duties' else 'derived'
    if path.startswith('header.'):
        return 'derived' if path.split('.')[1] in {'pages','start_instant','end_instant','end_day'} or path.endswith('.provenance') else 'extracted'
    if path.startswith('activities.'):
        return 'derived' if path.split('.')[2] in {'kind','pages','source_order','start_instant','end_instant','start_day','end_day','field_provenance','provenance'} else 'extracted'
    raise ValueError('Unclassified comparison field: '+path)


def valid_location(location,actual,field,value,pages):
    if not isinstance(location,dict) or set(location)!={'page','column','line'}:
        return False
    page,column,line=(location[key] for key in ('page','column','line'))
    if any(type(number) is not int for number in (page,column,line)) or page not in pages or column not in (1,2) or line<1:
        return False
    return any(row.get('location')==location and field in row.get('fields',{}) and row['fields'][field]==value
               for row in actual.get('provenance',{}).get('source_rows',[]))


def valid_field_provenance(got,key,want,actual):
    locations=got.get('provenance',{}).get(key)
    if not isinstance(locations,list) or not locations:
        return False
    # Continuation endpoints must point to their last source page; starts to their first.
    pages=[want['pages'][-1]] if key in ('end','destination') else [want['pages'][0]]
    source_key='label' if key=='kind' else key
    value=got.get('label') if key=='kind' else got.get(key)
    return all(valid_location(location,actual,source_key,value,pages) for location in locations)


def expected_calendar_provenance(clock_path):
    return {'derived_from':[clock_path,'header.service_date','header.start','header.span','header.end','timezone'],
            'rule':'unique instant in header interval'}


def compare(expected,actual):
    comparisons=[]
    def check(path,want,got,assisted=False):
        comparisons.append(dict(field=path,expected=want,actual=got,match=want==got,
                                basis='owner-clarified' if assisted else 'required-source',
                                actual_origin='unresolved' if got is None and want is not None else field_origin(path)))
    for key,value in expected['header'].items():
        check('header.'+key,value,actual['header'].get(key))
        provenance=actual.get('provenance',{}).get('header',{}).get(key)
        if key=='pages':
            valid=provenance=={'derived_from':['document.pages']}
        elif key=='end_day':
            valid=provenance==expected_calendar_provenance('header.end')
        else:
            valid=(provenance=={'page':1,'region':'header','field':key}
                   and actual.get('provenance',{}).get('header_evidence',{}).get('1',{}).get(key)==value)
        check('header.'+key+'.provenance',True,valid)
    from datetime import timedelta
    from zoneinfo import ZoneInfo
    for field in ('start','end'):
        instant=(datetime.fromisoformat(expected['header']['service_date']+'T'+expected['header'][field])+
                 timedelta(days=expected['header']['end_day'] if field=='end' else 0)).replace(tzinfo=ZoneInfo('Europe/Oslo')).isoformat()
        check('header.'+field+'_instant',instant,actual['header'].get(field+'_instant'))
        check('header.'+field+'_instant.provenance',expected_calendar_provenance('header.'+field),actual.get('provenance',{}).get('header',{}).get(field+'_instant'))
    check('activity_count',len(expected['activities']),len(actual['activities']))
    for index,want in enumerate(expected['activities']):
        got=actual['activities'][index] if index<len(actual['activities']) else {}
        check(f'activities.{index+1}.source_order',index+1,got.get('source_order'))
        for key,value in want.items():
            if key=='owner_fields':
                continue
            check(f'activities.{index+1}.{key}',value,got.get(key), key in want['owner_fields'] or
                  (bool(want['owner_fields']) and key in ('start_day',)))
        for key in ('start_instant','end_instant'):
            # Validate the explicit calendar instant against the independent expected calendar day.
            field=key.split('_')[0]
            instant=(datetime.fromisoformat(expected['header']['service_date']+'T'+want[field])+
                     timedelta(days=want[field+'_day'])).replace(tzinfo=ZoneInfo('Europe/Oslo')).isoformat()
            check(f'activities.{index+1}.{key}',instant,got.get(key),field in want['owner_fields'])
        for key in ('label','kind','line','trip_id','origin','destination','start','end'):
            if got.get(key) is not None:
                check(f'activities.{index+1}.provenance.{key}',True,valid_field_provenance(got,key,want,actual))
        for field in ('start','end'):
            for suffix in ('_instant','_day'):
                check(f'activities.{index+1}.provenance.{field+suffix}',expected_calendar_provenance(f'activities.{index+1}.{field}'),got.get('provenance',{}).get(field+suffix))
    check('duties',[d for d in expected['duties']],[d['value'] for d in actual['duties']])
    check('duty_suffixes',[d[-3:] for d in expected['duties']],[d['suffix'] for d in actual['duties']])
    check('duty_occurrences',expected['duty_after_activities'],[d['after_activity'] for d in actual['duties']])
    check('duty_provenance',True,all(valid_location(d.get('provenance'),actual,'duty',d['value'],range(1,expected['header']['pages']+1)) for d in actual['duties']))
    check('pause_groups',expected['pause_groups'],actual.get('pause_groups'))
    check('physical_bus',None,actual.get('physical_bus'))
    check('timezone','Europe/Oslo',actual.get('timezone'))
    failures=[c for c in comparisons if not c['match'] and c['basis']=='required-source']
    assisted=[c for c in comparisons if not c['match'] and c['basis']=='owner-clarified']
    requires_owner=any(row['owner_fields'] for row in expected['activities'])
    status='supported' if not failures and not requires_owner and not actual['unresolved'] else 'partial' if actual['activities'] else 'unsupported'
    return dict(status=status,source_mismatches=len(failures),owner_assistance_gaps=len(assisted),
                owner_assistance_required=requires_owner,
                owner_assisted_facts=[dict(activity=index+1,fields={key:row[key] for key in row['owner_fields']},
                                           attribution='Jonas Øisund, 2026-10-20; not automatic extraction')
                                      for index,row in enumerate(expected['activities']) if row['owner_fields']],
                unresolved=actual['unresolved'],comparisons=comparisons,
                extracted_counts=dict(activities=len(actual['activities']),trips=sum(a['kind']=='trip' for a in actual['activities']),
                                      numbered_deadheads=sum(a['kind']=='deadhead' for a in actual['activities'])),
                owner_notes=expected['owner_notes'],pause_groups=actual['pause_groups'],duties=actual['duties'],
                source_evidence=actual['provenance'],
                activity_provenance=[dict(source_order=row['source_order'],pages=row['pages'],fields=row['provenance']) for row in actual['activities']],
                unknown_annotations=actual['annotations'])


def qualify(directory,oracle=ORACLE):
    started=time.monotonic()
    expected=json.loads(oracle.read_text(encoding='utf-8'))
    results=[]
    for fixture in expected['fixtures']:
        path=directory/fixture['file']
        item=dict(file=fixture['file'],expected_sha256=fixture['sha256'])
        begin=time.monotonic()
        if not path.is_file():
            item.update(status='untested',reason='missing_input')
        else:
            # Bounded read; the adapter separately enforces its byte ceiling.
            from app.pdf_import import MAX_BYTES
            with path.open('rb') as stream:
                data=stream.read(MAX_BYTES+1)
            item['actual_sha256']=hashlib.sha256(data).hexdigest()
            if item['actual_sha256'] != fixture['sha256']:
                item.update(status='untested',reason='unapproved_input_hash')
            else:
                try:
                    item.update(compare(fixture,extract_pdf(data,filename=path.name)))
                except ImportFailure as exc:
                    item.update(status='unsupported',reason=str(exc))
        item['seconds']=round(time.monotonic()-begin,3)
        results.append(item)
    return dict(generated_at=datetime.now(timezone.utc).isoformat(),approval=expected['approval'],
                oracle_sha256=hashlib.sha256(oracle.read_bytes()).hexdigest(),
                versions={name:importlib.metadata.version(name) for name in ['pdfplumber','pdfminer.six','pypdfium2','pillow','charset-normalizer','cryptography','cffi','pycparser']},
                implementation_sha256={name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
                                       for name in ['pdf_import.py','qualify_imports.py']},
                requirements_lock_sha256=hashlib.sha256((ORACLE.parents[2]/'requirements.lock').read_bytes()).hexdigest(),
                limits=dict(bytes=10*1024*1024,pages=20,seconds=30,result_bytes=2*1024*1024),
                python=platform.python_version(),elapsed_seconds=round(time.monotonic()-started,3),fixtures=results,
                recommendation='Use only individually supported layouts for automatic source facts; retain review for every import. Owner-assisted or unresolved inputs remain partial. Intermediate stops are unqualified.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    report=qualify(args.directory)
    payload=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        args.output.write_text(payload,encoding='utf-8')
    else:
        print(payload,end='')
    return 0 if all(f['status']=='supported' for f in report['fixtures']) else 1


if __name__=='__main__':
    raise SystemExit(main())
