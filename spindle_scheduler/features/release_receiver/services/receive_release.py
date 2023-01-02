from ..domains import Release, SpiderRunTask
from .create_spider_run_tasks import create_spider_run_tasks


def receive_release(release: Release) -> list[SpiderRunTask]:
    return create_spider_run_tasks(release)
