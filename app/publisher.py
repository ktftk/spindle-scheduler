import json

from google.cloud import pubsub_v1

from .config import PUBSUB_PROJECT_ID, PUBSUB_TOPIC_ID
from .domains import ReleaseReminder

publisher = pubsub_v1.PublisherClient()

topic_path = publisher.topic_path(PUBSUB_PROJECT_ID, PUBSUB_TOPIC_ID)


def publish_release_reminder(release_reminder: ReleaseReminder) -> None:
    publisher.publish(
        topic_path, json.dumps(release_reminder.dict()).encode("utf-8")
    )
