import copy
import hashlib
import json
import multiprocessing
from pathlib import Path
from threading import Event, Timer

import pytest

from app import pdf_import
from app.pdf_import import ImportFailure, extract_pdf
from app.qualify_imports import ORACLE, compare, qualify

EXPECTED=json.loads(ORACLE.read_text(encoding='utf-8'))
FIXTURES=Path('/fixtures')


def synthetic_pdf(pages=1, encrypted=False):
    """Minimal genuine PDF with blank pages; no external test-generation dependency."""
    objects=[b'<< /Type /Catalog /Pages 2 0 R >>',
             ('<< /Type /Pages /Count %s /Kids [%s] >>'%(pages,' '.join(f'{i+3} 0 R' for i in range(pages)))).encode()]
    objects += [b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 841] /Resources << >> >>']*pages
    if encrypted:
        objects.append(b'<< /Filter /Standard /V 1 /R 2 /O <'+b'00'*32+b'> /U <'+b'00'*32+b'> /P -4 >>')
    encryption=f' /Encrypt {len(objects)} 0 R /ID [<00000000><00000000>]' if encrypted else ''
    return pdf_bytes(objects,encryption)


def pdf_bytes(objects,encryption=''):
    result=b'%PDF-1.4\n'; offsets=[0]
    for i,obj in enumerate(objects,1):
        offsets.append(len(result)); result+=f'{i} 0 obj\n'.encode()+obj+b'\nendobj\n'
    xref=len(result)
    result+=f'xref\n0 {len(offsets)}\n0000000000 65535 f \n'.encode()
    result+=b''.join(f'{offset:010} 00000 n \n'.encode() for offset in offsets[1:])
    return result+f'trailer\n<< /Size {len(offsets)} /Root 1 0 R{encryption} >>\nstartxref\n{xref}\n%%EOF'.encode()


def synthetic_text_pdf():
    lines=[(810,'Synthetic Employer - Origin Skift: TEST'),
           (790,'Date: 01/01/2030 Tue Synthetic Driver'),(770,'Division: Example'),
           (750,'Skift start: 06:00 Origin Arb.tid: 0h10 Utstrekk: 0h10'),
           (738,'Skift slutt: 06:10 Destination Tillegg: 25,00%0h00'),
           (720,'Sign-on 06:00 06:01'),(700,'tom / 99 Origin 06:02 t'),
           (680,'N'),(660,'1.0 Destination 06:03'),(640,'Coffee 06:03 06:04 N'),(620,'t')]
    content='\n'.join(f'BT /F1 9 Tf 20 {y} Td ({text}) Tj ET' for y,text in lines).encode()
    return pdf_bytes([b'<< /Type /Catalog /Pages 2 0 R >>',b'<< /Type /Pages /Count 1 /Kids [3 0 R] >>',
        b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 841] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
        b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
        f'<< /Length {len(content)} >>\nstream\n'.encode()+content+b'\nendstream'])


@pytest.fixture(scope='module')
def extracted():
    assert FIXTURES.is_dir(), 'Mount all approved PDFs read-only at /fixtures; do not skip qualification'
    return [extract_pdf((FIXTURES/f['file']).read_bytes()) for f in EXPECTED['fixtures']]


def test_oracle_independence_integrity_and_counts():
    assert EXPECTED['approval']['date']=='2026-10-20'
    # The live README now also contains the separately approved examples 8/9.
    # Preserve the exact historical source rather than changing its approval hash.
    approved_source = ORACLE.parent / 'import-source-2026-10-20.md'
    assert hashlib.sha256(approved_source.read_bytes()).hexdigest()==EXPECTED['approval']['source_sha256']
    assert [len(f['activities']) for f in EXPECTED['fixtures']]==[33,16,6,16,5,16,21]
    assert sum(f['expected_counts']['trips'] for f in EXPECTED['fixtures'])==46
    assert sum(f['expected_counts']['deadheads'] for f in EXPECTED['fixtures'])==31
    for f in EXPECTED['fixtures']:
        assert hashlib.sha256((FIXTURES/f['file']).read_bytes()).hexdigest()==f['sha256']
    # The adapter cannot import/read expected facts, fixture paths or owner answers.
    source=Path(pdf_import.__file__).read_text()
    assert all(word not in source for word in ('import_expected','Eksempel-','Skoglyst','Breivika','960006'))


