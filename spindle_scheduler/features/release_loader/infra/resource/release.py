import datetime

import pandera as pa
from pandera.typing import Series

from spindle_scheduler.utils import datetime_from_timestamp

from ...config import RELEASE_RESOURCE_PATH
from ...domains import ReleaseResource
from .io import read_csv

FREQUENCY_CODES = ["Y", "Q", "M", "W", "D"]


class ReleaseResourceSchema(pa.SchemaModel):
    id: Series[str] = pa.Field(
        unique=True, str_length={"min_value": 32, "max_value": 32}
    )
    group_code: Series[str]
    dataset_code: Series[str]
    frequency: Series[str] = pa.Field(isin=FREQUENCY_CODES)
    edition_period_start_date: Series[str]
    scheduled_timestamp: Series[str]

    class Config:
        strict = True


def read_release_resources() -> list[ReleaseResource]:
    df = read_csv(RELEASE_RESOURCE_PATH)
    df = df[
        [
            "id",
            "group_code",
            "dataset_code",
            "frequency",
            "edition_period_start_date",
            "scheduled_timestamp",
        ]
    ]
    ReleaseResourceSchema.validate(df)
    df["edition"] = df["edition_period_start_date"].apply(
        lambda x: datetime.date.fromisoformat(x)
    )
    df = df.astype({"scheduled_timestamp": int})
    df["scheduled_datetime"] = df["scheduled_timestamp"].apply(
        datetime_from_timestamp
    )
    return [
        ReleaseResource.parse_obj(record) for record in df.to_dict("records")
    ]
