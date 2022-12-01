import abc
import datetime

from pydantic import BaseModel

from spinner_scheduler import Release


class ScrapingTask(BaseModel):
    name: str
    inputs: dict
    scheduled_datetime: datetime.datetime


class ReleaseReceiverBase(BaseModel, abc.ABC):
    @abc.abstractmethod
    def run(self, release: Release) -> list[ScrapingTask]:
        ...
