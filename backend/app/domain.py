from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid')


class Activity(StrictModel):
    id: UUID
    kind: Literal['trip', 'break']
    start: datetime
    end: datetime
    place: str | None
    trip_code: str | None
    provenance: Literal['fictional-planned']

    @model_validator(mode='after')
    def validate_times(self):
        if self.start.utcoffset() is None or self.end.utcoffset() is None or self.end <= self.start:
            raise ValueError('Explicit ordered calendar dates with timezone required')
        return self


class FictionalDay(StrictModel):
    fictional: Literal[True]
    service_date: date
    timezone: Literal['Europe/Oslo']
    vehicle_duty: str | None
    physical_bus: str | None
    activities: list[Activity]

    @field_validator('fictional', mode='before')
    @classmethod
    def require_boolean(cls, value):
        if type(value) is not bool:
            raise ValueError('fictional must be a JSON boolean')
        return value


class CreateDay(StrictModel):
    operation_id: UUID
    day: FictionalDay


FIXTURE = FictionalDay.model_validate({
    'fictional': True, 'service_date': '2026-10-19', 'timezone': 'Europe/Oslo',
    'vehicle_duty': 'DEMO-01', 'physical_bus': None,
    'activities': [
        {'id': '11111111-1111-4111-8111-111111111111', 'kind': 'trip',
         'start': '2026-10-19T23:30:00+02:00', 'end': '2026-10-20T00:15:00+02:00',
         'place': 'Eksempelbyen', 'trip_code': None, 'provenance': 'fictional-planned'},
        {'id': '22222222-2222-4222-8222-222222222222', 'kind': 'break',
         'start': '2026-10-20T00:15:00+02:00', 'end': '2026-10-20T00:45:00+02:00',
         'place': None, 'trip_code': None, 'provenance': 'fictional-planned'},
    ],
})
