import datetime
import uuid

from pydantic import BaseModel

from .context_load import ContextLoad


class Release(BaseModel):
    hash: str
    id: uuid.UUID
    group_code: str
    dataset_code: str
    frequency: str
    edition: datetime.date
    scheduled_datetime: datetime.datetime
    context_load: ContextLoad
