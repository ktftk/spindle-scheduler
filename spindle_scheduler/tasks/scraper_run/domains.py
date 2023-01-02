import abc
import datetime
import uuid

from pydantic import BaseModel, Field

from spindle_scheduler import Release


class ScraperRunTask(BaseModel):
    scraper_name: str
    scraper_inputs: dict
    scraper_run_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    metadata: dict = Field(default_factory=dict)
    scheduled_datetime: datetime.datetime


class ReleaseReceiverBase(BaseModel, abc.ABC):
    @abc.abstractmethod
    def run(self, release: Release) -> list[ScraperRunTask]:
        ...
