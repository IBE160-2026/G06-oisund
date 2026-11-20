"""Independently labelled controlled XML and two dated plan examples."""

from datetime import datetime, UTC
from uuid import UUID

import pytest

from app.automatic_notice_relevance import classify
from app.automatic_notice_source import SourceError, parse_page


REQUESTOR = UUID('d55c9441-4cc0-43f8-b6a3-e195675c9a09')
NOW = datetime(2026, 11, 20, 9, tzinfo=UTC)
HEADERS = {'datasetid': 'TRO', 'requestorid': str(REQUESTOR)}
LINE20 = '<Networks><AffectedNetwork><NetworkRef>TRO:Network:1</NetworkRef><AffectedLine><LineRef>TRO:Line:1_20</LineRef></AffectedLine></AffectedNetwork></Networks>'
LINE24 = LINE20.replace('1_20', '1_24')
STOP = '<StopPoints><AffectedStopPoint><StopPointRef>NSR:StopPlace:55902</StopPointRef></AffectedStopPoint></StopPoints>'
BROAD = '<Networks><AffectedNetwork><NetworkRef>TRO:Network:1</NetworkRef><AllLines>true</AllLines></AffectedNetwork></Networks>'
EVENING = ('2026-11-23T22:00:00+01:00', '2026-11-23T23:00:00+01:00')
MORNING = ('2026-11-24T00:05:00+01:00', '2026-11-24T01:30:00+01:00')


def situation(name='controlled', affects=LINE20, windows=(EVENING,), status='open', version=None, text=None):
    validity = ''.join('<ValidityPeriod>' + (f'<StartTime>{start}</StartTime>' if start else '') +
                       (f'<EndTime>{end}</EndTime>' if end else '') + '</ValidityPeriod>' for start, end in windows)
    return (f'<PtSituationElement><CreationTime>2026-11-19T06:00:00+01:00</CreationTime>'
            f'<ParticipantRef>TRO</ParticipantRef><SituationNumber>TRO:SituationNumber:{name}</SituationNumber>'
            + (f'<Version>{version}</Version>' if version else '') + (f'<Progress>{status}</Progress>' if status else '')
            + validity + (text or '<Summary xml:lang="NO">Kontrollert eksempel</Summary>')
            + f'<Affects>{affects}</Affects></PtSituationElement>')


def envelope(items='', flag='false', requestor=REQUESTOR, stamp='2026-11-20T10:00:00.3215431+01:00'):
    return (f'<Siri xmlns="http://www.siri.org.uk/siri" version="2.0"><ServiceDelivery>'
            f'<ResponseTimestamp>{stamp}</ResponseTimestamp><RequestMessageRef>{requestor}</RequestMessageRef>'
            f'<MoreData>{flag}</MoreData><SituationExchangeDelivery><Situations>{items}</Situations>'
            f'</SituationExchangeDelivery></ServiceDelivery></Siri>').encode()


def page(items='', flag='false', requestor=REQUESTOR, stamp='2026-11-20T10:00:00.3215431+01:00'):
    return parse_page(envelope(items, flag, requestor, stamp), HEADERS | {'requestorid': str(requestor)}, requestor)


def activity(line='20', start='2026-11-23T22:10:00+01:00', end='2026-11-23T22:20:00+01:00'):
    return {'id': 'controlled-activity', 'line': line, 'start': start, 'end': end}


