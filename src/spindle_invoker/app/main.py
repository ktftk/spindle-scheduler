import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Body, Depends, FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import BaseModel, Field

from prisma import Prisma

from .config import TASK_QUERY_END_OFFSET, TASK_QUERY_START_OFFSET
from .domains import (
    CompleteSpiderWorkflowRun,
    InovkedSpiderRunTask,
    SpiderRunTask,
)
from .repository import Repository
from .services import execute_workflow
from .tracer import tracer

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
    with tracer.start_as_current_span("spider_workflow_run") as span:
        span.set_attribute(
            "base_datetime", task_query.base_datetime.isoformat()
        )
        span.set_attribute("start_offset", task_query.start_offset)
        span.set_attribute("end_offset", task_query.end_offset)

        start = task_query.base_datetime - timedelta(
            seconds=task_query.start_offset
        )
        end = task_query.base_datetime + timedelta(
            seconds=task_query.end_offset
        )
        span.set_attribute("start", start.isoformat())
        span.set_attribute("end", end.isoformat())

        eligible_tasks = repository.read_spider_run_tasks_by_datetime_range(
            start=start,
            end=end,
        )
        span.set_attribute("eligible_tasks_count", len(eligible_tasks))

        upcoming_tasks = [
            task
            for task in eligible_tasks
            if not repository.is_spider_run_task_invoked(hash=task.hash)
        ]
        span.set_attribute("upcoming_tasks_count", len(upcoming_tasks))

        result: list[InovkedSpiderRunTask] = []
        for task in upcoming_tasks:
            completed_task = workflow_executor.run(task)
            repository.write_invoked_spider_run_task(completed_task)
            result.append(completed_task)
            logger.info(f"invoked task: {task.json()}")
            span.add_event("invoked_task", json.loads(task.json()))
        return result


@app.post(
    "/v1/completed-spider-workflow-run",
    response_model=list[InovkedSpiderRunTask],
    status_code=201,
)
def completed_spider_workflow_run(
    repository: Annotated[Repository, Depends(Repository)],
    copmleted_run: Annotated[CompleteSpiderWorkflowRun, Body(embed=True)],
) -> CompleteSpiderWorkflowRun:
    with tracer.start_as_current_span(
        "completed_spider_workflow_run",
        attributes=json.loads(copmleted_run.json()),
    ):
        repository.write_completed_spider_workflow_run(copmleted_run)
        return copmleted_run


FastAPIInstrumentor.instrument_app(app)
