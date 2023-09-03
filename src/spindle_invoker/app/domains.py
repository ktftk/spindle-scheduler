from datetime import date, datetime
from typing import Literal, Optional

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


class LaunchSpiderWorkflowRun(BaseModel):
    workflow_execution_id: str
    trigger_type: Literal["on_demand", "on_release"]
    spider_name: str
    params: dict
    target_period: date
    launched_at: datetime


class CompleteSpiderWorkflowRun(LaunchSpiderWorkflowRun):
    status: Literal["success", "failure"]
    completed_at: datetime