@pytest.mark.parametrize('identifier,plan,scope,windows,status,expected,reason', [
    ('day-one-line20', activity(), LINE20, (EVENING,), 'open', 'possible-relevance', 'exact-line-planned-overlap'),
    ('day-two-line24', activity('24', *MORNING), LINE24, (MORNING,), 'open', 'possible-relevance', 'exact-line-planned-overlap'),
    ('line020', activity('020'), LINE20, (EVENING,), 'open', 'review', 'no-matching-printed-line'),
    ('lineX20', activity('X20'), LINE20, (EVENING,), 'open', 'review', 'no-matching-printed-line'),
    ('line20E', activity('20E'), LINE20, (EVENING,), 'open', 'review', 'no-matching-printed-line'),
    ('line24-for-20', activity('24'), LINE20, (EVENING,), 'open', 'review', 'no-matching-printed-line'),
    ('codespace-mismatch', activity(), LINE20.replace('TRO:Line', 'ATB:Line'), (EVENING,), 'open', 'review', 'line-binding-unavailable'),
    ('other-authority', activity(), LINE20.replace('<LineRef>', '<AuthorityRef>TRO:Authority:2</AuthorityRef><LineRef>'), (EVENING,), 'open', 'review', 'authority-unverified'),
    ('other-operator', activity(), LINE20.replace('<LineRef>', '<OperatorRef>TRO:Operator:2</OperatorRef><LineRef>'), (EVENING,), 'open', 'review', 'authority-unverified'),
    ('out-of-date', activity('20', '2026-11-25T09:00+01:00', '2026-11-25T10:00+01:00'), LINE20, ((EVENING[0], None),), 'open', 'review', 'no-dated-binding'),
    ('overnight', activity('24', '2026-11-23T23:55+01:00', '2026-11-24T00:10+01:00'), LINE24, (MORNING,), 'open', 'possible-relevance', 'exact-line-planned-overlap'),
    ('outside-pilot-overnight', activity('24', '2026-11-24T23:55+01:00', '2026-11-25T00:10+01:00'), LINE24, (('2026-11-25T00:01+01:00', '2026-11-25T00:09+01:00'),), 'open', 'review', 'no-dated-binding'),
    ('touches-inactive-end', activity('20', EVENING[1], '2026-11-23T23:10+01:00'), LINE20, (EVENING,), 'open', 'outside-scope', 'no-planned-overlap'),
    ('touches-inactive-start', activity('20', '2026-11-23T21:30+01:00', EVENING[0]), LINE20, (EVENING,), 'open', 'outside-scope', 'no-planned-overlap'),
    ('point-at-start', activity('20', EVENING[0], EVENING[0]), LINE20, (EVENING,), 'open', 'possible-relevance', 'exact-line-planned-overlap'),
    ('point-at-end', activity('20', EVENING[1], EVENING[1]), LINE20, (EVENING,), 'open', 'outside-scope', 'no-planned-overlap'),
    ('second-window', activity('24', *MORNING), LINE24, (EVENING, MORNING), 'open', 'possible-relevance', 'exact-line-planned-overlap'),
    ('between-windows', activity('20', '2026-11-23T23:10+01:00', '2026-11-23T23:30+01:00'), LINE20, (EVENING, MORNING), 'open', 'outside-scope', 'no-planned-overlap'),
    ('missing-plan-offset', activity(start='2026-11-23T22:10'), LINE20, (EVENING,), 'open', 'review', 'uncertain-planned-time'),
    ('bad-plan-offset', activity(start='2026-11-23T22:10+02:00'), LINE20, (EVENING,), 'open', 'review', 'uncertain-planned-time'),
    ('dst-gap', activity(start='2026-03-29T02:30+01:00'), LINE20, (EVENING,), 'open', 'review', 'uncertain-planned-time'),
    ('missing-source-offset', activity(), LINE20, ((EVENING[0][:-6], EVENING[1]),), 'open', 'review', 'uncertain-validity'),
    ('unknown-source-offset', activity(), LINE20, ((EVENING[0][:-6]+'-00:00', EVENING[1]),), 'open', 'review', 'uncertain-validity'),
    ('reverse-window', activity(), LINE20, (EVENING[::-1],), 'open', 'review', 'uncertain-validity'),
    ('open-window', activity(), LINE20, ((EVENING[0], None),), 'open', 'possible-relevance', 'open-ended-validity'),
    ('nested-direction', activity(), LINE20.replace('</AffectedLine>', '<DirectionRef>direction</DirectionRef></AffectedLine>'), (EVENING,), 'open', 'possible-relevance', 'unresolved-qualifiers'),
    ('nested-quay', activity(), LINE20.replace('</AffectedLine>', f'<AffectedRoute>{STOP.replace("StopPlace", "Quay")}</AffectedRoute></AffectedLine>'), (EVENING,), 'open', 'possible-relevance', 'unresolved-qualifiers'),
    ('stop-only', activity(), STOP, (EVENING,), 'open', 'review', 'stop-scope-unverified'),
    ('quay-only', activity(), STOP.replace('StopPlace', 'Quay'), (EVENING,), 'open', 'review', 'stop-scope-unverified'),
    ('broad', activity(), BROAD, (EVENING,), 'open', 'broad-context', 'explicit-broad-scope'),
    ('broad-foreign-network', activity(), BROAD.replace('TRO:Network:1', 'TRO:Network:9'), (EVENING,), 'open', 'review', 'scope-unresolved'),
    ('empty-lines', activity(), '<Networks/>', (EVENING,), 'open', 'review', 'scope-unresolved'),
    ('explicit-ferry', activity(), LINE20.replace('</AffectedLine>', '<VehicleMode>ferry</VehicleMode></AffectedLine>'), (EVENING,), 'open', 'outside-scope', 'other-mode'),
    ('explicit-close', activity(), LINE20, (EVENING,), 'closed', 'outside-scope', 'source-closed'),
    ('expired', activity(), LINE20, (('2026-11-19T10:00Z', '2026-11-19T12:00Z'),), 'open', 'outside-scope', 'validity-expired'),
    ('unknown-status', activity(), LINE20, (EVENING,), None, 'possible-relevance', 'source-status-unknown'),
    ('future-source-unknown-end', activity(), LINE20, ((EVENING[0], 'not-an-instant'),), 'open', 'review', 'uncertain-validity'),
], ids=lambda value: value if isinstance(value, str) and ' ' not in value and '<' not in value else None)
def test_relevance(identifier, plan, scope, windows, status, expected, reason):
    facts = page(situation(affects=scope, windows=windows, status=status)).items[0]
    result = classify(facts, [plan], NOW)
    assert result['classification'] == expected, identifier
    assert reason in result['reasons']
    assert bool(result['matches']) == (expected == 'possible-relevance')


