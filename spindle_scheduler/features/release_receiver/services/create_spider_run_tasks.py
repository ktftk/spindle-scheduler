from ..domains import Release, SpiderRunTask


def create_spider_run_tasks(releases: list[Release]) -> list[SpiderRunTask]:
    result = []
    for release in releases:
        result += receive_release(release)
    return result


def receive_release(release: Release) -> list[SpiderRunTask]:
    if release.group_code == "economy.us.cpi.main":
        return [
            SpiderRunTask(
                spider_name="topics.economy.us.cpi.cpiu",
                spider_inputs={"latest": release.edition},
                scheduled_datetime=release.scheduled_datetime,
                created_by=release,
            )
        ]
    return []
