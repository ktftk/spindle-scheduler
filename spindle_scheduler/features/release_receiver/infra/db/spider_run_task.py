from __future__ import annotations

import datetime
import json
import uuid

from psycopg import Cursor

from spindle_scheduler.config import DB_SCHEMA
from spindle_scheduler.repository import RecordBase, create_many

from ...domains import SpiderRunTask as AppSpiderRunTask


class SpiderRunTask(RecordBase):
    _schema = DB_SCHEMA
    _tablename = "spider_run_task"
    id: uuid.UUID
    spider_name: str
    spider_inputs: str
    scheduled_datetime: datetime.datetime
    metadata: str

    @classmethod
    def create(cls, spider_run_task: AppSpiderRunTask) -> SpiderRunTask:
        return cls(
            id=spider_run_task.id,
            spider_name=spider_run_task.spider_name,
            spider_inputs=json.dumps(
                json.loads(spider_run_task.json())["spider_inputs"]
            ),
            scheduled_datetime=spider_run_task.scheduled_datetime,
            metadata=json.dumps(spider_run_task.metadata),
        )


def create_spider_run_tasks(
    cursor: Cursor,
    spider_run_tasks: list[AppSpiderRunTask],
) -> list[SpiderRunTask]:
    return create_many(
        cursor,
        [
            SpiderRunTask.create(spider_run_task)
            for spider_run_task in spider_run_tasks
        ],
    )
