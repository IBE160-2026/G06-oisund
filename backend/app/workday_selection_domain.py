"""An explicit member choice never changes the confirmed snapshot or lifecycle."""
from datetime import datetime
from uuid import UUID
from pydantic import Field
from .draft_domain import StrictModel


class SaveSelection(StrictModel):
    operation_id: UUID
    expected_revision: int = Field(ge=0, strict=True)
    activity_id: UUID


class SelectionRecord(StrictModel):
    workday_id: UUID
    activity_id: UUID | None
    revision: int
    expires_at: datetime


class SelectionReceipt(StrictModel):
    operation_id: UUID
    result: SelectionRecord
