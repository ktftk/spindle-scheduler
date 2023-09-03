from __future__ import annotations

import os
import uuid
from datetime import date, datetime, timezone
from typing import Literal, Optional

from google.cloud.workflows import executions_v1
from pydantic import BaseModel

from .domains import InovkedSpiderRunTask, SpiderRunTask


class SpiderWorkflowPayload(BaseModel):
    invocation_id: str
    invocation_type: Literal["release_based"] = "release_based"
    spider_name: str
    params: Optional[dict]
    target_period: Optional[date]
    scheduled_timestamp: float

    @classmethod
    def from_spider_run_task(
        cls, task: SpiderRunTask
    ) -> SpiderWorkflowPayload:
        return cls(
            invocation_id=str(uuid.uuid4()),
            spider_name=task.spider_name,
            params=task.input_params,
            target_period=task.target_period,
            scheduled_timestamp=task.scheduled_at.timestamp(),
        )


# projects/{project}/locations/{location}/workflows/{workflow}/executions/{execution}
def get_workflow_execution_id(s: str) -> str:
    return s.split("/")[-1]


def execute_workflow(task: SpiderRunTask) -> InovkedSpiderRunTask:
    WORKFLOW_PROJECT_ID = os.environ["WORKFLOW_PROJECT_ID"]
    WORKFLOW_LOCATION = os.environ["WORKFLOW_LOCATION"]
    WORKFLOW_NAME = os.environ["WORKFLOW_NAME"]

    workflows_client = executions_v1.ExecutionsClient()

    parent = workflows_client.workflow_path(
        WORKFLOW_PROJECT_ID, WORKFLOW_LOCATION, WORKFLOW_NAME
    )

    execution_client = executions_v1.ExecutionsClient()

    payload = SpiderWorkflowPayload.from_spider_run_task(task)

    request = executions_v1.CreateExecutionRequest(
        parent=parent,
        execution=executions_v1.Execution(argument=payload.json()),
    )

    execution = execution_client.create_execution(request=request)
    execiton_id = get_workflow_execution_id(execution.name)

    return InovkedSpiderRunTask(
        hash=task.hash,
        spider_name=task.spider_name,
        input_params=task.input_params,
        target_period=task.target_period,
        scheduled_at=task.scheduled_at,
        invocation_id=payload.invocation_id,
        invoked_at=datetime.now(timezone.utc),
        execution_id=execiton_id,
    )
