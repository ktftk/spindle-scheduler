import uuid

from psycopg import Cursor

from .. import repository
from ..domains import Release
from .parse_release import parse_release


def load_releases(cursor: Cursor, load_id: uuid.UUID) -> list[Release]:
    raw_releases = repository.read_releases()
    releases = [
        parse_release(raw_release, load_id=load_id)
        for raw_release in raw_releases
    ]
    repository.create_releases(cursor, releases, load_id=load_id)
    return releases
