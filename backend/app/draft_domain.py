"""Manual draft facts; unknowns remain null and source clocks stay verbatim."""
import re
from datetime import date, datetime
from typing import Annotated, Literal
from uuid import UUID
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator, model_serializer


class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid')


class SourceLocation(StrictModel):
    page: int = Field(ge=1, le=20)
    column: int | None = Field(default=None, ge=1, le=2)
    line: int | None = Field(default=None, ge=1, le=10000)
    region: Literal['header'] | None = None
    field: str | None = Field(default=None, max_length=100)


class Derivation(StrictModel):
    derived_from: list[Annotated[str, Field(max_length=100)]] = Field(max_length=10)
    rule: str | None = Field(default=None, max_length=100)


class SourceHeader(StrictModel):
    shift_id: str = Field(max_length=100)
    service_date: str = Field(max_length=10)
    weekday: str = Field(max_length=100)
    department: str = Field(max_length=300)
    start: str = Field(max_length=10)
    end: str = Field(max_length=10)
    origin: str = Field(max_length=300)
    destination: str = Field(max_length=300)
    work: str = Field(max_length=30)
    span: str = Field(max_length=30)
    supplements: list[Annotated[str, Field(max_length=100)]] = Field(max_length=50)
    pages: int = Field(ge=1, le=20)
    start_instant: str | None = Field(max_length=40)
    end_instant: str | None = Field(max_length=40)
    end_day: int | None = Field(ge=0, le=1)


class SourceActivity(StrictModel):
    activity_id: UUID
    source_order: int = Field(ge=1, le=200)
    label: str = Field(max_length=100)
    kind: str = Field(max_length=100)
    line: str | None = Field(max_length=100)
    trip_id: str | None = Field(max_length=100)
    origin: str | None = Field(max_length=300)
    destination: str | None = Field(max_length=300)
    start: str | None = Field(max_length=100)
    end: str | None = Field(max_length=100)
    start_instant: str | None = Field(max_length=40)
    end_instant: str | None = Field(max_length=40)
    start_day: int | None = Field(ge=0, le=1)
    end_day: int | None = Field(ge=0, le=1)
    pages: list[Annotated[int, Field(ge=1, le=20)]] = Field(max_length=20)
    provenance: dict[Annotated[str, Field(max_length=100)], Annotated[list[SourceLocation], Field(max_length=20)] | Derivation] = Field(max_length=30)
    origins: dict[Annotated[str, Field(max_length=100)], Literal['extracted', 'derived', 'unresolved']] = Field(max_length=30)

    @model_validator(mode='after')
    def complete_field_origins(self):
        fields = {'label', 'kind', 'line', 'trip_id', 'origin', 'destination', 'start', 'end', 'start_instant', 'end_instant', 'start_day', 'end_day'}
        if set(self.provenance) != fields or set(self.origins) != fields:
            raise ValueError('Missing field provenance')
        return self


class SourceDuty(StrictModel):
    value: str = Field(max_length=100)
    suffix: str | None = Field(max_length=3, pattern=r'^[0-9]{3}$')
    after_activity: int = Field(ge=0, le=200)
    provenance: SourceLocation


class SourceAnnotation(StrictModel):
    value: str = Field(max_length=100)
    meaning: None = None
    provenance: SourceLocation


class SourceUncertainty(StrictModel):
    code: str = Field(max_length=100)
    activity: int | None = Field(default=None, ge=1, le=200)
    field: str | None = Field(default=None, max_length=100)
    provenance: SourceLocation | None = None


class SourcePause(StrictModel):
    rows: list[Annotated[int, Field(ge=1, le=200)]] = Field(max_length=200)
    start: str | None = Field(max_length=40)
    end: str | None = Field(max_length=40)
    labels: list[Annotated[str, Field(max_length=100)]] = Field(max_length=200)
    kind: Literal['meal', 'split', 'coffee', 'paid_meal']


class ImportMetadata(StrictModel):
    version: Literal[1] = 1
    qualification: Literal['bounded-layout', 'partial']
    timezone: Literal['Europe/Oslo']
    header: SourceHeader
    header_provenance: dict[Annotated[str, Field(max_length=100)], SourceLocation | Derivation] = Field(max_length=30)
    activities: list[SourceActivity] = Field(max_length=200)
    duties: list[SourceDuty] = Field(max_length=200)
    annotations: list[SourceAnnotation] = Field(max_length=400)
    unresolved: list[SourceUncertainty] = Field(max_length=1000)
    pause_groups: list[SourcePause] = Field(max_length=200)

    @model_validator(mode='after')
    def ordered_sources(self):
        if set(self.header_provenance) != set(SourceHeader.model_fields):
            raise ValueError('Missing header provenance')
        if [a.source_order for a in self.activities] != list(range(1, len(self.activities) + 1)):
            raise ValueError('Invalid source order')
        if len({a.activity_id for a in self.activities}) != len(self.activities):
            raise ValueError('Duplicate source identity')
        return self


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
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?[+-](?:[01]\d|2[0-3]):[0-5]\d', value):
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


class DutyChange(StrictModel):
    from_activity_id: UUID
    vehicle_duty: str | None = Field(default=None, max_length=100)
    realtime_duty: str | None = Field(default=None, max_length=3, pattern=r'^[0-9]{3}$')

    @model_validator(mode='before')
    @classmethod
    def derive_suffix(cls, value):
        if isinstance(value, dict):
            value = dict(value)
            duty = value.get('vehicle_duty')
            suffix = re.search(r'([0-9]{3})$', duty) if isinstance(duty, str) else None
            value['realtime_duty'] = suffix.group(1) if suffix else None
        return value


class DraftContent(StrictModel):
    service_date: date | None = None
    vehicle_duty: str | None = Field(default=None, max_length=100)
    realtime_duty: str | None = Field(default=None, max_length=3, pattern=r'^[0-9]{3}$')
    physical_bus: str | None = Field(default=None, max_length=100)
    activities: list[Activity] = Field(default_factory=list, max_length=200)
    import_metadata: ImportMetadata | None = None
    vehicle_duty_changes: list[DutyChange] | None = Field(default=None, max_length=200)

    @model_serializer(mode='wrap')
    def compatible_json(self, handler):
        value = handler(self)
        if value.get('import_metadata') is None:
            value.pop('import_metadata', None)
        if value.get('vehicle_duty_changes') is None:
            value.pop('vehicle_duty_changes', None)
        return value

    @model_validator(mode='before')
    @classmethod
    def derived_realtime(cls, value):
        if isinstance(value, dict):
            value = dict(value)
            duty = value.get('vehicle_duty')
            suffix = re.search(r'([0-9]{3})$', duty) if isinstance(duty, str) else None
            value['realtime_duty'] = suffix.group(1) if suffix else None
        return value

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
        anchors = [change.from_activity_id for change in self.vehicle_duty_changes or []]
        if len(set(anchors)) != len(anchors) or not set(anchors) <= {a.id for a in self.activities}:
            raise ValueError('Invalid vehicle duty change activity')
        return self


class IssueOperation(StrictModel):
    draft_id: UUID | None = None


class SaveDraft(StrictModel):
    operation_id: UUID
    expected_revision: int = Field(ge=0, strict=True)
    draft: DraftContent


class DeleteDraft(StrictModel):
    operation_id: UUID
    expected_revision: int = Field(ge=1, strict=True)


class DeletedDraft(StrictModel):
    deleted_id: UUID


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
