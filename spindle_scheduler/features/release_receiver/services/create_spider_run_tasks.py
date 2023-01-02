from ..domains import Release, SpiderRunTask


def create_spider_run_tasks(release: Release) -> list[SpiderRunTask]:
    if release.group_code == "economy.us.cpi":
        return [
            SpiderRunTask(
                spider_name="topics.economy.us.cpi.cpiu",
                spider_inputs={"latest": release.edition},
                scheduled_datetime=release.scheduled_datetime,
                received_release=release,
            )
        ]
    return []