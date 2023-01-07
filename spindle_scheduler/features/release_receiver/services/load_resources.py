from psycopg import Cursor

from spindle_scheduler.domains import Release

from .create_spider_run_tasks import create_spider_run_tasks
from .load_spider_run_tasks import load_spider_run_tasks


def load_resources(cursor: Cursor, releases: list[Release]) -> None:
    spider_run_tasks = create_spider_run_tasks(releases)
    load_spider_run_tasks(cursor, spider_run_tasks)
