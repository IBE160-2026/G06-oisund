"""Current manual registration, independent of the reviewed snapshot."""
from datetime import datetime
from uuid import UUID
from pydantic import Field, field_validator
from .draft_domain import StrictModel

from .bus_value import normalize_bus, validate_bus


class SaveBus(StrictModel):
    operation_id: UUID
    expected_revision: int = Field(ge=0, strict=True)
    physical_bus: str | None = Field(max_length=100, strict=True)

    @field_validator('physical_bus')
    @classmethod
    def representable(cls, value):
        return validate_bus(value)


class BusRecord(StrictModel):
    workday_id: UUID
    physical_bus: str | None
    revision: int
    expires_at: datetime


class BusReceipt(StrictModel):
    operation_id: UUID
    result: BusRecord
