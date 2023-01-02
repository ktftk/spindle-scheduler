from psycopg import Cursor

from spindle_scheduler.domains import ContextLoad

from .. import repository
from ..domains import Release
from .parse_release import parse_release


def load_releases(cursor: Cursor, context_load: ContextLoad) -> list[Release]:
    raw_releases = repository.read_releases()
    releases = [
        parse_release(raw_release, context_load)
        for raw_release in raw_releases
    ]
    repository.create_releases(cursor, releases)
    return releases
