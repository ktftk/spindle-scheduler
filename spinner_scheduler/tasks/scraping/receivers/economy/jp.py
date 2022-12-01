from spinner_scheduler import Release
from spinner_scheduler.tasks.scraping import ReleaseReceiverBase, ScrapingTask


class EWSReciever(ReleaseReceiverBase):
    def run(self, release: Release) -> list[ScrapingTask]:
        return [
            ScrapingTask(
                name="economy.jp.ews.main",
                inputs={
                    "period_start_date": release.edition_period_start_date
                },
                scheduled_datetime=release.scheduled_datetime,
            )
        ]
