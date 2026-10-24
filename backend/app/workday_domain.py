"""Exact saved-revision review and explicit confirmation decisions."""
from datetime import datetime, timedelta
from typing import Annotated, Literal, get_args
from uuid import UUID

from pydantic import Field, model_validator

from .draft_domain import DraftContent, StrictModel
from .bus_value import normalize_bus
from .import_issues import current_uncertainty, marker_fragments

SupportedType = Literal['trip', 'deadhead', 'deadhead_car', 'Tomkjøring med CAR', 'CAR',
                   'Sign-on', 'Sign-off', 'MealBreak', 'Coffee', 'Split break',
                   'Paid meal before', 'Paid meal after', 'Travel to', 'Travel from', 'Fadder', 'Instruktør', 'manual']
SUPPORTED_TYPES = get_args(SupportedType)


class ReviewRequest(StrictModel):
    draft_id: UUID
    expected_revision: int = Field(ge=1, strict=True)


class DeleteWorkdayRequest(StrictModel):
    operation_id: UUID
    source_revision: int = Field(ge=1, strict=True)


class DeletedWorkday(StrictModel):
    operation_id: UUID
    deleted_id: UUID
    source_revision: int


class ConfirmRequest(StrictModel):
    operation_id: UUID
    expected_revision: int = Field(ge=1, strict=True)
    acknowledgements: list[Annotated[str, Field(max_length=200)]] = Field(default_factory=list, max_length=3000)
    classifications: dict[UUID, SupportedType] = Field(default_factory=dict, max_length=200)

    @model_validator(mode='after')
    def unique_decisions(self):
        if len(set(self.acknowledgements)) != len(self.acknowledgements):
            raise ValueError('Duplicate acknowledgement')
        return self


