import os

from dotenv import load_dotenv

load_dotenv()

INSTANCE_UNIX_SOCKET = os.environ.get("INSTANCE_UNIX_SOCKET")

DB_DBNAME = os.environ["DB_DBNAME"]

DB_USER = os.environ["DB_USER"]

DB_PASSWORD = os.environ["DB_PASSWORD"]

DB_HOST = os.environ.get("DB_HOST")

DB_PORT = os.environ.get("DB_PORT")

PUBSUB_PROJECT_ID = os.environ.get("PUBSUB_PROJECT_ID")

PUBSUB_TOPIC_ID = os.environ.get("PUBSUB_TOPIC_ID")

REMINDER_ADVANCE_TIME = 60 * 60

REMINDER_DEADLINE_TIME = 60 * 60 * 24 * 30
