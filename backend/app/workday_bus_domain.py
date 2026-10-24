"""Current manual registration, independent of the reviewed snapshot."""
from datetime import datetime
from uuid import UUID
from pydantic import Field, field_validator
from .draft_domain import StrictModel

# Unicode White_Space, explicitly shared with PrivateBus.tsx. FEFF is meaningful.
BUS_WHITESPACE = '\u0009\u000a\u000b\u000c\u000d\u0020\u0085\u00a0\u1680\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a\u2028\u2029\u202f\u205f\u3000'


def normalize_bus(value):
    return value if value and any(character not in BUS_WHITESPACE for character in value) else None


class SaveBus(StrictModel):
    operation_id: UUID
    expected_revision: int = Field(ge=0, strict=True)
    physical_bus: str | None = Field(max_length=100, strict=True)

    @field_validator('physical_bus')
    @classmethod
    def representable(cls, value):
        if value and '\x00' in value:
            raise ValueError('NUL is not supported')
        return value


class BusRecord(StrictModel):
    workday_id: UUID
    physical_bus: str | None
    revision: int
    expires_at: datetime


class BusReceipt(StrictModel):
    operation_id: UUID
    result: BusRecord
