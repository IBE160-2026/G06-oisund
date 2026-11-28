from datetime import UTC, datetime, timedelta
from io import BytesIO
import json

from app import weather


def hour(time, symbol='snow'):
    return {'time': time, 'data': {'instant': {'details': {'air_temperature': -2.5, 'wind_speed': 15}},
                                   'next_1_hours': {'summary': {'symbol_code': symbol}}}}


def test_forecast_day_rolls_over_at_oslo_midnight():
    now = datetime(2026, 11, 27, 23, 30, tzinfo=UTC)
    rows = [weather.verified_details(hour(t)) for t in (
        '2026-11-27T22:00:00Z', '2026-11-27T23:00:00Z', '2026-11-28T00:00:00Z',
    )]
    cache = {'hours': rows, 'updated': (now-timedelta(hours=1)).isoformat(),
             'valid_until': (now-timedelta(minutes=2)).isoformat()}
    response = weather.today(cache, now)
    assert response['day'] == '2026-11-28'
    assert response['place'] == 'Tromsø' and response['stale']
    assert response['hours'] == rows[1:]
    assert response['current'] == rows[1]
    assert weather.today(cache, now+timedelta(hours=13))['current'] is None
    assert weather.today(None, now)['current'] is None


def test_fetch_uses_fixed_place_identification_and_source_expiry(monkeypatch):
    now = datetime(2026, 11, 28, 0, 10, tzinfo=UTC)
    updated = '2026-11-28T00:00:00Z'
    blob = {'properties': {'meta': {'updated_at': updated}, 'timeseries': [hour(updated)]}}
    response = BytesIO(json.dumps(blob).encode())
    response.code = 200
    response.headers = {'Expires': 'Sat, 28 Nov 2026 00:57:00 GMT', 'Last-Modified': 'Sat, 28 Nov 2026 00:05:00 GMT'}
    def source(request, timeout):
        assert request.full_url == weather.URL
        assert request.get_header('User-agent') == weather.AGENT
        assert request.get_header('If-modified-since') == 'Fri, 27 Nov 2026 23:30:00 GMT'
        assert timeout == 5
        return response
    monkeypatch.setattr(weather, 'urlopen', source)
    value = weather.fetch(now, 'Fri, 27 Nov 2026 23:30:00 GMT')
    assert value['valid_until'] == '2026-11-28T00:57:00+00:00'
    assert value['hours'][0]['symbol'] == 'snow'
    assert value['hours'][0]['wind'] == 15
