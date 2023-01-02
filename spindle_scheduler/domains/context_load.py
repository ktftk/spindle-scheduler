import datetime
import uuid

import uuid6
from pydantic import BaseModel, Field


class ContextLoad(BaseModel):

    id: uuid.UUID = Field(default_factory=uuid6.uuid7)
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow
    )