def test_all_actual_fixtures_compare_every_required_fact(extracted):
    results=[compare(want,got) for want,got in zip(EXPECTED['fixtures'],extracted)]
    assert [r['status'] for r in results]==['supported']*5+['partial','supported']
    assert all(r['source_mismatches']==0 for r in results)
    assert results[5]['owner_assistance_gaps']==6
    assert sum(len(a['activities']) for a in extracted)==113


def test_continuations_zero_duration_identity_and_unknowns(extracted):
    first=extracted[0]
    assert first['activities'][6]['start_instant']==first['activities'][6]['end_instant']
    assert first['activities'][8]['pages']==[1,2]
    assert first['activities'][18]['pages']==[2,3]
    assert first['activities'][29]['pages']==[3,4]
    assert len({r['source_order'] for r in first['activities']})==33
    assert extracted[5]['activities'][2]['trip_id']==extracted[5]['activities'][11]['trip_id']=='1001'
    assert extracted[5]['activities'][11]['line']=='X35'
    assert extracted[6]['activities'][15]['trip_id']=='14'
    assert extracted[3]['duties'][0]['suffix']=='090'
    assert extracted[4]['duties'][0]['suffix']=='006'
    assert all(r['physical_bus'] is None for r in extracted)
    assert first['annotations'] and all(a['meaning'] is None for a in first['annotations'])


def test_calendar_and_owner_facts(extracted):
    overnight=extracted[3]
    assert overnight['header']['service_date']=='2030-01-05'
    assert overnight['header']['weekday']=='Sat'
    assert overnight['activities'][3]['start_instant']=='2030-01-05T23:50:00+01:00'
    assert overnight['activities'][3]['end_instant']=='2030-01-06T00:35:00+01:00'
    assert extracted[4]['header']['end']=='08:51'
    assert extracted[4]['activities'][-1]['end']=='08:29'
    assert len(extracted[4]['activities'])==5
    travel=extracted[5]['activities'][12]
    assert travel['label']==travel['kind']=='Travel to'
    assert travel['start'] is travel['origin'] is travel['destination'] is travel['trip_id'] is None
    assert travel['end']=='16:00'
    assert extracted[0]['activities'][23]['kind']=='Travel to'


def test_pause_groups_retain_rows_and_do_not_fill_gaps(extracted):
    assert [len(f['pause_groups']) for f in EXPECTED['fixtures']]==[2,1,0,1,0,1,3]
    assert all(actual['pause_groups']==expected['pause_groups'] for actual,expected in zip(extracted,EXPECTED['fixtures']))
    assert extracted[1]['pause_groups'][0]['rows']==[8,9]
    assert extracted[1]['pause_groups'][0]['kind']=='meal'
    assert extracted[6]['pause_groups'][0]['rows']==[8,9]
    assert [g['kind'] for g in extracted[6]['pause_groups']]==['meal','coffee','coffee']
    assert extracted[2]['pause_groups']==extracted[4]['pause_groups']==[]
    assert len(extracted[1]['activities'])==16


def test_independent_synthetic_unknown_annotations():
    actual=extract_pdf(synthetic_text_pdf())
    assert actual['annotations']==[
        {'value':value,'meaning':None,'provenance':{'page':1,'column':1,'line':line}}
        for value,line in [('t',2),('N',3),('N',5),('t',6)]]
    assert actual['activities'][1]['trip_id']=='99'
    assert actual['activities'][1]['destination']=='Destination'


def test_calendar_derivation_links(extracted):
    for actual in extracted:
        for row in actual['activities']:
            for field in ('start','end'):
                for suffix in ('_instant','_day'):
                    assert row['provenance'][field+suffix]['derived_from']==[
                        f'activities.{row["source_order"]}.{field}','header.service_date','header.start','header.span','header.end','timezone']
        assert actual['provenance']['header']['start_instant']['derived_from'][0]=='header.start'
        for field in ('end_instant','end_day'):
            assert actual['provenance']['header'][field]['derived_from'][0]=='header.end'


