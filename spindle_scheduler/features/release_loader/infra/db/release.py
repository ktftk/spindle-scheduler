from __future__ import annotations

import datetime
import uuid

from psycopg import Cursor

from spindle_scheduler import Release as AppRelease
from spindle_scheduler.config import DB_SCHEMA
from spindle_scheduler.infra.db import RecordBase, create_many


class Release(RecordBase):
    _schema = DB_SCHEMA
    _tablename = "release"
    hash: str
    id: uuid.UUID
    group_code: str
    dataset_code: str
    frequency: str
    edition: datetime.date
    scheduled_datetime: datetime.datetime
    load_id: uuid.UUID

    @classmethod
    def create(cls, release: AppRelease, load_id: uuid.UUID) -> Release:
        return cls(
            hash=release.hash,
            id=release.id,
            group_code=release.group_code,
            dataset_code=release.group_code,
            frequency=release.frequency,
            edition=release.edition,
            scheduled_datetime=release.scheduled_datetime,
            load_id=load_id,
        )


def create_releases(
    cursor: Cursor, releases: list[AppRelease], load_id: uuid.UUID
) -> list[AppRelease]:
    create_many(
        cursor,
        [Release.create(release, load_id=load_id) for release in releases],
    )
    return releases
