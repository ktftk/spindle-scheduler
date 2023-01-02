import datetime
import uuid

from pydantic import BaseModel, Field

from spindle_scheduler.domains import Release


class SpiderRunTask(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    spider_name: str
    spider_inputs: dict
    scheduled_datetime: datetime.datetime
    metadata: dict = Field(default_factory=dict)
    trigger_release: Release
