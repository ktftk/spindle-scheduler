from psycopg import Cursor

from spindle_scheduler import Release

from .. import repository
from ..domains import SpiderRunTask
from .create_spider_run_tasks import create_spider_run_tasks


def load_spider_run_tasks(
    cursor: Cursor, releases: list[Release]
) -> list[SpiderRunTask]:
    spider_run_tasks = create_spider_run_tasks(releases)
    repository.create_spider_run_tasks(cursor, spider_run_tasks)
    repository.create_spider_run_task_by_releases(cursor, spider_run_tasks)
    return spider_run_tasks
