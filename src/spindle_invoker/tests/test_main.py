import uuid
from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.domains import InovkedSpiderRunTask, SpiderRunTask
from app.main import WorkflowExecutor, app

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
