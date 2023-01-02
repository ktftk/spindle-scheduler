import datetime

import pandera as pa
from pandera.typing import Series

from ...config import RELEASE_RESOURCE_PATH
from ...domains import RawRelease
from .utils import read_csv

FREQUENCY_CODES = ["Y", "Q", "M", "W", "D"]


class RawReleaseSchema(pa.SchemaModel):
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


def read_releases() -> list[RawRelease]:
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
    RawReleaseSchema.validate(df)
    df["edition"] = df["edition_period_start_date"].apply(
        lambda x: datetime.date.fromisoformat(x)
    )
    df = df.astype({"scheduled_timestamp": int})
    df["scheduled_datetime"] = df["scheduled_timestamp"].apply(
        datetime.datetime.fromtimestamp
    )
    return [RawRelease.parse_obj(record) for record in df.to_dict("records")]
