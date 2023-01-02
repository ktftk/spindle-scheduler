from spinner_scheduler import Release
from spinner_scheduler.tasks.scraper_run import (
    ReleaseReceiverBase,
    ScraperRunTask,
)


class EWSReciever(ReleaseReceiverBase):
    def run(self, release: Release) -> list[ScraperRunTask]:
        return [
            ScraperRunTask(
                scraper_name="economy.jp.ews.main",
                scraper_inputs={
                    "period_start_date": release.edition_period_start_date
                },
                scheduled_datetime=release.scheduled_datetime,
            )
        ]
