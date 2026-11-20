"""Collect bounded public NVDB evidence for manual road qualification."""

import argparse
from contextlib import contextmanager
from datetime import UTC, date, datetime
from hashlib import sha256
from http.client import HTTPException
import json
import os
from pathlib import Path
import re
import signal
from tempfile import NamedTemporaryFile
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener
from zipfile import ZIP_DEFLATED, ZipFile


BASE = 'https://nvdbapiles.atlas.vegvesen.no'
NETWORK = '/vegnett/api/v4/veglenkesekvenser/segmentert'
OBJECT_TYPES = (105, 573, 607, 616, 721, 856, 913, 977, 979)
SRID = 5973
PAGE_SIZE = 180
MAX_SEGMENTS = 500
MAX_LIMITS = 100
MAX_ATTEMPTS = 20
MAX_RETRIES = 2
MAX_PAGE_BYTES = 3_000_000
MAX_TOTAL_BYTES = 10_000_000
TIMEOUT_SECONDS = 12


class IncompleteEvidence(ValueError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def unique_json_members(pairs):
    result = {}
    for name, value in pairs:
        if name in result:
            raise IncompleteEvidence('NVDB returned a duplicate JSON member')
        result[name] = value
    return result


def reject_json_constant(_):
    raise IncompleteEvidence('NVDB returned a non-JSON numeric constant')


def collection_expired(_signum, _frame):
    raise IncompleteEvidence('NVDB collection deadline exceeded')


@contextmanager
def deadline(enabled):
    if not enabled or not hasattr(signal, 'SIGALRM'):
        yield
        return
    previous = signal.signal(signal.SIGALRM, collection_expired)
    signal.alarm(MAX_ATTEMPTS * TIMEOUT_SECONDS)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


class Collector:
    def __init__(self, archive, open_response):
        self.archive = archive
        self.open_response = open_response
        self.attempts = 0
        self.retries = 0
        self.bytes = 0
        self.pages = []

    def open(self, url):
        request = Request(url, headers={'Accept': 'application/json', 'X-Client': 'IBE160-Bussassistent-V2-evidence'})
        while self.attempts < MAX_ATTEMPTS:
            self.attempts += 1
            try:
                return self.open_response(request, timeout=TIMEOUT_SECONDS)
            except HTTPError as error:
                error.close()
                if error.code not in (502, 503, 504) or self.retries == MAX_RETRIES:
                    raise IncompleteEvidence(f'NVDB returned HTTP {error.code}') from error
            except (TimeoutError, URLError) as error:
                if not isinstance(getattr(error, 'reason', error), TimeoutError) or self.retries == MAX_RETRIES:
                    raise IncompleteEvidence('NVDB request failed') from error
            except (OSError, HTTPException) as error:
                raise IncompleteEvidence('NVDB response could not be opened') from error
            self.retries += 1
        raise IncompleteEvidence('NVDB request budget exhausted')

    def page(self, name, path, params):
        url = BASE + path + '?' + urlencode(params)
        maximum = min(MAX_PAGE_BYTES, MAX_TOTAL_BYTES - self.bytes)
        if maximum <= 0:
            raise IncompleteEvidence('NVDB byte budget exhausted')
        with self.open(url) as response:
            if response.status != 200:
                raise IncompleteEvidence(f'NVDB returned HTTP {response.status}')
            try:
                body = response.read(maximum + 1)
            except (OSError, HTTPException) as error:
                # A failed read may already have consumed bytes which cannot be counted safely.
                raise IncompleteEvidence('NVDB response body could not be read') from error
            if len(body) > maximum:
                raise IncompleteEvidence('NVDB response exceeds byte budget')
            content_length = response.headers.get('Content-Length')
            if content_length is not None and (not re.fullmatch(r'[0-9]+', content_length)
                                               or len(content_length) > 10 or int(content_length) != len(body)):
                raise IncompleteEvidence('NVDB response length mismatch')
            receipt = {'file': name, 'url': url, 'bytes': len(body), 'sha256': sha256(body).hexdigest(),
                       'observed_at': datetime.now(UTC).isoformat(), 'response_date': response.headers.get('Date'),
                       'cache_age': response.headers.get('Age')}
        self.bytes += len(body)
        self.archive.writestr(name, body)
        self.pages.append(receipt)
        try:
            return json.loads(body, object_pairs_hook=unique_json_members, parse_constant=reject_json_constant)
        except (json.JSONDecodeError, UnicodeDecodeError, RecursionError) as error:
            raise IncompleteEvidence('NVDB returned malformed JSON') from error

    def series(self, name, path, params, identify, max_rows=None):
        declared = None
        seen = set()
        cursors = set()
        query = params
        for index in range(MAX_ATTEMPTS):
            document = self.page(f'{name}-{index}.json', path, query)
            if not isinstance(document, dict):
                raise IncompleteEvidence(f'{name}: expected a page of objects')
            metadata, rows = document.get('metadata'), document.get('objekter')
            if not isinstance(metadata, dict) or not isinstance(rows, list):
                raise IncompleteEvidence(f'{name}: missing page metadata or rows')
            total, returned = metadata.get('antall'), metadata.get('returnert')
            if type(total) is not int or total < 0 or type(returned) is not int or returned != len(rows):
                raise IncompleteEvidence(f'{name}: invalid NVDB counts')
            if declared is not None and total != declared:
                raise IncompleteEvidence(f'{name}: NVDB count changed between pages')
            declared = total
            if max_rows is not None and declared > max_rows:
                raise IncompleteEvidence(f'{name}: row budget exceeded')
            if len(rows) > PAGE_SIZE or len(rows) + len(seen) > declared:
                raise IncompleteEvidence(f'{name}: more rows returned than declared or requested')
            for row in rows:
                if not isinstance(row, dict):
                    raise IncompleteEvidence(f'{name}: invalid row')
                identity = identify(row)
                if identity in seen:
                    raise IncompleteEvidence(f'{name}: duplicate row')
                seen.add(identity)
            cursor = None
            if 'neste' in metadata:
                next_page = metadata['neste']
                cursor = next_page.get('start') if isinstance(next_page, dict) else None
                if not isinstance(cursor, str) or not cursor.strip() or len(cursor) > 2048:
                    raise IncompleteEvidence(f'{name}: invalid NVDB cursor')
            if not rows or cursor is None:
                if len(seen) != declared:
                    raise IncompleteEvidence(f'{name}: incomplete NVDB page series')
                # An empty tail may echo its request cursor. An empty first page uses 0:0.
                if cursor is not None and cursor != query.get('start', '0:0'):
                    raise IncompleteEvidence(f'{name}: unexpected cursor on empty NVDB page')
                return declared
            if cursor in cursors:
                raise IncompleteEvidence(f'{name}: repeated NVDB cursor')
            cursors.add(cursor)
            query = dict(params, start=cursor)
        raise IncompleteEvidence(f'{name}: NVDB pagination exhausted the request budget')


def network_reference(row, selected, returned):
    sequence, reference = row.get('veglenkesekvensid'), row.get('referanse')
    link, segment = row.get('veglenkenummer'), row.get('segmentnummer')
    if (type(sequence) is not int or sequence not in selected or type(link) is not int or type(segment) is not int
            or link < 0 or segment < 0 or reference != f'{sequence}-{link}-{segment}'):
        raise IncompleteEvidence('Network row has no scoped segment identity')
    returned.add(sequence)
    return reference


def object_reference(row, type_id, selected):
    identifier, metadata, location = row.get('id'), row.get('metadata'), row.get('lokasjon')
    if not isinstance(metadata, dict) or not isinstance(location, dict):
        raise IncompleteEvidence(f'{type_id}: missing object metadata or location')
    kind, revision, placements = metadata.get('type'), metadata.get('versjon'), location.get('stedfestinger')
    kind_id = kind.get('id') if isinstance(kind, dict) else None
    if (type(identifier) is not int or identifier < 1 or type(revision) is not int or revision < 1
            or type(kind_id) is not int or kind_id != type_id or not isinstance(placements, list)):
        raise IncompleteEvidence(f'{type_id}: invalid NVDB object identity or placements')
    for placement in placements:
        if not isinstance(placement, dict):
            continue
        for point in (placement, placement.get('startpunkt'), placement.get('sluttpunkt')):
            sequence = point.get('veglenkesekvensid') if isinstance(point, dict) else None
            if type(sequence) is int and sequence in selected:
                return identifier
    raise IncompleteEvidence(f'{type_id}: object has no placement in selected scope')


def collect(municipality, sequences, effective_date, output, *, open_response=None, use_deadline=False):
    sequences = tuple(sequences)
    if (not re.fullmatch(r'[0-9]{4}', municipality) or not 1 <= len(sequences) <= MAX_SEGMENTS
            or any(type(value) is not int or not 0 < value < 2**63 for value in sequences)
            or len(set(sequences)) != len(sequences)):
        raise IncompleteEvidence('Use one four-digit municipality and distinct positive NVDB sequence IDs')
    if output.suffix.lower() != '.zip':
        raise IncompleteEvidence('The road evidence output must have a .zip suffix')
    scope = {'kommune': municipality, 'veglenkesekvens': ','.join(map(str, sorted(sequences))),
             'tidspunkt': effective_date.isoformat(), 'antall': PAGE_SIZE, 'inkluderAntall': 'true'}
    network_filter = dict(scope, srid=SRID, trafikantgruppe='K')
    object_filter = dict(scope, inkluder='egenskaper,metadata,lokasjon')
    selected, returned = set(sequences), set()
    open_response = open_response or build_opener(NoRedirect()).open
    temporary = None
    try:
        with NamedTemporaryFile(dir=output.parent, prefix='.road-evidence-', delete=False) as stream:
            temporary = Path(stream.name)
            with ZipFile(stream, 'w', compression=ZIP_DEFLATED) as archive:
                collector = Collector(archive, open_response)
                with deadline(use_deadline):
                    counts = {'network': collector.series('network', NETWORK, network_filter,
                                                           lambda row: network_reference(row, selected, returned),
                                                           MAX_SEGMENTS)}
                    for type_id in OBJECT_TYPES:
                        counts[str(type_id)] = collector.series(str(type_id), f'/vegobjekter/api/v4/vegobjekter/{type_id}',
                                                               object_filter,
                                                               lambda row: object_reference(row, type_id, selected),
                                                               MAX_LIMITS if type_id == 105 else None)
                receipt = {'format': 'nvdb-v4-road-evidence', 'version': 1, 'status': 'research',
                           'municipality': municipality, 'sequences': sorted(sequences), 'srid': SRID,
                           'effective_date': effective_date.isoformat(), 'counts': counts,
                           'missing_network_sequences': sorted(selected - returned), 'attempts': collector.attempts,
                           'raw_bytes': collector.bytes, 'pages': collector.pages}
                archive.writestr('receipt.json', json.dumps(receipt, indent=2) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--municipality', required=True, help='Four-digit public municipality code')
    parser.add_argument('--sequence', type=int, required=True, nargs='+', help='Selected public NVDB link sequence IDs')
    parser.add_argument('--date', type=date.fromisoformat, required=True, help='NVDB effective date (YYYY-MM-DD)')
    parser.add_argument('--output', type=Path, required=True, help='Local evidence ZIP path')
    args = parser.parse_args()
    try:
        result = collect(args.municipality, args.sequence, args.date, args.output, use_deadline=True)
    except (ValueError, OSError, HTTPException, RecursionError) as error:
        parser.exit(1, f'Road evidence incomplete: {error}\n')
    print(f"Saved research evidence to {args.output} ({result['attempts']} requests, {result['raw_bytes']} raw bytes).")
    if result['missing_network_sequences']:
        print('Network sequences missing from NVDB: ' + ', '.join(map(str, result['missing_network_sequences'])))


if __name__ == '__main__':
    main()
