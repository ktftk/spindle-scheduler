import psycopg

from spindle_scheduler.config import DB_URL
from spindle_scheduler.features.release_loader.services import load_releases
from spindle_scheduler.features.release_receiver.services import (
    create_spider_run_tasks,
    load_spider_run_tasks,
)
from spindle_scheduler.infra.db import create_context_load

from ..domains import ContextLoad


def load_resources() -> None:
    with psycopg.connect(DB_URL) as conn:
        cur = conn.cursor()
        context_load = ContextLoad()
        create_context_load(cur, context_load)
        releases = load_releases(cur, context_load)
        spider_run_tasks = []
        for release in releases:
            spider_run_tasks += create_spider_run_tasks(release)
        load_spider_run_tasks(cur, spider_run_tasks)
