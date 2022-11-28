from fastapi import Depends, FastAPI
from psycopg2._psycopg import connection

from .domains import ReleaseReminder
from .repository import get_conn, read_releases_to_remind

app = FastAPI()


@app.post("/release-reminders", response_model=list[ReleaseReminder])
def root(conn: connection = Depends(get_conn)):
    releases = read_releases_to_remind(conn)
    release_reminders = [
        ReleaseReminder(release=release) for release in releases
    ]
    return release_reminders
