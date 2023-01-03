import datetime
import uuid

from pydantic import BaseModel


class SpiderRunTask(BaseModel):
    id: uuid.UUID
    spider_name: str
    spider_inputs: dict
    scheduled_datetime: datetime.datetime
    metadata: dict
