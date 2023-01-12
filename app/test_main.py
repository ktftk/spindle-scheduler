from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_execute_spider_run_tasks() -> None:
    response = client.post("/execute-spider-run-tasks", json={})
    assert response.status_code == 200
