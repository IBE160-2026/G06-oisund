"""Versioned NeTEx catalogue for the published Tromsø city lines."""

import argparse
from collections import Counter
from datetime import UTC, date, datetime, timedelta
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
import sys
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZIP_STORED, ZipFile

from . import quay_catalogue, route_source as netex

CODES = tuple('20 21 22 X23 24 26 26B X27 28 X29 30 X31 X32 33 34 X35 X36 40 42 X43 X44'.split())
LINE_IDS = {code: f'TRO:Line:1_{25 if code == "26B" else code.lstrip("X")}' for code in CODES}
CODES_BY_ID = {identifier: code for code, identifier in LINE_IDS.items()}
MAX_ARCHIVE_BYTES = 16_000_000


def code_for(value):
    return CODES_BY_ID.get(value, value.strip().upper()) if isinstance(value, str) else None


def service_dates(first, last):
    days = (last - first).days + 1
    if not 1 <= days <= 14:
        raise ValueError('Import an inclusive range of 1 to 14 service dates')
    return tuple(first + timedelta(days=offset) for offset in range(days))


def read_catalogue(path, dates, observed_at, generation, codes=CODES):
    if not netex.GENERATION_ID.fullmatch(generation):
        raise ValueError('Missing Entur archive generation')
    with Path(path).open('rb') as stream:
        raw = stream.read(MAX_ARCHIVE_BYTES + 1)
    if len(raw) > MAX_ARCHIVE_BYTES:
        raise ValueError('NeTEx archive exceeds the size limit')
    digest = sha256(raw).hexdigest()

    with ZipFile(BytesIO(raw)) as archive:
        entries = archive.infolist()
        names = {entry.filename for entry in entries}
        if (len(entries) > 512 or len(entries) != len(names)
                or sum(entry.file_size for entry in entries) > 160_000_000
                or any(not re.fullmatch(r'[a-zA-Z0-9_.()-]{1,200}\.xml', entry.filename)
                       or entry.flag_bits & 1 or entry.file_size > 20_000_000
                       or entry.compress_type not in (ZIP_STORED, ZIP_DEFLATED) for entry in entries)):
            raise ValueError('Unexpected NeTEx archive inventory')
        shared = netex.xml_member(archive, netex.SHARED_MEMBER)
        for code in codes:
            prefix = f'TRO_{LINE_IDS[code].replace(":", "-")}_{code}_'
            matches = [name for name in names if name.startswith(prefix)]
            if len(matches) != 1:
                raise ValueError(f'Expected one NeTEx member for line {code}, found {len(matches)}')
            member = matches[0]
            line = netex.xml_member(archive, member)
            netex.verify_line_reference_versions(line, shared)
            evidence = netex.normalize(line, shared, observed_at, line_id=LINE_IDS[code],
                                       public_code=code, dates=dates, expected=None)
            evidence['provenance'].update(generation=generation, sha256=digest,
                                          etag=None, parser_revision=2,
                                          manifest_revision='tromso-city', members=[member, netex.SHARED_MEMBER])
            yield code, evidence


def coverage_report(catalogue):
    return {code: {day.isoformat(): {
        'departures': len(value['journeys']),
        'morning_departures': sum(
            journey['calls'][0]['departure']['day_offset'] == 0
            and journey['calls'][0]['departure']['raw_time'] < '09:00:00'
            for journey in value['journeys'].values()
        ),
        'variants': dict(sorted(Counter(journey['pattern_id'] for journey in value['journeys'].values()).items())),
        'reasons': value['reasons'],
    } for day, value in evidence['days'].items()} for code, evidence in catalogue}


def publish(catalogue, observed_at, nsr):
    from psycopg.types.json import Jsonb
    from .private_storage import database

    with database() as conn:
        if nsr is not None:
            source, records = nsr
            with conn.cursor() as cursor:
                cursor.executemany(
                    'INSERT INTO public_quay_versions VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING',
                    ((source['revision'], identifier, Jsonb(source), Jsonb(record)) for identifier, record in records.items()),
                )
        for code, evidence in catalogue:
            for day, value in evidence['days'].items():
                conn.execute(
                    '''INSERT INTO public_route_days(service_date, line_code, observed_at, provenance, journeys)
                       VALUES (%s, %s, %s, %s, %s)
                       ON CONFLICT (service_date, line_code) DO UPDATE
                           SET observed_at = EXCLUDED.observed_at,
                               provenance = EXCLUDED.provenance, journeys = EXCLUDED.journeys
                       WHERE public_route_days.observed_at <= EXCLUDED.observed_at
                         AND (public_route_days.provenance->>'generation')::numeric
                             <= (EXCLUDED.provenance->>'generation')::numeric''',
                    (day, code, observed_at, Jsonb(evidence['provenance']), Jsonb(value['journeys'])),
                )


