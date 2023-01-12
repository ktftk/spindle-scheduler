import uuid

from psycopg import Cursor

from spindle_scheduler.config import DB_SCHEMA
from spindle_scheduler.repository import RecordBase, create_many

from ...domains import SpiderRunTask


class ExecutedSpiderRunTask(RecordBase):
    _schema = DB_SCHEMA
    _tablename = "executed_spider_run_task"
    id: uuid.UUID


def create_executed_spider_run_tasks(
    cursor: Cursor,
    spider_run_tasks: list[SpiderRunTask],
) -> list[SpiderRunTask]:
    executed_spider_run_tasks = [
        ExecutedSpiderRunTask(id=spider_run_task.id)
        for spider_run_task in spider_run_tasks
    ]
    create_many(cursor, executed_spider_run_tasks)
    return spider_run_tasks
