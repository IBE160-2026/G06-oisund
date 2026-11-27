"""A rejected replacement leaves committed routes and the referenced NSR generation."""

from datetime import UTC, date, datetime
from zipfile import ZipFile

import pytest

from app import position_coordinates, quay_catalogue, route_catalogue
from app.private_storage import database
from test_private_access import client, login, pytestmark, synthetic_only, users
from test_quay_catalogue import BOUNDARY, QUAY, entry, point


def archive_with(path, stops):
    with ZipFile(path, 'w') as archive:
        archive.writestr('tiamat-export-CurrentAndFuture-1.xml', f"""
          <PublicationDelivery xmlns="http://www.netex.org.uk/netex">
            <PublicationTimestamp>2026-11-22T12:00:00</PublicationTimestamp>
            <SiteFrame><stopPlaces>{stops}</stopPlaces></SiteFrame>
          </PublicationDelivery>""")


def test_rejected_nsr_import_preserves_api_and_dated_platforms(tmp_path, monkeypatch, client, users):
    day = date(2061, 11, 30)
    observed = datetime.now(UTC)
    nsr = tmp_path / 'nsr.zip'
    archive_with(nsr, entry('4', '2026-11-25T00:00:00', BOUNDARY) + entry('5', '2026-12-01T00:00:00'))
    calls = [{'quay_id': QUAY, 'departure': {'day_offset': 0, 'raw_time': '23:59:00'}}]
    journey = {'pattern_id': 'synthetic', 'calls': calls}

    def catalogue(*args):
        return [('26', {'provenance': {'generation': args[3]},
                        'days': {day: {'journeys': {'synthetic': journey}, 'reasons': []}}})]

    monkeypatch.setattr(route_catalogue, 'read_catalogue', catalogue)
    try:
        route_catalogue.import_dates(None, [day], observed, '99001', ('26',), nsr, '99001', observed, True)
        with database() as conn:
            active = route_catalogue.lookup(conn, day, observed, '26')
            revision = active['provenance']['nsr_revision']
        frozen = {'position_coordinate_revision': revision, 'provenance': {'nsr_revision': revision}, 'calls': calls}
        assert login(client, users).status_code == 200
        assert client.get('/health').status_code == 200
        archive_with(nsr, entry('6', '2026-12-01T00:00:00', override='<Name>' + 'x' * 600 + '</Name>'))
        monkeypatch.setattr(quay_catalogue, 'XML_CHUNK_BYTES', 64)
        monkeypatch.setattr(quay_catalogue, 'MAX_STOP_BYTES', 512)
        with pytest.raises(ValueError, match='StopPlace exceeds its XML byte budget'):
            route_catalogue.import_dates(None, [day], observed, '99002', ('26',), nsr, '99002', observed, True)
        assert client.get('/health').status_code == 200
        with database() as conn:
            assert route_catalogue.lookup(conn, day, observed, '26') == active
            old_catalogue = quay_catalogue.load_for_reference(conn, frozen)
        assert point(old_catalogue, '2026-11-30T22:59:00Z')[0]['quay_version'] == '4'
        assert point(old_catalogue, '2026-11-30T23:01:00Z')[0]['quay_version'] == '5'
    finally:
        with database() as conn:
            conn.execute("DELETE FROM public_route_days WHERE service_date=%s AND line_code='26'", (day,))
            conn.execute("DELETE FROM public_quay_versions WHERE left(revision,17) IN ('nsr-future-99001-', 'nsr-future-99002-')")
