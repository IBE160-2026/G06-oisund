"""Manual draft facts; unknowns remain null and source clocks stay verbatim."""
import re
from datetime import date, datetime
from typing import Literal
from uuid import UUID
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid')


class Activity(StrictModel):
    id: UUID
    type: str | None = Field(default=None, max_length=100)
    raw_code: str | None = Field(default=None, max_length=100)
    start: str | None = Field(default=None, max_length=40)
    end: str | None = Field(default=None, max_length=40)
    source_start: str | None = Field(default=None, max_length=100)
    source_end: str | None = Field(default=None, max_length=100)
    from_place: str | None = Field(default=None, max_length=300)
    to_place: str | None = Field(default=None, max_length=300)
    trip: str | None = Field(default=None, max_length=100)
    line: str | None = Field(default=None, max_length=100)
    direction: str | None = Field(default=None, max_length=100)
    uncertainty: str | None = Field(default=None, max_length=1000)
    provenance: str | None = Field(default=None, max_length=1000)

    @field_validator('start', 'end')
    @classmethod
    def oslo_instant(cls, value):
        if value is None:
            return value
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?[+-]\d{2}:\d{2}', value):
            raise ValueError('Explicit date and offset required')
        instant = datetime.fromisoformat(value)
        try:
            oslo_offset = instant.astimezone(ZoneInfo('Europe/Oslo')).utcoffset()
        except OverflowError:
            raise ValueError('Oslo conversion outside supported calendar') from None
        if instant.utcoffset() != oslo_offset:
            raise ValueError('Invalid Oslo offset')
        return value

    @model_validator(mode='after')
    def interval(self):
        if self.start and self.end and datetime.fromisoformat(self.end) < datetime.fromisoformat(self.start):
            raise ValueError('Negative interval')
        return self


class DraftContent(StrictModel):
    service_date: date | None = None
    vehicle_duty: str | None = Field(default=None, max_length=100)
    realtime_duty: str | None = Field(default=None, max_length=3, pattern=r'^[0-9]{3}$')
    physical_bus: None = None
    activities: list[Activity] = Field(default_factory=list, max_length=200)

    @field_validator('service_date', mode='before')
    @classmethod
    def explicit_date(cls, value):
        if value is not None and (not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value)):
            raise ValueError('Explicit calendar date required')
        return value

    @model_validator(mode='after')
    def identities(self):
        if len({a.id for a in self.activities}) != len(self.activities):
            raise ValueError('Duplicate activity identities')
        return self


class IssueOperation(StrictModel):
    draft_id: UUID | None = None


class SaveDraft(StrictModel):
    operation_id: UUID
    expected_revision: int = Field(ge=0, strict=True)
    draft: DraftContent


class DraftRecord(StrictModel):
    id: UUID
    created_at: datetime
    expires_at: datetime
    revision: int = Field(ge=1)
    draft: DraftContent

    @model_validator(mode='after')
    def deadline(self):
        if (self.expires_at - self.created_at).total_seconds() != 7 * 86400:
            raise ValueError('Invalid fixed retention deadline')
        return self


class DraftSummary(StrictModel):
    id: UUID
    created_at: datetime
    expires_at: datetime
    revision: int = Field(ge=1)
    service_date: date | None


class DraftList(StrictModel):
    drafts: list[DraftSummary] = Field(max_length=200)


class IssuedOperation(StrictModel):
    operation_id: UUID
    expires_at: datetime


class OperationResult(StrictModel):
    state: Literal['accepted', 'pending']
    result: DraftRecord | None