def assessment(content, classifications=None, policy_version=1):
    """Stable keys bind decisions to an issued revision and internal policy.

    Required: date, activities, explicit ordered times and supported classification.
    Decisions: places, passenger identifiers, day duty/bus, duty anchors, source
    issues/annotations and uncertainty. Unknown original types retain passenger
    decisions regardless of classification. Movement identifiers, source clocks,
    raw codes and provenance add no decisions. V1 keeps historical strip behavior;
    V2 assesses bus absence using the fresh-write Unicode White_Space contract.
    V3 only asks for effective passenger-trip facts and substantive current notes;
    original annotations/issues stay neutral source information.
    """
    classifications = classifications or {}
    fragments = marker_fragments(content) if policy_version >= 3 else None
    blockers, unknowns, required = [], [], []
    if not content.service_date:
        blockers.append('Tjenestedato mangler. Rett og lagre utkastet.')
    if not content.activities:
        blockers.append('Legg til og lagre minst én aktivitet.')
    def unknown(key, label):
        unknowns.append({'id': key, 'label': label})
    for field, label in [('vehicle_duty', 'Vognløp'), ('physical_bus', 'Buss/vogn')]:
        value = getattr(content, field)
        missing = normalize_bus(value) is None if field == 'physical_bus' and policy_version >= 2 else not (value or '').strip()
        if missing and policy_version < 3:
            unknown('day:' + field, label + ' er ukjent.')
    previous = None
    ends = []
    duty_changes = {change.from_activity_id: change for change in content.vehicle_duty_changes or []}
    for index, activity in enumerate(content.activities):
        key, label = str(activity.id), f'Aktivitet {index + 1}'
        change = duty_changes.get(activity.id)
        if policy_version < 3 and change and not (change.vehicle_duty or '').strip():
            unknown('duty:' + key + ':vehicle_duty', label + ': vognløpet fra denne aktiviteten er ukjent.')
        kind = classifications.get(key, activity.type)
        if activity.type not in SUPPORTED_TYPES:
            required.append(key)
        if not activity.start or not activity.end:
            blockers.append(label + ': start og slutt med dato og Oslo-tid må fylles ut og lagres.')
        if activity.start:
            start = datetime.fromisoformat(activity.start)
            if previous and start < previous:
                blockers.append(label + ': start er før forrige aktivitets start. Rett rekkefølgen og lagre.')
            previous = start
        if activity.end:
            ends.append(datetime.fromisoformat(activity.end))
        # Fresh reviews offer trip candidates for unresolved types. Confirmation
        # supplies classifications and independently narrows the exact set.
        if policy_version >= 3:
            if kind == 'trip' or activity.type not in SUPPORTED_TYPES and key not in classifications:
                for field, title in [('from_place', 'fra sted'), ('to_place', 'til sted'), ('trip', 'turnummer'), ('line', 'linje'), ('direction', 'retning')]:
                    if not (getattr(activity, field) or '').strip():
                        unknown(key + ':' + field, label + ': ' + title + ' er ukjent.')
                note = current_uncertainty(content, activity, fragments)
                if note:
                    unknown(key + ':uncertainty', label + ': ' + note)
            continue
        for field, title in [('from_place', 'fra sted'), ('to_place', 'til sted'), ('uncertainty', 'usikkerhetsnotat')]:
            value = getattr(activity, field)
            if field == 'uncertainty':
                if value and value.strip(): unknown(key + ':' + field, label + ': ' + value)
            elif not (value or '').strip():
                unknown(key + ':' + field, label + ': ' + title + ' er ukjent.')
        # Unknown types show all potentially required passenger unknowns during
        # review, so choosing a classification cannot hide a missing fact.
        if kind == 'trip' or activity.type not in SUPPORTED_TYPES:
            for field, title in [('trip', 'turnummer'), ('line', 'linje'), ('direction', 'retning')]:
                if not (getattr(activity, field) or '').strip():
                    unknown(key + ':' + field, label + ': ' + title + ' er ukjent.')
    metadata = content.import_metadata
    if metadata and policy_version < 3:
        for index, item in enumerate(metadata.unresolved):
            unknown(f'source:unresolved:{index}', f'Kildeusikkerhet: {item.code} (aktivitet {item.activity or "ukjent"}, felt {item.field or "ukjent"}).')
        for index, item in enumerate(metadata.annotations):
            unknown(f'source:annotation:{index}', f'Kildemerket {item.value} har ukjent betydning (side {item.provenance.page}).')
    final_end = max(ends) if ends and not blockers else None
    try:
        expiry = final_end + timedelta(days=7) if final_end else None
    except OverflowError:
        blockers.append('Sluttidspunktet er utenfor støttet kalender.'); expiry = None
    return {'blockers': blockers, 'unknowns': unknowns, 'classifications_required': required,
            'final_end': final_end, 'expires_at': expiry}


class Unknown(StrictModel):
    id: str
    label: str


class Review(StrictModel):
    operation_id: UUID
    operation_expires_at: datetime
    draft_id: UUID
    revision: int
    draft: DraftContent
    blockers: list[str]
    unknowns: list[Unknown]
    classifications_required: list[UUID]
    supported_types: list[str]
    final_end: datetime | None
    expires_at: datetime | None


class WorkdayRecord(StrictModel):
    id: UUID
    source_draft_id: UUID
    source_revision: int
    confirmed_at: datetime
    final_end: datetime
    expires_at: datetime
    state: Literal['confirmed'] = 'confirmed'
    draft: DraftContent
    acknowledgements: list[str]
    classifications: dict[UUID, str]
    unknowns: list[Unknown]

    @model_validator(mode='after')
    def fixed_deadline(self):
        if self.expires_at - self.final_end != timedelta(days=7):
            raise ValueError('Invalid plan retention')
        return self


class WorkdaySummary(StrictModel):
    id: UUID
    source_draft_id: UUID
    source_revision: int
    service_date: str | None
    expires_at: datetime


class WorkdayList(StrictModel):
    workdays: list[WorkdaySummary]
    next_cursor: UUID | None


class WorkdayOperation(StrictModel):
    state: Literal['accepted', 'pending']
    result: WorkdayRecord | None