@pytest.mark.parametrize('field',['start_instant','end_instant','start_day','end_day'])
def test_broken_calendar_derivation_link_fails(extracted,field):
    actual=copy.deepcopy(extracted[2])
    actual['activities'][1]['provenance'][field]['derived_from']=[]
    result=compare(EXPECTED['fixtures'][2],actual)
    assert result['status']=='partial'
    assert any(c['field']==f'activities.2.provenance.{field}' and not c['match'] for c in result['comparisons'])


def test_continuation_endpoint_provenance(extracted):
    for index,end_page in [(8,2),(18,3),(29,4)]:
        row=extracted[0]['activities'][index]
        assert row['provenance']['origin'][0]['page']==end_page-1
        for field in ('destination','end'):
            location=row['provenance'][field][0]
            assert location['page']==end_page
            assert any(e['location']==location and e['fields'].get(field)==row[field]
                       for e in extracted[0]['provenance']['source_rows'])


@pytest.mark.parametrize('field',['destination','end','origin','start','label','line','trip_id'])
@pytest.mark.parametrize('mutation',['missing','page','column','line','unrelated_row'])
def test_individual_field_provenance_mutations_fail(extracted,field,mutation):
    actual=copy.deepcopy(extracted[0]); row=actual['activities'][8]
    if mutation=='missing': row['provenance'].pop(field)
    elif mutation=='unrelated_row': row['provenance'][field]=[actual['activities'][0]['provenance']['label'][0]]
    else: row['provenance'][field][0][mutation]=0
    result=compare(EXPECTED['fixtures'][0],actual)
    assert result['status']=='partial'
    assert any(c['field']==f'activities.9.provenance.{field}' and not c['match'] for c in result['comparisons'])


@pytest.mark.parametrize('mutation',['missing','rows','kind','start','end','labels'])
def test_pause_group_mutations_fail(extracted,mutation):
    actual=copy.deepcopy(extracted[1])
    if mutation=='missing': actual['pause_groups']=[]
    else: actual['pause_groups'][0][mutation]=[] if mutation in ('rows','labels') else 'changed'
    result=compare(EXPECTED['fixtures'][1],actual)
    assert result['status']=='partial'
    assert any(c['field']=='pause_groups' and not c['match'] for c in result['comparisons'])


@pytest.mark.parametrize('value',[1,99])
def test_wrong_or_duplicate_exported_source_order_fails(extracted,value):
    actual=copy.deepcopy(extracted[2]); actual['activities'][1]['source_order']=value
    result=compare(EXPECTED['fixtures'][2],actual)
    assert result['status']=='partial'
    assert any(c['field']=='activities.2.source_order' and not c['match'] for c in result['comparisons'])


@pytest.mark.parametrize('boundary',['gap','unresolved','missing_end'])
def test_unproven_or_non_touching_pause_rows_do_not_merge(boundary):
    rows=[dict(source_order=1,label='MealBreak',start_instant='2030-01-01T12:00:00+01:00',end_instant='2030-01-01T12:30:00+01:00'),
          dict(source_order=2,label='Paid meal before',start_instant='2030-01-01T12:30:00+01:00',end_instant='2030-01-01T12:40:00+01:00')]
    if boundary=='gap': rows[1]['start_instant']='2030-01-01T12:31:00+01:00'
    elif boundary=='unresolved': rows[0]['end_instant']=rows[1]['start_instant']=None
    else: rows[1]['end_instant']=None
    assert len(pdf_import.group_pauses(rows))==2


def test_explicit_fact_origins(extracted):
    comparisons=compare(EXPECTED['fixtures'][2],extracted[2])['comparisons']
    origins={c['field']:c['actual_origin'] for c in comparisons}
    assert origins['timezone']=='owner-approved'
    for path in ('header.pages','duty_occurrences','duty_suffixes','activity_count','activities.1.source_order','activities.1.start_day','activities.1.start_instant','pause_groups'):
        assert origins[path]=='derived'
    for path in ('header.service_date','header.weekday','activities.1.label','activities.1.start','duties'):
        assert origins[path]=='extracted'


