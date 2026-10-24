"""Current lifecycle authority is separate from historical confirmation receipts."""
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import Field
from .draft_domain import StrictModel


class StartWorkday(StrictModel):
    operation_id: UUID
    expected_revision: int = Field(ge=0, strict=True)


class LifecycleRecord(StrictModel):
    workday_id: UUID
    state: Literal['confirmed', 'active']
    started_at: datetime | None
    revision: int
    expires_at: datetime


class StartReceipt(StrictModel):
    operation_id: UUID
    result: LifecycleRecord
