"""The current-and-future NSR source selects the exact version at a dated stop call."""

from datetime import UTC, datetime
from io import BytesIO
from zipfile import ZipFile

import pytest

from app import position_coordinates, quay_catalogue


QUAY = 'NSR:Quay:123'
PARENT = 'NSR:StopPlace:456'
BOUNDARY = '2026-12-01T00:00:00+01:00'


def entry(version, start, end='', override=''):
    ending = f'<ToDate>{end}</ToDate>' if end else ''
    return f'''
        <StopPlace id="{PARENT}" version="{version}">
            <ValidBetween><FromDate>{start}</FromDate>{ending}</ValidBetween>
            <quays><Quay id="{QUAY}" version="{version}">
                {override}
                <Centroid><Location><Latitude>69.65</Latitude><Longitude>18.9</Longitude></Location></Centroid>
            </Quay></quays>
        </StopPlace>
    '''


def source(tmp_path, *entries, outside=''):
    xml = f'''
        <PublicationDelivery xmlns="http://www.netex.org.uk/netex">
            <PublicationTimestamp>2026-11-22T12:00:00</PublicationTimestamp>
            <dataObjects><SiteFrame>{outside}<stopPlaces>{''.join(entries)}</stopPlaces></SiteFrame></dataObjects>
        </PublicationDelivery>
    '''
    archive = tmp_path / 'future.zip'
    with ZipFile(archive, 'w') as output:
        output.writestr('tiamat-export-CurrentAndFuture-20261122120000001.xml', xml)
    source, records = quay_catalogue.read(archive, '1234567890', {QUAY}, datetime(2026, 11, 22, 12, tzinfo=UTC))
    return {**source, 'stops': records[QUAY]['versions']}


def point(data, arrival, departure=None, *, parent=PARENT):
    call = {'quay_id': QUAY, 'stop_place_id': parent, 'scheduled_stop_point_id': 'TRO:ScheduledStopPoint:13',
            'arrival': {'utc': arrival}, 'departure': {'utc': departure} if departure else None}
    return position_coordinates.point_for(call, data, True, False)


def test_inherited_quay_versions_use_calendar_instants(tmp_path):
    data = source(tmp_path, entry('4', '2026-11-25T00:00:00', BOUNDARY), entry('5', '2026-12-01T00:00:00'))
    assert data['stops'][1]['quay_validity'] == {'valid_from': BOUNDARY, 'valid_until': None}
    assert data['stops'][1]['validity_basis'] == 'containing-stop-place'
    assert point(data, '2026-11-30T22:59:00Z')[0]['quay_version'] == '4'
    assert point(data, '2026-11-30T23:01:00Z')[0]['quay_version'] == '5'
    assert point(data, '2026-11-30T22:59:45Z', '2026-11-30T23:00:15Z') == (None, PARENT, 'coordinate-ambiguous')
    legacy = {**data, 'scope': None, 'stops': [data['stops'][1]]}
    assert point(legacy, '2026-11-30T23:01:00Z') == (None, PARENT, 'validity-unknown')


def test_overlapping_or_unsupported_quay_conditions_remain_manual(tmp_path):
    overlapping = source(tmp_path, entry('4', '2026-11-25T00:00:00'), entry('5', '2026-12-01T00:00:00'))
    assert point(overlapping, '2026-11-30T23:01:00Z') == (None, PARENT, 'coordinate-ambiguous')
    assert point(overlapping, '2026-11-30T23:01:00Z', parent=None) == (None, PARENT, 'coordinate-ambiguous')
    unsupported = source(tmp_path, entry('5', '2026-12-01T00:00:00', override='<validityConditions><AvailabilityCondition/></validityConditions>'))
    assert point(unsupported, '2026-11-30T23:01:00Z') == (None, PARENT, 'validity-unknown')
    wrapped = source(tmp_path, entry('5', '2026-11-25T00:00:00', override=f'''
        <validityConditions><ValidBetween><FromDate>{BOUNDARY}</FromDate></ValidBetween></validityConditions>
    '''))
    assert point(wrapped, '2026-11-30T23:01:00Z')[0]['quay_version'] == '5'
    assert point(wrapped, '2026-11-30T23:01:00Z')[0]['validity_basis'] == 'quay'
    assert point(wrapped, '2026-11-30T22:59:00Z') == (None, PARENT, 'validity-mismatch')
    assert quay_catalogue.zoned('2026-10-25T02:30:00') is None
    assert quay_catalogue.zoned('2026-03-29T02:30:00') is None


