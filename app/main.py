import logging
from typing import Optional

from fastapi import Depends, FastAPI, Request
from psycopg2._psycopg import connection

from .domains import ReleaseReminder
from .publisher import get_topic_path, publisher
from .repository import get_conn, read_releases_to_remind

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

app = FastAPI()


@app.post("/release-reminders", response_model=list[ReleaseReminder])
def create_release_reminders(
    conn: connection = Depends(get_conn),
    topic_path: Optional[str] = Depends(get_topic_path),
):
    releases = read_releases_to_remind(conn)
    release_reminders = [
        ReleaseReminder(release=release) for release in releases
    ]
    if topic_path is not None:
        for release_reminder in release_reminders:
            publisher.publish(
                topic_path, release_reminder.json().encode("utf-8")
            )
    return release_reminders


@app.post("/release-reminder-receivers/create-scheduled-spinners")
async def create_scheduled_spinners(request: Request):
    data = await request.json()
    logger.info(data)
    return {"message": "Hello World"}
