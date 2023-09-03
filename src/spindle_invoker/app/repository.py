from dataclasses import dataclass
from datetime import datetime

from prisma import Json, Prisma

from .domains import (
    CompleteSpiderWorkflowRun,
    InovkedSpiderRunTask,
    LaunchSpiderWorkflowRun,
    SpiderRunTask,
)


@dataclass
class Repository:
    def read_spider_run_tasks_by_datetime_range(
        self, start: datetime, end: datetime
    ) -> list[SpiderRunTask]:
        with Prisma() as db:
            rows = db.spiderruntask.find_many(
                where={
                    "scheduled_at": {
                        "gte": start,
                        "lte": end,
                    }
                }
            )
        return [SpiderRunTask.parse_obj(row.dict()) for row in rows]

    def is_spider_run_task_invoked(self, hash: str) -> bool:
        with Prisma() as db:
            row = db.invokedspiderruntask.find_unique(where={"hash": hash})
        return True if row is not None else False

    def write_invoked_spider_run_task(
        self, task: InovkedSpiderRunTask
    ) -> None:
        with Prisma() as db:
            db.invokedspiderruntask.create(
                data={
                    "hash": task.hash,
                    "invoked_at": task.invoked_at,
                    "invocation_id": task.invocation_id,
                    "execution_id": task.execution_id,
                }
            )

    def write_launched_spider_workflow_run(
        self, launch_task: LaunchSpiderWorkflowRun
    ) -> None:
        with Prisma() as db:
            db.launchedspiderworkflowrun.create(
                data={
                    "invocation_id": (launch_task.invocation_id),
                    "invocation_type": launch_task.invocation_type,
                    "spider_name": launch_task.spider_name,
                    "params": Json(launch_task.params),
                    "target_period": datetime.fromisoformat(
                        launch_task.target_period.isoformat()
                    ),
                    "launched_at": launch_task.launched_at,
                }
            )

    def write_completed_spider_workflow_run(
        self, completed_run: CompleteSpiderWorkflowRun
    ) -> None:
        with Prisma() as db:
            db.completedspiderworkflowrun.create(
                data={
                    "invocation_id": completed_run.invocation_id,
                    "status": completed_run.status,
                    "completed_at": completed_run.completed_at,
                }
            )
