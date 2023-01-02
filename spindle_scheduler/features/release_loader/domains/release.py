import datetime
import uuid

from pydantic import BaseModel


class RawRelease(BaseModel):
    id: uuid.UUID
    group_code: str
    dataset_code: str
    frequency: str
    edition: datetime.date
    scheduled_datetime: datetime.datetime
