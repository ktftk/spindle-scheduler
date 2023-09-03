import json
import uuid
from datetime import datetime, timezone

from app.domains import (
    CompleteSpiderWorkflowRun,
    InovkedSpiderRunTask,
    LaunchSpiderWorkflowRun,
    SpiderRunTask,
)
from app.main import WorkflowExecutor, app
from fastapi.testclient import TestClient

client = TestClient(app)


class MockWorkflowExecutor:
    def run(self, spider_run_task: SpiderRunTask) -> InovkedSpiderRunTask:
        return InovkedSpiderRunTask(
            hash=spider_run_task.hash,
            spider_name=spider_run_task.spider_name,
            input_params=spider_run_task.input_params,
            target_period=spider_run_task.target_period,
            scheduled_at=spider_run_task.scheduled_at,
            invoked_at=datetime.now(timezone.utc),
            workflow_execution_id=str(uuid.uuid4()),
        )


app.dependency_overrides[WorkflowExecutor] = MockWorkflowExecutor


def test_spider_run() -> None:
    response = client.post(
        "/v1/spider-workflow-run",
        json={
            "task_query": {
                "base_datetime": datetime(2023, 6, 29, 0, 28, 0).isoformat(),
                "start_offset": 60 * 5,
                "end_offset": 60 * 15,
            }
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert len(data) == 2


def test_launched_spider_workflow_run() -> None:
    launced_run = LaunchSpiderWorkflowRun(
        workflow_execution_id=str(uuid.uuid4()),
        trigger_type="on_demand",
        spider_name="test_spider",
        params={},
        target_period=datetime(2023, 6, 29).date(),
        launched_at=datetime.now(timezone.utc),
    )
    response = client.post(
        "/v1/launched-spider-workflow-run",
        json={
            "launched_run": json.loads(launced_run.json()),
        },
    )
    assert response.status_code == 201


def test_completed_spider_workflow_run() -> None:
    completed_run = CompleteSpiderWorkflowRun(
        workflow_execution_id=str(uuid.uuid4()),
        trigger_type="on_demand",
        spider_name="test_spider",
        params={},
        target_period=datetime(2023, 6, 29).date(),
        launched_at=datetime.now(timezone.utc),
        status="success",
        completed_at=datetime.now(timezone.utc),
    )
    response = client.post(
        "/v1/completed-spider-workflow-run",
        json={
            "completed_run": json.loads(completed_run.json()),
        },
    )
    assert response.status_code == 201
