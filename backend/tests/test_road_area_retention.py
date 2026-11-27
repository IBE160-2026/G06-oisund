"""Dated area packages are replaceable independently of private route evidence."""

from datetime import UTC, date, datetime, timedelta

from app.private_storage import database
from app.road_area_catalogue import AREAS, prune_versions
from test_private_access import pytestmark, synthetic_only


def test_road_retention_preserves_active_and_preloaded_oslo_dates():
    local_midnight = datetime(2026, 11, 29, 23, tzinfo=UTC)
    first = date(2026, 11, 30)
    field_dates = {first + timedelta(days=offset) for offset in range(11)}
    with database() as conn:
        conn.execute('CREATE TEMP TABLE public_road_area_versions (LIKE public.public_road_area_versions INCLUDING ALL)')
        for day in sorted(field_dates | {date(2026, 11, 28), date(2026, 11, 29)}):
            for area in AREAS:
                for version in range(3):
                    observed = local_midnight + timedelta(minutes=version)
                    conn.execute(
                        "INSERT INTO public_road_area_versions VALUES (%s,%s,%s,%s,%s,%s,'{}','{}')",
                        (day, area, observed, observed, 'a' * 64, format(version, '064x')),
                    )
        assert prune_versions(conn, local_midnight - timedelta(seconds=1), batch=2) == 2
        prune_versions(conn, local_midnight - timedelta(seconds=1))
        current_and_future = conn.execute(
            'SELECT effective_date,area_id,array_agg(revision ORDER BY observed_at DESC) AS revisions '
            'FROM public_road_area_versions GROUP BY effective_date,area_id'
        ).fetchall()
        assert {row['effective_date'] for row in current_and_future} == field_dates | {date(2026, 11, 29)}
        assert all(row['revisions'] == [format(2, '064x'), format(1, '064x')] for row in current_and_future)
        assert prune_versions(conn, local_midnight) == 6
        assert prune_versions(conn, local_midnight) == 0
        assert conn.execute('SELECT count(*) AS n FROM public_road_area_versions').fetchone()['n'] == 66
