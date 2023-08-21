from dataclasses import dataclass
from datetime import datetime

from prisma import Prisma

from .domains import InovkedSpiderRunTask, SpiderRunTask


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
                    "workflow_execution_id": task.workflow_execution_id,
                }
            )
