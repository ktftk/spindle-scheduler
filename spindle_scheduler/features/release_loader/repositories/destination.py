from __future__ import annotations

import datetime
import hashlib
import json
import uuid
from dataclasses import asdict, dataclass, field
from typing import TypedDict

import uuid6
from psycopg import Cursor, sql
from pydantic import BaseModel

from spindle_scheduler.config import DB_SCHEMA

from ..domains import RawRelease, Release


class Table(TypedDict):
    name: str
    field_names: list[str]


CONTEXT_LOAD_TABLE = Table(name="context_load", field_names=["id"])

RELEASE_TABLE = Table(
    name="release",
    field_names=[
        "hash",
        "id",
        "group_code",
        "dataset_code",
        "frequency",
        "edition",
        "scheduled_datetime",
        "load_id",
    ],
)


class DBRelease(BaseModel):
    hash: str
    id: uuid.UUID
    group_code: str
    dataset_code: str
    frequency: str
    edition: datetime.date
    scheduled_datetime: datetime.datetime
    load_id: uuid.UUID

    def __post_init__(self) -> None:
        self.hash = calculate_release_hash(self.id, self.load_id)

    @classmethod
    def from_raw_release(
        cls, raw_release: RawRelease, load_id: uuid.UUID
    ) -> DBRelease:
        hash = calculate_release_hash(raw_release.id, load_id)
        return cls.parse_obj(
            {**raw_release.dict(), "hash": hash, "load_id": load_id}
        )

    def to_release(self) -> Release:
        return Release.parse_obj(asdict(self))


@dataclass
class DestinationRepository:
    load_id: uuid.UUID = field(default_factory=uuid6.uuid7, init=False)
    cursor: Cursor

    def __post_init__(self) -> None:
        self.cursor.execute(
            sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
                sql.Identifier(DB_SCHEMA, CONTEXT_LOAD_TABLE["name"]),
                sql.SQL(", ").join(
                    map(sql.Identifier, CONTEXT_LOAD_TABLE["field_names"])
                ),
                sql.SQL(", ").join(
                    sql.Placeholder() * len(CONTEXT_LOAD_TABLE["field_names"])
                ),
            ),
            [self.load_id],
        )

    def create_releases(self, raw_releases: list[RawRelease]) -> list[Release]:
        db_releases = [
            DBRelease.from_raw_release(raw_release, load_id=self.load_id)
            for raw_release in raw_releases
        ]
        with self.cursor.copy(
            sql.SQL("COPY {} ({}) FROM STDOUT").format(
                sql.Identifier(DB_SCHEMA, RELEASE_TABLE["name"]),
                sql.SQL(", ").join(
                    map(sql.Identifier, RELEASE_TABLE["field_names"])
                ),
            )
        ) as copy:
            for db_release in db_releases:
                db_release_dict = db_release.dict()
                copy.write_row(
                    tuple(
                        [
                            db_release_dict[field_name]
                            for field_name in RELEASE_TABLE["field_names"]
                        ]
                    )
                )
        return [db_release.to_release() for db_release in db_releases]


def calculate_release_hash(release_id: uuid.UUID, load_id: uuid.UUID) -> str:
    return hashlib.md5(
        json.dumps(
            {"release_id": release_id.hex, "load_id": load_id.hex}
        ).encode()
    ).hexdigest()
