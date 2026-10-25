"""Current lifecycle authority is separate from historical confirmation receipts."""
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import Field, model_validator
from .draft_domain import StrictModel


class StartWorkday(StrictModel):
    operation_id: UUID
    expected_revision: int = Field(ge=0, strict=True)


class LifecycleRecord(StrictModel):
    workday_id: UUID
    state: Literal['confirmed', 'active', 'ended', 'aborted']
    started_at: datetime | None
    ended_at: datetime | None = None
    revision: int
    expires_at: datetime

    @model_validator(mode='after')
    def coherent_state(self):
        if self.state == 'confirmed':
            valid = self.revision == 0 and self.started_at is None and self.ended_at is None
        elif self.state == 'active':
            valid = self.revision == 1 and self.started_at is not None and self.ended_at is None
        else:
            valid = self.revision == 2 and self.started_at is not None and self.ended_at is not None and self.ended_at >= self.started_at
        if not valid:
            raise ValueError('Invalid lifecycle state')
        return self


class StartReceipt(StrictModel):
    operation_id: UUID
    result: LifecycleRecord


class CloseWorkday(StrictModel):
    operation_id: UUID
    expected_revision: int = Field(ge=0, strict=True)
    expected_outcome_revision: int = Field(ge=0, strict=True)
    action: Literal['ended', 'aborted']
