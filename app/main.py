import logging

from fastapi import Depends, FastAPI, Request
from psycopg2._psycopg import connection

from .domains import ReleaseReminder
from .repository import get_conn, read_releases_to_remind

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

app = FastAPI()


@app.post("/release-reminders", response_model=list[ReleaseReminder])
def root(
    request: Request,
    conn: connection = Depends(get_conn),
):
    logger.info(
        {"Requested": {"Method": request.method, "URL": str(request.url)}}
    )
    releases = read_releases_to_remind(conn)
    release_reminders = [
        ReleaseReminder(release=release) for release in releases
    ]
    return release_reminders
