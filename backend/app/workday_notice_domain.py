"""Explicit source facts and manual actions, without inferred freshness or relevance."""
import unicodedata
from datetime import datetime, timezone
from typing import Annotated, Literal
from urllib.parse import urlsplit
from uuid import UUID
from zoneinfo import ZoneInfo
from pydantic import Field, TypeAdapter, AnyHttpUrl, field_serializer, field_validator, model_validator
from .draft_domain import StrictModel, Activity

HTTP_SOURCE = TypeAdapter(AnyHttpUrl)


def text(value):
    if not isinstance(value, str) or any(unicodedata.category(c) in {'Cc', 'Cs'} for c in value):
        raise ValueError('Plain text required')
    value = value.strip()
    if not value:
        raise ValueError('Blank value')
    return value


class NoticeContent(StrictModel):
    title: str = Field(min_length=1, max_length=300, strict=True)
    line_tags: list[Annotated[str, Field(min_length=1, max_length=300, strict=True)]] = Field(max_length=50)
    summary: str | None = Field(default=None, max_length=1000, strict=True)
    description: str | None = Field(default=None, max_length=5000, strict=True)
    source_note: str | None = Field(default=None, max_length=500, strict=True)
    line_scope: Literal['selected', 'all'] = 'selected'
    source_url: str | None = Field(default=None, max_length=2048, strict=True)
    source_updated_at: str | None = None
    valid_from: str | None = None
    valid_until: str | None = None

    @field_validator('title', mode='before')
    @classmethod
    def clean_text(cls, value):
        return text(value)

    @field_validator('summary', 'description', 'source_note', 'source_url', mode='before')
    @classmethod
    def optional_text(cls, value, info):
        if value is None:
            return None
        if not isinstance(value, str) or any(unicodedata.category(c) in {'Cc', 'Cs'} and not (info.field_name == 'description' and c in '\n\r\t') for c in value):
            raise ValueError('Plain text required')
        return value.strip() or None

    @field_validator('line_tags', mode='before')
    @classmethod
    def tags(cls, value):
        if not isinstance(value, list) or not 0 <= len(value) <= 50:
            raise ValueError('Explicit bounded tags required')
        return list(dict.fromkeys(text(tag) for tag in value))

    @field_validator('source_url')
    @classmethod
    def http_source(cls, value):
        if value is None:
            return None
        try:
            parsed = urlsplit(value)
            if parsed.scheme.lower() not in {'http', 'https'} or not parsed.hostname or any(c.isspace() for c in value) or '\\' in value:
                raise ValueError('HTTP(S) original source required')
            parsed.port
            # Pydantic's WHATWG-compatible parser rejects malformed percent
            # hosts and invalid numeric IPv4 forms that urlsplit accepts.
            HTTP_SOURCE.validate_python(value)
        except ValueError:
            raise ValueError('HTTP(S) original source required') from None
        return value

    @field_validator('source_updated_at', 'valid_from', 'valid_until')
    @classmethod
    def oslo_time(cls, value):
        return Activity.oslo_instant(value)

    @model_validator(mode='after')
    def ordered(self):
        if (self.line_scope == 'selected' and not self.line_tags) or (self.line_scope == 'all' and self.line_tags):
            raise ValueError('Selected lines require tags; all lines require empty tags')
        if self.valid_from and self.valid_until and datetime.fromisoformat(self.valid_from).astimezone(timezone.utc) > datetime.fromisoformat(self.valid_until).astimezone(timezone.utc):
            raise ValueError('Negative validity')
        return self


class NoticeCommand(StrictModel):
    operation_id: UUID
    expected_revision: int = Field(ge=0, strict=True)
    expected_lifecycle_revision: int = Field(ge=0, strict=True)


class SaveNotice(NoticeCommand):
    content: NoticeContent


class NoticeRecord(StrictModel):
    id: UUID
    workday_id: UUID
    revision: int = Field(ge=1)
    title: str
    line_tags: list[str]
    summary: str | None = None
    description: str | None = None
    source_note: str | None = None
    line_scope: Literal['selected', 'all'] = 'selected'
    source_url: str | None
    source_updated_at: datetime | None
    valid_from: datetime | None
    valid_until: datetime | None
    status: Literal['registered', 'ended_manually']
    entered_at: datetime
    edited_at: datetime
    checked_at: datetime | None
    checked_revision: int | None
    expires_at: datetime

    @field_serializer('source_updated_at', 'valid_from', 'valid_until', when_used='json')
    def source_oslo(self, value):
        # Source clocks must roundtrip under the server's authoritative rules,
        # including historical offsets which browser Intl may interpret differently.
        return value.astimezone(ZoneInfo('Europe/Oslo')).isoformat() if value is not None else None


class NoticeList(StrictModel):
    workday_id: UUID
    expires_at: datetime
    notices: list[NoticeRecord] = Field(max_length=50)
    next_cursor: UUID | None


class NoticeReceipt(StrictModel):
    operation_id: UUID
    result: NoticeRecord
