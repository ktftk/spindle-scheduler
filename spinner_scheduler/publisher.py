from typing import Optional

from google.cloud import pubsub_v1

from .config import PUBSUB_PROJECT_ID, PUBSUB_TOPIC_ID

publisher = pubsub_v1.PublisherClient()


def get_topic_path() -> Optional[str]:
    if PUBSUB_PROJECT_ID is None or PUBSUB_TOPIC_ID is None:
        return None
    return publisher.topic_path(PUBSUB_PROJECT_ID, PUBSUB_TOPIC_ID)
