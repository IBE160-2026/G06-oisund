"""Read-only candidates against explicit confirmed lines and planned intervals."""
from datetime import date, datetime, time, timedelta, timezone
from typing import Annotated, Literal
from uuid import UUID
from zoneinfo import ZoneInfo
from fastapi import HTTPException
from pydantic import Field
from .draft_domain import StrictModel
from .workday_notice_domain import NoticeRecord

OSLO = ZoneInfo('Europe/Oslo')
Line = Annotated[str, Field(min_length=1, max_length=300)]


class ReaderCandidate(StrictModel):
    notice: NoticeRecord
    matching_lines: list[Line] = Field(max_length=200)
    unmatched_tags: list[Line] = Field(max_length=50)
    line_uncertain: bool
    validity: Literal['known', 'partial', 'unknown']


class NoticeReader(StrictModel):
    workday_id: UUID
    expires_at: datetime
    server_now: datetime
    available_lines: list[Line] = Field(max_length=200)
    available_dates: list[date] = Field(max_length=400)
    unknown_line_count: int = Field(ge=0, le=200)
    unmatched_notice_count: int = Field(ge=0)
    selected_line: Line | None
    selected_date: date | None
    stored_count: int = Field(ge=0)
    candidates: list[ReaderCandidate]


def instant(value):
    return (datetime.fromisoformat(value) if isinstance(value, str) else value).astimezone(timezone.utc)


def project(plan, rows, line=None, calendar_date=None):
    projected_at = datetime.now(timezone.utc)
    activities = plan['content']['activities']
    lines = sorted({a['line'].strip() for a in activities if (a.get('line') or '').strip()})
    unknown = sum(not (a.get('line') or '').strip() for a in activities)
    intervals = [(instant(a['start']), instant(a['end'])) for a in activities]
    dates = set()
    for start, end in intervals:
        current, last = start.astimezone(OSLO).date(), end.astimezone(OSLO).date()
        # Dates describe actual intervals, never an envelope spanning plan gaps.
        while current <= last:
            dates.add(current)
            if len(dates) > 400:
                raise HTTPException(422, 'Planens kalenderomfang kan ikke leses her.')
            if current == last:
                break
            current += timedelta(days=1)
    dates = sorted(dates)
    if line is not None and line not in lines or calendar_date is not None and calendar_date not in dates:
        raise HTTPException(422, 'Velg en bekreftet linje eller planlagt kalenderdato.')
    if calendar_date is not None:
        lower = datetime.combine(calendar_date, time(), OSLO).astimezone(timezone.utc)
        upper = datetime.combine(calendar_date + timedelta(days=1), time(), OSLO).astimezone(timezone.utc)
        # A day ends exclusively; a planned/notice endpoint is otherwise inclusive.
        intervals = [(max(a, lower), min(b, upper)) for a, b in intervals if a < upper and b >= lower]
    else:
        upper = None
    candidates = []
    unmatched_count = 0
    for row in rows:
        if row['status'] != 'registered' or row['valid_until'] is None or instant(row['valid_until']) <= projected_at:
            continue
        all_lines = row.get('line_scope', 'selected') == 'all'
        tags = [t.strip() for t in row['line_tags']]
        matched = lines if all_lines else [l for l in lines if l in tags]
        unmatched = [] if all_lines else [t for t in tags if t not in lines]
        if unmatched:
            unmatched_count += 1
        uncertain = not all_lines and (bool(unmatched) or not matched)
        # Exact mismatches remain in the global coverage warning, never matches.
        if not all_lines and not matched:
            continue
        if line is not None and line not in matched:
            continue
        start, end = row['valid_from'], row['valid_until']
        validity = 'known' if start is not None and end is not None else 'partial' if start is not None or end is not None else 'unknown'
        if end is not None:
            start, end = instant(start) if start is not None else datetime.min.replace(tzinfo=timezone.utc), instant(end)
            if not any(start <= b and end >= a and (upper is None or start < upper) for a, b in intervals):
                continue
        candidates.append({'notice': {key: row[key] for key in NoticeRecord.model_fields}, 'matching_lines': matched,
                           'unmatched_tags': unmatched, 'line_uncertain': uncertain, 'validity': validity})
    return {'workday_id': plan['id'], 'expires_at': plan['expires_at'], 'server_now': projected_at, 'available_lines': lines,
            'available_dates': dates, 'unknown_line_count': unknown, 'unmatched_notice_count': unmatched_count, 'selected_line': line,
            'selected_date': calendar_date, 'stored_count': len(rows), 'candidates': candidates}