def lookup(conn, service_date, now, code):
    if code not in LINE_IDS:
        return {'coverage': 'unavailable', 'source_state': 'outside_scope',
                'reasons': ['line_outside_network'], 'provenance': None, 'journeys': {}}

    row = conn.execute('SELECT observed_at, provenance, journeys FROM public_route_days '
                       'WHERE service_date = %s AND line_code = %s', (service_date, code)).fetchone()
    if row is None:
        if code == '20' and service_date in netex.DATES:
            return netex.lookup(service_date, now)
        return {'coverage': 'unavailable', 'source_state': 'unavailable',
                'reasons': ['catalogue_missing'], 'provenance': None, 'journeys': {}}

    return {'coverage': 'complete', 'source_state': 'stale' if now - row['observed_at'] > timedelta(days=1) else 'available',
            'reasons': [], 'provenance': row['provenance'], 'journeys': row['journeys']}


def import_dates(archive, dates, observed, generation, codes, nsr_path, nsr_generation, nsr_observed, write):
    if any(stamp.utcoffset() != timedelta(0) or stamp > datetime.now(UTC) + timedelta(minutes=1)
           for stamp in (observed, nsr_observed)):
        raise ValueError('Use UTC observation times recorded when the public archives were fetched')
    catalogue = list(read_catalogue(archive, dates, observed, generation, codes))
    nsr = None
    if nsr_path is not None:
        scheduled = {day: set() for day in dates}
        for _, evidence in catalogue:
            for day, value in evidence['days'].items():
                scheduled[day].update(call['quay_id'] for journey in value['journeys'].values() for call in journey['calls'])
        wanted = set().union(*scheduled.values())
        nsr = quay_catalogue.read(nsr_path, nsr_generation, wanted, nsr_observed)
        if wanted and not nsr[1]:
            raise ValueError('NSR archive contains none of the planned platforms. The active catalogue was preserved.')
        for _, evidence in catalogue:
            evidence['provenance']['nsr_revision'] = nsr[0]['revision']
        print(json.dumps({'nsr_revision': nsr[0]['revision'], 'unmatched_quays': {
            day.isoformat(): sorted(identifiers - nsr[1].keys()) for day, identifiers in scheduled.items()
        }}), file=sys.stderr)
    coverage = coverage_report(catalogue)
    print(json.dumps(coverage, indent=2))
    if any(day['reasons'] for line in coverage.values() for day in line.values()):
        raise ValueError('Route import incomplete. The active catalogue was preserved.')
    if write:
        publish(catalogue, observed, nsr)


def import_bundle(dates, codes, write):
    cap = MAX_ARCHIVE_BYTES + quay_catalogue.MAX_ARCHIVE_BYTES + 4096
    data = sys.stdin.buffer.read(cap + 1)
    if len(data) > cap:
        raise ValueError('Public route bundle too large')
    with ZipFile(BytesIO(data)) as bundle, TemporaryDirectory(prefix='public-routes-') as tmp:
        limits = {'routes.zip': MAX_ARCHIVE_BYTES, 'quays.zip': quay_catalogue.MAX_ARCHIVE_BYTES, 'source.json': 2_048}
        entries = bundle.infolist()
        if (len(entries) != 3 or {entry.filename for entry in entries} != limits.keys()
                or any(entry.compress_type != ZIP_STORED or not 0 < entry.file_size <= limits[entry.filename]
                       or entry.flag_bits & 1 for entry in entries)):
            raise ValueError('Unexpected public route bundle')
        paths = {name: Path(tmp) / name for name in ('routes.zip', 'quays.zip')}
        for name, path in paths.items():
            path.write_bytes(bundle.read(name))
        source = json.loads(bundle.read('source.json'))
        routes, quays = source['routes'], source['quays']
        import_dates(
            paths['routes.zip'], dates, datetime.fromisoformat(routes['observed_at']), routes['generation'],
            codes, paths['quays.zip'], quays['generation'], datetime.fromisoformat(quays['observed_at']), write,
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument('archive', type=Path, nargs='?')
    inputs.add_argument('--bundle-stdin', action='store_true')
    parser.add_argument('--from-date', type=date.fromisoformat, required=True)
    parser.add_argument('--through-date', type=date.fromisoformat, required=True)
    parser.add_argument('--generation')
    parser.add_argument('--observed-at', type=datetime.fromisoformat)
    parser.add_argument('--nsr', type=Path)
    parser.add_argument('--nsr-generation')
    parser.add_argument('--nsr-observed-at', type=datetime.fromisoformat)
    parser.add_argument('--line', choices=CODES, action='append')
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    dates = service_dates(args.from_date, args.through_date)
    codes = args.line or CODES
    if args.bundle_stdin:
        import_bundle(dates, codes, args.publish)
    else:
        if not args.generation or not args.observed_at:
            parser.error('An archive path requires --generation and --observed-at')
        if args.nsr and (not args.nsr_generation or not args.nsr_observed_at):
            parser.error('--nsr requires --nsr-generation and --nsr-observed-at')
        import_dates(args.archive, dates, args.observed_at, args.generation, codes,
                     args.nsr, args.nsr_generation, args.nsr_observed_at or args.observed_at, args.publish)


if __name__ == '__main__':
    main()
