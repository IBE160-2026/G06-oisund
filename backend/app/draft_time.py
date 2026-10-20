"""Resolve local clocks using server Oslo rules without guessing a calendar day."""
from datetime import datetime, timezone
from typing import Literal
from zoneinfo import ZoneInfo

from pydantic import Field

from .draft_domain import StrictModel


class LocalTime(StrictModel):
    calendar_date: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$', max_length=10)
    clock: str = Field(pattern=r'^(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?$', max_length=8)


class TimeResolution(StrictModel):
    state: Literal['resolved', 'ambiguous', 'gap']
    candidates: list[str] = Field(max_length=2)


def resolve(value: LocalTime):
    local = datetime.fromisoformat(value.calendar_date + 'T' + value.clock)
    oslo = ZoneInfo('Europe/Oslo')
    candidates = {}
    for fold in (0, 1):
        aware = local.replace(tzinfo=oslo, fold=fold)
        utc = aware.astimezone(timezone.utc)
        if utc.astimezone(oslo).replace(tzinfo=None) == local:
            candidates[utc] = aware.isoformat(timespec='seconds' if len(value.clock) == 8 else 'minutes')
    values = [candidates[key] for key in sorted(candidates)]
    return {'state': 'gap' if not values else 'ambiguous' if len(values) == 2 else 'resolved', 'candidates': values}
