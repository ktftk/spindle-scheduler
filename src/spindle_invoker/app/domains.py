from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class SpiderRunTask(BaseModel):
    hash: str
    spider_name: str
    input_params: Optional[dict]
    target_period: date
    scheduled_at: datetime


class InovkedSpiderRunTask(BaseModel):
    hash: str
    spider_name: str
    input_params: Optional[dict]
    target_period: date
    scheduled_at: datetime
    invoked_at: datetime
    workflow_execution_id: str
