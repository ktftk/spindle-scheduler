import os
from dataclasses import InitVar, dataclass, field
from pathlib import Path
from uuid import UUID

from google.cloud import storage


@dataclass
class Repository:
    bucket_name: InitVar[str]
    bucket: storage.Bucket = field(init=False)

    def __post_init__(self, bucket_name: str) -> None:
        storage_client = storage.Client()
        self.bucket = storage_client.bucket(bucket_name)

    def upload_raw_calendar(self, id_: UUID, source: str | Path) -> None:
        dest = f"{os.environ['GCS_RAW_CALENDAR_FOLDER']}/{id_}.html"
        blob = self.bucket.blob(dest)
        blob.upload_from_filename(source)

    def upload_parsed_calendar(self, id_: UUID, source: str | Path) -> None:
        blob = self.bucket.blob(
            f"{os.environ['GCS_PARSED_CALENDAR_FOLDER']}/{id_}.csv"
        )
        blob.upload_from_filename(source)
        blob = self.bucket.blob(
            f"{os.environ['GCS_LATEST_CALENDAR_NAME']}.csv"
        )
        blob.upload_from_filename(source)
