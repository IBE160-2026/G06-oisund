"""Explicit exact-member manual outcomes, independently revisioned from selection."""
from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import Field
from .draft_domain import StrictModel

Outcome = Literal['unregistered', 'completed', 'skipped', 'interrupted']


class SaveOutcome(StrictModel):
    operation_id: UUID
    expected_revision: int = Field(ge=0, strict=True)
    expected_lifecycle_revision: int = Field(ge=0, strict=True)
    activity_id: UUID
    outcome: Outcome


class MemberOutcome(StrictModel):
    activity_id: UUID
    outcome: Outcome


class OutcomeRecord(StrictModel):
    workday_id: UUID
    revision: int
    outcomes: list[MemberOutcome]
    expires_at: datetime


class OutcomeReceipt(StrictModel):
    operation_id: UUID
    result: OutcomeRecord


from .workday_domain import WorkdayRecord
from .workday_lifecycle_domain import LifecycleRecord
from .workday_bus_domain import BusRecord


class WorkdayRecap(StrictModel):
    plan: WorkdayRecord
    lifecycle: LifecycleRecord
    outcomes: OutcomeRecord
    bus: BusRecord
