import datetime
from datetime import timezone


def datetime_from_timestamp(timestamp: int) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(timestamp, tz=timezone.utc)
