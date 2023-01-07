import uuid

from psycopg import Cursor

from spindle_scheduler import Release

from .. import repository
from .create_release import create_release


def load_releases(cursor: Cursor, load_id: uuid.UUID) -> list[Release]:
    release_resources = repository.read_release_resources()
    releases = [
        create_release(release_resource, load_id=load_id)
        for release_resource in release_resources
    ]
    repository.create_releases(cursor, releases, load_id=load_id)
    return releases
