"""One public forecast for Tromsø. The production API reads a host-managed cache."""
import argparse
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime
import json
import math
import os
from pathlib import Path
from threading import Lock
from urllib.error import HTTPError
from urllib.request import Request as WebRequest, urlopen
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Request

from . import auth
from .private_storage import database

URL = 'https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=69.6492&lon=18.9553'
AGENT = 'Bussassistent/2.1 (https://github.com/IBE160-2026/G06-oisund)'
CACHE_FILE = Path('/maintenance/tromso-weather.json')
MAX_BODY = 2_000_000
OSLO = ZoneInfo('Europe/Oslo')
MINIMUM = timedelta(minutes=30)
STALE_LIMIT = timedelta(hours=12)
router = APIRouter()
local_cache = None
local_retry = datetime.min.replace(tzinfo=UTC)
local_lock = Lock()


def instant(value):
    stamp = datetime.fromisoformat(value)
    if stamp.utcoffset() is None:
        raise ValueError('Forecast timestamp has no offset')
    return stamp.astimezone(UTC)


def verified_details(row):
    stamp = instant(row['time'])
    data = row['data']
    facts = data['instant']['details']
    air, wind = facts['air_temperature'], facts['wind_speed']
    if (type(air) not in (int, float) or not math.isfinite(air) or not -100 <= air <= 70
            or type(wind) not in (int, float) or not math.isfinite(wind) or not 0 <= wind <= 110):
        raise ValueError('Invalid temperature or wind')
    symbol = next((data[period]['summary']['symbol_code'] for period in ('next_1_hours', 'next_6_hours', 'next_12_hours')
                   if period in data), None)
    if symbol is not None and (not isinstance(symbol, str) or len(symbol) > 70 or not symbol.replace('_', '').isalnum()):
        raise ValueError('Invalid symbol')
    return {'time': stamp.isoformat(), 'temperature': air, 'wind': wind, 'symbol': symbol}


def fetch(now, last_modified=None):
    headers = {'User-Agent': AGENT, 'Accept': 'application/json'}
    if last_modified:
        parsedate_to_datetime(last_modified)
        headers['If-Modified-Since'] = last_modified
    try:
        response = urlopen(WebRequest(URL, headers=headers), timeout=5)
    except HTTPError as error:
        if error.code != 304 or not last_modified:
            raise
        response = error
    with response:
        until = now + MINIMUM
        if response.headers.get('Expires'):
            until = max(until, parsedate_to_datetime(response.headers['Expires']).astimezone(UTC))
        expiry = {'checked': now.isoformat(), 'valid_until': until.isoformat()}
        if response.code == 304:
            return expiry
        raw = response.read(MAX_BODY + 1)
        if len(raw) > MAX_BODY:
            raise ValueError('Forecast exceeds input limit')
        properties = json.loads(raw)['properties']
        updated = instant(properties['meta']['updated_at'])
        if not now - STALE_LIMIT <= updated <= now + timedelta(minutes=15):
            raise ValueError('Forecast is outside update window')
        hours = [verified_details(row) for row in properties['timeseries'][:60]]
        if not hours or any(a['time'] >= b['time'] for a, b in zip(hours, hours[1:])):
            raise ValueError('Forecast times are empty or unordered')
        return {**expiry, 'updated': updated.isoformat(), 'hours': hours, 'last_modified': response.headers.get('Last-Modified')}


def local_forecast(now):
    global local_cache, local_retry
    if now < local_retry:
        return local_cache
    # A request for the plan can run independently of this weather lookup.
    with local_lock:
        if now >= local_retry:
            local_retry = now + timedelta(minutes=5)
            try:
                refresh = fetch(now, local_cache and local_cache.get('last_modified'))
                local_cache = {**(local_cache or {}), **refresh}
                local_retry = instant(local_cache['valid_until'])
            except (OSError, ValueError, KeyError, TypeError):
                pass
    return local_cache


def today(cache, now):
    day = now.astimezone(OSLO).date()
    base = {'place': 'Tromsø', 'day': day.isoformat(), 'current': None, 'hours': [], 'updated': None, 'stale': False}
    if not cache or instant(cache['updated']) < now - STALE_LIMIT:
        return base
    hours = [row for row in cache['hours'] if instant(row['time']).astimezone(OSLO).date() == day]
    if not hours:
        return base
    # Use the latest hour at or before the local time, or the first forecast if
    # that day has only future values. Include the forecast's actual valid time.
    current = next((row for row in reversed(hours) if instant(row['time']) <= now), hours[0])
    return {**base, 'current': current, 'hours': hours, 'updated': cache['updated'],
            'stale': instant(cache['valid_until']) <= now}


@router.get('/tromso-weather')
def tromso_weather(request: Request):
    with database() as conn:
        auth.session(conn, request)
    now = datetime.now(UTC)
    try:
        if os.environ.get('PRIVATE_LOOPBACK_DEVELOPMENT') == '1':
            cache = local_forecast(now)
        else:
            with CACHE_FILE.open(encoding='utf-8') as stream:
                cache = json.load(stream)
        return today(cache, now)
    except (OSError, ValueError, KeyError, TypeError):
        return today(None, now)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--last-modified')
    argument = parser.parse_args()
    print(json.dumps(fetch(datetime.now(UTC), argument.last_modified), allow_nan=False))