def test_fields_preserve_source_text_qualifiers_and_missing_clocks():
    text = ('<Summary xml:lang="nb">&lt;svg&gt;Ordlyd &amp; tegn</Summary><Advice>Råd</Advice><InfoLinks>'
            '<InfoLink><Uri>javascript:alert(1)</Uri></InfoLink><InfoLink><Uri>https://999.9.9.9/</Uri></InfoLink>'
            '<InfoLink><Uri>https://svipper.no/avvik</Uri></InfoLink></InfoLinks>')
    parsed = page(situation(affects=LINE20 + STOP, windows=((EVENING[0], None), MORNING), text=text))
    item = parsed.items[0]
    assert parsed.response_at.isoformat() == '2026-11-20T09:00:00.321543+00:00'
    assert item['summary'] == [{'language': 'nb', 'text': '<svg>Ordlyd & tegn'}]
    assert item['links'] == ['https://svipper.no/avvik']
    assert item['version'] is item['publisher_updated_at'] is None
    assert item['source_created_at'] == '2026-11-19T06:00:00+01:00'
    assert item['windows'] == [{'start': EVENING[0], 'end': None}, {'start': MORNING[0], 'end': MORNING[1]}]
    assert item['affects'][1]['children'][0]['children'][0]['value'] == 'NSR:StopPlace:55902'


@pytest.mark.parametrize('payload,headers,code', [
    (b'', HEADERS, 'xml-size'), (b'<Siri/>', HEADERS, 'siri-envelope'),
    (b'<!DOCTYPE a [<!ENTITY replacement "x">]><a>&replacement;</a>', HEADERS, 'xml-doctype'),
    (envelope(flag='1'), HEADERS, 'more-data'),
    (envelope().replace(b'<MoreData>false</MoreData>', b''), HEADERS, 'more-data'),
    (envelope().replace(b'<Situations></Situations>', b''), HEADERS, 'field-Situations'),
    (envelope().replace(b'<SituationExchangeDelivery>', b'<SituationExchangeDelivery><Status>false</Status>'), HEADERS, 'delivery-status'),
    (envelope(stamp='2026-11-20T09:00:00'), HEADERS, 'response-time'),
    (envelope().replace(str(REQUESTOR).encode(), b'different'), HEADERS, 'xml-continuity'),
    (envelope().replace(b'<Situations>', f'<RequestMessageRef>{REQUESTOR}</RequestMessageRef><Situations>'.encode()), HEADERS, 'xml-continuity'),
    (envelope().replace(b'<Situations>', b'<MoreData>true</MoreData><Situations>'), HEADERS, 'more-data'),
    (envelope(), HEADERS | {'requestorid': 'different'}, 'header-continuity'),
    (envelope(), HEADERS | {'datasetid': 'ALL'}, 'header-continuity'),
    (envelope(situation().replace('<ParticipantRef>TRO', '<ParticipantRef>ATB')), HEADERS, 'source-scope'),
    (envelope(situation() * 6), HEADERS, 'situation-collection'),
    (envelope(situation(affects='<Depth>' * 33 + '</Depth>' * 33)), HEADERS, 'xml-complexity'),
    (b'x' * (512 * 1024 + 1), HEADERS, 'xml-size'),
])
def test_reject_unsafe_or_unqualified_pages(payload, headers, code):
    with pytest.raises(SourceError) as error:
        parse_page(payload, headers, REQUESTOR)
    assert error.value.code == code
