import datetime
import uuid

from pydantic import BaseModel, Field


class Release(BaseModel):
    gen_id: uuid.UUID
    id: uuid.UUID
    group_code: str
    dataset_code: str
    frequency: str
    edition_period_start_date: datetime.date
    scheduled_datetime: datetime.datetime


class ReleaseReminder(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    release: Release
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow
    )
