"""Download only the two published Entur archives for the root route import."""

from contextlib import closing
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime
from http.client import HTTPSConnection
from io import BytesIO
import json
import re
from time import monotonic
from zipfile import ZipFile

HOST = 'storage.googleapis.com'
FILES = (
    ('routes', '/marduk-production/outbound/netex/rb_tro-aggregated-netex.zip', 16_000_000),
    ('quays', '/marduk-production/tiamat/CurrentAndFuture_latest.zip', 60_000_000),
)


def download(path, maximum):
    deadline = monotonic() + 45
    with closing(HTTPSConnection(HOST, timeout=8)) as connection:
        connection.request('GET', path, headers={'User-Agent': 'IBE160-Bussassistent-route-import/1.0',
                                                  'Accept-Encoding': 'identity', 'Cache-Control': 'no-cache'})
        with connection.getresponse() as response:
            checked = datetime.now(UTC)
            headers = response.headers
            size = headers.get('Content-Length', '')
            generation = headers.get('X-Goog-Generation', '')
            age = headers.get('Age', '0')
            if (response.status != 200 or not re.fullmatch(r'[1-9][0-9]{0,7}', size)
                    or not 0 < int(size) <= maximum or not re.fullmatch(r'[1-9][0-9]{0,19}', generation)
                    or headers.get('Content-Encoding', 'identity') != 'identity'
                    or not re.fullmatch(r'[0-9]{1,7}', age) or int(age) > 3600):
                raise ValueError('Unexpected Entur transport metadata')
            date = parsedate_to_datetime(headers.get('Date', ''))
            observed = min(checked - timedelta(seconds=int(age)), date)
            if date.utcoffset() != timedelta(0) or date > checked + timedelta(minutes=1) or checked - observed > timedelta(hours=1):
                raise ValueError('Entur response clock outside the allowed interval')
            data = bytearray()
            while len(data) < int(size) and monotonic() < deadline:
                chunk = response.read1(min(65536, int(size) - len(data)))
                if not chunk:
                    break
                data.extend(chunk)
            if len(data) != int(size) or monotonic() >= deadline:
                raise ValueError('Incomplete Entur archive download')
    return bytes(data), {'observed_at': observed.isoformat(), 'generation': generation}


def bundle():
    result = BytesIO()
    meta = {}
    with ZipFile(result, 'w') as archive:
        for name, path, maximum in FILES:
            data, meta[name] = download(path, maximum)
            archive.writestr(name + '.zip', data)
        archive.writestr('source.json', json.dumps(meta))
    return result.getvalue()


if __name__ == '__main__':
    import sys

    sys.stdout.buffer.write(bundle())
