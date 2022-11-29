import base64
import logging
from typing import Optional

from fastapi import Body, Depends, FastAPI
from psycopg2._psycopg import connection

from spinner_scheduler.domains import PubSubMessage, ReleaseReminder
from spinner_scheduler.publisher import get_topic_path, publisher
from spinner_scheduler.repository import get_conn, read_releases_to_remind

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
async def create_scheduled_spinners(message: PubSubMessage = Body(embed=True)):
    release_reminder = ReleaseReminder.parse_raw(
        base64.b64decode(message.data)
    )
    return {"message": "Hello World"}
