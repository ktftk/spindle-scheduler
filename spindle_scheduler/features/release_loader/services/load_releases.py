from psycopg import Cursor

from ..domains import Release
from ..repositories import DestinationRepository, SourceRepository


def load_releases(cursor: Cursor) -> list[Release]:
    source_repository = SourceRepository()
    raw_releases = source_repository.read_releases()
    destination_repository = DestinationRepository(cursor)
    releases = destination_repository.create_releases(raw_releases)
    return releases
