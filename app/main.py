from typing import Callable

from fastapi import Depends, FastAPI
from psycopg2._psycopg import connection

from .domains import ReleaseReminder
from .publisher import publish_release_reminder
from .repository import get_conn, read_releases_to_remind

app = FastAPI()


def get_publish_release_reminder() -> Callable[[ReleaseReminder], None]:
    return publish_release_reminder


@app.post("/release-reminders", response_model=list[ReleaseReminder])
def root(
    conn: connection = Depends(get_conn),
    publish_release_reminder: Callable[[ReleaseReminder], None] = Depends(
        get_publish_release_reminder
    ),
):
    releases = read_releases_to_remind(conn)
    release_reminders = [
        ReleaseReminder(release=release) for release in releases
    ]
    for release_reminder in release_reminders:
        publish_release_reminder(release_reminder)
    return release_reminders