def test_manual_owner_completion_cannot_pass_automatic_completeness(extracted):
    actual=copy.deepcopy(extracted[5])
    expected=EXPECTED['fixtures'][5]
    actual['activities'][12].update({key:expected['activities'][12][key] for key in expected['activities'][12]['owner_fields']})
    actual['activities'][12].update(start_day=0,start_instant='2030-01-07T15:33:00+01:00')
    actual['unresolved']=[]
    result=compare(expected,actual)
    assert result['owner_assistance_gaps']==0
    assert result['owner_assistance_required'] and result['status']=='partial'


@pytest.mark.parametrize('mutation',['missing_row','changed_time','changed_endpoint','changed_header','changed_duty','missing_provenance'])
def test_comparator_fails_deliberate_lost_or_changed_facts(extracted,mutation):
    actual=copy.deepcopy(extracted[2])
    if mutation=='missing_row': actual['activities'].pop()
    elif mutation=='changed_time': actual['activities'][1]['start']='07:00'
    elif mutation=='changed_endpoint': actual['activities'][1]['destination']='invented'
    elif mutation=='changed_header': actual['header']['end']='09:25'
    elif mutation=='changed_duty': actual['duties'][0]['value']='960999'
    else: actual['activities'][1]['provenance']={}
    result=compare(EXPECTED['fixtures'][2],actual)
    assert result['status']=='partial' and result['source_mismatches']>0


@pytest.mark.parametrize('data,filename,code',[
    (b'hello','a.pdf','wrong_type'),(b'%PDF-1.4','a.txt','wrong_type'),
    (b'%PDF-'+b' '*pdf_import.MAX_BYTES,'a.pdf','size_limit'),
    (b'%PDF-corrupt','a.pdf','corrupt_or_unsupported'),
    (synthetic_pdf(),'a.pdf','image_only_or_empty'),
    (synthetic_pdf(21),'a.pdf','page_limit'),
    (synthetic_pdf(encrypted=True),'a.pdf','encrypted'),
],ids=['wrong_magic','wrong_extension','excess_size','corrupt','image_only','excess_pages','encrypted'])
def test_explicit_rejections(data,filename,code,capsys):
    with pytest.raises(ImportFailure,match='^'+code+'$'):
        extract_pdf(data,filename=filename)
    assert not multiprocessing.active_children()
    assert capsys.readouterr().out==''


def test_timeout_and_cancellation_terminate_worker(extracted):
    data=(FIXTURES/EXPECTED['fixtures'][0]['file']).read_bytes()
    before=set(multiprocessing.active_children())
    with pytest.raises(ImportFailure,match='timeout'):
        extract_pdf(data,timeout=.001)
    cancel=Event(); cancel.set()
    with pytest.raises(ImportFailure,match='cancelled'):
        extract_pdf(data,cancel=cancel)
    cancel.clear(); timer=Timer(.01,cancel.set); timer.start()
    try:
        with pytest.raises(ImportFailure,match='cancelled'):
            extract_pdf(data,cancel=cancel)
    finally:
        timer.cancel(); timer.join()
    assert set(multiprocessing.active_children())==before


def test_bounded_worker_output(monkeypatch):
    monkeypatch.setattr(pdf_import,'parse_document',lambda data:{'large':'x'*(pdf_import.MAX_OUTPUT+1)})
    # _worker redirects descriptors: isolate it in a child so pytest output is untouched.
    # Check output transport with a real pipe instead of the parent's copied object.
    receive,send=multiprocessing.get_context('fork').Pipe(duplex=False)
    process=multiprocessing.get_context('fork').Process(target=pdf_import._worker,args=(b'',send))
    process.start(); send.close()
    assert receive.poll(5)
    assert json.loads(receive.recv_bytes(pdf_import.MAX_OUTPUT))=={'error':'output_limit'}
    process.join(5); assert not process.is_alive()
    receive.close(); process.close()


def test_missing_and_changed_inputs_never_pass(tmp_path):
    result=qualify(tmp_path)
    assert all(r['status']=='untested' for r in result['fixtures'])
    (tmp_path/EXPECTED['fixtures'][0]['file']).write_bytes(b'%PDF-changed')
    assert qualify(tmp_path)['fixtures'][0]['reason']=='unapproved_input_hash'