@pytest.mark.parametrize('invalid_end', ['<ToDate/>', '<ToDate> </ToDate>', '<ToDate>invalid</ToDate>',
                                         '<ToDate/><ToDate/>'])
def test_present_but_invalid_end_is_not_open_ended(tmp_path, invalid_end):
    xml = entry('5', '2026-11-25T00:00:00').replace('</ValidBetween>', invalid_end + '</ValidBetween>')
    data = source(tmp_path, xml)
    assert point(data, '2026-11-30T23:01:00Z') == (None, PARENT, 'validity-unknown')


def test_competitor_overlapping_only_part_of_call_still_blocks_automation(tmp_path):
    competitor = entry('5', '2026-12-01T00:00:00', '2026-12-01T00:01:00')
    competitor = competitor.replace('<Longitude>18.9</Longitude>', '')
    data = source(tmp_path, entry('4', '2026-11-25T00:00:00'), competitor)
    assert len(data['stops']) == 2
    assert point(data, '2026-11-30T22:59:00Z', '2026-11-30T23:02:00Z') == (None, PARENT, 'coordinate-ambiguous')
    assert point(data, '2026-11-30T23:02:00Z')[0]['quay_version'] == '4'
    reversed_interval = source(tmp_path, entry('4', '2026-11-25T00:00:00'),
                               entry('5', '2026-12-01T00:01:00', '2026-12-01T00:00:00'))
    assert point(reversed_interval, '2026-11-30T23:02:00Z') == (None, PARENT, 'coordinate-ambiguous')


def test_future_archive_rejects_entity_declarations_even_at_read_boundaries():
    payload = quay_catalogue.SourceXML(BytesIO(b'<?xml version="1.0"?><!DOCTYPE x [<!ENTITY a "b">]>'))
    payload.read(23)
    with pytest.raises(ValueError, match='XML declaration'):
        payload.read(20)


@pytest.mark.parametrize('limit', ['bytes', 'nodes'])
def test_stop_budget_rejects_during_xml_read(tmp_path, monkeypatch, limit):
    monkeypatch.setattr(quay_catalogue, 'XML_CHUNK_BYTES', 64)
    label = 'byte' if limit == 'bytes' else 'node'
    if limit == 'bytes':
        monkeypatch.setattr(quay_catalogue, 'MAX_STOP_BYTES', 512)
        extra = '<Name>' + 'x' * 600 + '</Name>'
    else:
        monkeypatch.setattr(quay_catalogue, 'MAX_STOP_NODES', 15)
        extra = '<Name>x</Name>' * 16
    # Fail while the stop is open, before trying to extract any Quay from it.
    def must_not_extract(*args):
        pytest.fail('The over-budget stop reached Quay extraction')
    monkeypatch.setattr(quay_catalogue, 'quay_record', must_not_extract)
    with pytest.raises(ValueError, match=f'StopPlace exceeds its XML {label} budget'):
        source(tmp_path, entry('5', '2026-12-01T00:00:00', override=extra))


def test_unrelated_gml_text_uses_a_separate_bound(tmp_path, monkeypatch):
    monkeypatch.setattr(quay_catalogue, 'XML_CHUNK_BYTES', 64)
    monkeypatch.setattr(quay_catalogue, 'MAX_XML_GAP_BYTES', 256)
    monkeypatch.setattr(quay_catalogue, 'MAX_XML_OUTSIDE_STOP_BYTES', 1024)
    geometry = '<gml:posList xmlns:gml="http://www.opengis.net/gml/3.2">' + '18.90 69.65 ' * 50 + '</gml:posList>'
    data = source(tmp_path, entry('5', '2026-12-01T00:00:00'), outside=geometry)
    assert point(data, '2026-11-30T23:01:00Z')[0]['quay_version'] == '5'

