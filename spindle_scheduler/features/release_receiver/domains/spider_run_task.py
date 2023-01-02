import datetime
import uuid

from pydantic import BaseModel, Field

from .release import Release


class SpiderRunTask(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    spider_name: str
    spider_inputs: dict
    scheduled_datetime: datetime.datetime
    metadata: dict = Field(default_factory=dict)
    received_release: Release
