import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Body, Depends, FastAPI
from pydantic import BaseModel, Field

from prisma import Prisma

from .config import TASK_QUERY_END_OFFSET, TASK_QUERY_START_OFFSET
from .domains import InovkedSpiderRunTask, SpiderRunTask
from .repository import Repository
from .services import execute_workflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskQuery(BaseModel):
    base_datetime: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    start_offset: int = TASK_QUERY_START_OFFSET
    end_offset: int = TASK_QUERY_END_OFFSET


class WorkflowExecutor:
    def run(self, spider_run_task: SpiderRunTask) -> InovkedSpiderRunTask:
        return execute_workflow(spider_run_task)


app = FastAPI()

prisma = Prisma()


@app.on_event("startup")
def startup() -> None:
    prisma.connect()


@app.on_event("shutdown")
def shutdown() -> None:
    if prisma.is_connected():
        prisma.disconnect()


@app.post(
    "/v1/spider-workflow-run",
    response_model=list[InovkedSpiderRunTask],
    status_code=201,
)
def spider_workflow_run(
    repository: Annotated[Repository, Depends(Repository)],
    workflow_executor: Annotated[WorkflowExecutor, Depends(WorkflowExecutor)],
    task_query: Annotated[TaskQuery, Body(embed=True)] = TaskQuery(),
) -> list[InovkedSpiderRunTask]:
    print(task_query)
    tasks = repository.read_spider_run_tasks_by_datetime_range(
        start=task_query.base_datetime
        - timedelta(seconds=task_query.start_offset),
        end=task_query.base_datetime
        + timedelta(seconds=task_query.end_offset),
    )
    upcoming_tasks = [
        task
        for task in tasks
        if not repository.is_spider_run_task_invoked(hash=task.hash)
    ]
    logger.info(f"tasks count: {len(upcoming_tasks)}")
    result: list[InovkedSpiderRunTask] = []
    for task in upcoming_tasks:
        completed_task = workflow_executor.run(task)
        repository.write_invoked_spider_run_task(completed_task)
        result.append(completed_task)
        logger.info(f"invoked task: {task.json()}")
    return result
