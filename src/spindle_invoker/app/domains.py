import uuid
from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


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
    invocation_id: str
    invoked_at: datetime
    execution_id: str


class LaunchSpiderWorkflowRun(BaseModel):
    invocation_id: str = Field(lambda: str(uuid.uuid4()))
    invocation_type: Literal["on_demand", "on_release"]
    spider_name: str
    params: dict
    target_period: date
    launched_at: datetime


class CompleteSpiderWorkflowRun(LaunchSpiderWorkflowRun):
    status: Literal["success", "failure"]
    completed_at: datetime