def grouped_child(version='5', reference_version='9', override=''):
    return entry(version, BOUNDARY, override=override).replace(
        f'<ValidBetween><FromDate>{BOUNDARY}</FromDate></ValidBetween>',
        f'<ParentSiteRef ref="NSR:StopPlace:789" version="{reference_version}"/>',
    )


def group(start='2026-11-29T00:00:00', end=BOUNDARY):
    return f'''
        <StopPlace id="NSR:StopPlace:789" version="9">
            <ValidBetween><FromDate>{start}</FromDate><ToDate>{end}</ToDate></ValidBetween>
        </StopPlace>
    '''


def test_exact_parent_site_interval_for_an_undated_child(tmp_path):
    data = source(tmp_path, grouped_child(), group())
    assert data['revision'].endswith('-v2')
    assert data['stops'][0]['stop_place_id'] == PARENT
    assert data['stops'][0]['stop_place_validity'] == data['stops'][0]['quay_validity']
    assert point(data, '2026-11-30T22:59:00Z')[0]['validity_basis'] == 'parent-site'
    assert point(data, '2026-11-30T23:00:00Z') == (None, PARENT, 'validity-mismatch')
    assert point(data, '2026-11-28T22:59:00Z') == (None, PARENT, 'validity-mismatch')
    assert point(data, '2026-11-30T22:59:00Z', '2026-11-30T23:00:01Z') == (None, PARENT, 'validity-mismatch')
    early = source(tmp_path, group('2020-01-01T00:00:00Z'), grouped_child())
    assert point(early, '2026-11-21T12:00:00Z') == (None, PARENT, 'validity-mismatch')


def test_missing_or_ambiguous_parent_site_does_not_qualify(tmp_path):
    for entries in ((grouped_child(),), (grouped_child(reference_version='8'), group()),
                    (group(), grouped_child(), group()),
                    (grouped_child(), '</stopPlaces></SiteFrame><SiteFrame><stopPlaces>', group())):
        data = source(tmp_path, *entries)
        assert point(data, '2026-11-30T22:59:00Z') == (None, PARENT, 'validity-unknown')
    data = source(tmp_path, group(), grouped_child(), outside='<validityConditions><AvailabilityCondition/></validityConditions>')
    assert point(data, '2026-11-30T22:59:00Z') == (None, PARENT, 'validity-unknown')


def test_parent_site_never_masks_child_conditions_or_conflicting_quays(tmp_path):
    unknown = source(tmp_path, group(), grouped_child(override='<ValidBetween/>'))
    assert point(unknown, '2026-11-30T22:59:00Z') == (None, PARENT, 'validity-unknown')
    child_condition = '<ValidBetween><FromDate>invalid</FromDate></ValidBetween>'
    undated = grouped_child().replace('<ParentSiteRef', child_condition + '<ParentSiteRef')
    unknown = source(tmp_path, group(), undated)
    assert point(unknown, '2026-11-30T22:59:00Z') == (None, PARENT, 'validity-unknown')
    conflict = grouped_child('6').replace('18.9', '18.91')
    ambiguous = source(tmp_path, group(), grouped_child(), conflict)
    assert point(ambiguous, '2026-11-30T22:59:00Z') == (None, PARENT, 'coordinate-ambiguous')


def test_explicit_end_only_still_expires(tmp_path):
    end_only = group().replace('<FromDate>2026-11-29T00:00:00</FromDate>', '')
    data = source(tmp_path, end_only, grouped_child())
    assert point(data, '2026-11-30T22:59:00Z')[0]['quay_validity'] == {'valid_from': None, 'valid_until': BOUNDARY}
    assert point(data, '2026-11-30T23:00:00Z') == (None, PARENT, 'validity-mismatch')
