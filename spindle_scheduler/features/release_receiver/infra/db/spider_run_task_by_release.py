from __future__ import annotations

import uuid

from psycopg import Cursor

from spindle_scheduler.config import DB_SCHEMA
from spindle_scheduler.infra.db import RecordBase, create_many

from ...domains import SpiderRunTask


class SpiderRunTaskByRelease(RecordBase):
    _schema = DB_SCHEMA
    _tablename = "spider_run_task_by_release"
    spider_run_task_id: uuid.UUID
    release_hash: str

    @classmethod
    def create(cls, spider_run_task: SpiderRunTask) -> SpiderRunTaskByRelease:
        return cls(
            spider_run_task_id=spider_run_task.id,
            release_hash=spider_run_task.created_by.hash,
        )


def create_spider_run_task_by_releases(
    cursor: Cursor, spider_run_tasks: list[SpiderRunTask]
) -> list[SpiderRunTaskByRelease]:
    return create_many(
        cursor,
        [
            SpiderRunTaskByRelease.create(spider_run_task)
            for spider_run_task in spider_run_tasks
        ],
    )
