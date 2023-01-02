from psycopg import Cursor

from .. import repository
from ..domains import SpiderRunTask


def load_spider_run_tasks(
    cursor: Cursor, spider_run_tasks: list[SpiderRunTask]
) -> list[SpiderRunTask]:
    repository.create_spider_run_tasks(cursor, spider_run_tasks)
    repository.create_spider_run_task_by_releases(cursor, spider_run_tasks)
    return spider_run_tasks
