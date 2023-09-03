import os

ENV = os.getenv("ENV", "dev")

TASK_QUERY_START_OFFSET = int(
    os.getenv("TASK_QUERY_START_OFFSET", 60 * 60 * 24)
)

TASK_QUERY_END_OFFSET = int(os.getenv("TASK_QUERY_END_OFFSET", 60 * 10))


GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
